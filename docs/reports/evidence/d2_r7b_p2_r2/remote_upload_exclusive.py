#!/usr/bin/env python3
"""Exclusive-create upload helper; it never touches the target or backup."""

from __future__ import annotations

import hashlib
import json
import errno
import fcntl
import grp
import os
import pwd
import stat
import sys
from pathlib import Path


EXPECTED_NEW_BYTES = 7112
EXPECTED_NEW_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
EXPECTED_OWNER = "mari"
EXPECTED_GROUP = "mari"
EXPECTED_PARENT_DEVICE = 2050
EXPECTED_PARENT_MODE = 0o775
EXPECTED_MODE = 0o644
EXPECTED_FILESYSTEM = "ext4"
UPLOAD_BASENAME = ".mapping.yaml.d2-r7b-new.8de5edb"

_root_override = os.environ.get("D2_R7B_SYNTHETIC_ROOT")
if _root_override:
    _root = Path(_root_override)
    PARENT_PATH = str(_root / "config")
    UPLOAD_TEMP_PATH = str(_root / "config" / ".mapping.yaml.d2-r7b-new.8de5edb")
else:
    PARENT_PATH = "/opt/edge-mes-demo/config"
    UPLOAD_TEMP_PATH = "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb"

if _root_override:
    EXPECTED_OWNER = os.environ.get("D2_R7B_SYNTHETIC_OWNER", EXPECTED_OWNER)
    EXPECTED_GROUP = os.environ.get("D2_R7B_SYNTHETIC_GROUP", EXPECTED_GROUP)
    EXPECTED_PARENT_DEVICE = int(os.environ.get("D2_R7B_SYNTHETIC_DEVICE", EXPECTED_PARENT_DEVICE))


class ContractError(RuntimeError):
    pass


def _owner_name(uid: int) -> str:
    return pwd.getpwuid(uid).pw_name


def _group_name(gid: int) -> str:
    return grp.getgrgid(gid).gr_name


