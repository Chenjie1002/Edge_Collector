#!/usr/bin/env python3
"""Read-only D2-R7B file and Collector postflight classification."""

from __future__ import annotations

import hashlib
import json
import os
import pwd
import grp
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


TRANSPORT_ENDPOINT = "mari@10.0.0.217"
EXPECTED_OWNER = "mari"
EXPECTED_GROUP = "mari"
EXPECTED_FILESYSTEM = "ext4"
EXPECTED_PARENT_DEVICE = 2050
EXPECTED_FILE_MODE = 0o644
EXPECTED_OLD_BYTES = 5935
EXPECTED_OLD_SHA256 = "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"
EXPECTED_NEW_BYTES = 7112
EXPECTED_NEW_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
EXPECTED_CONTAINER_ID = "5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524"
EXPECTED_CONTAINER_NAME = "edge-mes-collector"
EXPECTED_CONFIGURED_IMAGE = "edge-mes-demo-collector"
EXPECTED_IMAGE_ID = (
    "sha256:0bfcbad5baa26db15642136c847ddccc"
    "210784a625767a9aa3b9c4104757ab4a"
)
EXPECTED_STARTED_AT = "2026-07-23T12:23:25.959624Z"
EXPECTED_RESTART_COUNT = 0
EXPECTED_MOUNT_DESTINATION = "/app/config"
EXPECTED_MOUNT_TYPE = "bind"
EXPECTED_MOUNT_RW = False

_root_override = os.environ.get("D2_R7B_SYNTHETIC_ROOT")
if _root_override:
    _root = Path(_root_override)
    PARENT_PATH = str(_root / "config")
    TARGET_PATH = str(_root / "config" / "mapping.yaml")
    UPLOAD_TEMP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-new.8de5edb")
    BACKUP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    ROLLBACK_TEMP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    EXPECTED_MOUNT_SOURCE = str(_root / "config")
    EXPECTED_OWNER = os.environ.get("D2_R7B_SYNTHETIC_OWNER", EXPECTED_OWNER)
    EXPECTED_GROUP = os.environ.get("D2_R7B_SYNTHETIC_GROUP", EXPECTED_GROUP)
    EXPECTED_PARENT_DEVICE = int(os.environ.get("D2_R7B_SYNTHETIC_DEVICE", EXPECTED_PARENT_DEVICE))
    EXPECTED_FILESYSTEM = os.environ.get("D2_R7B_SYNTHETIC_FILESYSTEM", EXPECTED_FILESYSTEM)
    EXPECTED_OLD_SHA256 = os.environ.get("D2_R7B_SYNTHETIC_OLD_SHA256", EXPECTED_OLD_SHA256)
else:
    PARENT_PATH = "/opt/edge-mes-demo/config"
    TARGET_PATH = "/opt/edge-mes-demo/config/mapping.yaml"
    UPLOAD_TEMP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb"
    BACKUP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
    ROLLBACK_TEMP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
    EXPECTED_MOUNT_SOURCE = "/opt/edge-mes-demo/config"


class ContractError(RuntimeError):
    pass


def _owner_name(uid: int) -> str:
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return f"uid:{uid}"


def _group_name(gid: int) -> str:
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return f"gid:{gid}"


def _digest(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)


def _observed_stat(path: str, listed: os.stat_result) -> dict[str, Any]:
    return {
        "path": path,
        "realpath": os.path.realpath(path),
        "device": listed.st_dev,
        "inode": listed.st_ino,
        "owner": _owner_name(listed.st_uid),
        "group": _group_name(listed.st_gid),
        "mode": f"{stat.S_IMODE(listed.st_mode):04o}",
        "bytes": listed.st_size,
        "sha256": _digest(path),
    }


