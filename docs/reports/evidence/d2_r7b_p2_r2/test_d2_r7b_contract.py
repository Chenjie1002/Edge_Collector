#!/usr/bin/env python3
"""T1-T37 synthetic matrix against the persisted exact artifacts."""

from __future__ import annotations

import errno
import fcntl
import hashlib
import importlib.util
import json
import os
import pwd
import grp
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ARTIFACT_DIR.parents[3]
P2_R3_DIR = REPO_ROOT / "docs/reports/evidence/d2_r7b_p2_r3"
LOCAL = ARTIFACT_DIR / "local_materialization.sh"
PREflight = ARTIFACT_DIR / "remote_preflight.py"
UPLOAD = ARTIFACT_DIR / "remote_upload_exclusive.py"
DEPLOY = ARTIFACT_DIR / "remote_deploy.py"
ROLLBACK = ARTIFACT_DIR / "remote_rollback.py"

NEW_BYTES = subprocess.check_output(
    ["git", "-C", str(REPO_ROOT), "cat-file", "-p", "HEAD:config/mapping.yaml"]
)
NEW_SHA256 = hashlib.sha256(NEW_BYTES).hexdigest()
OLD_BYTES = (b"synthetic-remote-old\n" * ((5935 // len(b"synthetic-remote-old\n")) + 1))[:5935]
OLD_SHA256 = hashlib.sha256(OLD_BYTES).hexdigest()

records: list[bool] = []
RETAINED_ROOTS: list[Path] = []
synthetic_root: Path
config_dir: Path
target_path: Path
owner_name = pwd.getpwuid(os.getuid()).pw_name
group_name = grp.getgrgid(os.getgid()).gr_name
filesystem_name = "ext4"


_MISSING_MODULE = object()


def load_artifact(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load persisted artifact: {path}")
    module = importlib.util.module_from_spec(spec)
    source_bytes = path.read_bytes()
    code = compile(source_bytes, str(path), "exec")
    previous = sys.modules.get(name, _MISSING_MODULE)
    sys.modules[name] = module
    try:
        exec(code, module.__dict__, module.__dict__)
    except BaseException:
        if previous is _MISSING_MODULE:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return module


def repository_cache_snapshot() -> dict[str, Any]:
    cache_dirs: list[str] = []
    cache_entries: dict[str, list[str]] = {}
    cache_files: dict[str, dict[str, Any]] = {}
    for evidence_root in (ARTIFACT_DIR, P2_R3_DIR):
        for candidate in evidence_root.rglob("__pycache__"):
            if not candidate.is_dir() or candidate.is_symlink():
                continue
            relative = str(candidate.relative_to(REPO_ROOT))
            cache_dirs.append(relative)
            cache_entries[relative] = sorted(entry.name for entry in candidate.iterdir())
            for entry in candidate.iterdir():
                if not entry.is_file() or entry.is_symlink():
                    continue
                data = entry.read_bytes()
                cache_files[str(entry.relative_to(REPO_ROOT))] = {
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "mtime_ns": entry.stat().st_mtime_ns,
                }
    return {
        "cache_dirs": sorted(set(cache_dirs)),
        "cache_entries": cache_entries,
        "cache_files": cache_files,
    }


def make_persisted_loader_fixture(prefix: str) -> tuple[Path, Path, Path]:
    root = Path(tempfile.mkdtemp(prefix=prefix)).resolve()
    RETAINED_ROOTS.append(root)
    success = root / "loader_success.py"
    success.write_text(
        """import sys
from dataclasses import dataclass

EXECUTION_SAW_SELF = sys.modules.get(__name__) is not None

@dataclass
class FixtureRecord:
    value: int

def add_one(value: int) -> int:
    return value + 1
""",
        encoding="utf-8",
    )
    failure = root / "loader_failure.py"
    failure.write_text(
        """import sys

EXECUTION_SAW_SELF = sys.modules.get(__name__) is not None
raise RuntimeError("synthetic persisted loader failure")
""",
        encoding="utf-8",
    )
    return root, success, failure


def assert_persisted_loader_semantics(load_fn, prefix: str) -> None:
    assert sys.dont_write_bytecode is False
    assert sys.pycache_prefix is None
    root, success, failure = make_persisted_loader_fixture(prefix)
    success_name = f"{prefix}_success"
    module = load_fn(success_name, success)
    assert module.__file__ == str(success)
    assert module.__name__ == success_name
    assert module.__package__ == ""
    assert module.__spec__ is not None and module.__spec__.name == success_name
    assert module.__loader__ is module.__spec__.loader
    assert module.__cached__ == importlib.util.cache_from_source(str(success))
    assert module.EXECUTION_SAW_SELF is True
    assert sys.modules[success_name] is module
    assert module.FixtureRecord(7).value == 7
    assert module.add_one(4) == 5
    assert not list(root.rglob("__pycache__")), "persisted loader created __pycache__"
    assert not list(root.rglob("*.pyc")), "persisted loader created .pyc"

    existing_name = f"{prefix}_existing"
    sentinel = object()
    sys.modules[existing_name] = sentinel
    try:
        try:
            load_fn(existing_name, failure)
        except RuntimeError as exc:
            assert str(exc) == "synthetic persisted loader failure"
        else:
            raise AssertionError("failing fixture unexpectedly succeeded")
        assert sys.modules[existing_name] is sentinel
    finally:
        sys.modules.pop(existing_name, None)

    absent_name = f"{prefix}_absent"
    try:
        try:
            load_fn(absent_name, failure)
        except RuntimeError as exc:
            assert str(exc) == "synthetic persisted loader failure"
        else:
            raise AssertionError("failing fixture unexpectedly succeeded")
        assert absent_name not in sys.modules
    finally:
        sys.modules.pop(absent_name, None)
    assert not list(root.rglob("__pycache__")), "failing loader created __pycache__"
    assert not list(root.rglob("*.pyc")), "failing loader created .pyc"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inode(path: Path) -> int | str:
    return path.stat().st_ino if path.exists() else "ABSENT"


def clear_artifacts() -> None:
    for path in (
        config_dir / ".mapping.yaml.d2-r7b-new.8de5edb",
        config_dir / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
        config_dir / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
    ):
        if path.exists() or path.is_symlink():
            path.unlink()


def set_target(payload: bytes) -> None:
    target_path.write_bytes(payload)
    os.chmod(target_path, 0o644)


def refresh_identities(modules: dict[str, ModuleType]) -> None:
    device = target_path.stat().st_dev
    target_inode = target_path.stat().st_ino
    for module in modules.values():
        if hasattr(module, "EXPECTED_OWNER"):
            module.EXPECTED_OWNER = owner_name
        if hasattr(module, "EXPECTED_GROUP"):
            module.EXPECTED_GROUP = group_name
        if hasattr(module, "EXPECTED_FILESYSTEM"):
            module.EXPECTED_FILESYSTEM = filesystem_name
        if hasattr(module, "EXPECTED_PARENT_DEVICE"):
            module.EXPECTED_PARENT_DEVICE = device
        if hasattr(module, "EXPECTED_TARGET_DEVICE"):
            module.EXPECTED_TARGET_DEVICE = device
        if hasattr(module, "EXPECTED_TARGET_INODE"):
            module.EXPECTED_TARGET_INODE = target_inode
        if hasattr(module, "EXPECTED_TARGET_BYTES"):
            module.EXPECTED_TARGET_BYTES = len(OLD_BYTES)
        if hasattr(module, "EXPECTED_TARGET_SHA256"):
            module.EXPECTED_TARGET_SHA256 = OLD_SHA256
        if hasattr(module, "EXPECTED_OLD_BYTES"):
            module.EXPECTED_OLD_BYTES = len(OLD_BYTES)
        if hasattr(module, "EXPECTED_OLD_SHA256"):
            module.EXPECTED_OLD_SHA256 = OLD_SHA256
        if hasattr(module, "_filesystem_type"):
            module._filesystem_type = lambda _path, *, pass_fds=(): filesystem_name
    preflight = modules["preflight"]
    preflight.EXPECTED_PRINCIPAL = owner_name
    preflight.EXPECTED_MOUNT_SOURCE = str(config_dir)


def state_hash(path: Path) -> str:
    return digest(path) if path.exists() else "ABSENT"


def emit(
    label: str,
    passed: bool,
    *,
    expected: str,
    observed: str,
    helper: Path,
    relation: str,
    helper_exit_status: str = "N/A",
) -> None:
    records.append(passed)
    target_sha = state_hash(target_path)
    backup = config_dir / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
    helper_sha = digest(helper)
    print(
        f"{label}|{'PASS' if passed else 'FAIL'}|expected={expected}|observed={observed}"
        f"|matrix_exit_status={0 if passed else 1}|helper_exit_status={helper_exit_status}|helper_sha256={helper_sha}"
        f"|target_sha256={target_sha}|backup_sha256={state_hash(backup)}"
        f"|target_inode={inode(target_path)}|backup_inode={inode(backup)}|inode_relation={relation}"
    )


def expect_hold(call: Callable[[], Any]) -> tuple[bool, str]:
    try:
        call()
    except Exception as exc:  # persisted helpers expose ContractError; OSError is also fail-closed.
        return True, f"HOLD:{exc.__class__.__name__}:{exc}"
    return False, "unexpected success"


def expect_contract_error(call: Callable[[], Any], error_type: type[BaseException]) -> tuple[bool, str]:
    try:
        call()
    except error_type as exc:
        return True, f"HOLD:{exc.__class__.__name__}"
    except Exception as exc:
        return False, f"unexpected:{exc.__class__.__name__}"
    return False, "unexpected success"


def retained_artifact_state(path: Path) -> dict[str, Any]:
    listed = os.lstat(path)
    return {
        "inode": listed.st_ino,
        "uid": listed.st_uid,
        "gid": listed.st_gid,
        "mode": stat.S_IMODE(listed.st_mode),
        "bytes": path.read_bytes(),
    }


def install_pathname_mutation_counter(module: ModuleType) -> tuple[dict[str, int], Callable[[], None]]:
    names = ("unlink", "rename", "replace", "rmdir")
    originals = {name: getattr(module.os, name) for name in names}
    counts = {name: 0 for name in names}

    for name in names:
        original = originals[name]

        def counted(*args, _name=name, _original=original, **kwargs):
            counts[_name] += 1
            return _original(*args, **kwargs)

        setattr(module.os, name, counted)

    def restore() -> None:
        for name, original in originals.items():
            setattr(module.os, name, original)

    return counts, restore


def load_contract_modules(prefix: str, *, preserve_filesystem_query: bool = False) -> dict[str, ModuleType]:
    modules = {
        "preflight": load_artifact(f"{prefix}_preflight", PREflight),
        "upload": load_artifact(f"{prefix}_upload", UPLOAD),
        "deploy": load_artifact(f"{prefix}_deploy", DEPLOY),
        "rollback": load_artifact(f"{prefix}_rollback", ROLLBACK),
    }
    preflight = modules["preflight"]
    upload = modules["upload"]
    deploy = modules["deploy"]
    rollback = modules["rollback"]
    preflight.PARENT_PATH = str(config_dir)
    preflight.TARGET_PATH = str(target_path)
    preflight.UPLOAD_TEMP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-new.8de5edb")
    preflight.BACKUP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    upload.PARENT_PATH = str(config_dir)
    upload.UPLOAD_TEMP_PATH = preflight.UPLOAD_TEMP_PATH
    deploy.PARENT_PATH = str(config_dir)
    deploy.TARGET_PATH = str(target_path)
    deploy.UPLOAD_TEMP_PATH = upload.UPLOAD_TEMP_PATH
    deploy.BACKUP_PATH = preflight.BACKUP_PATH
    rollback.PARENT_PATH = str(config_dir)
    rollback.TARGET_PATH = str(target_path)
    rollback.BACKUP_PATH = preflight.BACKUP_PATH
    rollback.ROLLBACK_TEMP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    if preserve_filesystem_query:
        filesystem_queries = {name: module._filesystem_type for name, module in modules.items()}
        refresh_identities(modules)
        for name, query in filesystem_queries.items():
            modules[name]._filesystem_type = query
    else:
        refresh_identities(modules)
    return modules


def filesystem_query_matrix(
    modules: dict[str, ModuleType],
    *,
    stdout: str = "ext4\n",
    returncode: int = 0,
    error: BaseException | None = None,
) -> tuple[dict[str, tuple[bool, str]], list[tuple[list[str], dict[str, Any]]]]:
    calls: list[tuple[list[str], dict[str, Any]]] = []
    original_run = subprocess.run

    def fake_run(command, **kwargs):
        calls.append((list(command), dict(kwargs)))
        if error is not None:
            raise error
        return SimpleNamespace(returncode=returncode, stdout=stdout)

    subprocess.run = fake_run
    results: dict[str, tuple[bool, str]] = {}
    try:
        for name, module in modules.items():
            results[name] = expect_contract_error(
                lambda module=module: module._filesystem_type(module.PARENT_PATH),
                module.ContractError,
            )
    finally:
        subprocess.run = original_run
    return results, calls


def assert_exact_findmnt_calls(calls: list[tuple[list[str], dict[str, Any]]], modules: dict[str, ModuleType]) -> None:
    assert len(calls) == len(modules), calls
    for (name, module), (command, kwargs) in zip(modules.items(), calls):
        assert command == ["findmnt", "-T", module.PARENT_PATH, "-n", "-o", "FSTYPE"], (name, command)
        assert kwargs.get("shell", False) is False, (name, kwargs)


def assert_filesystem_gate_blocks_mutation(modules: dict[str, ModuleType], *, error: BaseException | None = None) -> None:
    set_target(OLD_BYTES)
    clear_artifacts()
    fixture = container_fixture(modules["preflight"])
    original_run = subprocess.run

    def fake_run(command, **kwargs):
        assert command == ["findmnt", "-T", modules["preflight"].PARENT_PATH, "-n", "-o", "FSTYPE"] or command == ["findmnt", "-T", modules["upload"].PARENT_PATH, "-n", "-o", "FSTYPE"]
        if error is not None:
            raise error
        return SimpleNamespace(returncode=1, stdout="xfs\n")

    subprocess.run = fake_run
    try:
        calls: tuple[Callable[[], Any], ...] = (
            lambda: modules["preflight"].run_preflight(
                docker_payload=fixture,
                hostname="Pi-5b-Li",
                principal=owner_name,
            ),
            lambda: modules["upload"].upload(NEW_BYTES),
            modules["deploy"].deploy,
            modules["rollback"].rollback,
        )
        for call in calls:
            passed, observed = expect_hold(call)
            assert passed, observed
    finally:
        subprocess.run = original_run
    assert target_path.read_bytes() == OLD_BYTES
    assert not Path(modules["upload"].UPLOAD_TEMP_PATH).exists()
    assert not Path(modules["deploy"].BACKUP_PATH).exists()
    assert not Path(modules["rollback"].ROLLBACK_TEMP_PATH).exists()


def make_upload_only_fixture(prefix: str) -> tuple[Path, Path, ModuleType]:
    root = Path(tempfile.mkdtemp(prefix=prefix)).resolve()
    RETAINED_ROOTS.append(root)
    parent = root / "config"
    parent.mkdir()
    os.chmod(parent, 0o775)
    module = load_artifact(f"{prefix}_upload", UPLOAD)
    module.PARENT_PATH = str(parent)
    module.UPLOAD_TEMP_PATH = str(parent / ".mapping.yaml.d2-r7b-new.8de5edb")
    module.EXPECTED_OWNER = owner_name
    module.EXPECTED_GROUP = group_name
    module.EXPECTED_PARENT_DEVICE = parent.stat().st_dev
    module.EXPECTED_FILESYSTEM = filesystem_name
    module._filesystem_type = lambda _path, *, pass_fds=(): filesystem_name
    return root, parent, module


def fd_is_closed(fd: int) -> bool:
    try:
        os.fstat(fd)
    except OSError as exc:
        return exc.errno == errno.EBADF
    return False


class PayloadStdin:
    class Buffer:
        def __init__(self, payload: bytes) -> None:
            self.payload = payload

        def read(self) -> bytes:
            return self.payload

    def __init__(self, payload: bytes) -> None:
        self.buffer = self.Buffer(payload)


def invoke_persisted_main(module: ModuleType, *, payload: bytes | None = None) -> tuple[int, bytes, bytes]:
    original_stdin = sys.stdin
    stdout = StringIO()
    stderr = StringIO()
    if payload is not None:
        sys.stdin = PayloadStdin(payload)  # type: ignore[assignment]
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            returncode = module.main()
    finally:
        sys.stdin = original_stdin
    return returncode, stdout.getvalue().encode("utf-8"), stderr.getvalue().encode("utf-8")


def parse_compact_json_line(stdout: bytes) -> dict[str, Any]:
    assert stdout.endswith(b"\n")
    assert stdout.count(b"\n") == 1
    line = stdout[:-1].decode("utf-8")
    value = json.loads(line)
    assert isinstance(value, dict)
    assert line == json.dumps(value, sort_keys=True, separators=(",", ":"))
    return value


def container_fixture(preflight: ModuleType, *, rw: bool = False) -> list[dict[str, Any]]:
    return [
        {
            "Id": preflight.EXPECTED_CONTAINER_ID,
            "Name": "/edge-mes-collector",
            "Image": preflight.EXPECTED_IMAGE_ID,
            "Config": {"Image": preflight.EXPECTED_CONFIGURED_IMAGE},
            "State": {"Running": True, "StartedAt": preflight.EXPECTED_STARTED_AT},
            "RestartCount": 0,
            "Mounts": [
                {
                    "Source": str(config_dir),
                    "Destination": "/app/config",
                    "Type": "bind",
                    "RW": rw,
                }
            ],
        }
    ]


def main() -> int:
    global synthetic_root, config_dir, target_path
    repository_cache_before = repository_cache_snapshot()
    local_run = subprocess.run(
        [str(LOCAL)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
        check=False,
    )
    if local_run.returncode != 0:
        print(local_run.stdout, end="")
        print(local_run.stderr, end="", file=sys.stderr)
        raise SystemExit("T1 local materialization failed before matrix")
    local_fields = dict(line.split("=", 1) for line in local_run.stdout.splitlines() if "=" in line)
    synthetic_root = Path(local_fields["TEMP_ROOT"])
    RETAINED_ROOTS.append(synthetic_root.resolve())
    config_dir = synthetic_root / "config"
    target_path = config_dir / "mapping.yaml"
    os.chmod(config_dir, 0o775)
    if target_path.read_bytes() != NEW_BYTES:
        raise SystemExit("T1 materialized bytes differ from Git object")
    if local_fields.get("BLOB") != "b46a637f23c761d0a4c3fe048b3b7480a3dec2ce" or local_fields.get("BYTES") != "7112" or local_fields.get("SHA256") != NEW_SHA256:
        raise SystemExit("T1 materialization identity mismatch")
    preflight = load_artifact("d2_r7b_preflight", PREflight)
    upload = load_artifact("d2_r7b_upload", UPLOAD)
    deploy = load_artifact("d2_r7b_deploy", DEPLOY)
    rollback = load_artifact("d2_r7b_rollback", ROLLBACK)
    modules = {"preflight": preflight, "upload": upload, "deploy": deploy, "rollback": rollback}

    preflight.PARENT_PATH = str(config_dir)
    preflight.TARGET_PATH = str(target_path)
    preflight.UPLOAD_TEMP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-new.8de5edb")
    preflight.BACKUP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")
    upload.PARENT_PATH = str(config_dir)
    upload.UPLOAD_TEMP_PATH = preflight.UPLOAD_TEMP_PATH
    deploy.PARENT_PATH = str(config_dir)
    deploy.TARGET_PATH = str(target_path)
    deploy.UPLOAD_TEMP_PATH = upload.UPLOAD_TEMP_PATH
    deploy.BACKUP_PATH = preflight.BACKUP_PATH
    rollback.PARENT_PATH = str(config_dir)
    rollback.TARGET_PATH = str(target_path)
    rollback.BACKUP_PATH = preflight.BACKUP_PATH
    rollback.ROLLBACK_TEMP_PATH = str(config_dir / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml")

    refresh_identities(modules)
    emit("T1", True, expected="PASS", observed="Git object materialized", helper=LOCAL, relation="materialized exact source", helper_exit_status=str(local_run.returncode))
    shell_ok = subprocess.run(["sh", "-n", str(LOCAL)], check=False).returncode == 0
    ahead_value = local_fields.get("AHEAD_BEHIND", "")
    tab_ok = "\t" in ahead_value and ahead_value.split("\t") == ["0", "0"]
    t2_ok = shell_ok and tab_ok and local_fields.get("NO_AUTO_CLEANUP") == "1" and "glob cleanup" in local_fields.get("BOUNDED_CLEANUP_CONTRACT", "")
    emit("T2", t2_ok, expected="shell syntax PASS; tab 0<TAB>0; cached/clean gate PASS", observed=f"syntax={shell_ok};ahead={ahead_value!r};cleanup_contract={local_fields.get('NO_AUTO_CLEANUP')}", helper=LOCAL, relation="baseline unchanged", helper_exit_status=str(subprocess.run(["sh", "-n", str(LOCAL)], check=False).returncode))

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload_result = upload.upload(NEW_BYTES)
    t3_ok = upload_result["bytes"] == 7112 and upload_result["sha256"] == NEW_SHA256 and target_path.read_bytes() == OLD_BYTES
    emit("T3", t3_ok, expected="PASS exclusive create exact new identity", observed=json.dumps(upload_result, sort_keys=True), helper=UPLOAD, relation=f"upload_inode={upload_result['inode']} target_inode={target_path.stat().st_ino}")

    clear_artifacts()
    refresh_identities(modules)
    original_read = upload._read_all_fd
    mutation_evidence = {"performed": False, "stat_changed": False}

    def mutate_during_read(fd: int) -> tuple[int, str, bytes]:
        result = original_read(fd)
        before = os.stat(upload.UPLOAD_TEMP_PATH, follow_symlinks=False)
        mutation_fd = os.open(upload.UPLOAD_TEMP_PATH, os.O_WRONLY | os.O_NOFOLLOW)
        try:
            os.ftruncate(mutation_fd, max(0, result[0] - 1))
            os.fsync(mutation_fd)
        finally:
            os.close(mutation_fd)
        after = os.stat(upload.UPLOAD_TEMP_PATH, follow_symlinks=False)
        mutation_evidence["performed"] = True
        mutation_evidence["stat_changed"] = before != after
        return result

    upload._read_all_fd = mutate_during_read
    target_before_t4 = target_path.read_bytes()
    t4_contract_error, t4_observed = expect_contract_error(lambda: upload.upload(NEW_BYTES), upload.ContractError)
    t4_ok = (
        t4_contract_error
        and mutation_evidence["performed"]
        and mutation_evidence["stat_changed"]
        and target_path.read_bytes() == target_before_t4
    )
    upload._read_all_fd = original_read
    clear_artifacts()
    emit(
        "T4",
        t4_ok,
        expected="HOLD:ContractError after independent-FD mutation; target unchanged",
        observed=f"{t4_observed};mutation_performed={mutation_evidence['performed']};stat_changed={mutation_evidence['stat_changed']};target_unchanged={target_path.read_bytes() == target_before_t4}",
        helper=UPLOAD,
        relation="target unchanged",
    )

    stale = Path(upload.UPLOAD_TEMP_PATH)
    stale.write_bytes(b"stale-upload")
    os.chmod(stale, 0o644)
    stale_before = stale.read_bytes()
    t5_ok, t5_observed = expect_hold(lambda: upload.upload(NEW_BYTES))
    t5_ok = t5_ok and stale.read_bytes() == stale_before
    clear_artifacts()
    emit("T5", t5_ok, expected="FAIL/HOLD before touching unchanged stale temp", observed=t5_observed, helper=UPLOAD, relation="stale artifact unchanged")

    original_write = upload._write_all
    def corrupt_after_write(fd: int, payload: bytes) -> None:
        original_write(fd, payload)
        os.ftruncate(fd, len(payload) - 1)
    upload._write_all = corrupt_after_write
    t6_ok, t6_observed = expect_hold(lambda: upload.upload(NEW_BYTES))
    upload._write_all = original_write
    clear_artifacts()
    emit("T6", t6_ok, expected="HOLD on upload identity/content mismatch", observed=t6_observed, helper=UPLOAD, relation="target unchanged")

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload.upload(NEW_BYTES)
    deploy.before_rename_recheck_hook = lambda: None
    deploy_result = deploy.deploy()
    if "target" in deploy_result:
        target_inode_before = deploy_result["target"]["inode_before"]
        target_inode_after = deploy_result["target"]["inode_after"]
    else:
        target_inode_before = deploy_result["target_inode_before"]
        target_inode_after = deploy_result["target_inode_after"]
    t7_ok = target_path.read_bytes() == NEW_BYTES and Path(deploy.BACKUP_PATH).read_bytes() == OLD_BYTES and target_inode_before != target_inode_after
    emit("T7", t7_ok, expected="PASS atomic replacement with old backup and changed target inode", observed=json.dumps(deploy_result, sort_keys=True), helper=DEPLOY, relation=f"{target_inode_before}->{target_inode_after}")

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload.upload(NEW_BYTES)
    def drift_target_before_recheck() -> None:
        target_path.write_bytes(b"target-drift")
        os.chmod(target_path, 0o644)
    deploy.before_rename_recheck_hook = drift_target_before_recheck
    t8_ok, t8_observed = expect_hold(deploy.deploy)
    deploy.before_rename_recheck_hook = lambda: None
    emit("T8", t8_ok, expected="HOLD before replace on target drift", observed=t8_observed, helper=DEPLOY, relation="replace not reached")
    clear_artifacts()

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload.upload(NEW_BYTES)
    original_replace = deploy.os.replace
    deploy.os.replace = lambda _source, _target: (_ for _ in ()).throw(OSError(errno.EXDEV, "synthetic EXDEV"))
    t9_ok, t9_observed = expect_hold(deploy.deploy)
    deploy.os.replace = original_replace
    t9_ok = t9_ok and target_path.read_bytes() == OLD_BYTES and Path(deploy.BACKUP_PATH).read_bytes() == OLD_BYTES and Path(deploy.UPLOAD_TEMP_PATH).read_bytes() == NEW_BYTES
    emit("T9", t9_ok, expected="HOLD EXDEV with no fallback", observed=t9_observed, helper=DEPLOY, relation="target inode/content unchanged")
    clear_artifacts()

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload.upload(NEW_BYTES)
    deploy_result = deploy.deploy()
    rollback_result = rollback.rollback()
    t10_ok = target_path.read_bytes() == OLD_BYTES and Path(rollback.BACKUP_PATH).read_bytes() == OLD_BYTES and rollback_result["target_inode_before"] != rollback_result["target_inode_after"]
    emit("T10", t10_ok, expected="PASS independent rollback; backup unchanged; target inode changed", observed=json.dumps(rollback_result, sort_keys=True), helper=ROLLBACK, relation=f"{rollback_result['target_inode_before']}->{rollback_result['target_inode_after']}")

    clear_artifacts()
    set_target(OLD_BYTES)
    refresh_identities(modules)
    t11_ok, t11_observed = expect_hold(lambda: upload.upload(b"wrong-payload"))
    t11_ok = t11_ok and not Path(upload.UPLOAD_TEMP_PATH).exists()
    emit("T11", t11_ok, expected="FAIL before upload-temp creation on wrong stdin payload", observed=t11_observed, helper=UPLOAD, relation="upload temp ABSENT")

    clear_artifacts()
    refresh_identities(modules)
    env = {
        **os.environ,
        "D2_R7B_SYNTHETIC_ROOT": str(synthetic_root),
        "D2_R7B_SYNTHETIC_OWNER": owner_name,
        "D2_R7B_SYNTHETIC_GROUP": group_name,
        "D2_R7B_SYNTHETIC_DEVICE": str(target_path.stat().st_dev),
        "D2_R7B_SYNTHETIC_FILESYSTEM": filesystem_name,
    }
    fake_findmnt_root = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r2-t12-findmnt-"))
    RETAINED_ROOTS.append(fake_findmnt_root)
    fake_findmnt = fake_findmnt_root / "findmnt"
    fake_findmnt.write_text(
        "#!/bin/sh\nprintf '%s\\n' ext4\n",
        encoding="utf-8",
    )
    fake_findmnt.chmod(0o755)
    env["PATH"] = f"{fake_findmnt_root}{os.pathsep}{env['PATH']}"
    t12_run = subprocess.run([sys.executable, str(UPLOAD)], input=NEW_BYTES, capture_output=True, env=env, check=False)
    t12_ok = t12_run.returncode == 0 and Path(upload.UPLOAD_TEMP_PATH).read_bytes() == NEW_BYTES
    emit("T12", t12_ok, expected="exit 0 from final persisted remote_upload_exclusive.py", observed=f"returncode={t12_run.returncode};stdout={t12_run.stdout.decode().strip()!r}", helper=UPLOAD, relation="target unchanged", helper_exit_status=str(t12_run.returncode))

    ahead_value = local_fields.get("AHEAD_BEHIND", "")
    t13_ok = ahead_value == "0\t0" and ahead_value.split("\t") == ["0", "0"]
    emit("T13", t13_ok, expected="Git output parsed as 0<TAB>0", observed=repr(ahead_value), helper=LOCAL, relation="not ordinary-string comparison", helper_exit_status=str(local_run.returncode))

    clear_artifacts()
    set_target(OLD_BYTES)
    refresh_identities(modules)
    fixture = container_fixture(preflight)
    t14_result = preflight.run_preflight(docker_payload=fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name)
    t14_ok = t14_result["transport_endpoint"] == "mari@10.0.0.217" and t14_result["target_inode"] == target_path.stat().st_ino
    emit("T14", t14_ok, expected="PASS exact preflight fixture", observed=json.dumps(t14_result, sort_keys=True), helper=PREflight, relation="read-only fixture")

    image_drift_fixture = container_fixture(preflight)
    image_drift_fixture[0]["Image"] = "sha256:top-level-image-drift"
    t15_image_ok, t15_image_observed = expect_contract_error(
        lambda: preflight.run_preflight(docker_payload=image_drift_fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name),
        preflight.ContractError,
    )
    rw_drift_fixture = container_fixture(preflight, rw=True)
    t15_rw_ok, t15_rw_observed = expect_contract_error(
        lambda: preflight.run_preflight(docker_payload=rw_drift_fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name),
        preflight.ContractError,
    )
    t15_ok = t15_image_ok and t15_rw_ok
    emit(
        "T15",
        t15_ok,
        expected="HOLD on top-level Image ID drift and mount RW=true",
        observed=f"top_level_image={t15_image_observed};mount_rw={t15_rw_observed}",
        helper=PREflight,
        relation="no write",
    )

    set_target(OLD_BYTES)
    clear_artifacts()
    refresh_identities(modules)
    upload.upload(NEW_BYTES)
    deploy.before_rename_recheck_hook = lambda: None
    deploy.deploy()
    rollback_before_inode = target_path.stat().st_ino
    def same_content_new_inode() -> None:
        race_path = config_dir / ".race-target"
        race_path.write_bytes(NEW_BYTES)
        os.chmod(race_path, 0o644)
        os.replace(race_path, target_path)
    rollback.before_rollback_rename_hook = same_content_new_inode
    t16_ok, t16_observed = expect_hold(rollback.rollback)
    rollback.before_rollback_rename_hook = lambda: None
    t16_ok = t16_ok and target_path.read_bytes() == NEW_BYTES and target_path.stat().st_ino != rollback_before_inode and Path(rollback.BACKUP_PATH).read_bytes() == OLD_BYTES and Path(rollback.ROLLBACK_TEMP_PATH).exists()
    emit("T16", t16_ok, expected="HOLD before rollback rename on same-hash target inode drift", observed=t16_observed, helper=ROLLBACK, relation=f"initial={rollback_before_inode};drifted={target_path.stat().st_ino};no replace")

    clear_artifacts()
    set_target(OLD_BYTES)
    refresh_identities(modules)
    correct_image_fixture = container_fixture(preflight)
    t17_pass_result = preflight.run_preflight(docker_payload=correct_image_fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name)
    top_level_image_fixture = container_fixture(preflight)
    top_level_image_fixture[0]["Image"] = "sha256:top-level-image-drift"
    t17_top_ok, t17_top_observed = expect_contract_error(
        lambda: preflight.run_preflight(docker_payload=top_level_image_fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name),
        preflight.ContractError,
    )
    configured_image_fixture = container_fixture(preflight)
    configured_image_fixture[0]["Config"]["Image"] = "edge-mes-demo-collector-drift"
    t17_config_ok, t17_config_observed = expect_contract_error(
        lambda: preflight.run_preflight(docker_payload=configured_image_fixture, hostname="Pi-5b-Li", principal=owner_name, filesystem=filesystem_name),
        preflight.ContractError,
    )
    t17_ok = (
        t17_pass_result["transport_endpoint"] == "mari@10.0.0.217"
        and t17_top_ok
        and t17_config_ok
    )
    emit(
        "T17",
        t17_ok,
        expected="PASS correct Image/Config.Image; HOLD each identity drift",
        observed=f"correct=PASS;top_level={t17_top_observed};configured={t17_config_observed}",
        helper=PREflight,
        relation="image identity fields independently enforced",
    )

    def t20() -> tuple[bool, str]:
        modules = load_contract_modules("d2_r7b_p2_r2_t20", preserve_filesystem_query=True)
        results, calls = filesystem_query_matrix(modules)
        assert all(result == (False, "unexpected success") for result in results.values()), results
        assert_exact_findmnt_calls(calls, modules)
        return True, "all four helpers returned ext4 from exact findmnt argv; stat not called"

    t20_ok, t20_observed = t20()
    emit("T20", t20_ok, expected="exact findmnt primitive; ext4\\n normalized; no stat/shell", observed=t20_observed, helper=PREflight, relation="four-helper read-only filesystem gate")

    def t21() -> tuple[bool, str]:
        modules = load_contract_modules("d2_r7b_p2_r2_t21", preserve_filesystem_query=True)
        good_results, good_calls = filesystem_query_matrix(modules, stdout="ext4\n")
        assert all(result == (False, "unexpected success") for result in good_results.values()), good_results
        assert_exact_findmnt_calls(good_calls, modules)
        for output in ("ext2\n", "ext3\n", "xfs\n", "", " \n", "ext4\nxfs\n", "ext4 ext4\n"):
            bad_results, bad_calls = filesystem_query_matrix(modules, stdout=output)
            assert all(result[0] and result[1].startswith("HOLD:ContractError") for result in bad_results.values()), (output, bad_results)
            assert_exact_findmnt_calls(bad_calls, modules)
        assert_filesystem_gate_blocks_mutation(modules)
        return True, "ext4 PASS; ext2/ext3/xfs/empty/whitespace/multiline/multiple-type HOLD; mutation paths unchanged"

    t21_ok, t21_observed = t21()
    emit("T21", t21_ok, expected="exact ext4 only; all malformed/non-ext4 output fail closed", observed=t21_observed, helper=DEPLOY, relation="filesystem gate precedes upload/backup/replace/rollback-temp")

    def t22() -> tuple[bool, str]:
        modules = load_contract_modules("d2_r7b_p2_r2_t22", preserve_filesystem_query=True)
        for returncode, error in (
            (0, FileNotFoundError("findmnt unavailable")),
            (1, None),
            (0, subprocess.SubprocessError("findmnt failed")),
            (0, UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")),
        ):
            results, calls = filesystem_query_matrix(modules, stdout="ext4\n", returncode=returncode, error=error)
            assert all(result[0] and result[1].startswith("HOLD:ContractError") for result in results.values()), (returncode, error, results)
            assert_exact_findmnt_calls(calls, modules)
        assert_filesystem_gate_blocks_mutation(modules, error=FileNotFoundError("findmnt unavailable"))
        return True, "command unavailable/nonzero/subprocess failure became ContractError; no mutation or traceback path"

    t22_ok, t22_observed = t22()
    emit("T22", t22_ok, expected="findmnt failures clean HOLD in all four helpers", observed=t22_observed, helper=PREflight, relation="no mutation before filesystem PASS")

    def t23() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t23-")
        upload_module._parent_stat = lambda: (_ for _ in ()).throw(upload_module.ContractError("parent identity drift"))
        passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        return passed and not (parent / ".mapping.yaml.d2-r7b-new.8de5edb").exists(), observed

    t23_ok, t23_observed = t23()
    emit("T23", t23_ok, expected="HOLD before upload temp mutation on parent identity drift", observed=t23_observed, helper=UPLOAD, relation="upload temp absent")

    def t24() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t24-")
        original = upload_module._parent_stat
        upload_module._parent_stat = lambda: original()
        os.rename(parent, parent.with_name("config-drift"))
        passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        return passed, observed

    t24_ok, t24_observed = t24()
    emit("T24", t24_ok, expected="HOLD on parent path drift", observed=t24_observed, helper=UPLOAD, relation="no create")

    def t25() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t25-")
        result = upload_module.upload(NEW_BYTES)
        return result["bytes"] == len(NEW_BYTES) and (parent / ".mapping.yaml.d2-r7b-new.8de5edb").exists(), "exclusive create completed"

    t25_ok, t25_observed = t25()
    emit("T25", t25_ok, expected="PASS fd-bound upload contract", observed=t25_observed, helper=UPLOAD, relation="created fd verified")

    def t26() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t26-")
        original = upload_module._write_all
        upload_module._write_all = lambda fd, payload: (_ for _ in ()).throw(upload_module.ContractError("injected write failure"))
        try:
            passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._write_all = original
        named = parent / upload_module.UPLOAD_BASENAME
        state = retained_artifact_state(named) if named.exists() else None
        return (
            passed
            and state is not None
            and state["bytes"] == b""
            and state["uid"] == os.getuid()
            and state["gid"] == os.getgid()
            and "RETAINED_RECOVERY_REQUIRED" in observed
        ), f"{observed};retained_state={state!r}"

    t26_ok, t26_observed = t26()
    emit("T26", t26_ok, expected="write failure -> HOLD; named helper-owned artifact retained; RETAINED_RECOVERY_REQUIRED", observed=t26_observed, helper=UPLOAD, relation="retained exact upload basename")

    def t27() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t27-")
        original = upload_module._verify_upload_fd
        def fail_after_write(fd: int, parent_device: int):
            verified = original(fd, parent_device)
            raise upload_module.ContractError(f"injected verification failure after write; verified={verified[2].st_ino}")

        upload_module._verify_upload_fd = fail_after_write
        try:
            passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original
        named = parent / upload_module.UPLOAD_BASENAME
        state = retained_artifact_state(named) if named.exists() else None
        return (
            passed
            and state is not None
            and state["bytes"] == NEW_BYTES
            and state["uid"] == os.getuid()
            and state["gid"] == os.getgid()
            and "RETAINED_RECOVERY_REQUIRED" in observed
        ), f"{observed};retained_state={state!r}"

    t27_ok, t27_observed = t27()
    emit("T27", t27_ok, expected="verification failure after write -> HOLD; written payload retained; RETAINED_RECOVERY_REQUIRED", observed=t27_observed, helper=UPLOAD, relation="written payload remains observable")

    def t28() -> tuple[bool, str]:
        root = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r2-t28-")).resolve()
        RETAINED_ROOTS.append(root)
        parent = root / "config"
        parent.mkdir()
        os.chmod(parent, 0o775)
        keys = (
            "D2_R7B_SYNTHETIC_ROOT",
            "D2_R7B_SYNTHETIC_OWNER",
            "D2_R7B_SYNTHETIC_GROUP",
            "D2_R7B_SYNTHETIC_DEVICE",
            "D2_R7B_SYNTHETIC_FILESYSTEM",
        )
        previous = {key: os.environ.get(key) for key in keys}
        os.environ.update({
            "D2_R7B_SYNTHETIC_ROOT": str(root),
            "D2_R7B_SYNTHETIC_OWNER": owner_name,
            "D2_R7B_SYNTHETIC_GROUP": group_name,
            "D2_R7B_SYNTHETIC_DEVICE": str(parent.stat().st_dev),
            "D2_R7B_SYNTHETIC_FILESYSTEM": "xfs",
        })
        original_run = subprocess.run
        calls: list[tuple[list[str], dict[str, Any]]] = []

        def fake_run(command, **kwargs):
            calls.append((list(command), dict(kwargs)))
            return SimpleNamespace(returncode=0, stdout="ext4\n")

        try:
            subprocess.run = fake_run
            upload_module = load_artifact("d2_r7b_p2_r2_t28_upload", UPLOAD)
            observed = upload_module._filesystem_type(upload_module.PARENT_PATH)
            expected_call = ["findmnt", "-T", upload_module.PARENT_PATH, "-n", "-o", "FSTYPE"]
            return (
                observed == "ext4"
                and upload_module.EXPECTED_FILESYSTEM == "ext4"
                and calls == [(expected_call, {"check": False, "capture_output": True, "text": True, "shell": False, "pass_fds": ()})],
                f"observed={observed!r};expected_filesystem={upload_module.EXPECTED_FILESYSTEM!r};calls={calls!r}",
            )
        except Exception as exc:
            return False, f"unexpected:{exc.__class__.__name__}:{exc}"
        finally:
            subprocess.run = original_run
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    t28_ok, t28_observed = t28()
    emit("T28", t28_ok, expected="synthetic filesystem bypass rejected", observed=t28_observed, helper=UPLOAD, relation="real filesystem authority")

    def t29() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t29-")
        original_verify = upload_module._verify_upload_fd
        original_replace = os.replace
        foreign_payload = b"foreign-before-cleanup"
        foreign_inode = {"value": None}
        counters, restore_counters = install_pathname_mutation_counter(upload_module)

        def verify_then_replace(fd: int, parent_device: int):
            result = original_verify(fd, parent_device)
            foreign = parent / ".foreign-before-cleanup"
            foreign.write_bytes(foreign_payload)
            os.chmod(foreign, 0o644)
            foreign_inode["value"] = foreign.stat().st_ino
            original_replace(foreign, parent / upload_module.UPLOAD_BASENAME)
            raise upload_module.ContractError("injected failure after foreign replacement")

        upload_module._verify_upload_fd = verify_then_replace
        try:
            passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original_verify
            restore_counters()
        named = parent / upload_module.UPLOAD_BASENAME
        state = retained_artifact_state(named) if named.exists() else None
        return (
            passed
            and state is not None
            and state["bytes"] == foreign_payload
            and state["inode"] == foreign_inode["value"]
            and counters == {"unlink": 0, "rename": 0, "replace": 0, "rmdir": 0}
        ), f"{observed};foreign_state={state!r};pathname_mutations={counters!r}"

    t29_ok, t29_observed = t29()
    emit(
        "T29",
        t29_ok,
        expected="foreign inode replaces named basename -> HOLD; foreign inode/bytes preserved; zero helper pathname cleanup mutation",
        observed=t29_observed,
        helper=UPLOAD,
        relation="foreign inode preserved",
    )

    def t30() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t30-")
        original_verify = upload_module._verify_upload_fd
        original_replace = os.replace
        foreign_payload = b"foreign-after-helper-verification"
        foreign_inode = {"value": None}

        counters, restore_counters = install_pathname_mutation_counter(upload_module)

        def verify_then_foreign_replace(fd: int, parent_device: int):
            verified = original_verify(fd, parent_device)
            foreign = parent / ".foreign-during-cleanup-race"
            foreign.write_bytes(foreign_payload)
            os.chmod(foreign, 0o644)
            foreign_inode["value"] = foreign.stat().st_ino
            original_replace(foreign, parent / upload_module.UPLOAD_BASENAME)
            raise upload_module.ContractError(f"injected failure after helper verification; verified={verified[2].st_ino}")

        upload_module._verify_upload_fd = verify_then_foreign_replace
        try:
            passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original_verify
            restore_counters()
        foreign_target = parent / upload_module.UPLOAD_BASENAME
        foreign_state = retained_artifact_state(foreign_target) if foreign_target.exists() else None
        return (
            passed
            and foreign_state is not None
            and foreign_state["bytes"] == foreign_payload
            and foreign_state["inode"] == foreign_inode["value"]
            and counters == {"unlink": 0, "rename": 0, "replace": 0, "rmdir": 0}
        ), f"{observed};foreign_state={foreign_state!r};pathname_mutations={counters!r}"

    t30_ok, t30_observed = t30()
    emit(
        "T30",
        t30_ok,
        expected="helper verifies own FD -> foreign inode replaces exact basename -> HOLD; zero cleanup mutation; foreign inode/bytes remain",
        observed=t30_observed,
        helper=UPLOAD,
        relation="R7-A foreign inode preserved after final verification boundary",
    )

    def t34() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t34-")
        original_verify = upload_module._verify_upload_fd

        def fail_after_named_create(fd: int, parent_device: int):
            raise upload_module.ContractError("injected post-write failure")

        upload_module._verify_upload_fd = fail_after_named_create
        counters, restore_counters = install_pathname_mutation_counter(upload_module)
        try:
            held, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original_verify
            restore_counters()
        named = parent / upload_module.UPLOAD_BASENAME
        state = retained_artifact_state(named) if named.exists() else None
        return (
            held
            and state is not None
            and state["bytes"] == NEW_BYTES
            and counters == {"unlink": 0, "rename": 0, "replace": 0, "rmdir": 0}
            and "RETAINED_RECOVERY_REQUIRED" in observed
        ), f"{observed};retained_state={state!r};pathname_mutations={counters!r}"

    t34_ok, t34_observed = t34()
    emit(
        "T34",
        t34_ok,
        expected="failure-path unlink=0 rename=0 replace=0 rmdir=0; HOLD; owned artifact RETAINED_RECOVERY_REQUIRED",
        observed=t34_observed,
        helper=UPLOAD,
        relation="zero failure-path pathname mutation plus retained final state",
    )

    def t35() -> tuple[bool, str]:
        """A retained upload basename is a fail-closed terminal disposition."""
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t35-")
        original_verify = upload_module._verify_upload_fd

        def fail_after_named_create(fd: int, parent_device: int):
            raise upload_module.ContractError("injected terminal failure")

        upload_module._verify_upload_fd = fail_after_named_create
        counters, restore_counters = install_pathname_mutation_counter(upload_module)
        try:
            first_held, first_observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
            named = parent / upload_module.UPLOAD_BASENAME
            first_state = retained_artifact_state(named) if named.exists() else None
            second_held, second_observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original_verify
            restore_counters()
        second_state = retained_artifact_state(named) if named.exists() else None
        return (
            first_held
            and second_held
            and "RETAINED_RECOVERY_REQUIRED" in first_observed
            and "RETAINED_RECOVERY_REQUIRED" not in second_observed
            and first_state == second_state
            and counters == {"unlink": 0, "rename": 0, "replace": 0, "rmdir": 0}
        ), f"first={first_observed};second={second_observed};first_state={first_state!r};second_state={second_state!r};pathname_mutations={counters!r}"

    t35_ok, t35_observed = t35()
    emit(
        "T35",
        t35_ok,
        expected="failure after named create -> HOLD; no cleanup retry; exact retained basename blocks second upload; RETAINED_RECOVERY_REQUIRED",
        observed=t35_observed,
        helper=UPLOAD,
        relation="retained inode/bytes unchanged and stale basename remains fail closed",
    )

    def t31() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t31-")
        original_verify = upload_module._verify_upload_fd

        def fail_after_verified_write(fd: int, parent_device: int):
            result = original_verify(fd, parent_device)
            raise upload_module.ContractError("injected owned-temp failure")

        upload_module._verify_upload_fd = fail_after_verified_write
        try:
            passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        finally:
            upload_module._verify_upload_fd = original_verify
        named = parent / upload_module.UPLOAD_BASENAME
        state = retained_artifact_state(named) if named.exists() else None
        return passed and state is not None and state["bytes"] == NEW_BYTES and "RETAINED_RECOVERY_REQUIRED" in observed, f"{observed};retained_state={state!r}"

    t31_ok, t31_observed = t31()
    emit(
        "T31",
        t31_ok,
        expected="post-verification failure -> HOLD; expected payload retained; no automatic cleanup; RETAINED_RECOVERY_REQUIRED",
        observed=t31_observed,
        helper=UPLOAD,
        relation="verified payload retained at exact upload basename",
    )

    def t32() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t32-")
        stale = parent / upload_module.UPLOAD_BASENAME
        stale_payload = b"stale-upload-object"
        stale.write_bytes(stale_payload)
        os.chmod(stale, 0o644)
        passed, observed = expect_hold(lambda: upload_module.upload(NEW_BYTES))
        return passed and stale.exists() and stale.read_bytes() == stale_payload, observed

    t32_ok, t32_observed = t32()
    emit(
        "T32",
        t32_ok,
        expected="HOLD on stale temp and preserve stale object unchanged",
        observed=t32_observed,
        helper=UPLOAD,
        relation="stale object preserved",
    )

    def t33() -> tuple[bool, str]:
        keys = (
            "D2_R7B_SYNTHETIC_ROOT",
            "D2_R7B_SYNTHETIC_OWNER",
            "D2_R7B_SYNTHETIC_GROUP",
            "D2_R7B_SYNTHETIC_DEVICE",
            "D2_R7B_SYNTHETIC_FILESYSTEM",
        )
        previous = {key: os.environ.get(key) for key in keys}
        root = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r2-t33-")).resolve()
        RETAINED_ROOTS.append(root)
        parent = root / "config"
        parent.mkdir()
        os.chmod(parent, 0o775)
        unrelated_fd = os.open(str(parent), os.O_RDONLY | os.O_DIRECTORY)
        failure_root = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r2-t33-failure-")).resolve()
        RETAINED_ROOTS.append(failure_root)
        failure_parent = failure_root / "config"
        failure_parent.mkdir()
        os.chmod(failure_parent, 0o775)
        calls: list[tuple[list[str], dict[str, Any]]] = []
        upload_parent_fd: int | None = None
        original_run = subprocess.run
        failure_phase = False

        def configure_upload(module: ModuleType, configured_parent: Path) -> None:
            module.PARENT_PATH = str(configured_parent)
            module.UPLOAD_TEMP_PATH = str(configured_parent / module.UPLOAD_BASENAME)
            module.EXPECTED_OWNER = owner_name
            module.EXPECTED_GROUP = group_name
            module.EXPECTED_PARENT_DEVICE = configured_parent.stat().st_dev
            module.EXPECTED_FILESYSTEM = "ext4"

        def fake_run(command: list[str], **kwargs: Any) -> SimpleNamespace:
            nonlocal failure_phase, upload_parent_fd
            command = list(command)
            kwargs = dict(kwargs)
            calls.append((command, kwargs))
            assert command[:2] == ["findmnt", "-T"]
            assert command[3:] == ["-n", "-o", "FSTYPE"]
            assert kwargs.get("shell") is False
            pass_fds = tuple(kwargs.get("pass_fds", ()))
            query_path = command[2]
            if query_path.startswith("/proc/self/fd/"):
                queried_fd = int(query_path.rsplit("/", 1)[1])
                assert pass_fds == (queried_fd,)
                os.fstat(queried_fd)
                assert unrelated_fd not in pass_fds
                upload_parent_fd = queried_fd
                return SimpleNamespace(returncode=0, stdout="xfs\n" if failure_phase else "ext4\n")
            assert pass_fds == ()
            if query_path == str(failure_parent):
                return SimpleNamespace(returncode=0, stdout="xfs\n")
            return SimpleNamespace(returncode=0, stdout="ext4\n")

        try:
            for key in keys:
                os.environ.pop(key, None)
            upload_module = load_artifact("d2_r7b_p2_r2_t33_upload", UPLOAD)
            configure_upload(upload_module, parent)
            subprocess.run = fake_run
            result = upload_module.upload(NEW_BYTES)
            named = parent / upload_module.UPLOAD_BASENAME
            success_ok = (
                result["bytes"] == len(NEW_BYTES)
                and named.exists()
                and named.read_bytes() == NEW_BYTES
                and stat.S_IMODE(named.stat().st_mode) == upload_module.EXPECTED_MODE
                and named.stat().st_uid == os.getuid()
                and named.stat().st_gid == os.getgid()
                and named.stat().st_dev == parent.stat().st_dev
                and result["sha256"] == NEW_SHA256
                and result["inode"] == named.stat().st_ino
                and upload_parent_fd is not None
                and fd_is_closed(upload_parent_fd)
                and all(key not in os.environ for key in keys)
            )

            failure_module = load_artifact("d2_r7b_p2_r2_t33_failure_upload", UPLOAD)
            configure_upload(failure_module, failure_parent)
            failure_phase = True
            try:
                failed, failure_observed = expect_hold(lambda: failure_module.upload(NEW_BYTES))
            finally:
                failure_phase = False
            failure_named = failure_parent / failure_module.UPLOAD_BASENAME
            failure_ok = failed and not failure_named.exists()

            path_modules = load_contract_modules("d2_r7b_p2_r2_t33_path", preserve_filesystem_query=True)
            path_results = {
                name: module._filesystem_type(module.PARENT_PATH)
                for name, module in path_modules.items()
                if name in ("preflight", "deploy", "rollback")
            }
            path_calls = calls[-3:]
            path_ok = (
                path_results == {"preflight": "ext4", "deploy": "ext4", "rollback": "ext4"}
                and len(path_calls) == 3
                and all(tuple(kwargs.get("pass_fds", ())) == () for _, kwargs in path_calls)
                and all(command[2] == str(config_dir) for command, _ in path_calls)
            )
            return (
                success_ok and failure_ok and path_ok,
                f"success={success_ok};failure={failure_ok};path_based_no_fd={path_ok};"
                f"upload_parent_fd={upload_parent_fd};calls={calls!r};failure={failure_observed}",
            )
        finally:
            subprocess.run = original_run
            os.close(unrelated_fd)
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    t33_ok, t33_observed = t33()
    emit(
        "T33",
        t33_ok,
        expected="upload parent FD is live in findmnt pass_fds; path callers inherit no upload FD; failure precedes create",
        observed=t33_observed,
        helper=UPLOAD,
        relation="exact parent-FD subprocess boundary and path-based FD isolation",
    )

    def t36() -> tuple[bool, str]:
        _, parent, upload_module = make_upload_only_fixture("d2-r7b-p2-r2-t36-")
        orchestrator = load_artifact("d2_r7b_p2_r2_t36_orchestrator", P2_R3_DIR / "remote_i1_orchestrator.py")
        returncode, stdout, stderr = invoke_persisted_main(upload_module, payload=NEW_BYTES)
        try:
            value = parse_compact_json_line(stdout)
        except Exception as exc:
            return False, f"returncode={returncode};stderr={stderr!r};legacy_stdout={stdout!r};parse_error={exc!r}"
        upload_path = Path(upload_module.UPLOAD_TEMP_PATH)
        listed = os.lstat(upload_path)
        expected_keys = {
            "bytes", "device", "group", "inode", "mode", "owner", "path",
            "phase", "realpath", "sha256", "status",
        }
        outcome = {"child_returncode": returncode, "stdout": stdout}
        normalized = orchestrator._normalize_invalid_child_json(outcome)
        ok = (
            returncode == 0
            and stderr == b""
            and set(value) == expected_keys
            and value["status"] == "PASS"
            and value["phase"] == "REMOTE_UPLOAD"
            and value["path"] == str(upload_path)
            and value["realpath"] == os.path.realpath(upload_path)
            and value["bytes"] == len(NEW_BYTES)
            and value["sha256"] == NEW_SHA256
            and type(value["device"]) is int and value["device"] > 0
            and type(value["inode"]) is int and value["inode"] > 0
            and value["owner"] == owner_name
            and value["group"] == group_name
            and value["mode"] == "0644"
            and upload_path.exists()
            and listed.st_dev == value["device"]
            and listed.st_ino == value["inode"]
            and listed.st_size == value["bytes"]
            and hashlib.sha256(upload_path.read_bytes()).hexdigest() == value["sha256"]
            and stat.S_IMODE(listed.st_mode) == 0o644
            and orchestrator._decode_json(stdout) == value
            and normalized == outcome
            and "interruption_kind" not in normalized
            and "interruption_source" not in normalized
        )
        return ok, f"returncode={returncode};stderr={stderr!r};stdout={stdout!r};normalized={normalized!r}"

    t36_ok, t36_observed = t36()
    emit(
        "T36",
        t36_ok,
        expected="persisted upload main emits one compact canonical JSON object accepted by strict orchestrator decode",
        observed=t36_observed,
        helper=UPLOAD,
        relation="actual helper stdout and upload-temp identity",
    )

    def t37() -> tuple[bool, str]:
        root = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r2-t37-")).resolve()
        RETAINED_ROOTS.append(root)
        parent = root / "config"
        parent.mkdir()
        os.chmod(parent, 0o775)
        target = parent / "mapping.yaml"
        upload_path = parent / ".mapping.yaml.d2-r7b-new.8de5edb"
        backup_path = parent / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
        target.write_bytes(OLD_BYTES)
        upload_path.write_bytes(NEW_BYTES)
        os.chmod(target, 0o644)
        os.chmod(upload_path, 0o644)
        deploy_module = load_artifact("d2_r7b_p2_r2_t37_deploy", DEPLOY)
        deploy_module.PARENT_PATH = str(parent)
        deploy_module.TARGET_PATH = str(target)
        deploy_module.UPLOAD_TEMP_PATH = str(upload_path)
        deploy_module.BACKUP_PATH = str(backup_path)
        deploy_module.EXPECTED_OWNER = owner_name
        deploy_module.EXPECTED_GROUP = group_name
        deploy_module.EXPECTED_TARGET_DEVICE = parent.stat().st_dev
        deploy_module.EXPECTED_TARGET_INODE = target.stat().st_ino
        deploy_module.EXPECTED_OLD_BYTES = len(OLD_BYTES)
        deploy_module.EXPECTED_OLD_SHA256 = OLD_SHA256
        deploy_module.EXPECTED_FILESYSTEM = filesystem_name
        deploy_module._filesystem_type = lambda _path: filesystem_name
        before_upload = os.lstat(upload_path)
        before_upload_realpath = os.path.realpath(upload_path)
        before_target = os.lstat(target)
        returncode, stdout, stderr = invoke_persisted_main(deploy_module)
        try:
            value = parse_compact_json_line(stdout)
        except Exception as exc:
            return False, f"returncode={returncode};stderr={stderr!r};legacy_stdout={stdout!r};parse_error={exc!r}"
        orchestrator = load_artifact("d2_r7b_p2_r2_t37_orchestrator", P2_R3_DIR / "remote_i1_orchestrator.py")
        source = value["source_upload_temp"]
        target_value = value["target"]
        backup_value = value["backup"]
        target_after = os.lstat(target)
        backup_after = os.lstat(backup_path)
        expected_top_keys = {"backup", "operation", "phase", "source_upload_temp", "status", "target"}
        expected_identity_keys = {"bytes", "device", "group", "inode", "mode", "owner", "path", "realpath", "sha256"}
        expected_source_keys = expected_identity_keys | {"state"}
        expected_target_keys = (expected_identity_keys - {"inode"}) | {"inode_after", "inode_before"}
        outcome = {"child_returncode": returncode, "stdout": stdout}
        normalized = orchestrator._normalize_invalid_child_json(outcome)
        ok = (
            returncode == 0
            and stderr == b""
            and set(value) == expected_top_keys
            and value["status"] == "PASS"
            and value["phase"] == "REMOTE_DEPLOY"
            and value["operation"] == "ATOMIC_REPLACE_WITH_BACKUP"
            and set(source) == expected_source_keys
            and source["state"] == "CONSUMED_BY_ATOMIC_REPLACE"
            and source["path"] == str(upload_path)
            and source["realpath"] == before_upload_realpath
            and source["bytes"] == len(NEW_BYTES)
            and source["sha256"] == NEW_SHA256
            and source["device"] == before_upload.st_dev
            and source["inode"] == before_upload.st_ino
            and source["owner"] == owner_name
            and source["group"] == group_name
            and source["mode"] == "0644"
            and set(target_value) == expected_target_keys
            and target_value["path"] == str(target)
            and target_value["realpath"] == os.path.realpath(target)
            and target_value["bytes"] == len(NEW_BYTES)
            and target_value["sha256"] == NEW_SHA256
            and target_value["device"] == target_after.st_dev
            and target_value["inode_before"] == before_target.st_ino
            and target_value["inode_after"] == target_after.st_ino
            and target_value["inode_after"] != target_value["inode_before"]
            and target_value["owner"] == owner_name
            and target_value["group"] == group_name
            and target_value["mode"] == "0644"
            and set(backup_value) == expected_identity_keys
            and backup_value["path"] == str(backup_path)
            and backup_value["realpath"] == os.path.realpath(backup_path)
            and backup_value["bytes"] == len(OLD_BYTES)
            and backup_value["sha256"] == OLD_SHA256
            and backup_value["device"] == backup_after.st_dev
            and backup_value["inode"] == backup_after.st_ino
            and backup_value["owner"] == owner_name
            and backup_value["group"] == group_name
            and backup_value["mode"] == "0644"
            and not upload_path.exists()
            and target.read_bytes() == NEW_BYTES
            and backup_path.read_bytes() == OLD_BYTES
            and orchestrator._decode_json(stdout) == value
            and normalized == outcome
            and "interruption_kind" not in normalized
            and "interruption_source" not in normalized
        )
        return ok, f"returncode={returncode};stderr={stderr!r};stdout={stdout!r};normalized={normalized!r}"

    t37_ok, t37_observed = t37()
    emit(
        "T37",
        t37_ok,
        expected="persisted deploy main emits exact nested JSON; upload is consumed; target NEW_EXACT and backup OLD_EXACT",
        observed=t37_observed,
        helper=DEPLOY,
        relation="actual helper stdout and atomic replacement identities",
    )

    t18_ok = True
    t18_observed = "PASS"
    try:
        assert_persisted_loader_semantics(load_artifact, "d2_r7b_p2_r2_t18")
    except Exception as exc:
        t18_ok = False
        t18_observed = repr(exc)
    emit(
        "T18",
        t18_ok,
        expected="PASS bytecode-free persisted artifact loader semantics",
        observed=t18_observed,
        helper=Path(__file__).resolve(),
        relation="external fixture cache absent; sys.modules transaction",
    )

    t19_ok = (
        sys.dont_write_bytecode is False
        and sys.pycache_prefix is None
        and repository_cache_snapshot() == repository_cache_before
    )
    emit(
        "T19",
        t19_ok,
        expected="repository cache path/hash/size/mtime/entry set unchanged",
        observed=f"ordinary_env={sys.dont_write_bytecode is False and sys.pycache_prefix is None};cache_equal={repository_cache_snapshot() == repository_cache_before}",
        helper=Path(__file__).resolve(),
        relation="full T-matrix repository cache invariance",
    )

    print(f"SYNTHETIC_ROOT={synthetic_root}")
    for retained in RETAINED_ROOTS:
        print(f"RETAINED_ROOT={retained}")
    print(f"MATRIX={'PASS' if all(records) and len(records) == 37 else 'FAIL'} count={len(records)}/37")
    print(f"SOURCE_NEW_BYTES={len(NEW_BYTES)} SOURCE_NEW_SHA256={NEW_SHA256}")
    print(f"SYNTHETIC_OLD_BYTES={len(OLD_BYTES)} SYNTHETIC_OLD_SHA256={OLD_SHA256}")
    return 0 if all(records) and len(records) == 37 else 1


if __name__ == "__main__":
    raise SystemExit(main())
