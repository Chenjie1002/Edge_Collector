#!/usr/bin/env python3
"""Read-only remote preflight contract for the frozen D2-R7B target."""

from __future__ import annotations

import getpass
import grp
import json
import os
import pwd
import socket
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


TRANSPORT_ENDPOINT = "mari@10.0.0.217"
EXPECTED_HOSTNAME = "Pi-5b-Li"
EXPECTED_PRINCIPAL = "mari"
EXPECTED_OWNER = "mari"
EXPECTED_GROUP = "mari"
EXPECTED_FILESYSTEM = "ext4"
EXPECTED_TARGET_DEVICE = 2050
EXPECTED_TARGET_INODE = 550698
EXPECTED_TARGET_BYTES = 5935
EXPECTED_TARGET_SHA256 = "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"
EXPECTED_TARGET_MODE = 0o644
EXPECTED_PARENT_DEVICE = 2050
EXPECTED_PARENT_MODE = 0o775
EXPECTED_CONTAINER_ID = "5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524"
EXPECTED_CONTAINER_NAME = "edge-mes-collector"
EXPECTED_CONFIGURED_IMAGE = "edge-mes-demo-collector"
EXPECTED_IMAGE_ID = (
    "sha256:0bfcbad5baa26db15642136c847ddccc"
    "210784a625767a9aa3b9c4104757ab4a"
)
EXPECTED_STARTED_AT = "2026-07-23T12:23:25.959624Z"
EXPECTED_RESTART_COUNT = 0
EXPECTED_MOUNT_SOURCE = "/opt/edge-mes-demo/config"
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
else:
    PARENT_PATH = "/opt/edge-mes-demo/config"
    TARGET_PATH = "/opt/edge-mes-demo/config/mapping.yaml"
    UPLOAD_TEMP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb"
    BACKUP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"


class ContractError(RuntimeError):
    pass


def _owner_name(uid: int) -> str:
    return pwd.getpwuid(uid).pw_name


def _group_name(gid: int) -> str:
    return grp.getgrgid(gid).gr_name


def _principal_name() -> str:
    return pwd.getpwuid(os.geteuid()).pw_name