def _classify_file(
    path: str,
    *,
    absent_state: str,
    expected_state: str,
    expected_bytes: int,
    expected_sha256: str,
) -> dict[str, Any]:
    if not os.path.lexists(path):
        return {"path": path, "state": absent_state, "exists": False, "realpath": None}
    try:
        listed = os.lstat(path)
    except OSError as exc:
        return {"path": path, "state": "UNSAFE_TYPE", "exists": True, "error": str(exc)}
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISREG(listed.st_mode):
        return {
            "path": path,
            "state": "UNSAFE_TYPE",
            "exists": True,
            "realpath": os.path.realpath(path),
            "device": listed.st_dev,
            "inode": listed.st_ino,
            "mode": f"{stat.S_IMODE(listed.st_mode):04o}",
        }
    observed = _observed_stat(path, listed)
    observed["exists"] = True
    observed_realpath = observed["realpath"]
    exact_realpath = os.path.isabs(path) and observed_realpath == path
    observed["exact_realpath"] = exact_realpath
    exact = (
        exact_realpath
        and observed["device"] == EXPECTED_PARENT_DEVICE
        and observed["owner"] == EXPECTED_OWNER
        and observed["group"] == EXPECTED_GROUP
        and observed["mode"] == f"{EXPECTED_FILE_MODE:04o}"
        and observed["bytes"] == expected_bytes
        and observed["sha256"] == expected_sha256
    )
    observed["state"] = expected_state if exact else "OTHER"
    return observed


def _classify_target() -> dict[str, Any]:
    if not os.path.lexists(TARGET_PATH):
        return {"path": TARGET_PATH, "state": "MISSING", "exists": False, "realpath": None}
    try:
        listed = os.lstat(TARGET_PATH)
    except OSError as exc:
        return {"path": TARGET_PATH, "state": "UNSAFE_TYPE", "exists": True, "error": str(exc)}
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISREG(listed.st_mode):
        return {
            "path": TARGET_PATH,
            "state": "UNSAFE_TYPE",
            "exists": True,
            "realpath": os.path.realpath(TARGET_PATH),
            "device": listed.st_dev,
            "inode": listed.st_ino,
            "mode": f"{stat.S_IMODE(listed.st_mode):04o}",
        }
    observed = _observed_stat(TARGET_PATH, listed)
    observed["exists"] = True
    observed_realpath = observed["realpath"]
    exact_realpath = os.path.isabs(TARGET_PATH) and observed_realpath == TARGET_PATH
    observed["exact_realpath"] = exact_realpath
    common_exact = (
        exact_realpath
        and observed["device"] == EXPECTED_PARENT_DEVICE
        and observed["owner"] == EXPECTED_OWNER
        and observed["group"] == EXPECTED_GROUP
        and observed["mode"] == f"{EXPECTED_FILE_MODE:04o}"
    )
    if common_exact and observed["bytes"] == EXPECTED_NEW_BYTES and observed["sha256"] == EXPECTED_NEW_SHA256:
        observed["state"] = "NEW_EXACT"
    elif common_exact and observed["bytes"] == EXPECTED_OLD_BYTES and observed["sha256"] == EXPECTED_OLD_SHA256:
        observed["state"] = "OLD_EXACT"
    else:
        observed["state"] = "OTHER"
    return observed


