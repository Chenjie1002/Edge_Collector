from __future__ import annotations

import json
import hashlib
import os
import re
import stat
import tempfile
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import snap7
import yaml
from snap7.type import Parameter

from common.line_config import (
    debug_candidate_content_hash,
    debug_candidate_to_dict,
    debug_contract_content_hash,
    debug_contract_from_candidate,
    debug_contract_from_mapping,
    engineering_export,
    engineering_rows,
    normalize_debug_candidate,
    LineConfig,
    LineConfigError,
    PlcDeploymentCandidate,
    compile_runtime_mapping,
    default_runtime_layout_registry,
    load_line_config,
    parse_deployment_candidate,
    parse_debug_candidate,
)
from common.line_config.runtime_projection import RuntimeMappingProjection, RuntimeProjectionError
from common.runtime_mapping import EffectiveMappingUnavailable, read_effective_mapping

_SERVICE_PATH = Path(__file__).resolve()
PROJECT_ROOT = (
    _SERVICE_PATH.parents[3]
    if _SERVICE_PATH.parents[2].name == "api"
    else _SERVICE_PATH.parents[2]
)
DEFAULT_MAPPING_PATH = PROJECT_ROOT / "config" / "mapping.yaml"
DEFAULT_LINES_PATH = PROJECT_ROOT / "config" / "lines"
DEFAULT_STORE_PATH = PROJECT_ROOT / "data" / "deployment-config"

_CANDIDATE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_ACTIVATION_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
CONNECTIVITY_FIELDS = (
    "host",
    "port",
    "rack",
    "slot",
    "connection_timeout_ms",
    "poll_interval_ms",
)


class DeploymentConfigUnavailable(Exception):
    pass


def load_active_deployment_config(
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    store_path: Path | None = None,
) -> dict[str, object]:
    root, content_sha256, source, _path, _used_overlay = _read_active_mapping(
        mapping_path,
        store_path=store_path,
    )
    plcs = root.get("plcs")
    if not isinstance(plcs, list) or not plcs or not isinstance(plcs[0], dict):
        raise DeploymentConfigUnavailable("active mapping has no PLC configuration")
    plc = plcs[0]
    stations = root.get("stations")
    if not isinstance(stations, list) or not stations:
        raise DeploymentConfigUnavailable("active mapping has no stations")
    line = root.get("line")
    if not isinstance(line, dict):
        raise DeploymentConfigUnavailable("active mapping has no line configuration")

    active_station_ids = [
        _required_text(station.get("station_id"), "station_id")
        for station in stations
        if isinstance(station, dict) and station.get("station_enabled", True) is not False
    ]
    if not active_station_ids:
        raise DeploymentConfigUnavailable("active mapping has no enabled stations")

    activation = _load_active_activation(
        store_path=store_path,
        active_mapping_hash=f"sha256:{content_sha256}",
    )
    debug_contract = debug_contract_from_mapping(root)
    base_topology = _mapping_topology(root, active_station_ids)
    return {
        "authority": {
            "kind": "active_runtime_mapping",
            "source": source,
            "config_version": _required_text(root.get("config_version"), "config_version"),
            "content_sha256": f"sha256:{content_sha256}",
        },
        "line_id": _required_text(root.get("line_id"), "line_id"),
        "line_name": _required_text(line.get("name"), "line.name"),
        "plc": {
            "plc_id": _required_text(plc.get("plc_id"), "plc_id"),
            "host": _required_text(plc.get("host"), "host"),
            "port": _required_int(plc.get("port"), "port"),
            "rack": _required_int(plc.get("rack"), "rack"),
            "slot": _required_int(plc.get("slot"), "slot"),
            "connection_timeout_ms": _required_int(
                plc.get("connection_timeout_ms"), "connection_timeout_ms"
            ),
            "poll_interval_ms": _required_int(plc.get("poll_interval_ms"), "poll_interval_ms"),
        },
        "active_station_count": len(active_station_ids),
        "active_station_ids": active_station_ids,
        "entry_station_id": root.get("entry_station_id"),
        "terminal_station_id": root.get("terminal_station_id"),
        "active_projection_hash": root.get("projection_hash"),
        "debug_contract": debug_contract,
        "debug_contract_hash": f"sha256:{debug_contract_content_hash(debug_contract)}",
        "engineering_rows": engineering_rows(debug_contract),
        "engineering_export": engineering_export(
            debug_contract,
            base_topology=base_topology,
        ),
        "debug_scope": debug_contract.get("debug_scope"),
        "base_topology": base_topology,
        "activation": activation,
        "rollback_available": activation is not None,
    }