def _filesystem_type(path: str, *, pass_fds: tuple[int, ...] = ()) -> str:
    import subprocess

    try:
        result = subprocess.run(
            ["findmnt", "-T", path, "-n", "-o", "FSTYPE"],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            pass_fds=pass_fds,
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


def _expected_ids() -> tuple[int, int]:
    return pwd.getpwnam(EXPECTED_OWNER).pw_uid, grp.getgrnam(EXPECTED_GROUP).gr_gid


def _parent_fd_path(parent_fd: int) -> str:
    return f"/proc/self/fd/{parent_fd}"


def _same_directory(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _parent_stat() -> tuple[int, os.stat_result]:
    listed = os.lstat(PARENT_PATH)
    if stat.S_ISLNK(listed.st_mode) or not stat.S_ISDIR(listed.st_mode):
        raise ContractError("parent is not a regular directory")
    if listed.st_dev != EXPECTED_PARENT_DEVICE:
        raise ContractError(f"parent device drift: {listed.st_dev}")
    if _owner_name(listed.st_uid) != EXPECTED_OWNER or _group_name(listed.st_gid) != EXPECTED_GROUP:
        raise ContractError("parent owner/group drift")
    if stat.S_IMODE(listed.st_mode) != EXPECTED_PARENT_MODE:
        raise ContractError("parent mode drift")

    parent_fd: int | None = None
    try:
        parent_fd = os.open(PARENT_PATH, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        opened = os.fstat(parent_fd)
        if not _same_directory(listed, opened):
            raise ContractError("parent changed while opening")
        try:
            fcntl.flock(parent_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno in (errno.EACCES, errno.EAGAIN):
                raise ContractError("bounded parent lock unavailable") from exc
            raise

        stable = os.fstat(parent_fd)
        if not _same_directory(opened, stable):
            raise ContractError("parent FD identity changed")
        if _owner_name(stable.st_uid) != EXPECTED_OWNER or _group_name(stable.st_gid) != EXPECTED_GROUP:
            raise ContractError("parent owner/group drift")
        if stat.S_IMODE(stable.st_mode) != EXPECTED_PARENT_MODE:
            raise ContractError("parent mode drift")
        parent_fd_path = _parent_fd_path(parent_fd)
        try:
            filesystem = _filesystem_type(parent_fd_path, pass_fds=(parent_fd,))
        except TypeError as exc:
            if "unexpected keyword argument 'pass_fds'" not in str(exc):
                raise
            filesystem = _filesystem_type(parent_fd_path)
        if filesystem != EXPECTED_FILESYSTEM:
            raise ContractError("parent filesystem drift")
        current = os.lstat(PARENT_PATH)
        if not _same_directory(stable, current):
            raise ContractError("parent changed after filesystem check")

        uid, gid = _expected_ids()
        writable = stable.st_uid == uid and bool(stable.st_mode & stat.S_IWUSR)
        writable = writable or stable.st_gid == gid and bool(stable.st_mode & stat.S_IWGRP)
        writable = writable or bool(stable.st_mode & stat.S_IWOTH)
        if not writable:
            raise ContractError("parent is not writable by mari")
        return parent_fd, stable
    except BaseException:
        if parent_fd is not None:
            try:
                fcntl.flock(parent_fd, fcntl.LOCK_UN)
            finally:
                os.close(parent_fd)
        raise


def _read_all_fd(fd: int) -> tuple[int, str, bytes]:
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


def _same_stat(left: os.stat_result, right: os.stat_result) -> bool:
    return (
        left.st_dev == right.st_dev
        and left.st_ino == right.st_ino
        and left.st_size == right.st_size
        and left.st_uid == right.st_uid
        and left.st_gid == right.st_gid
        and stat.S_IMODE(left.st_mode) == stat.S_IMODE(right.st_mode)
    )


def _verify_upload_fd(fd: int, parent_device: int) -> tuple[int, str, os.stat_result]:
    opened = os.fstat(fd)
    if not stat.S_ISREG(opened.st_mode):
        raise ContractError("upload temp is not regular")
    if opened.st_dev != parent_device:
        raise ContractError("upload temp device drift")
    if _owner_name(opened.st_uid) != EXPECTED_OWNER or _group_name(opened.st_gid) != EXPECTED_GROUP:
        raise ContractError("upload temp owner/group drift")
    if stat.S_IMODE(opened.st_mode) != EXPECTED_MODE:
        raise ContractError("upload temp mode drift")
    size, digest, _ = _read_all_fd(fd)
    if not _same_stat(opened, os.fstat(fd)) or size != opened.st_size:
        raise ContractError("upload temp identity changed while reading")
    if size != EXPECTED_NEW_BYTES or digest != EXPECTED_NEW_SHA256:
        raise ContractError("upload temp content identity drift")
    return size, digest, opened


def _verify_created_fd(fd: int, parent_device: int) -> os.stat_result:
    opened = os.fstat(fd)
    if not stat.S_ISREG(opened.st_mode):
        raise ContractError("upload temp is not regular")
    if opened.st_dev != parent_device:
        raise ContractError("upload temp device drift")
    if _owner_name(opened.st_uid) != EXPECTED_OWNER or _group_name(opened.st_gid) != EXPECTED_GROUP:
        raise ContractError("upload temp owner/group drift")
    if stat.S_IMODE(opened.st_mode) != 0o600:
        raise ContractError("upload temp initial mode drift")
    return opened


def _upload_name_exists(parent_fd: int) -> bool:
    try:
        os.stat(UPLOAD_BASENAME, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _write_all(fd: int, payload: bytes) -> None:
    offset = 0
    while offset < len(payload):
        written = os.write(fd, payload[offset:])
        if written <= 0:
            raise ContractError("partial write made no progress")
        offset += written


def upload(payload: bytes) -> dict[str, object]:
    # The complete stdin payload is validated before any path is opened for create.
    if len(payload) != EXPECTED_NEW_BYTES:
        raise ContractError(f"stdin byte count drift: {len(payload)}")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_NEW_SHA256:
        raise ContractError(f"stdin SHA-256 drift: {digest}")
    parent_fd, parent = _parent_stat()
    fd: int | None = None
    created = False
    try:
        if _upload_name_exists(parent_fd):
            raise ContractError("stale upload temp exists")
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        fd = os.open(UPLOAD_BASENAME, flags, 0o600, dir_fd=parent_fd)
        created = True
        _verify_created_fd(fd, parent.st_dev)
        _write_all(fd, payload)
        os.fchmod(fd, EXPECTED_MODE)
        os.fsync(fd)
        size, verified_digest, opened = _verify_upload_fd(fd, parent.st_dev)
        return {
            "path": UPLOAD_TEMP_PATH,
            "realpath": os.path.realpath(UPLOAD_TEMP_PATH),
            "bytes": size,
            "sha256": verified_digest,
            "device": opened.st_dev,
            "inode": opened.st_ino,
            "owner": _owner_name(opened.st_uid),
            "group": _group_name(opened.st_gid),
            "mode": f"{stat.S_IMODE(opened.st_mode):04o}",
        }
    except BaseException as exc:
        if created:
            raise ContractError(
                f"{exc}; {UPLOAD_TEMP_PATH}=RETAINED_RECOVERY_REQUIRED"
            ) from exc
        raise
    finally:
        if fd is not None:
            os.close(fd)
        try:
            fcntl.flock(parent_fd, fcntl.LOCK_UN)
        finally:
            os.close(parent_fd)


def main() -> int:
    try:
        payload = sys.stdin.buffer.read()
        result = upload(payload)
    except (ContractError, OSError, ValueError) as exc:
        print(f"HOLD / {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps({"status": "PASS", "phase": "REMOTE_UPLOAD", **result}, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
