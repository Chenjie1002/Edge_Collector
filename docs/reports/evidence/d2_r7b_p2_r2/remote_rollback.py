#!/usr/bin/env python3
"""Independent, bounded rollback helper; no restart, activation or cleanup."""

from __future__ import annotations

import errno
import fcntl
import grp
import hashlib
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
EXPECTED_PARENT_DEVICE = 2050
EXPECTED_PARENT_MODE = 0o775
EXPECTED_FILE_MODE = 0o644
EXPECTED_FILESYSTEM = "ext4"

_root_override = os.environ.get("D2_R7B_SYNTHETIC_ROOT")
if _root_override:
    _root = Path(_root_override)
    PARENT_PATH = str(_root / "config")
    TARGET_PATH = str(_root / "config" / "mapping.yaml")
    BACKUP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    ROLLBACK_TEMP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
else:
    PARENT_PATH = "/opt/edge-mes-demo/config"
    TARGET_PATH = "/opt/edge-mes-demo/config/mapping.yaml"
    BACKUP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
    ROLLBACK_TEMP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"


class ContractError(RuntimeError):
    pass


before_rollback_rename_hook = lambda: None


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


def _parent() -> tuple[int, os.stat_result]:
    listed = os.lstat(PARENT_PATH)
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISDIR(listed.st_mode):
        raise ContractError("parent is not a regular directory")
    if listed.st_dev != EXPECTED_PARENT_DEVICE:
        raise ContractError("parent device drift")
    if _owner_name(listed.st_uid) != EXPECTED_OWNER or _group_name(listed.st_gid) != EXPECTED_GROUP:
        raise ContractError("parent owner/group drift")
    if stat.S_IMODE(listed.st_mode) != EXPECTED_PARENT_MODE:
        raise ContractError("parent mode drift")
    if _filesystem_type(PARENT_PATH) != EXPECTED_FILESYSTEM:
        raise ContractError("parent filesystem drift")
    fd = os.open(PARENT_PATH, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    opened = os.fstat(fd)
    if opened.st_dev != listed.st_dev or opened.st_ino != listed.st_ino:
        os.close(fd)
        raise ContractError("parent changed while opening")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(fd)
        if exc.errno in (errno.EACCES, errno.EAGAIN):
            raise ContractError("bounded parent lock unavailable") from exc
        raise
    return fd, listed


def _path_stat(
    path: str,
    *,
    expected_bytes: int,
    expected_sha256: str,
    expected_inode: int | None,
    expected_device: int,
    label: str,
) -> os.stat_result:
    listed = os.lstat(path)
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISREG(listed.st_mode):
        raise ContractError(f"{label} is not regular/non-symlink")
    if listed.st_dev != expected_device or (expected_inode is not None and listed.st_ino != expected_inode):
        raise ContractError(f"{label} device/inode drift")
    if listed.st_size != expected_bytes:
        raise ContractError(f"{label} byte drift")
    if _owner_name(listed.st_uid) != EXPECTED_OWNER or _group_name(listed.st_gid) != EXPECTED_GROUP:
        raise ContractError(f"{label} owner/group drift")
    if stat.S_IMODE(listed.st_mode) != EXPECTED_FILE_MODE:
        raise ContractError(f"{label} mode drift")
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected_sha256:
        raise ContractError(f"{label} SHA-256 drift")
    return listed


def _open_verified(
    path: str,
    *,
    expected_bytes: int,
    expected_sha256: str,
    expected_inode: int | None,
    expected_device: int,
    label: str,
) -> tuple[int, os.stat_result]:
    listed = _path_stat(
        path,
        expected_bytes=expected_bytes,
        expected_sha256=expected_sha256,
        expected_inode=expected_inode,
        expected_device=expected_device,
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
    expected_bytes: int,
    expected_sha256: str,
    expected_device: int,
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


def rollback() -> dict[str, object]:
    parent_fd, parent = _parent()
    target_fd = backup_fd = rollback_fd = None
    try:
        target_fd, target_start = _open_verified(
            TARGET_PATH,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expected_inode=None,
            expected_device=parent.st_dev,
            label="deployed target",
        )
        _verify_fd(
            target_fd,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expected_device=parent.st_dev,
            label="deployed target",
        )
        backup_fd, backup_start = _open_verified(
            BACKUP_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=None,
            expected_device=parent.st_dev,
            label="backup",
        )
        _verify_fd(
            backup_fd,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_device=parent.st_dev,
            label="backup",
        )
        if os.path.lexists(ROLLBACK_TEMP_PATH):
            raise ContractError("rollback temp already exists")
        rollback_fd = os.open(ROLLBACK_TEMP_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        _copy_fd(backup_fd, rollback_fd)
        os.fchmod(rollback_fd, EXPECTED_FILE_MODE)
        os.fsync(rollback_fd)
        os.close(rollback_fd)
        rollback_fd = None
        check_fd, check_identity = _open_verified(
            ROLLBACK_TEMP_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=None,
            expected_device=parent.st_dev,
            label="rollback temp",
        )
        _verify_fd(
            check_fd,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_device=parent.st_dev,
            label="rollback temp",
        )
        os.close(check_fd)
        os.fsync(parent_fd)

        before_rollback_rename_hook()
        target_before = _path_stat(
            TARGET_PATH,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expected_inode=target_start.st_ino,
            expected_device=parent.st_dev,
            label="target before rollback rename",
        )
        backup_before = _path_stat(
            BACKUP_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=backup_start.st_ino,
            expected_device=parent.st_dev,
            label="backup before rollback rename",
        )
        temp_before = _path_stat(
            ROLLBACK_TEMP_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=check_identity.st_ino,
            expected_device=parent.st_dev,
            label="rollback temp before rename",
        )
        if target_before.st_ino != target_start.st_ino or backup_before.st_ino != backup_start.st_ino or temp_before.st_ino != check_identity.st_ino:
            raise ContractError("rollback rename inputs changed")
        try:
            os.replace(ROLLBACK_TEMP_PATH, TARGET_PATH)
        except OSError as exc:
            if exc.errno == errno.EXDEV:
                raise ContractError("EXDEV: atomic rollback unavailable; no fallback") from exc
            raise
        os.fsync(parent_fd)
        target_final = _path_stat(
            TARGET_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=None,
            expected_device=parent.st_dev,
            label="target after rollback",
        )
        if target_final.st_ino == target_start.st_ino:
            raise ContractError("rollback target inode did not change")
        backup_final = _path_stat(
            BACKUP_PATH,
            expected_bytes=EXPECTED_OLD_BYTES,
            expected_sha256=EXPECTED_OLD_SHA256,
            expected_inode=backup_start.st_ino,
            expected_device=parent.st_dev,
            label="backup after rollback",
        )
        return {
            "target_inode_before": target_start.st_ino,
            "target_inode_after": target_final.st_ino,
            "backup_inode": backup_final.st_ino,
            "target_sha256": EXPECTED_OLD_SHA256,
            "backup_sha256": EXPECTED_OLD_SHA256,
        }
    finally:
        for fd in (target_fd, backup_fd, rollback_fd):
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
        result = rollback()
    except (ContractError, OSError, ValueError) as exc:
        print(f"HOLD / NO WRITE: {exc}", file=sys.stderr)
        return 2
    print(f"PASS rollback target_inode={result['target_inode_before']}->{result['target_inode_after']} backup_inode={result['backup_inode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