def load_line_options(
    lines_path: Path = DEFAULT_LINES_PATH,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    store_path: Path | None = None,
) -> dict[str, object]:
    active = load_active_deployment_config(mapping_path, store_path=store_path)
    active_connectivity = active["plc"]
    assert isinstance(active_connectivity, dict)
    items: list[dict[str, object]] = []
    for line_path in sorted(lines_path.glob("*.yaml")):
        if line_path.is_symlink() or not line_path.is_file():
            continue
        try:
            config = load_line_config(line_path)
        except LineConfigError as exc:
            raise DeploymentConfigUnavailable(
                f"line configuration is invalid: {line_path.name}"
            ) from exc
        projection, projection_error = _try_compile_projection(
            config,
            active_connectivity,
            line_config_source=str(line_path.relative_to(PROJECT_ROOT)),
        )
        items.append(
            _line_option(
                config,
                line_path.name,
                active["line_id"],
                station_ids=_line_station_ids(config),
                projection=projection,
                projection_error=projection_error,
            )
        )
    if not items:
        raise DeploymentConfigUnavailable("no line configurations are available")
    return {"items": items}


def validate_candidate(
    raw: dict[str, object],
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
    store_path: Path | None = None,
) -> dict[str, object]:
    active = load_active_deployment_config(mapping_path, store_path=store_path)
    candidate, errors = parse_deployment_candidate(raw)
    base: dict[str, object] = {
        "validation_state": "INVALID",
        "debug_ready": False,
        "ready_to_activate": False,
        "errors": errors,
        "warnings": [],
        "active_mapping_hash": active["authority"]["content_sha256"],
    }
    if candidate is None:
        return base

    try:
        line_path = _line_path(lines_path, candidate.line_config)
        line_config = load_line_config(line_path)
    except (LineConfigError, DeploymentConfigUnavailable) as exc:
        return {
            **base,
            "errors": [
                {
                    "field": "line_config",
                    "message": "Selected line configuration is not available or valid.",
                }
            ],
        }

    base_projection, base_projection_error = _try_compile_projection(
        line_config,
        candidate_to_connectivity(candidate),
        line_config_source=str(line_path.relative_to(PROJECT_ROOT)),
    )
    expected_station_ids = _line_station_ids(line_config)
    raw_has_contract = bool(raw.get("stations")) or bool(
        isinstance(raw.get("debug_contract"), dict)
        and raw.get("debug_contract", {}).get("stations")
    )
    normalized_raw = {
        **raw,
        **candidate_to_connectivity(candidate),
        "line_config": candidate.line_config,
    }
    if base_projection is not None:
        active_contract = active.get("debug_contract")
        if (
            isinstance(active_contract, dict)
            and [
                str(item.get("station_id"))
                for item in active_contract.get("stations", [])
                if isinstance(item, dict)
            ]
            == expected_station_ids
            and not raw_has_contract
        ):
            seed_contract = active_contract
        else:
            seed_contract = debug_contract_from_mapping(base_projection.document)
        parsed_debug_candidate, debug_errors = parse_debug_candidate(
            normalized_raw,
            expected_station_ids=expected_station_ids,
            seed_contract=seed_contract,
        )
        if parsed_debug_candidate is None:
            return {**base, "errors": debug_errors}
        debug_contract = debug_contract_from_candidate(parsed_debug_candidate)
        projection, projection_error = _try_compile_projection(
            line_config,
            candidate_to_connectivity(candidate),
            line_config_source=str(line_path.relative_to(PROJECT_ROOT)),
            debug_contract=debug_contract,
        )
    else:
        # Preserve the legacy line-option behavior for a valid but currently
        # unsupported topology such as the multi-PLC 20WS configuration.  A
        # 3WS contract remains the only executable FV1A proof surface; the
        # unsupported option is never marked ready to activate.
        parsed_debug_candidate = normalize_debug_candidate(
            normalized_raw,
            seed_contract=active.get("debug_contract"),
        )
        debug_contract = debug_contract_from_candidate(parsed_debug_candidate)
        projection = None
        projection_error = base_projection_error
    option = _line_option(
        line_config,
        candidate.line_config,
        active["line_id"],
        station_ids=expected_station_ids,
        projection=projection,
        projection_error=projection_error,
    )
    content_hash = debug_candidate_content_hash(parsed_debug_candidate, line_config.config_hash)
    base_topology = _line_topology(line_config)
    scope_ids = list(parsed_debug_candidate.get("debug_scope", {}).get("station_ids", []))
    full_scope = scope_ids == expected_station_ids
    debug_ready = projection is not None
    result: dict[str, object] = {
        **base,
        "validation_state": "VALID",
        "debug_ready": debug_ready,
        "errors": [],
        "candidate": debug_candidate_to_dict(parsed_debug_candidate),
        "candidate_hash": f"sha256:{content_hash}",
        "debug_contract_hash": f"sha256:{debug_contract_content_hash(debug_contract)}",
        "line_config_hash": f"sha256:{line_config.config_hash}",
        "projection_hash": projection.projection_hash if projection else None,
        "line": option,
        "debug_scope": {"station_ids": scope_ids},
        "base_topology": base_topology,
        "engineering_rows": engineering_rows(parsed_debug_candidate),
        "engineering_export": engineering_export(
            parsed_debug_candidate,
            candidate_hash=f"sha256:{content_hash}",
            base_topology=base_topology,
        ),
    }
    if projection is None:
        result["validation_state"] = "VALID_RUNTIME_NOT_SUPPORTED"
        result["warnings"] = [
            {
                "field": "line_config",
                "message": (
                    "Configuration is valid, but the selected topology cannot be compiled "
                    "for the current single-PLC runtime."
                ),
            }
        ]
    else:
        result["ready_to_activate"] = full_scope
        result["line"] = {
            **option,
            "ready_to_activate": full_scope,
        }
    return result


