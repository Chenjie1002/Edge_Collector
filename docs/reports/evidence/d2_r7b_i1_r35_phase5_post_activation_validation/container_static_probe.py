#!/usr/bin/env python3
"""R35 active-container, read-only source/import/static-mapping probe."""

import hashlib
import importlib
import json
import sys
from pathlib import Path


SCHEMA_VERSION = "d2-r7b-i1-r35-container-static/v1"
EXPECTED_MAPPING = {
    "bytes": 7112,
    "sha256": "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d",
    "schema_version": "runtime-mapping/v1",
    "config_version": "2026.06.26-slice-a",
    "line_id": "LINE_001",
    "read_plan_count": 4,
    "resolved_config_hash": "0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38",
}
SOURCE_HASHES = {
    "/app/app/main.py": "a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090",
    "/app/app/services/event_collector.py": "eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f",
    "/app/app/services/accepted_station_event_fact.py": "6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911",
    "/app/app/services/storage.py": "f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b",
    "/app/app/plc/mapping.py": "c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098",
    "/app/app/plc/read_plan.py": "fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6",
    "/app/app/services/resolved_config_registry.py": "1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c",
    "/app/common/station_event/__init__.py": "d8a214d0c4a85e7bbaf7b5e79e6db905115be1f50effb27357fa9f371ea1c7a7",
    "/app/common/station_event/constants.py": "6dd60705ab192a1c889f0a4652d478f7d367bd24b980fc092c48a51e25214e11",
    "/app/common/station_event/errors.py": "355c882f51cc7c66cdf8f22c73c0d72633391dc8403d4f9f428b0b8ac510b4f3",
    "/app/common/station_event/fingerprint.py": "cb35dcf5ab5ba9ccb3e60d0e38b1c86cf24717559cc70e250adf297dff939608",
    "/app/common/station_event/lifecycle.py": "afec2c75010b8642239d2494c57f470f3414c4fbff486b588589adf7bc4efcff",
    "/app/common/station_event/models.py": "176627b71f32bdef08c75a6bfe3b7badab1094e8ec2c3cf7b1e719d0a2d1df77",
    "/app/common/station_event/projection.py": "39ed6034d87e23718a22a8a66fbb60af365a5d7b573ff045a021b7206c708623",
    "/app/common/station_event/serialization.py": "9cbabbd42e5685311829030b13f24fa16396fb853458e3f51bd7cb7bf5124407",
    "/app/common/station_event/validation.py": "e7cff46b91112236873744a32dafec5160a0ca6036f184106e1ec4a232724bd1",
}
REQUIRED_IMPORTS = (
    "common.station_event",
    "app.main",
    "app.services.event_collector",
    "app.services.accepted_station_event_fact",
    "app.services.storage",
    "app.plc.mapping",
    "app.plc.read_plan",
    "app.services.resolved_config_registry",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def emit(status: str, classification: str, observed: dict, assertions: dict) -> None:
    terminal = {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "classification": classification,
        "observed": observed,
        "assertions": assertions,
        "mutation_audit": {
            "filesystem_writes": 0,
            "db_connections": 0,
            "api_calls": 0,
            "plc_connections": 0,
            "socket_connections": 0,
            "production_data_generated": 0,
            "runtime_worker_constructions": 0,
            "storage_constructions": 0,
        },
        "evidence_boundary": {
            "STATIC_MAPPING_INITIALIZED": status == "PASS",
            "RUNTIME_LOADED": False,
            "PRODUCTION_ACCEPTED": False,
        },
    }
    sys.stdout.write(
        json.dumps(
            terminal,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def main() -> None:
    observed = {
        "dont_write_bytecode": sys.dont_write_bytecode,
        "source_hashes": {},
        "imports": {},
        "mapping": {},
    }
    assertions = {
        "dont_write_bytecode": sys.dont_write_bytecode is True,
        "source_hashes_exact": False,
        "imports_exact": False,
        "mapping_exact": False,
    }

    try:
        for source_path, expected_hash in sorted(SOURCE_HASHES.items()):
            data = Path(source_path).read_bytes()
            observed["source_hashes"][source_path] = {
                "bytes": len(data),
                "sha256": sha256(data),
                "expected_sha256": expected_hash,
                "match": sha256(data) == expected_hash,
            }
        assertions["source_hashes_exact"] = (
            len(observed["source_hashes"]) == len(SOURCE_HASHES)
            and all(item["match"] for item in observed["source_hashes"].values())
        )
        if not assertions["source_hashes_exact"]:
            emit("HOLD", "SOURCE_IDENTITY_FAILED", observed, assertions)
            return
    except Exception as exc:
        observed["source_error"] = type(exc).__name__
        emit("HOLD", "SOURCE_IDENTITY_FAILED", observed, assertions)
        return

    try:
        for module_name in REQUIRED_IMPORTS:
            imported = importlib.import_module(module_name)
            observed["imports"][module_name] = {
                "module": imported.__name__,
                "success": True,
            }
        assertions["imports_exact"] = (
            tuple(observed["imports"]) == REQUIRED_IMPORTS
            and all(item["success"] for item in observed["imports"].values())
        )
        if not assertions["imports_exact"]:
            emit("HOLD", "IMPORT_CLOSURE_FAILED", observed, assertions)
            return
    except Exception as exc:
        observed["import_error"] = {
            "type": type(exc).__name__,
            "module": module_name,
        }
        emit("HOLD", "IMPORT_CLOSURE_FAILED", observed, assertions)
        return

    try:
        mapping_path = Path("/app/config/mapping.yaml")
        mapping_bytes = mapping_path.read_bytes()
        from app.plc.mapping import load_edge_mapping
        from app.plc.read_plan import build_read_plans
        from app.services.resolved_config_registry import (
            build_resolved_config_snapshot_from_mapping,
        )

        mapping = load_edge_mapping(mapping_path)
        read_plans = build_read_plans(mapping)
        resolved = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
        observed["mapping"] = {
            "path": str(mapping_path),
            "bytes": len(mapping_bytes),
            "sha256": sha256(mapping_bytes),
            "schema_version": mapping.schema_version,
            "config_version": mapping.config_version,
            "line_id": mapping.line_id,
            "read_plan_count": len(read_plans),
            "resolved_config_hash": resolved.config_hash,
        }
        assertions["mapping_exact"] = observed["mapping"] == {
            "path": "/app/config/mapping.yaml",
            **EXPECTED_MAPPING,
        }
        if not assertions["mapping_exact"]:
            emit("HOLD", "MAPPING_IDENTITY_FAILED", observed, assertions)
            return
    except Exception as exc:
        observed["mapping_error"] = type(exc).__name__
        emit("HOLD", "MAPPING_IDENTITY_FAILED", observed, assertions)
        return

    if not all(assertions.values()):
        emit("HOLD", "CONTAINER_STATIC_PROBE_INVALID", observed, assertions)
        return
    emit("PASS", "STATIC_MAPPING_INITIALIZED", observed, assertions)


if __name__ == "__main__":
    main()
