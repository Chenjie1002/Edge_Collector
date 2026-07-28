#!/usr/bin/env python3
"""Locked, fail-closed atomic deployment helper; no cleanup or lifecycle actions."""

from __future__ import annotations

import errno
import fcntl
import grp
import hashlib
import json
import os
import pwd
import stat
import subprocess
import sys
from pathlib import Path


EXPECTED_OLD_BYTES = 5935
EXPECTED_OLD_SHA256 = "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"
EXPECTED_NEW_BYTES = 7112
EXPECTED_NEW_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
EXPECTED_OWNER = "mari"
EXPECTED_GROUP = "mari"
EXPECTED_TARGET_DEVICE = 2050
EXPECTED_TARGET_INODE = 550698
EXPECTED_PARENT_MODE = 0o775
EXPECTED_FILE_MODE = 0o644
EXPECTED_FILESYSTEM = "ext4"

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


before_rename_recheck_hook = lambda: None


def _owner_name(uid: int) -> str:
    return pwd.getpwuid(uid).pw_name


def _group_name(gid: int) -> str:
    return grp.getgrgid(gid).gr_name


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


def _read_fd(fd: int) -> tuple[int, str, bytes]:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    total = 0
    digest = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        digest.update(chunk)
    return total, digest.hexdigest(), b"".join(chunks)


def _write_all(fd: int, payload: bytes) -> None:
    offset = 0
    while offset < len(payload):
        written = os.write(fd, payload[offset:])
        if written <= 0:
            raise ContractError("partial write made no progress")
        offset += written


def _same_stat(left: os.stat_result, right: os.stat_result) -> bool:
    return (
        left.st_dev == right.st_dev
        and left.st_ino == right.st_ino
        and left.st_size == right.st_size
        and left.st_uid == right.st_uid
        and left.st_gid == right.st_gid
        and stat.S_IMODE(left.st_mode) == stat.S_IMODE(right.st_mode)
    )