def test_connection(
    raw: dict[str, object],
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
    store_path: Path | None = None,
    client_factory: Callable[[], Any] | None = None,
) -> dict[str, object]:
    validation = validate_candidate(
        raw,
        mapping_path=mapping_path,
        lines_path=lines_path,
        store_path=store_path,
    )
    if validation["errors"]:
        return {
            **validation,
            "status": "INVALID_CONFIGURATION",
            "read_only": True,
            "writes_performed": False,
            "operations": [],
        }
    if validation.get("debug_ready") is not True:
        return {
            **validation,
            "status": "CONFIG_NOT_RUNTIME_SUPPORTED",
            "read_only": True,
            "writes_performed": False,
            "operations": [],
    }

    candidate = _candidate_from_validated(validation)
    candidate_payload = validation.get("candidate")
    if not isinstance(candidate_payload, dict) or not isinstance(candidate_payload.get("stations"), list):
        return {
            **validation,
            "status": "INVALID_CONFIGURATION",
            "read_only": True,
            "writes_performed": False,
            "operations": [],
        }
    client = (client_factory or snap7.client.Client)()
    operations = ["connect"]
    probed_station_ids: list[str] = []
    probed_ranges: list[dict[str, int | str]] = []
    read_bytes = 0
    try:
        client.set_param(Parameter.RecvTimeout, candidate.connection_timeout_ms)
        client.connect(
            candidate.host,
            candidate.rack,
            candidate.slot,
            tcp_port=candidate.port,
        )
        for station in candidate_payload["stations"]:
            if not isinstance(station, dict):
                raise DeploymentConfigUnavailable("validated station mapping is invalid")
            station_id = str(station["station_id"])
            db_number = int(station["db_number"])
            read_start = int(station["read_start"])
            read_length = int(station["read_length"])
            client.db_read(db_number, read_start, read_length)
            operations.append("db_read")
            probed_station_ids.append(station_id)
            probed_ranges.append(
                {
                    "station_id": station_id,
                    "db_number": db_number,
                    "read_start": read_start,
                    "read_length": read_length,
                }
            )
            read_bytes += read_length
        operations.append("disconnect")
        return {
            **validation,
            "status": "CONNECTED_AND_READABLE",
            "read_only": True,
            "writes_performed": False,
            "operations": operations,
            "probed_station_ids": probed_station_ids,
            "probed_ranges": probed_ranges,
            "read_bytes": read_bytes,
            "message": "Read-only connection and selected-station bounded reads succeeded.",
        }
    except Exception as exc:
        return {
            **validation,
            "status": _connection_failure_status(exc),
            "read_only": True,
            "writes_performed": False,
            "operations": operations,
            "probed_station_ids": probed_station_ids,
            "probed_ranges": probed_ranges,
            "message": _connection_failure_message(exc),
        }
    finally:
        try:
            client.disconnect()
        except Exception:
            pass


def save_candidate(
    raw: dict[str, object],
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
    store_path: Path | None = None,
) -> dict[str, object]:
    validation = validate_candidate(
        raw,
        mapping_path=mapping_path,
        lines_path=lines_path,
        store_path=store_path,
    )
    if validation["errors"]:
        return validation

    candidate_id = uuid.uuid4().hex
    created_at = datetime.now(timezone.utc).isoformat()
    ready_to_activate = validation.get("ready_to_activate") is True
    status = (
        "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION"
        if ready_to_activate
        else "NOT ACTIVE / DEBUG PILOT ONLY / FULL-LINE ACTIVATION NOT READY"
    )
    document = {
        "candidate_id": candidate_id,
        "created_at": created_at,
        "status": status,
        "candidate_hash": validation["candidate_hash"],
        "line_config_hash": validation.get("line_config_hash"),
        "projection_hash": validation.get("projection_hash"),
        "active_mapping_hash": validation["active_mapping_hash"],
        "validation_state": validation["validation_state"],
        "debug_ready": validation.get("debug_ready") is True,
        "ready_to_activate": ready_to_activate,
        "debug_scope": validation.get("debug_scope"),
        "base_topology": validation.get("base_topology"),
        "candidate": validation["candidate"],
        "line": validation["line"],
        "debug_contract_hash": validation.get("debug_contract_hash"),
        "engineering_rows": validation.get("engineering_rows", []),
        "engineering_export": validation.get("engineering_export", ""),
        "last_connection_test": _safe_test_result(raw.get("last_connection_test")),
    }
    root = _store_root(store_path)
    destination = _candidate_path(root, candidate_id)
    _write_new_json(destination, document)
    return {
        **document,
        "retrieval_path": f"/api/v2/deployment/plc/candidates/{candidate_id}",
    }