def _filesystem_type(path: str) -> str:
    try:
        result = subprocess.run(
            ["findmnt", "-T", path, "-n", "-o", "FSTYPE"],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
        returncode = result.returncode
        stdout = result.stdout
        if returncode != 0:
            raise ContractError(f"findmnt exit code: {returncode}")
        if not isinstance(stdout, str):
            raise ContractError("findmnt stdout is not text")
        lines = stdout.splitlines()
        if len(lines) != 1 or lines[0].strip() != EXPECTED_FILESYSTEM:
            raise ContractError("findmnt FSTYPE output is not exactly one ext4 line")
        return lines[0].strip()
    except ContractError:
        raise
    except (OSError, subprocess.SubprocessError, UnicodeError, AttributeError, TypeError) as exc:
        raise ContractError(f"findmnt filesystem query failed: {exc}") from exc


def _docker_inspect() -> list[dict[str, Any]]:
    result = subprocess.run(
        ["docker", "inspect", EXPECTED_CONTAINER_ID],
        check=True,
        capture_output=True,
        text=True,
    )
    value = json.loads(result.stdout)
    if not isinstance(value, list):
        raise ContractError("docker inspect output is not a JSON list")
    return value


def _check_stat(
    path: str,
    *,
    label: str,
    expected_device: int | None = None,
    expected_inode: int | None = None,
    expected_bytes: int | None = None,
    expected_sha256: str | None = None,
    expected_owner: str | None = None,
    expected_group: str | None = None,
    expected_mode: int | None = None,
) -> os.stat_result:
    try:
        listed = os.lstat(path)
    except OSError as exc:
        raise ContractError(f"{label} cannot be lstat'ed: {exc}") from exc
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISREG(listed.st_mode):
        raise ContractError(f"{label} is not a regular non-symlink file")
    if expected_device is not None and listed.st_dev != expected_device:
        raise ContractError(f"{label} device drift: {listed.st_dev}")
    if expected_inode is not None and listed.st_ino != expected_inode:
        raise ContractError(f"{label} inode drift: {listed.st_ino}")
    if expected_bytes is not None and listed.st_size != expected_bytes:
        raise ContractError(f"{label} byte drift: {listed.st_size}")
    if expected_owner is not None and _owner_name(listed.st_uid) != expected_owner:
        raise ContractError(f"{label} owner drift: {_owner_name(listed.st_uid)}")
    if expected_group is not None and _group_name(listed.st_gid) != expected_group:
        raise ContractError(f"{label} group drift: {_group_name(listed.st_gid)}")
    if expected_mode is not None and stat.S_IMODE(listed.st_mode) != expected_mode:
        raise ContractError(f"{label} mode drift: {stat.S_IMODE(listed.st_mode):04o}")
    if expected_sha256 is not None:
        import hashlib

        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if digest != expected_sha256:
            raise ContractError(f"{label} SHA-256 drift: {digest}")
    return listed


def _check_parent(*, filesystem: str | None = None) -> os.stat_result:
    try:
        parent = os.lstat(PARENT_PATH)
    except OSError as exc:
        raise ContractError(f"parent cannot be lstat'ed: {exc}") from exc
    if not stat.S_ISDIR(parent.st_mode) or stat.S_ISLNK(parent.st_mode):
        raise ContractError("parent is not a regular directory")
    if parent.st_dev != EXPECTED_PARENT_DEVICE:
        raise ContractError(f"parent device drift: {parent.st_dev}")
    if _owner_name(parent.st_uid) != EXPECTED_OWNER or _group_name(parent.st_gid) != EXPECTED_GROUP:
        raise ContractError("parent owner/group drift")
    if stat.S_IMODE(parent.st_mode) != EXPECTED_PARENT_MODE:
        raise ContractError(f"parent mode drift: {stat.S_IMODE(parent.st_mode):04o}")
    if (filesystem if filesystem is not None else _filesystem_type(PARENT_PATH)) != EXPECTED_FILESYSTEM:
        raise ContractError("parent filesystem drift")
    uid = pwd.getpwnam(EXPECTED_OWNER).pw_uid
    gid = grp.getgrnam(EXPECTED_GROUP).gr_gid
    writable = parent.st_uid == uid and bool(parent.st_mode & stat.S_IWUSR)
    writable = writable or parent.st_gid == gid and bool(parent.st_mode & stat.S_IWGRP)
    writable = writable or bool(parent.st_mode & stat.S_IWOTH)
    if not writable:
        raise ContractError("parent is not writable by mari")
    return parent


def _check_mount(payload: dict[str, Any]) -> None:
    mounts = payload.get("Mounts")
    if not isinstance(mounts, list):
        raise ContractError("container Mounts is not a list")
    exact = [item for item in mounts if isinstance(item, dict) and item.get("Destination") == EXPECTED_MOUNT_DESTINATION]
    if len(exact) != 1:
        raise ContractError("exact collector config mount is absent or duplicated")
    mount = exact[0]
    observed = (mount.get("Source"), mount.get("Destination"), mount.get("Type"), mount.get("RW"))
    expected = (EXPECTED_MOUNT_SOURCE, EXPECTED_MOUNT_DESTINATION, EXPECTED_MOUNT_TYPE, EXPECTED_MOUNT_RW)
    if observed != expected:
        raise ContractError(f"collector mount drift: {observed!r}")


def _check_container(payload: dict[str, Any]) -> None:
    if payload.get("Id") != EXPECTED_CONTAINER_ID:
        raise ContractError("container ID drift")
    if payload.get("Name") not in (f"/{EXPECTED_CONTAINER_NAME}", EXPECTED_CONTAINER_NAME):
        raise ContractError("container name drift")
    if payload.get("Image") != EXPECTED_IMAGE_ID:
        raise ContractError("container image ID drift")
    config = payload.get("Config")
    if not isinstance(config, dict) or config.get("Image") != EXPECTED_CONFIGURED_IMAGE:
        raise ContractError("container configured image drift")
    state = payload.get("State")
    if not isinstance(state, dict):
        raise ContractError("container State is not an object")
    if state.get("Running") is not True:
        raise ContractError("collector is not running")
    if state.get("StartedAt") != EXPECTED_STARTED_AT:
        raise ContractError("collector StartedAt drift")
    if payload.get("RestartCount") != EXPECTED_RESTART_COUNT:
        raise ContractError("collector RestartCount drift")
    _check_mount(payload)


def run_preflight(
    *,
    docker_payload: list[dict[str, Any]] | None = None,
    hostname: str | None = None,
    principal: str | None = None,
    filesystem: str | None = None,
) -> dict[str, Any]:
    observed_hostname = socket.gethostname() if hostname is None else hostname
    if observed_hostname != EXPECTED_HOSTNAME:
        raise ContractError(f"hostname drift: {observed_hostname}")
    observed_principal = _principal_name() if principal is None else principal
    if observed_principal != EXPECTED_PRINCIPAL:
        raise ContractError(f"principal drift: {observed_principal}")
    if principal is None and getpass.getuser() != observed_principal:
        raise ContractError("login principal drift")
    target = _check_stat(
        TARGET_PATH,
        label="target",
        expected_device=EXPECTED_TARGET_DEVICE,
        expected_inode=EXPECTED_TARGET_INODE,
        expected_bytes=EXPECTED_TARGET_BYTES,
        expected_sha256=EXPECTED_TARGET_SHA256,
        expected_owner=EXPECTED_OWNER,
        expected_group=EXPECTED_GROUP,
        expected_mode=EXPECTED_TARGET_MODE,
    )
    realpath = os.path.realpath(TARGET_PATH)
    if realpath != TARGET_PATH:
        raise ContractError(f"target realpath drift: {realpath}")
    parent = _check_parent(filesystem=filesystem)
    for artifact in (UPLOAD_TEMP_PATH, BACKUP_PATH):
        if os.path.lexists(artifact):
            raise ContractError(f"stale artifact exists: {artifact}")
    payloads = _docker_inspect() if docker_payload is None else docker_payload
    if len(payloads) != 1 or not isinstance(payloads[0], dict):
        raise ContractError("docker inspect did not return exactly one object")
    _check_container(payloads[0])
    return {
        "transport_endpoint": TRANSPORT_ENDPOINT,
        "hostname": observed_hostname,
        "principal": observed_principal,
        "target_device": target.st_dev,
        "target_inode": target.st_ino,
        "parent_device": parent.st_dev,
        "filesystem": filesystem if filesystem is not None else _filesystem_type(PARENT_PATH),
    }


def main() -> int:
    try:
        result = run_preflight()
    except (ContractError, OSError, subprocess.SubprocessError, KeyError, ValueError) as exc:
        print(f"HOLD / NO WRITE: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "PASS", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
