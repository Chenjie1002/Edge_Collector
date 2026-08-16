from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import snap7
from snap7.type import Parameter

from common.line_config import (
    LineConfig,
    LineConfigError,
    PlcDeploymentCandidate,
    candidate_content_hash,
    candidate_to_dict,
    load_line_config,
    parse_deployment_candidate,
)

from app.services.scope_catalog import ScopeCatalogUnavailable, read_mapping_document


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


class DeploymentConfigUnavailable(Exception):
    pass


def load_active_deployment_config(
    mapping_path: Path = DEFAULT_MAPPING_PATH,
) -> dict[str, object]:
    root, content_sha256 = _read_active_mapping(mapping_path)
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

    return {
        "authority": {
            "kind": "active_runtime_mapping",
            "source": _required_text(root.get("authoritative_source"), "authoritative_source"),
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
    }


def load_line_options(
    lines_path: Path = DEFAULT_LINES_PATH,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
) -> dict[str, object]:
    active = load_active_deployment_config(mapping_path)
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
        items.append(_line_option(config, line_path.name, active["line_id"]))
    if not items:
        raise DeploymentConfigUnavailable("no line configurations are available")
    return {"items": items}


def validate_candidate(
    raw: dict[str, object],
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
) -> dict[str, object]:
    active = load_active_deployment_config(mapping_path)
    candidate, errors = parse_deployment_candidate(raw)
    base: dict[str, object] = {
        "validation_state": "INVALID",
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

    option = _line_option(line_config, candidate.line_config, active["line_id"])
    content_hash = candidate_content_hash(candidate, line_config.config_hash)
    result: dict[str, object] = {
        **base,
        "validation_state": "VALID",
        "errors": [],
        "candidate": candidate_to_dict(candidate),
        "candidate_hash": f"sha256:{content_hash}",
        "line": option,
    }
    if option["ready_to_activate"] is not True:
        result["validation_state"] = "VALID_RUNTIME_NOT_SUPPORTED"
        result["warnings"] = [
            {
                "field": "line_config",
                "message": "Configuration is valid, but the current R2 runtime cannot be marked ready for this topology.",
            }
        ]
    else:
        result["ready_to_activate"] = True
    return result


def test_connection(
    raw: dict[str, object],
    *,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    lines_path: Path = DEFAULT_LINES_PATH,
    client_factory: Callable[[], Any] | None = None,
) -> dict[str, object]:
    validation = validate_candidate(raw, mapping_path=mapping_path, lines_path=lines_path)
    if validation["errors"]:
        return {
            **validation,
            "status": "INVALID_CONFIGURATION",
            "read_only": True,
            "writes_performed": False,
            "operations": [],
        }
    if validation["ready_to_activate"] is not True:
        return {
            **validation,
            "status": "CONFIG_NOT_RUNTIME_SUPPORTED",
            "read_only": True,
            "writes_performed": False,
            "operations": [],
        }

    candidate = _candidate_from_validated(validation)
    line_config = load_line_config(
        _line_path(lines_path, candidate.line_config)
    )
    runtime_db = line_config.plcs[0].runtime_db
    client = (client_factory or snap7.client.Client)()
    operations = ["connect", "db_read", "disconnect"]
    try:
        client.set_param(Parameter.RecvTimeout, candidate.connection_timeout_ms)
        client.connect(
            candidate.host,
            candidate.rack,
            candidate.slot,
            tcp_port=candidate.port,
        )
        data = client.db_read(runtime_db, 0, 16)
        return {
            **validation,
            "status": "CONNECTED_AND_READABLE",
            "read_only": True,
            "writes_performed": False,
            "operations": operations,
            "runtime_db": runtime_db,
            "read_bytes": len(data),
            "message": "Read-only connection and bounded runtime probe succeeded.",
        }
    except Exception as exc:
        return {
            **validation,
            "status": _connection_failure_status(exc),
            "read_only": True,
            "writes_performed": False,
            "operations": operations,
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
    validation = validate_candidate(raw, mapping_path=mapping_path, lines_path=lines_path)
    if validation["errors"]:
        return validation

    candidate_id = uuid.uuid4().hex
    created_at = datetime.now(timezone.utc).isoformat()
    document = {
        "candidate_id": candidate_id,
        "created_at": created_at,
        "status": "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION",
        "candidate_hash": validation["candidate_hash"],
        "active_mapping_hash": validation["active_mapping_hash"],
        "validation_state": validation["validation_state"],
        "candidate": validation["candidate"],
        "line": validation["line"],
        "last_connection_test": _safe_test_result(raw.get("last_connection_test")),
    }
    root = store_path or Path(os.environ.get("DEPLOYMENT_CONFIG_DIR", DEFAULT_STORE_PATH))
    root.mkdir(parents=True, exist_ok=True)
    destination = root / f"{candidate_id}.json"
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
    return {
        **document,
        "retrieval_path": f"/api/v2/deployment/plc/candidates/{candidate_id}",
    }


def load_candidate(candidate_id: str, *, store_path: Path | None = None) -> dict[str, object]:
    if not _CANDIDATE_ID.fullmatch(candidate_id):
        raise DeploymentConfigUnavailable("candidate id is invalid")
    root = store_path or Path(os.environ.get("DEPLOYMENT_CONFIG_DIR", DEFAULT_STORE_PATH))
    path = root / f"{candidate_id}.json"
    try:
        with path.open(encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError) as exc:
        raise DeploymentConfigUnavailable("candidate is not available") from exc
    if not isinstance(document, dict) or document.get("candidate_id") != candidate_id:
        raise DeploymentConfigUnavailable("candidate document is invalid")
    return document


def _read_active_mapping(mapping_path: Path) -> tuple[dict[str, Any], str]:
    try:
        return read_mapping_document(mapping_path)
    except ScopeCatalogUnavailable as exc:
        raise DeploymentConfigUnavailable("active mapping is not available") from exc


def _line_option(config: LineConfig, file_name: str, active_line_id: object) -> dict[str, object]:
    station_count = len(config.stations)
    plc_count = len(config.plcs)
    if station_count == 3 and plc_count == 1:
        capability = "CURRENTLY_SUPPORTED"
        capability_label = "CURRENTLY SUPPORTED"
        ready_to_activate = True
    elif station_count == 20 and plc_count > 1:
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
        "plc_count": plc_count,
        "config_hash": f"sha256:{config.config_hash}",
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
    allowed = {"status", "message", "read_only", "writes_performed", "operations"}
    result = {key: value[key] for key in sorted(allowed) if key in value}
    return result if result else None