def load_candidate(candidate_id: str, *, store_path: Path | None = None) -> dict[str, object]:
    if not _CANDIDATE_ID.fullmatch(candidate_id):
        raise DeploymentConfigUnavailable("candidate id is invalid")
    root = _store_root(store_path)
    path = _candidate_path(root, candidate_id)
    try:
        document = _read_json(path)
    except (OSError, ValueError, DeploymentConfigUnavailable) as exc:
        raise DeploymentConfigUnavailable("candidate is not available") from exc
    if not isinstance(document, dict) or document.get("candidate_id") != candidate_id:
        raise DeploymentConfigUnavailable("candidate document is invalid")
    return document


def activate_candidate(
    candidate_id: str,
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
    store_path: Path | None = None,
    client_factory: Callable[[], Any] | None = None,
) -> dict[str, object]:
    candidate = load_candidate(candidate_id, store_path=store_path)
    current_root, current_hash, current_source, current_path, current_used_overlay = _read_active_mapping(
        mapping_path,
        store_path=store_path,
    )
    previous_active_mapping_hash = f"sha256:{current_hash}"
    if candidate.get("active_mapping_hash") != previous_active_mapping_hash:
        return {
            "status": "STALE_CANDIDATE",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Saved Candidate was created against a different effective active mapping.",
        }

    candidate_payload = candidate.get("candidate")
    if not isinstance(candidate_payload, dict):
        raise DeploymentConfigUnavailable("saved candidate payload is invalid")
    validation = validate_candidate(
        candidate_payload,
        mapping_path=mapping_path,
        lines_path=lines_path,
        store_path=store_path,
    )
    if validation.get("errors") or validation.get("ready_to_activate") is not True:
        message = "Saved Candidate is not full-line activation-ready."
        if validation.get("debug_ready") is True:
            message = "Partial Debug Pilot scope is debug-ready but cannot be activated as the full line."
        return {
            "status": "CANDIDATE_NOT_READY",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "validation": validation,
            "writes_performed": False,
            "message": message,
        }
    if validation.get("active_mapping_hash") != previous_active_mapping_hash:
        return {
            "status": "STALE_CANDIDATE",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Effective active mapping changed while the Candidate was being checked.",
        }
    if candidate.get("candidate_hash") != validation.get("candidate_hash"):
        return {
            "status": "CANDIDATE_IDENTITY_MISMATCH",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Saved Candidate content does not match its recorded identity.",
        }
    if (
        candidate.get("projection_hash") is not None
        and candidate.get("projection_hash") != validation.get("projection_hash")
    ):
        return {
            "status": "CANDIDATE_IDENTITY_MISMATCH",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Saved Candidate projection identity does not match a fresh server compilation.",
        }
    selected_line = validation.get("line")
    if (
        not isinstance(selected_line, dict)
        or selected_line.get("plc_count") != 1
        or validation.get("projection_hash") is None
        or validation.get("ready_to_activate") is not True
    ):
        return {
            "status": "UNSUPPORTED_TOPOLOGY",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Only a compiled 3WS/10WS single-PLC topology can be activated.",
        }

    fresh_connection_test = test_connection(
        candidate_payload,
        mapping_path=mapping_path,
        lines_path=lines_path,
        store_path=store_path,
        client_factory=client_factory,
    )
    if (
        fresh_connection_test.get("status") != "CONNECTED_AND_READABLE"
        or fresh_connection_test.get("read_only") is not True
        or fresh_connection_test.get("writes_performed") is not False
    ):
        return {
            "status": "FRESH_TEST_FAILED",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "fresh_connection_test": fresh_connection_test,
            "writes_performed": False,
        }

    latest_root, latest_hash, latest_source, latest_path, latest_used_overlay = _read_active_mapping(
        mapping_path,
        store_path=store_path,
    )
    if latest_hash != current_hash:
        return {
            "status": "STALE_CANDIDATE",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": f"sha256:{latest_hash}",
            "fresh_connection_test": fresh_connection_test,
            "writes_performed": False,
            "message": "Effective active mapping changed before activation write.",
        }

    candidate_object = _candidate_from_validated(validation)
    line_path = _line_path(lines_path, candidate_object.line_config)
    line_config = load_line_config(line_path)
    projection = compile_runtime_mapping(
        line_config,
        candidate_to_connectivity(candidate_object),
        default_runtime_layout_registry(),
        line_config_source=str(line_path.relative_to(PROJECT_ROOT)),
        debug_contract=debug_contract_from_candidate(candidate_payload),
    )
    if (
        candidate.get("projection_hash") is not None
        and candidate.get("projection_hash") != projection.projection_hash
    ):
        return {
            "status": "CANDIDATE_IDENTITY_MISMATCH",
            "candidate_id": candidate_id,
            "previous_active_mapping_hash": previous_active_mapping_hash,
            "writes_performed": False,
            "message": "Projection changed between validation and activation.",
        }
    if (
        line_config.line_id == latest_root.get("line_id")
        and len(latest_root.get("stations", [])) == 3
        and latest_root.get("projection_hash") is None
    ):
        active_document, changed_fields = _overlay_connectivity_fields(
            latest_root,
            candidate_object,
        )
    else:
        active_document = projection.document
        changed_fields = _projection_changed_fields(latest_root, active_document)
    active_bytes = _dump_yaml(active_document)
    activation_id = uuid.uuid4().hex
    root = _store_root(store_path)
    active_path = root / "active" / "mapping.yaml"
    backup_path = root / "backups" / f"{activation_id}.yaml"
    activation_record_path = root / "activations" / f"{activation_id}.json"
    active_record_path = root / "active" / "activation.json"
    previous_bytes = latest_path.read_bytes()
    active_mapping_hash = f"sha256:{hashlib.sha256(active_bytes).hexdigest()}"
    record: dict[str, object] = {
        "activation_id": activation_id,
        "candidate_id": candidate_id,
        "candidate_hash": candidate["candidate_hash"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "ACTIVATED_RESTART_REQUIRED",
        "previous_active_mapping_hash": previous_active_mapping_hash,
        "previous_active_mapping_source": current_source,
        "previous_active_mapping_path": str(current_path),
        "previous_used_overlay": current_used_overlay,
        "active_mapping_hash": active_mapping_hash,
        "active_line_id": active_document.get("line_id"),
        "line_config_hash": projection.line_config_hash,
        "projection_hash": projection.projection_hash,
        "entry_station_id": active_document.get("entry_station_id"),
        "terminal_station_id": active_document.get("terminal_station_id"),
        "active_mapping_source": "active/mapping.yaml",
        "active_mapping_path": str(active_path),
        "changed_fields": changed_fields,
        "backup_path": str(backup_path),
        "activation_record_path": str(activation_record_path),
        "fresh_connection_test": fresh_connection_test,
        "writes_performed": False,
        "rollback_available": True,
    }
    try:
        _atomic_write_bytes(backup_path, previous_bytes)
        _atomic_write_bytes(active_path, active_bytes)
        readback = read_effective_mapping(
            mapping_path,
            deployment_config_dir=root,
        )
        if (
            not readback.used_overlay
            or readback.content_sha256 != active_mapping_hash.removeprefix("sha256:")
            or (
                active_document.get("projection_hash") is not None
                and readback.root.get("projection_hash") != active_document.get("projection_hash")
            )
        ):
            raise DeploymentConfigUnavailable("active mapping readback identity verification failed")
        _atomic_write_json(activation_record_path, record)
        _atomic_write_json(active_record_path, record)
    except Exception as exc:
        try:
            _restore_previous_mapping(
                mapping_path=mapping_path,
                store_root=root,
                previous_bytes=previous_bytes,
                previous_used_overlay=latest_used_overlay,
            )
        except Exception as restore_exc:
            raise DeploymentConfigUnavailable(
                f"activation failed and previous mapping restore failed: {restore_exc}"
            ) from exc
        raise DeploymentConfigUnavailable("activation failed before a durable activation record") from exc

    return record


def rollback_activation(
    activation_id: str,
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    store_path: Path | None = None,
) -> dict[str, object]:
    if not _ACTIVATION_ID.fullmatch(activation_id):
        raise DeploymentConfigUnavailable("activation id is invalid")
    root = _store_root(store_path)
    record_path = root / "activations" / f"{activation_id}.json"
    record = _read_json(record_path)
    if not isinstance(record, dict) or record.get("activation_id") != activation_id:
        raise DeploymentConfigUnavailable("activation record is invalid")
    if record.get("status") != "ACTIVATED_RESTART_REQUIRED":
        raise DeploymentConfigUnavailable("activation is not rollbackable")

    current_root, current_hash, _source, _path, _used_overlay = _read_active_mapping(
        mapping_path,
        store_path=store_path,
    )
    if f"sha256:{current_hash}" != record.get("active_mapping_hash"):
        return {
            "status": "ROLLBACK_BLOCKED_ACTIVE_MAPPING_CHANGED",
            "activation_id": activation_id,
            "writes_performed": False,
        }
    backup_path = root / "backups" / f"{activation_id}.yaml"
    backup_bytes = _read_regular_bytes(backup_path, "activation backup")
    previous_hash = hashlib.sha256(backup_bytes).hexdigest()
    if f"sha256:{previous_hash}" != record.get("previous_active_mapping_hash"):
        raise DeploymentConfigUnavailable("activation backup identity does not match record")

    try:
        _restore_previous_mapping(
            mapping_path=mapping_path,
            store_root=root,
            previous_bytes=backup_bytes,
            previous_used_overlay=record.get("previous_used_overlay") is True,
        )
        restored_root, restored_hash, _restored_source, _restored_path, _restored_overlay = _read_active_mapping(
            mapping_path,
            store_path=store_path,
        )
        if restored_hash != previous_hash or not isinstance(restored_root, dict):
            raise DeploymentConfigUnavailable("rollback readback identity verification failed")
        rolled_back_at = datetime.now(timezone.utc).isoformat()
        record = {
            **record,
            "status": "ROLLED_BACK",
            "rolled_back_at": rolled_back_at,
            "rollback_available": False,
            "active_mapping_hash": f"sha256:{restored_hash}",
            "writes_performed": False,
        }
        _atomic_write_json(record_path, record)
        _remove_exact_file(root / "active" / "activation.json")
    except Exception as exc:
        raise DeploymentConfigUnavailable("rollback failed") from exc
    return record


def _overlay_connectivity_fields(
    mapping: dict[str, Any],
    candidate: PlcDeploymentCandidate,
) -> tuple[dict[str, Any], list[str]]:
    document = deepcopy(mapping)
    plcs = document.get("plcs")
    if not isinstance(plcs, list) or len(plcs) != 1 or not isinstance(plcs[0], dict):
        raise DeploymentConfigUnavailable("active mapping PLC selection is ambiguous")
    plc = plcs[0]
    values = {
        "host": candidate.host,
        "port": candidate.port,
        "rack": candidate.rack,
        "slot": candidate.slot,
        "connection_timeout_ms": candidate.connection_timeout_ms,
        "poll_interval_ms": candidate.poll_interval_ms,
    }
    changed_fields = [field for field in CONNECTIVITY_FIELDS if plc.get(field) != values[field]]
    plc.update(values)
    return document, changed_fields


def _without_connectivity_fields(mapping: dict[str, Any]) -> dict[str, Any]:
    document = deepcopy(mapping)
    plcs = document.get("plcs")
    if isinstance(plcs, list):
        for plc in plcs:
            if isinstance(plc, dict):
                for field in CONNECTIVITY_FIELDS:
                    plc.pop(field, None)
    return document


def _dump_yaml(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(document, sort_keys=False).encode("utf-8")


def _read_active_mapping(
    mapping_path: Path,
    *,
    store_path: Path | None = None,
) -> tuple[dict[str, Any], str, str, Path, bool]:
    try:
        document = read_effective_mapping(
            mapping_path,
            deployment_config_dir=_store_root(store_path),
        )
        return (
            document.root,
            document.content_sha256,
            document.source,
            document.path,
            document.used_overlay,
        )
    except EffectiveMappingUnavailable as exc:
        raise DeploymentConfigUnavailable("active mapping is not available") from exc


def _store_root(store_path: Path | None) -> Path:
    root = Path(store_path) if store_path is not None else Path(
        os.environ.get("DEPLOYMENT_CONFIG_DIR", DEFAULT_STORE_PATH)
    )
    try:
        root_stat = root.lstat()
    except FileNotFoundError:
        return root
    except OSError as exc:
        raise DeploymentConfigUnavailable("deployment-config store cannot be inspected") from exc
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise DeploymentConfigUnavailable("deployment-config store must be a directory")
    return root


def _candidate_path(root: Path, candidate_id: str) -> Path:
    return root / "candidates" / f"{candidate_id}.json"


def _write_new_json(destination: Path, document: dict[str, object]) -> None:
    try:
        destination.lstat()
    except FileNotFoundError:
        pass
    else:
        raise DeploymentConfigUnavailable("destination already exists")
    _atomic_write_json(destination, document)


def _read_json(path: Path) -> object:
    raw_bytes = _read_regular_bytes(path, "deployment-config artifact")
    try:
        return json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise DeploymentConfigUnavailable("deployment-config JSON is invalid") from exc


def _read_regular_bytes(path: Path, label: str) -> bytes:
    try:
        path_stat = path.lstat()
    except OSError as exc:
        raise DeploymentConfigUnavailable(f"{label} is not available") from exc
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISREG(path_stat.st_mode):
        raise DeploymentConfigUnavailable(f"{label} must be a regular file")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise DeploymentConfigUnavailable(f"{label} cannot be read") from exc


def _atomic_write_json(destination: Path, document: dict[str, object]) -> None:
    raw = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    _atomic_write_bytes(destination, raw)


def _atomic_write_bytes(destination: Path, raw_bytes: bytes) -> None:
    _ensure_directory(destination.parent)
    try:
        destination_stat = destination.lstat()
    except FileNotFoundError:
        destination_stat = None
    except OSError as exc:
        raise DeploymentConfigUnavailable("activation destination cannot be inspected") from exc
    if destination_stat is not None and stat.S_ISLNK(destination_stat.st_mode):
        raise DeploymentConfigUnavailable("activation destination must not be a symlink")
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            dir=str(destination.parent),
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, destination)
        temporary_path = None
        try:
            directory_descriptor = os.open(destination.parent, os.O_RDONLY)
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except OSError:
            pass
    except OSError as exc:
        raise DeploymentConfigUnavailable("durable activation write failed") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def _ensure_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
        path_stat = path.lstat()
    except OSError as exc:
        raise DeploymentConfigUnavailable("deployment-config directory cannot be created") from exc
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISDIR(path_stat.st_mode):
        raise DeploymentConfigUnavailable("deployment-config directory must be a real directory")


def _remove_exact_file(path: Path) -> None:
    try:
        path_stat = path.lstat()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise DeploymentConfigUnavailable("activation artifact cannot be inspected") from exc
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISREG(path_stat.st_mode):
        raise DeploymentConfigUnavailable("activation artifact must be a regular file")
    try:
        path.unlink()
    except OSError as exc:
        raise DeploymentConfigUnavailable("activation artifact cannot be removed") from exc


def _restore_previous_mapping(
    *,
    mapping_path: Path,
    store_root: Path,
    previous_bytes: bytes,
    previous_used_overlay: bool,
) -> None:
    del mapping_path
    active_path = store_root / "active" / "mapping.yaml"
    if previous_used_overlay:
        _atomic_write_bytes(active_path, previous_bytes)
    else:
        _remove_exact_file(active_path)


def _load_active_activation(
    *,
    store_path: Path | None,
    active_mapping_hash: str,
) -> dict[str, object] | None:
    path = _store_root(store_path) / "active" / "activation.json"
    try:
        path.lstat()
    except FileNotFoundError:
        return None
    document = _read_json(path)
    if not isinstance(document, dict):
        raise DeploymentConfigUnavailable("active activation metadata is invalid")
    if document.get("status") != "ACTIVATED_RESTART_REQUIRED":
        return None
    if document.get("active_mapping_hash") != active_mapping_hash:
        raise DeploymentConfigUnavailable("active activation metadata does not match mapping identity")
    return document


def _try_compile_projection(
    config: LineConfig,
    connectivity: dict[str, object],
    *,
    line_config_source: str,
    debug_contract: dict[str, object] | None = None,
) -> tuple[RuntimeMappingProjection | None, RuntimeProjectionError | None]:
    try:
        return (
            compile_runtime_mapping(
                config,
                connectivity,
                default_runtime_layout_registry(),
                line_config_source=line_config_source,
                debug_contract=debug_contract,
            ),
            None,
        )
    except RuntimeProjectionError as exc:
        return None, exc


def candidate_to_connectivity(candidate: PlcDeploymentCandidate) -> dict[str, object]:
    return {
        field: getattr(candidate, field)
        for field in CONNECTIVITY_FIELDS
    }


def _projection_changed_fields(
    previous: dict[str, Any],
    projected: dict[str, Any],
) -> list[str]:
    changed_fields: list[str] = []
    if (
        previous.get("line_id") != projected.get("line_id")
        or previous.get("projection_hash") != projected.get("projection_hash")
        or previous.get("entry_station_id") != projected.get("entry_station_id")
        or previous.get("terminal_station_id") != projected.get("terminal_station_id")
        or previous.get("stations") != projected.get("stations")
        or previous.get("route_graph") != projected.get("route_graph")
    ):
        changed_fields.append("projection")
    previous_plcs = previous.get("plcs")
    projected_plcs = projected.get("plcs")
    if (
        isinstance(previous_plcs, list)
        and previous_plcs
        and isinstance(previous_plcs[0], dict)
        and isinstance(projected_plcs, list)
        and projected_plcs
        and isinstance(projected_plcs[0], dict)
    ):
        for field in CONNECTIVITY_FIELDS:
            if previous_plcs[0].get(field) != projected_plcs[0].get(field):
                changed_fields.append(field)
    return changed_fields


def _line_station_ids(config: LineConfig) -> list[str]:
    enabled = {
        station.station_id
        for station in config.stations
        if station.station_enabled
    }
    successors = {
        edge.from_station_id: edge.to_station_id
        for edge in config.route_graph.edges
        if edge.from_station_id in enabled and edge.to_station_id in enabled
    }
    ordered: list[str] = []
    current = config.route_graph.entry_station_id
    while current in enabled and current not in ordered:
        ordered.append(current)
        current = successors.get(current)
        if current is None:
            break
    if set(ordered) == enabled:
        return ordered
    return [
        station.station_id
        for station in sorted(
            (item for item in config.stations if item.station_enabled),
            key=lambda item: (item.station_order, item.station_id),
        )
    ]


def _line_topology(config: LineConfig) -> dict[str, object]:
    station_ids = _line_station_ids(config)
    return {
        "line_id": config.line_id,
        "entry_station_id": config.route_graph.entry_station_id,
        "terminal_station_id": config.route_graph.terminal_station_id,
        "station_ids": station_ids,
        "edges": [
            {
                "from_station_id": edge.from_station_id,
                "to_station_id": edge.to_station_id,
            }
            for edge in config.route_graph.edges
        ],
    }


def _mapping_topology(root: dict[str, Any], fallback_station_ids: list[str]) -> dict[str, object]:
    topology = root.get("topology") if isinstance(root.get("topology"), dict) else {}
    raw_station_ids = topology.get("station_ids")
    if not isinstance(raw_station_ids, list) or not raw_station_ids:
        raw_station_ids = [
            station.get("station_id")
            for station in root.get("stations", [])
            if isinstance(station, dict) and station.get("station_id")
        ]
    station_ids = [str(item) for item in raw_station_ids if item]
    if not station_ids:
        station_ids = list(fallback_station_ids)
    raw_edges = topology.get("edges")
    if not isinstance(raw_edges, list):
        raw_edges = root.get("route_graph", [])
    edges = [
        {
            "from_station_id": str(edge.get("from_station_id")),
            "to_station_id": str(edge.get("to_station_id")),
        }
        for edge in raw_edges
        if isinstance(edge, dict)
        and edge.get("from_station_id")
        and edge.get("to_station_id")
    ]
    return {
        "line_id": str(root.get("line_id", "")),
        "entry_station_id": str(
            root.get("entry_station_id")
            or topology.get("entry_station_id")
            or station_ids[0]
        ),
        "terminal_station_id": str(
            root.get("terminal_station_id")
            or topology.get("terminal_station_id")
            or station_ids[-1]
        ),
        "station_ids": station_ids,
        "edges": edges,
    }


def _line_option(
    config: LineConfig,
    file_name: str,
    active_line_id: object,
    *,
    station_ids: list[str] | None = None,
    projection: RuntimeMappingProjection | None = None,
    projection_error: RuntimeProjectionError | None = None,
) -> dict[str, object]:
    station_count = len(config.stations)
    plc_count = len(config.plcs)
    if projection is not None and station_count == 3 and plc_count == 1:
        capability = "CURRENTLY_SUPPORTED"
        capability_label = "CURRENTLY SUPPORTED"
        ready_to_activate = True
    elif projection is not None and station_count == 10 and plc_count == 1:
        capability = "CURRENTLY_SUPPORTED_SINGLE_PLC"
        capability_label = "CURRENTLY SUPPORTED / SINGLE PLC"
        ready_to_activate = True
    elif (
        station_count == 20
        and plc_count > 1
        and projection_error is not None
        and projection_error.classification == "MULTI_PLC_RUNTIME_UNSUPPORTED"
    ):
        capability = "CONFIG_VALID_MULTI_PLC_RUNTIME_NOT_YET_SUPPORTED"
        capability_label = "CONFIG VALID / MULTI-PLC RUNTIME NOT YET SUPPORTED"
        ready_to_activate = False
    else:
        capability = "CONFIG_VALID_RUNTIME_NOT_YET_SUPPORTED"
        capability_label = "CONFIG VALID / RUNTIME NOT YET SUPPORTED"
        ready_to_activate = False
    return {
        "file_name": file_name,
        "line_id": config.line_id,
        "name": config.name,
        "station_count": station_count,
        "station_ids": station_ids or _line_station_ids(config),
        "plc_count": plc_count,
        "config_hash": f"sha256:{config.config_hash}",
        "line_config_hash": f"sha256:{config.config_hash}",
        "projection_hash": projection.projection_hash if projection else None,
        "capability": capability,
        "capability_label": capability_label,
        "ready_to_activate": ready_to_activate,
        "active": config.line_id == active_line_id,
    }


def _line_path(lines_path: Path, file_name: str) -> Path:
    path = lines_path / file_name
    if Path(file_name).name != file_name or path.is_symlink() or not path.is_file():
        raise DeploymentConfigUnavailable("line configuration is not available")
    return path


def _candidate_from_validated(validation: dict[str, object]) -> PlcDeploymentCandidate:
    candidate = validation.get("candidate")
    if not isinstance(candidate, dict):
        raise DeploymentConfigUnavailable("validated candidate is missing")
    parsed, errors = parse_deployment_candidate(candidate)
    if parsed is None or errors:
        raise DeploymentConfigUnavailable("validated candidate is invalid")
    return parsed


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeploymentConfigUnavailable(f"active mapping field {field} is invalid")
    return value


def _required_int(value: object, field: str) -> int:
    if type(value) is not int:
        raise DeploymentConfigUnavailable(f"active mapping field {field} is invalid")
    return value


def _connection_failure_status(exc: Exception) -> str:
    message = str(exc).lower()
    if "timeout" in message or "timed out" in message:
        return "TIMEOUT"
    if "rack" in message or "slot" in message or "tsap" in message:
        return "RACK_SLOT_REJECTED"
    if "read" in message or "db" in message:
        return "RUNTIME_DB_UNREADABLE"
    return "CONNECTION_REFUSED"


def _connection_failure_message(exc: Exception) -> str:
    status = _connection_failure_status(exc)
    messages = {
        "TIMEOUT": "The PLC did not respond before the short read-only timeout.",
        "RACK_SLOT_REJECTED": "The PLC rejected the requested rack or slot.",
        "RUNTIME_DB_UNREADABLE": "The session connected, but the bounded runtime read failed.",
        "CONNECTION_REFUSED": "The PLC connection could not be established.",
    }
    return messages[status]


def _safe_test_result(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    allowed = {
        "status",
        "message",
        "read_only",
        "writes_performed",
        "operations",
        "probed_station_ids",
        "probed_ranges",
        "read_bytes",
    }
    result = {key: value[key] for key in sorted(allowed) if key in value}
    return result if result else None