def _collector_from_payload(payload: list[dict[str, Any]]) -> dict[str, Any]:
    if len(payload) != 1 or not isinstance(payload[0], dict):
        return {"state": "UNKNOWN_OR_UNSAFE", "error": "docker inspect did not return exactly one object"}
    item = payload[0]
    config = item.get("Config") if isinstance(item.get("Config"), dict) else {}
    state = item.get("State") if isinstance(item.get("State"), dict) else {}
    mounts = item.get("Mounts") if isinstance(item.get("Mounts"), list) else []
    exact_mounts = [mount for mount in mounts if isinstance(mount, dict) and mount.get("Destination") == EXPECTED_MOUNT_DESTINATION]
    observed_mount = exact_mounts[0] if len(exact_mounts) == 1 else None
    observed = {
        "id": item.get("Id"),
        "name": item.get("Name"),
        "image": item.get("Image"),
        "configured_image": config.get("Image"),
        "running": state.get("Running"),
        "started_at": state.get("StartedAt"),
        "restart_count": item.get("RestartCount"),
        "mount": None if observed_mount is None else {
            "source": observed_mount.get("Source"),
            "destination": observed_mount.get("Destination"),
            "type": observed_mount.get("Type"),
            "rw": observed_mount.get("RW"),
        },
    }
    expected = {
        "id": EXPECTED_CONTAINER_ID,
        "name": (f"/{EXPECTED_CONTAINER_NAME}", EXPECTED_CONTAINER_NAME),
        "image": EXPECTED_IMAGE_ID,
        "configured_image": EXPECTED_CONFIGURED_IMAGE,
        "running": True,
        "started_at": EXPECTED_STARTED_AT,
        "restart_count": EXPECTED_RESTART_COUNT,
        "mount": {
            "source": EXPECTED_MOUNT_SOURCE,
            "destination": EXPECTED_MOUNT_DESTINATION,
            "type": EXPECTED_MOUNT_TYPE,
            "rw": EXPECTED_MOUNT_RW,
        },
    }
    unchanged = (
        observed["id"] == expected["id"]
        and observed["name"] in expected["name"]
        and observed["image"] == expected["image"]
        and observed["configured_image"] == expected["configured_image"]
        and observed["running"] == expected["running"]
        and observed["started_at"] == expected["started_at"]
        and observed["restart_count"] == expected["restart_count"]
        and observed["mount"] == expected["mount"]
    )
    return {"state": "UNCHANGED" if unchanged else "DRIFT", "observed": observed, "expected": expected}


def _collector_inspect(*, docker_payload: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if docker_payload is not None:
        return _collector_from_payload(docker_payload)
    docker_executable = os.environ.get("D2_R7B_DOCKER_EXECUTABLE", "docker")
    command = [docker_executable, "inspect", EXPECTED_CONTAINER_ID]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"state": "UNKNOWN_OR_UNSAFE", "command": command, "error": str(exc)}
    if result.returncode != 0:
        return {"state": "UNKNOWN_OR_UNSAFE", "command": command, "exit_code": result.returncode, "stderr": result.stderr.strip()}
    try:
        decoded = json.loads(result.stdout)
    except (TypeError, ValueError) as exc:
        return {"state": "UNKNOWN_OR_UNSAFE", "command": command, "error": f"invalid JSON: {exc}"}
    if not isinstance(decoded, list):
        return {"state": "UNKNOWN_OR_UNSAFE", "command": command, "error": "docker inspect output is not a list"}
    inspected = _collector_from_payload(decoded)
    inspected["command"] = command
    inspected["exit_code"] = result.returncode
    return inspected


def _classify(
    target: dict[str, Any],
    upload: dict[str, Any],
    backup: dict[str, Any],
    rollback_temp: dict[str, Any],
    collector: dict[str, Any],
) -> str:
    states = (target["state"], upload["state"], backup["state"], rollback_temp["state"])
    if any(state in {"UNSAFE_TYPE", "MISSING", "OTHER"} for state in states):
        if target["state"] == "NEW_EXACT" or backup["state"] == "OLD_EXACT":
            return "PARTIAL_DEPLOYMENT"
        return "UNKNOWN_OR_UNSAFE"
    if collector["state"] == "UNKNOWN_OR_UNSAFE":
        return "UNKNOWN_OR_UNSAFE"
    if (
        target["state"] == "NEW_EXACT"
        and upload["state"] == "ABSENT"
        and backup["state"] == "OLD_EXACT"
        and rollback_temp["state"] == "ABSENT"
    ):
        return "DEPLOYED_IDENTITY_VERIFIED" if collector["state"] == "UNCHANGED" else "PARTIAL_DEPLOYMENT"
    if target["state"] == "OLD_EXACT" and upload["state"] == "ABSENT" and backup["state"] == "ABSENT" and rollback_temp["state"] == "ABSENT":
        return "NO_MUTATION" if collector["state"] == "UNCHANGED" else "UNKNOWN_OR_UNSAFE"
    if target["state"] == "OLD_EXACT" and upload["state"] == "NEW_EXACT" and backup["state"] == "ABSENT" and rollback_temp["state"] == "ABSENT":
        return "UPLOAD_STAGED_NO_REPLACEMENT"
    if target["state"] == "OLD_EXACT" and upload["state"] == "ABSENT" and backup["state"] == "OLD_EXACT" and rollback_temp["state"] == "ABSENT":
        return "BACKUP_CREATED_NO_REPLACEMENT"
    if target["state"] == "NEW_EXACT" or backup["state"] == "OLD_EXACT":
        return "PARTIAL_DEPLOYMENT"
    return "UNKNOWN_OR_UNSAFE"