def _check_parent() -> tuple[int, os.stat_result]:
    parent = os.lstat(PARENT_PATH)
    if stat.S_ISLNK(parent.st_mode) or not stat.S_ISDIR(parent.st_mode):
        raise ContractError("parent is not a regular directory")
    if parent.st_dev != EXPECTED_TARGET_DEVICE:
        raise ContractError(f"parent device drift: {parent.st_dev}")
    if _owner_name(parent.st_uid) != EXPECTED_OWNER or _group_name(parent.st_gid) != EXPECTED_GROUP:
        raise ContractError("parent owner/group drift")
    if stat.S_IMODE(parent.st_mode) != EXPECTED_PARENT_MODE:
        raise ContractError("parent mode drift")
    if _filesystem_type(PARENT_PATH) != EXPECTED_FILESYSTEM:
        raise ContractError("parent filesystem drift")
    parent_fd = os.open(PARENT_PATH, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    fd_stat = os.fstat(parent_fd)
    if fd_stat.st_dev != parent.st_dev or fd_stat.st_ino != parent.st_ino:
        os.close(parent_fd)
        raise ContractError("parent changed while opening")
    try:
        fcntl.flock(parent_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(parent_fd)
        if exc.errno in (errno.EACCES, errno.EAGAIN):
            raise ContractError("bounded parent lock unavailable") from exc
        raise
    return parent_fd, parent


def _check_path_identity(
    path: str,
    *,
    expected_device: int | None,
    expected_inode: int | None,
    expected_bytes: int,
    expected_sha256: str,
    expected_mode: int,
    label: str,
    opened_fd: int | None = None,
) -> os.stat_result:
    listed = os.lstat(path)
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISREG(listed.st_mode):
        raise ContractError(f"{label} is not regular/non-symlink")
    if expected_device is not None and listed.st_dev != expected_device:
        raise ContractError(f"{label} device drift: {listed.st_dev}")
    if expected_inode is not None and listed.st_ino != expected_inode:
        raise ContractError(f"{label} inode drift: {listed.st_ino}")
    if listed.st_size != expected_bytes:
        raise ContractError(f"{label} byte drift: {listed.st_size}")
    if _owner_name(listed.st_uid) != EXPECTED_OWNER or _group_name(listed.st_gid) != EXPECTED_GROUP:
        raise ContractError(f"{label} owner/group drift")
    if stat.S_IMODE(listed.st_mode) != expected_mode:
        raise ContractError(f"{label} mode drift")
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != expected_sha256:
        raise ContractError(f"{label} SHA-256 drift: {digest}")
    if opened_fd is not None and not _same_stat(listed, os.fstat(opened_fd)):
        raise ContractError(f"{label} changed after open")
    return listed


def _open_checked(
    path: str,
    *,
    expected_device: int | None,
    expected_inode: int | None,
    expected_bytes: int,
    expected_sha256: str,
    label: str,
) -> tuple[int, os.stat_result]:
    listed = _check_path_identity(
        path,
        expected_device=expected_device,
        expected_inode=expected_inode,
        expected_bytes=expected_bytes,
        expected_sha256=expected_sha256,
        expected_mode=EXPECTED_FILE_MODE,
        label=label,
    )
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    if not _same_stat(listed, os.fstat(fd)):
        os.close(fd)
        raise ContractError(f"{label} changed while opening")
    return fd, listed


def _verify_fd(
    fd: int,
    *,
    expected_device: int,
    expected_bytes: int,
    expected_sha256: str,
    label: str,
) -> tuple[int, str, os.stat_result]:
    opened = os.fstat(fd)
    if opened.st_dev != expected_device or not stat.S_ISREG(opened.st_mode):
        raise ContractError(f"{label} FD identity drift")
    if _owner_name(opened.st_uid) != EXPECTED_OWNER or _group_name(opened.st_gid) != EXPECTED_GROUP:
        raise ContractError(f"{label} FD owner/group drift")
    if stat.S_IMODE(opened.st_mode) != EXPECTED_FILE_MODE:
        raise ContractError(f"{label} FD mode drift")
    size, digest, _ = _read_fd(fd)
    if not _same_stat(opened, os.fstat(fd)) or size != opened.st_size:
        raise ContractError(f"{label} changed while reading")
    if size != expected_bytes or digest != expected_sha256:
        raise ContractError(f"{label} content identity drift")
    return size, digest, opened


def _copy_fd(source_fd: int, destination_fd: int) -> None:
    os.lseek(source_fd, 0, os.SEEK_SET)
    while True:
        chunk = os.read(source_fd, 1024 * 1024)
        if not chunk:
            return
        _write_all(destination_fd, chunk)


def deploy() -> dict[str, object]:
    parent_fd, parent = _check_parent()
    target_fd = upload_fd = backup_fd = None
    try:
        target_listed = os.lstat(TARGET_PATH)
        if stat.S_ISLNK(target_listed.st_mode) or not stat.S_ISREG(target_listed.st_mode):
            raise ContractError("target is not regular/non-symlink")
        if target_listed.st_dev != EXPECTED_TARGET_DEVICE or target_listed.st_ino != EXPECTED_TARGET_INODE:
            raise ContractError("target initial device/inode drift")
        target_fd, target_identity = _open_checked(
            TARGET_PATH,
            expected_device=EXPECTED_TARGET_DEVICE,
            expected_inode=EXPECTED_TARGET_INODE,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            label="target",
        )
        _, _, target_identity = _verify_fd(
            target_fd,
            expected_device=EXPECTED_TARGET_DEVICE,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            label="target",
        )
        upload_fd, upload_identity = _open_checked(
            UPLOAD_TEMP_PATH,
            expected_device=parent.st_dev,
            expected_inode=None,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            label="upload",
        )
        upload_size, upload_digest, upload_identity = _verify_fd(
            upload_fd,
            expected_device=parent.st_dev,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            label="upload",
        )
        if os.path.lexists(BACKUP_PATH):
            raise ContractError("backup already exists")
        backup_fd = os.open(BACKUP_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        _copy_fd(target_fd, backup_fd)
        os.fchmod(backup_fd, EXPECTED_FILE_MODE)
        os.fsync(backup_fd)
        os.close(backup_fd)
        backup_fd = None
        backup_fd, backup_identity = _open_checked(
            BACKUP_PATH,
            expected_device=parent.st_dev,
            expected_inode=None,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            label="backup",
        )
        _, _, backup_identity = _verify_fd(
            backup_fd,
            expected_device=parent.st_dev,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            label="backup",
        )
        os.close(backup_fd)
        backup_fd = None
        os.fsync(parent_fd)
        before_rename_recheck_hook()

        latest_target = _check_path_identity(
            TARGET_PATH,
            expected_device=EXPECTED_TARGET_DEVICE,
            expected_inode=EXPECTED_TARGET_INODE,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_mode=EXPECTED_FILE_MODE,
            label="target before rename",
        )
        latest_upload = _check_path_identity(
            UPLOAD_TEMP_PATH,
            expected_device=parent.st_dev,
            expected_inode=upload_identity.st_ino,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expected_mode=EXPECTED_FILE_MODE,
            label="upload before rename",
        )
        if latest_target.st_ino != target_identity.st_ino or latest_upload.st_ino != upload_identity.st_ino:
            raise ContractError("rename inputs changed")
        upload_realpath = os.path.realpath(UPLOAD_TEMP_PATH)
        try:
            os.replace(UPLOAD_TEMP_PATH, TARGET_PATH)
        except OSError as exc:
            if exc.errno == errno.EXDEV:
                raise ContractError("EXDEV: atomic replacement unavailable; no fallback") from exc
            raise
        os.fsync(parent_fd)
        final_target = _check_path_identity(
            TARGET_PATH,
            expected_device=parent.st_dev,
            expected_inode=None,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expected_mode=EXPECTED_FILE_MODE,
            label="target after rename",
        )
        if final_target.st_ino == target_identity.st_ino:
            raise ContractError("target inode did not change")
        final_backup = _check_path_identity(
            BACKUP_PATH,
            expected_device=parent.st_dev,
            expected_inode=backup_identity.st_ino,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_mode=EXPECTED_FILE_MODE,
            label="backup after rename",
        )
        return {
            "status": "PASS",
            "phase": "REMOTE_DEPLOY",
            "operation": "ATOMIC_REPLACE_WITH_BACKUP",
            "source_upload_temp": {
                "state": "CONSUMED_BY_ATOMIC_REPLACE",
                "path": UPLOAD_TEMP_PATH,
                "realpath": upload_realpath,
                "bytes": upload_size,
                "sha256": upload_digest,
                "device": upload_identity.st_dev,
                "inode": upload_identity.st_ino,
                "owner": _owner_name(upload_identity.st_uid),
                "group": _group_name(upload_identity.st_gid),
                "mode": f"{stat.S_IMODE(upload_identity.st_mode):04o}",
            },
            "target": {
                "path": TARGET_PATH,
                "realpath": os.path.realpath(TARGET_PATH),
                "bytes": final_target.st_size,
                "sha256": EXPECTED_NEW_SHA256,
                "device": final_target.st_dev,
                "inode_before": target_identity.st_ino,
                "inode_after": final_target.st_ino,
                "owner": _owner_name(final_target.st_uid),
                "group": _group_name(final_target.st_gid),
                "mode": f"{stat.S_IMODE(final_target.st_mode):04o}",
            },
            "backup": {
                "path": BACKUP_PATH,
                "realpath": os.path.realpath(BACKUP_PATH),
                "bytes": final_backup.st_size,
                "sha256": EXPECTED_OLD_SHA256,
                "device": final_backup.st_dev,
                "inode": final_backup.st_ino,
                "owner": _owner_name(final_backup.st_uid),
                "group": _group_name(final_backup.st_gid),
                "mode": f"{stat.S_IMODE(final_backup.st_mode):04o}",
            },
        }
    finally:
        for fd in (target_fd, upload_fd, backup_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass
        try:
            fcntl.flock(parent_fd, fcntl.LOCK_UN)
        finally:
            os.close(parent_fd)


def main() -> int:
    try:
        result = deploy()
    except (ContractError, OSError, ValueError) as exc:
        print(f"HOLD / NO WRITE: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