def run_postflight(*, docker_payload: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    target = _classify_target()
    upload = _classify_file(
        UPLOAD_TEMP_PATH,
        absent_state="ABSENT",
        expected_state="NEW_EXACT",
        expected_bytes=EXPECTED_NEW_BYTES,
        expected_sha256=EXPECTED_NEW_SHA256,
    )
    backup = _classify_file(
        BACKUP_PATH,
        absent_state="ABSENT",
        expected_state="OLD_EXACT",
        expected_bytes=EXPECTED_OLD_BYTES,
        expected_sha256=EXPECTED_OLD_SHA256,
    )
    rollback_temp = _classify_file(
        ROLLBACK_TEMP_PATH,
        absent_state="ABSENT",
        expected_state="OLD_EXACT",
        expected_bytes=EXPECTED_OLD_BYTES,
        expected_sha256=EXPECTED_OLD_SHA256,
    )
    collector = _collector_inspect(docker_payload=docker_payload)
    classification = _classify(target, upload, backup, rollback_temp, collector)
    return {
        "status": "PASS" if classification == "DEPLOYED_IDENTITY_VERIFIED" else "HOLD",
        "phase": "REMOTE_POSTFLIGHT",
        "classification": classification,
        "target_state": target,
        "upload_temp_state": upload,
        "backup_state": backup,
        "rollback_temp_state": rollback_temp,
        "collector_state": collector,
        "exact_artifact_paths": {
            "target": TARGET_PATH,
            "upload_temp": UPLOAD_TEMP_PATH,
            "backup": BACKUP_PATH,
            "rollback_temp": ROLLBACK_TEMP_PATH,
        },
        "task_lifecycle_actions": {
            "cleanup_count": 0,
            "rollback_count": 0,
            "restart_count_by_task": 0,
            "activation_count": 0,
        },
        "message": "RUNTIME CONFIG LOAD NOT CLAIMED" if classification == "DEPLOYED_IDENTITY_VERIFIED" else "POSTFLIGHT DID NOT PROVE DEPLOYED IDENTITY",
    }


def main() -> int:
    try:
        result = run_postflight()
    except (ContractError, OSError, ValueError, KeyError, TypeError) as exc:
        result = {
            "status": "HOLD",
            "phase": "REMOTE_POSTFLIGHT",
            "classification": "UNKNOWN_OR_UNSAFE",
            "target_state": {"path": TARGET_PATH, "state": "UNKNOWN_OR_UNSAFE"},
            "upload_temp_state": {"path": UPLOAD_TEMP_PATH, "state": "UNKNOWN_OR_UNSAFE"},
            "backup_state": {"path": BACKUP_PATH, "state": "UNKNOWN_OR_UNSAFE"},
            "rollback_temp_state": {"path": ROLLBACK_TEMP_PATH, "state": "UNKNOWN_OR_UNSAFE"},
            "collector_state": {"state": "UNKNOWN_OR_UNSAFE"},
            "exact_artifact_paths": {
                "target": TARGET_PATH,
                "upload_temp": UPLOAD_TEMP_PATH,
                "backup": BACKUP_PATH,
                "rollback_temp": ROLLBACK_TEMP_PATH,
            },
            "task_lifecycle_actions": {
                "cleanup_count": 0,
                "rollback_count": 0,
                "restart_count_by_task": 0,
                "activation_count": 0,
            },
            "message": f"POSTFLIGHT ERROR: {exc}",
        }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["classification"] == "DEPLOYED_IDENTITY_VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
