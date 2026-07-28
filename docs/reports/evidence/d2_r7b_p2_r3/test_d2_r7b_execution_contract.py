#!/usr/bin/env python3
"""E1-E50 synthetic matrix against the persisted execution artifacts."""

from __future__ import annotations

import base64
from contextlib import redirect_stderr, redirect_stdout
import grp
import hashlib
import importlib.util
from io import StringIO
import json
import os
import pwd
import re
import shlex
import signal
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
P2_DIR = REPO_ROOT / "docs/reports/evidence/d2_r7b_p2_r2"
ORCH_PATH = ARTIFACT_DIR / "remote_i1_orchestrator.py"
POSTFLIGHT_PATH = ARTIFACT_DIR / "remote_postflight.py"
MANIFEST_BOUND = {
    "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh": P2_DIR / "local_materialization.sh",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py": P2_DIR / "remote_preflight.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py": P2_DIR / "remote_upload_exclusive.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py": P2_DIR / "remote_deploy.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py": P2_DIR / "remote_rollback.py",
    "docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py": P2_DIR / "test_d2_r7b_contract.py",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py": ORCH_PATH,
    "docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py": POSTFLIGHT_PATH,
    "docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py": Path(__file__).resolve(),
}
EXPECTED_ENDPOINT = "mari@10.0.0.217"
EXPECTED_CONTAINER_ID = "5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524"
EXPECTED_IMAGE_ID = "sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a"
EXPECTED_CONFIGURED_IMAGE = "edge-mes-demo-collector"
EXPECTED_STARTED_AT = "2026-07-23T12:23:25.959624Z"
EXPECTED_NEW_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
EXPECTED_OLD_SHA256 = "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"
EXPECTED_NEW_BYTES = 7112
EXPECTED_OLD_BYTES = 5935
TARGET_RELATIVE = "config/mapping.yaml"
UPLOAD_NAME = ".mapping.yaml.d2-r7b-new.8de5edb"
BACKUP_NAME = ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
ROLLBACK_NAME = ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"


RETAINED_ROOTS: list[Path] = []


def complete_phase_record(phase: str) -> dict[str, Any]:
    target = "/opt/edge-mes-demo/config/mapping.yaml"
    upload = f"/opt/edge-mes-demo/config/{UPLOAD_NAME}"
    backup = f"/opt/edge-mes-demo/config/{BACKUP_NAME}"
    rollback = f"/opt/edge-mes-demo/config/{ROLLBACK_NAME}"
    common_new = {
        "bytes": EXPECTED_NEW_BYTES,
        "sha256": EXPECTED_NEW_SHA256,
        "device": 2050,
        "owner": "mari",
        "group": "mari",
        "mode": "0644",
    }
    common_old = {
        "bytes": EXPECTED_OLD_BYTES,
        "sha256": EXPECTED_OLD_SHA256,
        "device": 2050,
        "owner": "mari",
        "group": "mari",
        "mode": "0644",
    }
    if phase == "REMOTE_PREFLIGHT":
        return {
            "status": "PASS",
            "transport_endpoint": EXPECTED_ENDPOINT,
            "hostname": "Pi-5b-Li",
            "principal": "mari",
            "target_device": 2050,
            "target_inode": 550698,
            "parent_device": 2050,
            "filesystem": "ext4",
        }
    if phase == "REMOTE_UPLOAD":
        return {
            "status": "PASS", "phase": phase, "path": upload, "realpath": upload,
            "inode": 7001, **common_new,
        }
    if phase == "REMOTE_DEPLOY":
        return {
            "status": "PASS",
            "phase": phase,
            "operation": "ATOMIC_REPLACE_WITH_BACKUP",
            "source_upload_temp": {
                "state": "CONSUMED_BY_ATOMIC_REPLACE", "path": upload, "realpath": upload,
                "inode": 7001, **common_new,
            },
            "target": {
                "path": target, "realpath": target, "inode_before": 550698,
                "inode_after": 7001, **common_new,
            },
            "backup": {"path": backup, "realpath": backup, "inode": 7002, **common_old},
        }
    if phase == "REMOTE_POSTFLIGHT":
        observed = {
            "id": EXPECTED_CONTAINER_ID,
            "name": "/edge-mes-collector",
            "image": EXPECTED_IMAGE_ID,
            "configured_image": EXPECTED_CONFIGURED_IMAGE,
            "running": True,
            "started_at": EXPECTED_STARTED_AT,
            "restart_count": 0,
            "mount": {"source": "/opt/edge-mes-demo/config", "destination": "/app/config", "type": "bind", "rw": False},
        }
        expected = {**observed, "name": ["/edge-mes-collector", "edge-mes-collector"]}
        return {
            "status": "PASS",
            "phase": phase,
            "classification": "DEPLOYED_IDENTITY_VERIFIED",
            "target_state": {
                "path": target, "realpath": target, "inode": 7001, "state": "NEW_EXACT",
                "exists": True, "exact_realpath": True, **common_new,
            },
            "upload_temp_state": {"path": upload, "state": "ABSENT", "exists": False, "realpath": None},
            "backup_state": {
                "path": backup, "realpath": backup, "inode": 7002, "state": "OLD_EXACT",
                "exists": True, "exact_realpath": True, **common_old,
            },
            "rollback_temp_state": {"path": rollback, "state": "ABSENT", "exists": False, "realpath": None},
            "collector_state": {
                "state": "UNCHANGED", "observed": observed, "expected": expected,
                "command": ["docker", "inspect", EXPECTED_CONTAINER_ID], "exit_code": 0,
            },
            "exact_artifact_paths": {"target": target, "upload_temp": upload, "backup": backup, "rollback_temp": rollback},
            "task_lifecycle_actions": {
                "cleanup_count": 0, "rollback_count": 0, "restart_count_by_task": 0, "activation_count": 0,
            },
            "message": "RUNTIME CONFIG LOAD NOT CLAIMED",
        }
    raise AssertionError(f"unknown phase: {phase}")


class FaultingTextStream:
    """Synthetic stdout that interrupts one primary JSON write at a named fault point."""

    encoding = "utf-8"

    def __init__(self, fault_point: str) -> None:
        self.fault_point = fault_point
        self.parts: list[str] = []
        self.first_prefix = ""
        self.write_calls = 0
        self.json_write_calls = 0
        self.flush_calls = 0
        self._faulted = False

    def write(self, text: str) -> int:
        self.write_calls += 1
        if "{" in text:
            self.json_write_calls += 1
        if not self._faulted and "{" in text:
            self._faulted = True
            if self.fault_point == "PARTIAL_JSON_BODY":
                prefix = text[:max(2, len(text) // 4)]
            elif self.fault_point == "COMPLETE_JSON_BEFORE_NEWLINE":
                prefix = text.split("\n", 1)[0]
            else:
                raise AssertionError(f"unknown stream fault point: {self.fault_point}")
            assert prefix
            self.first_prefix = prefix
            self.parts.append(prefix)
            raise KeyboardInterrupt()
        self.parts.append(text)
        return len(text)

    def flush(self) -> None:
        self.flush_calls += 1

    def getvalue(self) -> str:
        return "".join(self.parts)


_MISSING_MODULE = object()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
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
    for evidence_root in (P2_DIR, ARTIFACT_DIR):
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


def source_hashes() -> dict[str, str]:
    return {relative: hashlib.sha256(path.read_bytes()).hexdigest() for relative, path in MANIFEST_BOUND.items()}


def write_manifest(path: Path, *, drift: bool = False) -> None:
    lines = []
    for relative in sorted(MANIFEST_BOUND):
        digest = source_hashes()[relative]
        if drift and relative.endswith("remote_upload_exclusive.py"):
            digest = "0" * 64
        lines.append(f"{digest}  {relative}\n")
    path.write_text("".join(lines), encoding="utf-8")


def make_docker_payload(config_dir: Path, **changes: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "Id": EXPECTED_CONTAINER_ID,
        "Name": "/edge-mes-collector",
        "Image": EXPECTED_IMAGE_ID,
        "Config": {"Image": EXPECTED_CONFIGURED_IMAGE},
        "State": {"Running": True, "StartedAt": EXPECTED_STARTED_AT},
        "RestartCount": 0,
        "Mounts": [{
            "Source": str(config_dir),
            "Destination": "/app/config",
            "Type": "bind",
            "RW": False,
        }],
    }
    for key, value in changes.items():
        if key == "Config.Image":
            payload["Config"]["Image"] = value
        elif key == "State.StartedAt":
            payload["State"]["StartedAt"] = value
        elif key == "State.Running":
            payload["State"]["Running"] = value
        elif key == "Mounts.RW":
            payload["Mounts"][0]["RW"] = value
        elif key == "RestartCount":
            payload["RestartCount"] = value
        else:
            payload[key] = value
    return payload


def fake_tools(base: Path) -> None:
    fakebin = base / "fakebin"
    fakebin.mkdir(parents=True, exist_ok=True)
    ssh = fakebin / "ssh"
    ssh.write_text(
        '''#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import re
import shlex
import signal
import sys
from pathlib import Path

def configure(ns):
    root = Path(os.path.realpath(os.environ["D2_R7B_SYNTHETIC_ROOT"]))
    target = root / "config" / "mapping.yaml"
    device = int(os.environ["D2_R7B_SYNTHETIC_DEVICE"])
    owner = os.environ["D2_R7B_SYNTHETIC_OWNER"]
    group = os.environ["D2_R7B_SYNTHETIC_GROUP"]
    filesystem = os.environ["D2_R7B_SYNTHETIC_FILESYSTEM"]
    for name in ("EXPECTED_OWNER", "EXPECTED_GROUP"):
        if name in ns:
            ns[name] = owner if name.endswith("OWNER") else group
    if "EXPECTED_PRINCIPAL" in ns:
        ns["EXPECTED_PRINCIPAL"] = owner
    for name in ("EXPECTED_PARENT_DEVICE", "EXPECTED_TARGET_DEVICE"):
        if name in ns:
            ns[name] = device
    if "EXPECTED_TARGET_INODE" in ns:
        ns["EXPECTED_TARGET_INODE"] = target.stat().st_ino
    if "EXPECTED_TARGET_BYTES" in ns:
        ns["EXPECTED_TARGET_BYTES"] = 5935
    if "EXPECTED_TARGET_SHA256" in ns:
        ns["EXPECTED_TARGET_SHA256"] = os.environ["D2_R7B_SYNTHETIC_OLD_SHA256"]
    if "EXPECTED_OLD_BYTES" in ns:
        ns["EXPECTED_OLD_BYTES"] = 5935
    if "EXPECTED_OLD_SHA256" in ns:
        ns["EXPECTED_OLD_SHA256"] = os.environ["D2_R7B_SYNTHETIC_OLD_SHA256"]
    if "EXPECTED_FILESYSTEM" in ns:
        ns["EXPECTED_FILESYSTEM"] = filesystem
    if "_filesystem_type" in ns:
        ns["_filesystem_type"] = lambda _path: filesystem
    if "EXPECTED_MOUNT_SOURCE" in ns:
        ns["EXPECTED_MOUNT_SOURCE"] = str(Path(os.environ["D2_R7B_SYNTHETIC_ROOT"]) / "config")
    for name, value in {
        "PARENT_PATH": root / "config",
        "TARGET_PATH": target,
        "UPLOAD_TEMP_PATH": root / "config" / ".mapping.yaml.d2-r7b-new.8de5edb",
        "BACKUP_PATH": root / "config" / ".mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
        "ROLLBACK_TEMP_PATH": root / "config" / ".mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
    }.items():
        if name in ns:
            ns[name] = str(value)

class PayloadStdin:
    class Buffer:
        def __init__(self, payload):
            self.payload = payload

        def read(self):
            return self.payload

    def __init__(self, payload):
        self.buffer = self.Buffer(payload)

def run_persisted_main(ns, payload=None):
    original_stdin = sys.stdin
    if payload is not None:
        sys.stdin = PayloadStdin(payload)
    try:
        return int(ns["main"]())
    finally:
        sys.stdin = original_stdin

def corrupt_contract_record(record, variant):
    value = json.loads(json.dumps(record))
    if variant == "empty-object":
        return {}
    if variant == "wrong-status":
        value["status"] = "HOLD"
    elif variant == "wrong-phase":
        value["phase"] = "WRONG_PHASE"
    elif variant == "missing-field":
        value.pop("hostname", None)
    elif variant == "missing-identity":
        value.pop("inode", None)
    elif variant == "additional-field":
        value["unexpected"] = True
    elif variant == "wrong-path":
        value["path"] = value["path"] + ".wrong"
    elif variant == "wrong-hash":
        value["sha256"] = "0" * 64
    elif variant == "wrong-bytes":
        value["bytes"] += 1
    elif variant == "wrong-mode":
        value["mode"] = "0600"
    elif variant == "wrong-operation":
        value["operation"] = "COPY"
    elif variant == "missing-nested-field":
        value["source_upload_temp"].pop("sha256")
    elif variant == "additional-nested-field":
        value["target"]["unexpected"] = True
    elif variant == "upload-source-inode-mismatch":
        value["source_upload_temp"]["inode"] += 1
    elif variant == "source-target-inode-mismatch":
        value["target"]["inode_after"] += 1
    elif variant == "minimal-spoof":
        return {"classification": "DEPLOYED_IDENTITY_VERIFIED"}
    elif variant == "missing-state-object":
        value.pop("target_state")
    elif variant == "lifecycle-nonzero":
        value["task_lifecycle_actions"]["activation_count"] = 1
    else:
        raise AssertionError(f"unknown contract corruption: {variant}")
    return value

def main():
    if len(sys.argv) != 3:
        return 91
    endpoint, command = sys.argv[1:]
    command_parts = shlex.split(command)
    if len(command_parts) != 3 or command_parts[:2] != ["python3", "-c"]:
        return 92
    bootstrap = command_parts[2]
    match = re.search(r"base64\\.b64decode\\('([A-Za-z0-9+/=]+)'\\)", bootstrap)
    if match is None:
        return 92
    source = base64.b64decode(match.group(1))
    phase = next((name for name in ("remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py") if name in command), "unknown")
    payload = sys.stdin.buffer.read()
    log_path = Path(os.environ["D2_R7B_FAKE_LOG"])
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"endpoint": endpoint, "phase": phase, "stdin_bytes": len(payload), "source_sha256": hashlib.sha256(source).hexdigest()}, sort_keys=True) + "\\n")
    mode = os.environ.get("D2_R7B_FAKE_MODE", "")
    if phase == "remote_preflight.py" and mode in {"preflight-keyboardinterrupt", "preflight-password-prompt"}:
        if mode == "preflight-password-prompt":
            sys.stderr.write("mari@Pi-5b-Li's password: ")
            sys.stderr.flush()
        os.kill(os.getppid(), signal.SIGINT)
        signal.pause()
    if phase == "remote_upload_exclusive.py" and mode == "upload-keyboardinterrupt":
        os.kill(os.getppid(), signal.SIGINT)
        signal.pause()
    if phase == "remote_deploy.py" and mode == "deploy-before-replacement-interrupt":
        os.kill(os.getppid(), signal.SIGINT)
        signal.pause()
    if phase == "remote_postflight.py" and mode == "postflight-keyboardinterrupt":
        os.kill(os.getppid(), signal.SIGINT)
        signal.pause()
    if phase == "remote_preflight.py" and mode == "preflight-signal":
        os.kill(os.getpid(), signal.SIGTERM)
    if phase == "remote_preflight.py" and mode == "preflight-eof":
        sys.stderr.write("EOF while reading authentication input\\n")
        return 47
    if phase == "remote_preflight.py" and mode == "preflight-auth-fail":
        sys.stderr.write("Permission denied (publickey,password)\\n")
        return 255
    if phase == "remote_preflight.py" and mode == "preflight-unknown":
        sys.stderr.write("transport interrupted before authentication completed\\n")
        return 255
    if phase == "remote_deploy.py" and mode == "deploy-after-replacement-interrupt":
        ns = {"__name__": "persisted_remote_artifact"}
        exec(compile(source, phase, "exec"), ns, ns)
        configure(ns)
        ns["deploy"]()
        os.kill(os.getppid(), signal.SIGINT)
        signal.pause()
    if phase == "remote_preflight.py" and mode == "preflight-fail":
        return 23
    if phase == "remote_upload_exclusive.py" and mode == "upload-fail":
        return 31
    if phase == "remote_deploy.py" and mode == "deploy-fail":
        return 41
    invalid_outputs = {
        "empty": "",
        "legacy-text": "PASS upload bytes=7112 sha256=legacy inode=1\\n",
        "malformed-json": "{\\n",
        "multiple-json": "{}{}\\n",
        "json-list": "[]\\n",
        "json-scalar": "1\\n",
        "json-trailing-text": '{"status":"PASS"} trailing\\n',
    }
    if phase in {"remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py"}:
        phase_prefix = phase.replace(".py", "")
        for suffix, output in invalid_outputs.items():
            if mode == phase_prefix + "-invalid-" + suffix:
                sys.stdout.write(output)
                return 0
    if phase in {"remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py"} and mode == phase.replace(".py", "") + "-invalid-json":
        print("not-json")
        return 0
    ns = {"__name__": "persisted_remote_artifact"}
    exec(compile(source, phase, "exec"), ns, ns)
    root = Path(os.environ["D2_R7B_SYNTHETIC_ROOT"])
    config_dir = root / "config"
    if phase != "remote_postflight.py":
        configure(ns)
    if phase == "remote_preflight.py" and mode.startswith("preflight-contract-"):
        result = ns["run_preflight"](
            docker_payload=[json.loads(os.environ["D2_R7B_FAKE_DOCKER_PAYLOAD"])],
            hostname="Pi-5b-Li",
            principal=os.environ["D2_R7B_SYNTHETIC_OWNER"],
            filesystem=os.environ["D2_R7B_SYNTHETIC_FILESYSTEM"],
        )
        record = corrupt_contract_record({"status": "PASS", **result}, mode.removeprefix("preflight-contract-"))
        print(json.dumps(record, sort_keys=True))
        return 0
    if phase == "remote_upload_exclusive.py" and mode.startswith("upload-contract-"):
        result = ns["upload"](payload)
        record = corrupt_contract_record(
            {"status": "PASS", "phase": "REMOTE_UPLOAD", **result},
            mode.removeprefix("upload-contract-"),
        )
        print(json.dumps(record, sort_keys=True))
        return 0
    if phase == "remote_deploy.py" and mode.startswith("deploy-contract-"):
        record = corrupt_contract_record(ns["deploy"](), mode.removeprefix("deploy-contract-"))
        print(json.dumps(record, sort_keys=True))
        return 0
    if phase == "remote_postflight.py" and mode.startswith("postflight-contract-"):
        record = corrupt_contract_record(ns["run_postflight"](), mode.removeprefix("postflight-contract-"))
        print(json.dumps(record, sort_keys=True))
        return 0
    if phase == "remote_preflight.py":
        result = ns["run_preflight"](
            docker_payload=[json.loads(os.environ["D2_R7B_FAKE_DOCKER_PAYLOAD"])],
            hostname="Pi-5b-Li",
            principal=os.environ["D2_R7B_SYNTHETIC_OWNER"],
            filesystem=os.environ["D2_R7B_SYNTHETIC_FILESYSTEM"],
        )
        print(json.dumps({"status": "PASS", **result}, sort_keys=True))
        return 0
    if phase == "remote_upload_exclusive.py" and mode == "upload-helper-failure":
        return run_persisted_main(ns, b"invalid-payload")
    if phase == "remote_deploy.py" and mode == "deploy-helper-failure":
        Path(ns["UPLOAD_TEMP_PATH"]).unlink(missing_ok=True)
        return run_persisted_main(ns)
    if phase == "remote_upload_exclusive.py":
        return run_persisted_main(ns, payload)
    if phase == "remote_deploy.py":
        helper_code = run_persisted_main(ns)
        return 42 if mode == "deploy-after-replacement-fail" else helper_code
    if phase == "remote_postflight.py":
        return int(ns["main"]())
    return 93

if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")
    ssh.chmod(0o755)
    docker = fakebin / "docker"
    docker.write_text(
        '''#!/usr/bin/env python3
import json
import sys
if len(sys.argv) != 3 or sys.argv[1] != "inspect" or len(sys.argv[2]) != 64:
    raise SystemExit(2)
print(json.dumps([json.loads(__import__("os").environ["D2_R7B_FAKE_DOCKER_PAYLOAD"])]))
''', encoding="utf-8")
    docker.chmod(0o755)


def make_fixture() -> dict[str, Any]:
    base = Path(tempfile.mkdtemp(prefix="d2-r7b-p2-r3-")).resolve()
    RETAINED_ROOTS.append(base)
    (base / "local-stage-parent").mkdir()
    remote_root = (base / "remote").resolve()
    config_dir = remote_root / "config"
    config_dir.mkdir(parents=True)
    old_bytes = (b"synthetic-remote-old\n" * ((EXPECTED_OLD_BYTES // len(b"synthetic-remote-old\n")) + 1))[:EXPECTED_OLD_BYTES]
    (config_dir / "mapping.yaml").write_bytes(old_bytes)
    os.chmod(config_dir, 0o775)
    os.chmod(config_dir / "mapping.yaml", 0o644)
    owner = pwd.getpwuid(os.geteuid()).pw_name
    group = grp.getgrgid(os.getegid()).gr_name
    new_bytes = subprocess.check_output(["git", "-C", str(REPO_ROOT), "cat-file", "-p", "HEAD:config/mapping.yaml"])
    assert len(new_bytes) == EXPECTED_NEW_BYTES
    assert hashlib.sha256(new_bytes).hexdigest() == EXPECTED_NEW_SHA256
    fixture = {
        "base": base,
        "remote_root": remote_root,
        "config_dir": config_dir,
        "target": config_dir / "mapping.yaml",
        "upload": config_dir / UPLOAD_NAME,
        "backup": config_dir / BACKUP_NAME,
        "rollback": config_dir / ROLLBACK_NAME,
        "old_bytes": old_bytes,
        "new_bytes": new_bytes,
        "owner": owner,
        "group": group,
        "device": config_dir.stat().st_dev,
        "filesystem": "syntheticfs",
        "log": base / "ssh.log",
        "manifest": base / "manifest.sha256",
        "docker_payload": make_docker_payload(config_dir),
    }
    fake_tools(base)
    if all(path.exists() for path in MANIFEST_BOUND.values()):
        write_manifest(fixture["manifest"])
    return fixture


def env_for(
    fixture: dict[str, Any],
    *,
    interactive: bool = True,
    mode: str = "",
    manifest: Path | None = None,
    root_override: Path | None = None,
) -> dict[str, str]:
    env = dict(os.environ)
    root = fixture["remote_root"] if root_override is None else root_override
    env.update({
        "D2_R7B_SYNTHETIC_ROOT": str(root),
        "D2_R7B_SYNTHETIC_OWNER": fixture["owner"],
        "D2_R7B_SYNTHETIC_GROUP": fixture["group"],
        "D2_R7B_SYNTHETIC_DEVICE": str(fixture["device"]),
        "D2_R7B_SYNTHETIC_FILESYSTEM": fixture["filesystem"],
        "D2_R7B_SYNTHETIC_OLD_SHA256": hashlib.sha256(fixture["old_bytes"]).hexdigest(),
        "D2_R7B_FAKE_LOG": str(fixture["log"]),
        "D2_R7B_FAKE_MODE": mode,
        "D2_R7B_FAKE_DOCKER_PAYLOAD": json.dumps(fixture["docker_payload"], sort_keys=True),
        "PATH": str(fixture["base"] / "fakebin") + os.pathsep + env.get("PATH", ""),
        "TMPDIR": str(fixture["base"] / "local-stage-parent"),
    })
    if manifest is not None:
        env["D2_R7B_MANIFEST_PATH"] = str(manifest)
    else:
        env.pop("D2_R7B_MANIFEST_PATH", None)
    if interactive:
        env["D2_R7B_TEST_INTERACTIVE_TTY"] = "1"
    else:
        env.pop("D2_R7B_TEST_INTERACTIVE_TTY", None)
    return env


def reset_remote(fixture: dict[str, Any]) -> None:
    target = fixture["target"]
    if target.is_symlink() or target.exists():
        target.unlink()
    target.write_bytes(fixture["old_bytes"])
    os.chmod(target, 0o644)
    for key in ("upload", "backup", "rollback"):
        path = fixture[key]
        if path.is_symlink() or path.exists():
            path.unlink()


def set_state(fixture: dict[str, Any], state: str) -> None:
    reset_remote(fixture)
    if state == "upload-staged":
        fixture["upload"].write_bytes(fixture["new_bytes"])
    elif state == "backup-created":
        fixture["backup"].write_bytes(fixture["old_bytes"])
    elif state == "partial":
        fixture["target"].write_bytes(fixture["new_bytes"])
    elif state == "deployed":
        fixture["target"].write_bytes(fixture["new_bytes"])
        fixture["backup"].write_bytes(fixture["old_bytes"])
    elif state == "unknown":
        copy = fixture["base"] / "old-copy"
        copy.write_bytes(fixture["old_bytes"])
        fixture["target"].unlink()
        fixture["target"].symlink_to(copy)
    for key in ("upload", "backup", "rollback"):
        if fixture[key].exists():
            os.chmod(fixture[key], 0o644)


def parse_json_output(result: subprocess.CompletedProcess[bytes]) -> dict[str, Any]:
    stdout = result.stdout.decode("utf-8").strip()
    if not stdout:
        raise AssertionError(f"missing JSON stdout; stderr={result.stderr.decode()!r}")
    return json.loads(stdout)


class CapturedPayloadStdin:
    class Buffer:
        def __init__(self, payload: bytes) -> None:
            self.payload = payload

        def read(self) -> bytes:
            return self.payload

    def __init__(self, payload: bytes) -> None:
        self.buffer = self.Buffer(payload)


def invoke_persisted_main(module: Any, *, payload: bytes | None = None) -> tuple[int, bytes, bytes]:
    original_stdin = sys.stdin
    stdout = StringIO()
    stderr = StringIO()
    if payload is not None:
        sys.stdin = CapturedPayloadStdin(payload)  # type: ignore[assignment]
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            returncode = module.main()
    finally:
        sys.stdin = original_stdin
    return returncode, stdout.getvalue().encode("utf-8"), stderr.getvalue().encode("utf-8")


def run_orchestrator(fixture: dict[str, Any], *, mode: str = "", interactive: bool = True) -> tuple[subprocess.CompletedProcess[bytes], dict[str, Any]]:
    fixture["log"].unlink(missing_ok=True)
    reset_remote(fixture)
    result = subprocess.run(
        [sys.executable, str(ORCH_PATH), "--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"],
        cwd=REPO_ROOT,
        env=env_for(fixture, interactive=interactive, mode=mode, manifest=fixture["manifest"]),
        capture_output=True,
        check=False,
    )
    return result, parse_json_output(result)


def run_postflight(fixture: dict[str, Any], state: str, payload: dict[str, Any] | None = None) -> tuple[subprocess.CompletedProcess[bytes], dict[str, Any]]:
    set_state(fixture, state)
    selected = fixture["docker_payload"] if payload is None else payload
    env = env_for(fixture, interactive=False, manifest=None)
    env["D2_R7B_FAKE_DOCKER_PAYLOAD"] = json.dumps(selected, sort_keys=True)
    result = subprocess.run([sys.executable, str(POSTFLIGHT_PATH)], cwd=REPO_ROOT, env=env, capture_output=True, check=False)
    return result, parse_json_output(result)


def terminal_complete(terminal: dict[str, Any]) -> None:
    required = {
        "status", "phase", "phase_exit_codes", "local_source", "target_state",
        "upload_temp_state", "backup_state", "rollback_temp_state", "collector_state",
        "exact_artifact_paths", "retry_count", "resume_count", "cleanup_count",
        "rollback_count", "restart_count_by_task", "activation_count", "local_stage_root",
        "next_authority",
    }
    missing = required - terminal.keys()
    assert not missing, f"terminal missing {sorted(missing)}"
    assert terminal["retry_count"] == 0
    assert terminal["resume_count"] == 0
    assert terminal["cleanup_count"] == 0
    assert terminal["rollback_count"] == 0
    assert terminal["activation_count"] == 0
    assert type(terminal["restart_count_by_task"]) is int
    assert terminal["restart_count_by_task"] == 0


def assert_orchestrator_zero_counters(terminal: dict[str, Any]) -> None:
    for key in ("retry_count", "resume_count", "cleanup_count", "rollback_count", "activation_count"):
        assert type(terminal[key]) is int
        assert terminal[key] == 0
    assert type(terminal["restart_count_by_task"]) is int
    assert terminal["restart_count_by_task"] == 0


def assert_postflight_zero_counters(terminal: dict[str, Any]) -> None:
    actions = terminal["task_lifecycle_actions"]
    for key in ("cleanup_count", "rollback_count", "activation_count"):
        assert type(actions[key]) is int
        assert actions[key] == 0
    assert type(actions["restart_count_by_task"]) is int
    assert actions["restart_count_by_task"] == 0


def parse_complete_ndjson_records(stream_text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in stream_text.splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def postflight_state_check(fixture: dict[str, Any], state: str, expected: str) -> None:
    result, terminal = run_postflight(fixture, state)
    assert terminal["classification"] == expected, terminal
    assert result.returncode == (0 if expected == "DEPLOYED_IDENTITY_VERIFIED" else 2)


def main() -> int:
    fixture = make_fixture()
    repository_cache_before = repository_cache_snapshot()
    results: list[bool] = []

    def case(label: str, fn) -> None:
        try:
            fn()
        except Exception as exc:
            print(f"{label}: FAIL {exc!r}")
            results.append(False)
        else:
            print(f"{label}: PASS")
            results.append(True)

    def e1() -> None:
        result = subprocess.run([sys.executable, str(ORCH_PATH)], cwd=REPO_ROOT, capture_output=True, check=False)
        terminal = parse_json_output(result)
        assert result.returncode == 0
        assert terminal["status"] == "DRY_RUN"
        assert terminal["REMOTE_CALL_COUNT"] == 0

    def e2() -> None:
        for args in (("--execute",), ("--confirm", "D2-R7B-I1-CONFIG-ONLY")):
            result = subprocess.run([sys.executable, str(ORCH_PATH), *args], cwd=REPO_ROOT, capture_output=True, check=False)
            terminal = parse_json_output(result)
            assert result.returncode == 2
            assert terminal["status"] == "HOLD_REMOTE_EXECUTION_NOT_CONFIRMED"
            assert terminal["REMOTE_CALL_COUNT"] == 0

    def e3() -> None:
        drift = fixture["base"] / "manifest-drift.sha256"
        write_manifest(drift, drift=True)
        result = subprocess.run(
            [sys.executable, str(ORCH_PATH), "--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"],
            cwd=REPO_ROOT,
            env=env_for(fixture, manifest=drift),
            capture_output=True,
            check=False,
        )
        terminal = parse_json_output(result)
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_LOCAL_SOURCE"
        assert terminal["REMOTE_CALL_COUNT"] == 0
        assert not fixture["log"].exists()

    def e4() -> None:
        orch = load_module("e4_orchestrator", ORCH_PATH)
        helper = P2_DIR / "remote_upload_exclusive.py"
        command = orch.build_remote_command(helper.read_bytes(), helper.name)
        assert command.startswith("python3 -c ")
        assert "scp" not in command and "sshpass" not in command
        bootstrap = shlex.split(command)[2]
        match = re.search(r"base64\.b64decode\('([A-Za-z0-9+/=]+)'\)", bootstrap)
        assert match is not None
        assert base64.b64decode(match.group(1)) == helper.read_bytes()

    def e5() -> None:
        result, terminal = run_orchestrator(fixture)
        assert result.returncode == 0
        records = [json.loads(line) for line in fixture["log"].read_text().splitlines()]
        upload = next(item for item in records if item["phase"] == "remote_upload_exclusive.py")
        assert upload["stdin_bytes"] == EXPECTED_NEW_BYTES
        assert upload["source_sha256"] == hashlib.sha256((P2_DIR / "remote_upload_exclusive.py").read_bytes()).hexdigest()
        assert all(item["stdin_bytes"] == 0 for item in records if item["phase"] != "remote_upload_exclusive.py")
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"

    def e6() -> None:
        fixture["log"].unlink(missing_ok=True)
        result, terminal = run_orchestrator(fixture)
        assert result.returncode == 0
        records = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
        assert records == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"]
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"

    def e7() -> None:
        result, terminal = run_orchestrator(fixture, mode="preflight-fail")
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_PREFLIGHT"
        assert [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()] == ["remote_preflight.py"]
        assert terminal["retry_count"] == 0

    def e8() -> None:
        result, terminal = run_orchestrator(fixture, mode="upload-fail")
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_UPLOAD_FAILED_NO_REPLACEMENT"
        assert [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()] == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_postflight.py"]
        assert terminal["upload_temp_state"]["state"] == "ABSENT"

    def e9() -> None:
        result, terminal = run_orchestrator(fixture, mode="deploy-fail")
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_DEPLOY_FAILED_NO_REPLACEMENT"
        assert terminal["target_state"]["state"] == "OLD_EXACT"
        assert terminal["classification"] in {"NO_MUTATION", "UPLOAD_STAGED_NO_REPLACEMENT"}

    def e10() -> None:
        result, terminal = run_orchestrator(fixture, mode="deploy-after-replacement-fail")
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_PARTIAL_DEPLOYMENT"
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["target_state"]["state"] == "NEW_EXACT"
        assert terminal["backup_state"]["state"] == "OLD_EXACT"

    def e11() -> None:
        result, terminal = run_postflight(fixture, "deployed")
        assert result.returncode == 0
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"

    def e12() -> None:
        drift_cases = (
            {"Id": "0" * 64},
            {"State.StartedAt": "2026-07-23T12:23:26.000000Z"},
            {"RestartCount": 1},
            {"Mounts.RW": True},
        )
        for changes in drift_cases:
            payload = make_docker_payload(fixture["config_dir"], **changes)
            result, terminal = run_postflight(fixture, "deployed", payload)
            assert result.returncode == 2
            assert terminal["classification"] != "DEPLOYED_IDENTITY_VERIFIED"
            assert terminal["collector_state"]["state"] == "DRIFT"

    def e13() -> None:
        for state, expected in (
            ("no-mutation", "NO_MUTATION"),
            ("upload-staged", "UPLOAD_STAGED_NO_REPLACEMENT"),
            ("backup-created", "BACKUP_CREATED_NO_REPLACEMENT"),
            ("partial", "PARTIAL_DEPLOYMENT"),
            ("unknown", "UNKNOWN_OR_UNSAFE"),
        ):
            postflight_state_check(fixture, state, expected)

    def e14() -> None:
        orch_text = ORCH_PATH.read_text(encoding="utf-8").lower()
        post_text = POSTFLIGHT_PATH.read_text(encoding="utf-8").lower()
        for forbidden in ("scp", "sftp", "rsync", "sshpass", "docker compose", "docker restart", "rollback()", "restart()", "activate()"):
            assert forbidden not in orch_text
        for forbidden in ("os.replace", "unlink(", "write_bytes(", "mkdir(", "docker compose", "docker restart"):
            assert forbidden not in post_text
        assert "\"inspect\", expected_container_id" in post_text
        result, terminal = run_orchestrator(fixture)
        assert result.returncode == 0
        assert terminal["cleanup_count"] == terminal["rollback_count"] == terminal["activation_count"] == 0

    def e15() -> None:
        run_orchestrator(fixture)
        endpoints = {json.loads(line)["endpoint"] for line in fixture["log"].read_text().splitlines()}
        assert endpoints == {EXPECTED_ENDPOINT}

    def e16() -> None:
        fixture["log"].unlink(missing_ok=True)
        result, terminal = run_orchestrator(fixture, interactive=False)
        assert result.returncode == 2
        assert terminal["status"] == "HOLD_INTERACTIVE_AUTHENTICATION_UNAVAILABLE"
        assert "HOLD / INTERACTIVE AUTHENTICATION UNAVAILABLE" in terminal["message"]
        assert terminal["REMOTE_CALL_COUNT"] == 0
        assert not fixture["log"].exists()

    def e17() -> None:
        for mode in ("preflight-fail", "upload-fail", "deploy-fail", "deploy-after-replacement-fail"):
            _, terminal = run_orchestrator(fixture, mode=mode)
            terminal_complete(terminal)
            assert terminal["exact_artifact_paths"]["target"]
            assert terminal["next_authority"]

    def e18() -> None:
        before = source_hashes()
        write_manifest(fixture["manifest"])
        orch = load_module("e18_orchestrator", ORCH_PATH)
        verification = orch.verify_composite_manifest(REPO_ROOT, fixture["manifest"])
        after = source_hashes()
        assert before == after
        assert verification["ok"] is True
        assert verification["count"] == 9
        assert all(item["status"] == "OK" for item in verification["entries"])

    def e19() -> None:
        direct_cases = (
            ([], "DRY_RUN", None),
            (["--execute"], "HOLD_REMOTE_EXECUTION_NOT_CONFIRMED", None),
        )
        for args, expected, env in direct_cases:
            result = subprocess.run([sys.executable, str(ORCH_PATH), *args], cwd=REPO_ROOT, env=env, capture_output=True, check=False)
            terminal = parse_json_output(result)
            assert terminal["status"] == expected
            assert_orchestrator_zero_counters(terminal)

        drift = fixture["base"] / "e19-manifest-drift.sha256"
        write_manifest(drift, drift=True)
        result = subprocess.run(
            [sys.executable, str(ORCH_PATH), "--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"],
            cwd=REPO_ROOT,
            env=env_for(fixture, manifest=drift),
            capture_output=True,
            check=False,
        )
        terminal = parse_json_output(result)
        assert terminal["status"] == "HOLD_LOCAL_SOURCE"
        assert_orchestrator_zero_counters(terminal)

        for mode, expected in (
            ("preflight-fail", "HOLD_PREFLIGHT"),
            ("upload-fail", "HOLD_UPLOAD_FAILED_NO_REPLACEMENT"),
            ("deploy-fail", "HOLD_DEPLOY_FAILED_NO_REPLACEMENT"),
            ("deploy-after-replacement-fail", "HOLD_PARTIAL_DEPLOYMENT"),
        ):
            _, terminal = run_orchestrator(fixture, mode=mode)
            assert terminal["status"] == expected
            assert_orchestrator_zero_counters(terminal)

        _, terminal = run_orchestrator(fixture, interactive=False)
        assert terminal["status"] == "HOLD_INTERACTIVE_AUTHENTICATION_UNAVAILABLE"
        assert_orchestrator_zero_counters(terminal)

        _, terminal = run_orchestrator(fixture)
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert_orchestrator_zero_counters(terminal)

        result, terminal = run_postflight(fixture, "deployed")
        assert result.returncode == 0
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"
        assert_postflight_zero_counters(terminal)

        postflight = load_module("e19_postflight", POSTFLIGHT_PATH)
        captured = StringIO()
        original_run_postflight = postflight.run_postflight
        try:
            postflight.run_postflight = lambda: (_ for _ in ()).throw(ValueError("synthetic fallback"))
            with redirect_stdout(captured):
                returncode = postflight.main()
        finally:
            postflight.run_postflight = original_run_postflight
        fallback = json.loads(captured.getvalue())
        assert returncode == 2
        assert fallback["classification"] == "UNKNOWN_OR_UNSAFE"
        assert_postflight_zero_counters(fallback)

    def e20() -> None:
        result, canonical = run_postflight(fixture, "deployed")
        assert result.returncode == 0
        assert canonical["classification"] == "DEPLOYED_IDENTITY_VERIFIED"
        assert canonical["target_state"]["state"] == "NEW_EXACT"
        assert canonical["backup_state"]["state"] == "OLD_EXACT"
        assert canonical["target_state"]["realpath"] == canonical["target_state"]["path"]
        assert canonical["backup_state"]["realpath"] == canonical["backup_state"]["path"]

        canonical_root = Path(fixture["remote_root"]).resolve()
        alias_root = fixture["base"] / "config-alias"
        alias_root.symlink_to(canonical_root, target_is_directory=True)
        alias_config = alias_root / "config"
        alias_target = alias_config / "mapping.yaml"
        assert alias_target.is_file()
        alias_target_stat = os.lstat(alias_target)
        assert stat.S_ISREG(alias_target_stat.st_mode)
        assert not stat.S_ISLNK(alias_target_stat.st_mode)
        assert os.path.realpath(alias_target) != str(alias_target)

        before = {
            "target": alias_target.read_bytes(),
            "names": sorted(path.name for path in alias_config.iterdir()),
            "alias_is_symlink": alias_root.is_symlink(),
        }
        env = env_for(fixture, interactive=False, root_override=alias_root)
        env["D2_R7B_FAKE_DOCKER_PAYLOAD"] = json.dumps(make_docker_payload(alias_config), sort_keys=True)
        result = subprocess.run([sys.executable, str(POSTFLIGHT_PATH)], cwd=REPO_ROOT, env=env, capture_output=True, check=False)
        terminal = parse_json_output(result)
        after = {
            "target": alias_target.read_bytes(),
            "names": sorted(path.name for path in alias_config.iterdir()),
            "alias_is_symlink": alias_root.is_symlink(),
        }
        assert result.returncode == 2
        assert terminal["classification"] in {"UNKNOWN_OR_UNSAFE", "PARTIAL_DEPLOYMENT"}
        assert terminal["classification"] != "DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["target_state"]["state"] not in {"NEW_EXACT", "OLD_EXACT"}
        assert terminal["backup_state"]["state"] not in {"NEW_EXACT", "OLD_EXACT"}
        assert terminal["upload_temp_state"]["state"] == "ABSENT"
        assert terminal["rollback_temp_state"]["state"] == "ABSENT"
        assert before == after
        assert_postflight_zero_counters(terminal)

    def assert_interruption_fields(terminal: dict[str, Any], *, phase: str, calls: int) -> None:
        required = {
            "task", "endpoint", "status", "phase", "message", "interruption_kind",
            "interruption_source", "auth_state", "phase_started",
            "mutation_capable_phase_started", "child_started", "child_pid",
            "child_reaped", "child_returncode", "child_signal", "phase_exit_codes",
            "phase_exit_code_observed", "REMOTE_CALL_COUNT", "postflight_attempted",
            "postflight_completed", "postflight_call_count", "postflight_terminal",
        }
        missing = required - terminal.keys()
        assert not missing, f"interruption terminal missing {sorted(missing)}"
        assert terminal["phase"] == phase, terminal
        assert terminal["REMOTE_CALL_COUNT"] == calls, terminal
        assert type(terminal["REMOTE_CALL_COUNT"]) is int, terminal
        assert terminal["child_started"] is True, terminal
        assert terminal["child_reaped"] is True, terminal
        assert terminal["phase_exit_code_observed"] is True, terminal
        assert type(terminal["phase_exit_codes"][phase]) is int, terminal
        assert type(terminal["retry_count"]) is int and terminal["retry_count"] == 0
        assert type(terminal["resume_count"]) is int and terminal["resume_count"] == 0
        assert terminal["cleanup_count"] == 0
        assert terminal["rollback_count"] == 0
        assert terminal["restart_count_by_task"] == 0
        assert terminal["activation_count"] == 0

    def e21() -> None:
        result, terminal = run_orchestrator(fixture, mode="preflight-keyboardinterrupt")
        assert result.returncode == 2
        assert_interruption_fields(terminal, phase="REMOTE_PREFLIGHT", calls=1)
        assert terminal["status"].startswith("HOLD")
        assert terminal["interruption_kind"] == "OPERATOR_CANCELLATION"
        assert terminal["mutation_capable_phase_started"] is False
        assert terminal["target_state"]["state"] == "NOT_OBSERVED"
        assert terminal["upload_temp_state"]["state"] == "NOT_OBSERVED"
        assert terminal["backup_state"]["state"] == "NOT_OBSERVED"
        assert terminal["rollback_temp_state"]["state"] == "NOT_OBSERVED"
        assert terminal["postflight_attempted"] is False
        assert terminal["postflight_call_count"] == 0
        assert terminal["retry_count"] == terminal["resume_count"] == 0

    def e22() -> None:
        result, terminal = run_orchestrator(fixture, mode="upload-keyboardinterrupt")
        assert result.returncode == 2
        assert_interruption_fields(terminal, phase="REMOTE_UPLOAD", calls=3)
        assert terminal["interruption_kind"] == "OPERATOR_CANCELLATION"
        assert terminal["mutation_capable_phase_started"] is True
        assert terminal["postflight_attempted"] is True
        assert terminal["postflight_completed"] is True
        assert terminal["postflight_call_count"] == 1
        assert terminal["postflight_terminal"]["phase"] == "REMOTE_POSTFLIGHT"
        assert [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()] == [
            "remote_preflight.py", "remote_upload_exclusive.py", "remote_postflight.py"
        ]
        assert terminal["retry_count"] == terminal["resume_count"] == 0
        assert terminal["cleanup_count"] == terminal["rollback_count"] == 0

    def e23() -> None:
        for mode, expected in (
            ("deploy-before-replacement-interrupt", "UPLOAD_STAGED_NO_REPLACEMENT"),
            ("deploy-after-replacement-interrupt", "DEPLOYED_IDENTITY_VERIFIED"),
        ):
            result, terminal = run_orchestrator(fixture, mode=mode)
            assert result.returncode == 2
            assert_interruption_fields(terminal, phase="REMOTE_DEPLOY", calls=4)
            assert terminal["interruption_kind"] == "OPERATOR_CANCELLATION"
            assert terminal["mutation_capable_phase_started"] is True
            assert terminal["postflight_attempted"] is True
            assert terminal["postflight_completed"] is True
            assert terminal["postflight_call_count"] == 1
            assert terminal["classification"] == expected, terminal
            assert terminal["status"] == "HOLD_DEPLOY_INTERRUPTED", terminal
            assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
            assert terminal["retry_count"] == terminal["resume_count"] == 0
            assert terminal["cleanup_count"] == terminal["rollback_count"] == 0

    def e24() -> None:
        result, terminal = run_orchestrator(fixture, mode="postflight-keyboardinterrupt")
        assert result.returncode == 2
        assert_interruption_fields(terminal, phase="REMOTE_POSTFLIGHT", calls=4)
        assert terminal["interruption_kind"] == "OPERATOR_CANCELLATION", terminal
        assert terminal["postflight_attempted"] is True, terminal
        assert terminal["postflight_completed"] is False, terminal
        assert terminal["postflight_call_count"] == 1, terminal
        assert terminal["classification"] in {"UNKNOWN_OR_UNSAFE", "NOT_OBSERVED"}, terminal
        assert [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()] == [
            "remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"
        ], fixture["log"].read_text()

    def e25() -> None:
        for mode, expected_code, expected_signal in (
            ("preflight-fail", 23, None),
            ("preflight-signal", -signal.SIGTERM, signal.SIGTERM),
            ("preflight-eof", 47, None),
        ):
            result, terminal = run_orchestrator(fixture, mode=mode)
            assert result.returncode == 2
            assert_interruption_fields(terminal, phase="REMOTE_PREFLIGHT", calls=1)
            assert terminal["child_returncode"] == expected_code
            assert terminal["child_signal"] == expected_signal
            if mode == "preflight-eof":
                assert terminal["interruption_kind"] == "EOF"

        for mode, phase, calls, postflight_calls in (
            ("remote_preflight-invalid-json", "REMOTE_PREFLIGHT", 1, 0),
            ("remote_upload_exclusive-invalid-json", "REMOTE_UPLOAD", 3, 1),
            ("remote_deploy-invalid-json", "REMOTE_DEPLOY", 4, 1),
        ):
            result, terminal = run_orchestrator(fixture, mode=mode)
            assert result.returncode == 2, terminal
            assert terminal["phase"] == phase, terminal
            assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED", terminal
            assert terminal["interruption_kind"] is None, terminal
            assert terminal["auth_state"] == "NOT_STARTED", terminal
            assert terminal["REMOTE_CALL_COUNT"] == calls, terminal
            assert terminal["postflight_call_count"] == postflight_calls, terminal

        orch = load_module("e25_orchestrator", ORCH_PATH)
        terminated: list[int] = []

        class NeverReaped:
            pid = 94123
            returncode = None

            def communicate(self, *args, **kwargs):
                raise subprocess.TimeoutExpired(["ssh", "synthetic"], kwargs.get("timeout", 0.01))

            def poll(self):
                return None

        child = NeverReaped()
        original_popen = orch._Popen
        original_terminate = orch._terminate_owned_child
        try:
            orch._Popen = lambda *args, **kwargs: child
            orch._terminate_owned_child = lambda owned: terminated.append(owned.pid)
            runner = orch.PhaseOwnedRunner()
            outcome = runner.run(["ssh", "synthetic"], phase="REMOTE_PREFLIGHT", payload=None)
        finally:
            orch._Popen = original_popen
            orch._terminate_owned_child = original_terminate
        assert outcome["child_started"] is True
        assert outcome["child_reaped"] is False
        assert outcome["child_returncode"] is None
        assert outcome["phase_exit_code_observed"] is False
        assert outcome["status"] == "HOLD_UNKNOWN_REMOTE_STATE"
        assert terminated == [NeverReaped.pid]

    def e26() -> None:
        expected = (
            ("preflight-keyboardinterrupt", "OPERATOR_CANCELLATION"),
            ("preflight-eof", "EOF"),
            ("preflight-password-prompt", "PASSWORD_PROMPT_INTERRUPTED"),
            ("preflight-auth-fail", "AUTHENTICATION_FAILURE"),
            ("preflight-unknown", "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN"),
        )
        for mode, kind in expected:
            result, terminal = run_orchestrator(fixture, mode=mode)
            assert result.returncode == 2
            assert terminal["interruption_kind"] == kind
            assert terminal["auth_state"] in {"NOT_STARTED", "PROMPT_INTERRUPTED", "AUTHENTICATION_FAILED", "UNKNOWN"}
            serialized = json.dumps(terminal, sort_keys=True).lower()
            assert "password:" not in serialized
            assert "permission denied (publickey,password)" not in serialized
            assert "secret" not in serialized
            assert len(fixture["log"].read_text().splitlines()) == 1
        orch_text = ORCH_PATH.read_text(encoding="utf-8").lower()
        assert "password file" not in orch_text
        assert "sshpass" not in orch_text
        assert "credential material" not in orch_text

    def e27() -> None:
        result, terminal = run_orchestrator(fixture, mode="preflight-keyboardinterrupt")
        assert result.returncode == 2
        assert terminal["terminal_source"] == "orchestrator_shared_raw_terminal"
        assert terminal["raw_orchestrator_terminal_available"] is True
        wrapper = {
            "terminal_source": "execution_wrapper_interruption",
            "raw_orchestrator_terminal_available": False,
            "raw_orchestrator_terminal": None,
            "REMOTE_CALL_COUNT": None,
        }
        assert wrapper["terminal_source"] != terminal["terminal_source"]
        assert wrapper["raw_orchestrator_terminal_available"] is False
        assert wrapper["REMOTE_CALL_COUNT"] is None
        assert terminal["REMOTE_CALL_COUNT"] == 1

    def e28() -> None:
        orch = load_module("e28_orchestrator", ORCH_PATH)
        runner = orch.PhaseOwnedRunner()
        outcome = runner.run(
            [sys.executable, "-c", "import time; time.sleep(1.2)"],
            phase="REMOTE_PREFLIGHT",
            payload=None,
        )
        assert outcome["child_started"] is True
        assert outcome["child_reaped"] is True
        assert outcome["child_returncode"] == 0, outcome
        assert outcome["child_signal"] is None, outcome
        assert outcome["interruption_kind"] is None, outcome
        assert outcome["interruption_source"] == "NONE", outcome
        assert outcome["phase_exit_code"] == 0, outcome
        assert outcome["status"] == "OK", outcome
        assert runner.remote_call_count == 1

    def e29() -> None:
        orch = load_module("e29_orchestrator", ORCH_PATH)
        created_runners: list[Any] = []
        received_runners: list[Any] = []
        source_gate_called = False

        original_runner_type = orch.PhaseOwnedRunner
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        original_call_remote = orch._call_remote

        def runner_factory():
            runner = original_runner_type()
            created_runners.append(runner)
            return runner

        def synthetic_source_gate():
            nonlocal source_gate_called
            source_gate_called = True
            return {
                "stage_root": "/private/var/folders/e29-shared-runner",
                "mapping_payload": b"synthetic mapping payload",
            }

        def synthetic_call_remote(helper, *, payload, phase, runner):
            received_runners.append(runner)
            assert phase in {"REMOTE_PREFLIGHT", "REMOTE_UPLOAD"}
            assert runner is created_runners[0]
            child_json = json.dumps(complete_phase_record(phase), sort_keys=True)
            child = runner.run(
                [
                    sys.executable,
                    "-c",
                    f"print({child_json!r})",
                ],
                phase=phase,
                payload=payload,
            )
            assert child["child_returncode"] == 0
            if phase == "REMOTE_UPLOAD":
                raise KeyboardInterrupt()
            return child

        orch.PhaseOwnedRunner = runner_factory
        orch._interactive_auth_available = lambda: True
        orch.local_source_gate = synthetic_source_gate
        orch._call_remote = synthetic_call_remote
        captured = StringIO()
        try:
            with redirect_stdout(captured):
                returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
        finally:
            orch.PhaseOwnedRunner = original_runner_type
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate
            orch._call_remote = original_call_remote
        terminal = json.loads(captured.getvalue())
        assert source_gate_called is True
        assert len(created_runners) == 1
        assert len(received_runners) == 2
        assert received_runners[0] is created_runners[0]
        assert received_runners[1] is created_runners[0]
        assert returncode == 2
        assert terminal["terminal_source"] == "orchestrator_shared_raw_terminal"
        assert terminal["raw_orchestrator_terminal_available"] is True
        assert terminal["REMOTE_CALL_COUNT"] == 2
        assert type(terminal["REMOTE_CALL_COUNT"]) is int
        assert terminal["last_started_phase"] == "REMOTE_UPLOAD"
        assert terminal["mutation_capable_phase_started"] is True
        assert terminal.get("classification") != "NO_MUTATION"
        assert terminal["target_state"]["state"] in {"NOT_OBSERVED", "UNKNOWN_OR_UNSAFE"}
        assert terminal["phase_exit_codes"]["REMOTE_PREFLIGHT"] == 0
        assert terminal["phase_exit_codes"]["REMOTE_UPLOAD"] == 0
        assert "FINAL_TERMINAL" not in terminal["phase_exit_codes"]
        assert_orchestrator_zero_counters(terminal)

    def e30() -> None:
        for args, expected in (
            ([], "DRY_RUN"),
            (["--execute"], "HOLD_REMOTE_EXECUTION_NOT_CONFIRMED"),
            (["--confirm", "D2-R7B-I1-CONFIG-ONLY"], "HOLD_REMOTE_EXECUTION_NOT_CONFIRMED"),
            (["--execute", "--confirm", "wrong"], "HOLD_REMOTE_EXECUTION_NOT_CONFIRMED"),
        ):
            result = subprocess.run([sys.executable, str(ORCH_PATH), *args], cwd=REPO_ROOT, capture_output=True, check=False)
            terminal = parse_json_output(result)
            assert terminal["status"] == expected
            assert terminal["REMOTE_CALL_COUNT"] == 0

        _, terminal = run_orchestrator(fixture, interactive=False)
        assert terminal["status"] == "HOLD_INTERACTIVE_AUTHENTICATION_UNAVAILABLE"
        assert terminal["REMOTE_CALL_COUNT"] == 0

        orch = load_module("e30_orchestrator", ORCH_PATH)
        args = type("Args", (), {"execute": True, "confirm": "D2-R7B-I1-CONFIG-ONLY"})()
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        original_popen = orch._Popen
        try:
            orch._interactive_auth_available = lambda: True
            orch.local_source_gate = lambda: {"stage_root": "/private/var/folders/e30", "mapping_payload": b"synthetic"}
            orch._Popen = lambda *args, **kwargs: (_ for _ in ()).throw(OSError("synthetic create failure"))
            terminal, returncode = orch.execute(args)
        finally:
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate
            orch._Popen = original_popen
        assert returncode == 2
        assert terminal["REMOTE_CALL_COUNT"] == 0
        assert terminal["status"].startswith("HOLD")

        for exception in (orch.ContractError("synthetic local source failure"), KeyboardInterrupt(), EOFError()):
            original_source_gate = orch.local_source_gate
            try:
                orch._interactive_auth_available = lambda: True
                def fail_source(exception=exception):
                    raise exception
                orch.local_source_gate = fail_source
                terminal, returncode = orch.execute(args)
            finally:
                orch._interactive_auth_available = original_auth_available
                orch.local_source_gate = original_source_gate
            assert returncode == 2
            assert terminal["REMOTE_CALL_COUNT"] == 0
            assert terminal["status"].startswith("HOLD")
            assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == (2 if isinstance(exception, orch.ContractError) else None)
            if isinstance(exception, (KeyboardInterrupt, EOFError)):
                assert terminal["phase_exit_code_observed"] is False

    def e31() -> None:
        orch = load_module("e31_orchestrator", ORCH_PATH)
        normal_calls: list[dict[str, Any]] = []

        class NormalChild:
            pid = 93101
            returncode = 0
            stdin = None

            def communicate(self, *args, **kwargs):
                normal_calls.append(dict(kwargs))
                return b"", b""

        original_popen = orch._Popen
        try:
            orch._Popen = lambda *args, **kwargs: NormalChild()
            normal = orch.PhaseOwnedRunner().run(["synthetic"], phase="REMOTE_PREFLIGHT", payload=None)
        finally:
            orch._Popen = original_popen
        assert normal["status"] == "OK"
        assert normal_calls and "timeout" not in normal_calls[0]

        interrupted_calls: list[dict[str, Any]] = []

        class InterruptedChild:
            pid = 93102
            returncode = None
            stdin = None

            def communicate(self, *args, **kwargs):
                interrupted_calls.append(dict(kwargs))
                if len(interrupted_calls) == 1:
                    raise KeyboardInterrupt()
                self.returncode = -signal.SIGTERM
                return b"", b""

        original_popen = orch._Popen
        original_terminate = orch._terminate_owned_child
        try:
            orch._Popen = lambda *args, **kwargs: InterruptedChild()
            orch._terminate_owned_child = lambda child: None
            interrupted = orch.PhaseOwnedRunner().run(["synthetic"], phase="REMOTE_PREFLIGHT", payload=None)
        finally:
            orch._Popen = original_popen
            orch._terminate_owned_child = original_terminate
        assert interrupted["interruption_kind"] == "OPERATOR_CANCELLATION"
        assert len(interrupted_calls) == 2
        assert "timeout" not in interrupted_calls[0]
        assert interrupted_calls[1]["timeout"] == orch.INTERRUPTION_REAP_SECONDS

    def e32() -> None:
        orch = load_module("e32_orchestrator", ORCH_PATH)
        created_runners: list[Any] = []
        received_runners: list[Any] = []
        original_runner_type = orch.PhaseOwnedRunner
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        original_call_remote = orch._call_remote

        def runner_factory():
            runner = original_runner_type()
            created_runners.append(runner)
            return runner

        def synthetic_source_gate():
            return {
                "stage_root": "/private/var/folders/e32-actual-flow",
                "mapping_payload": b"synthetic mapping payload",
            }

        def synthetic_call_remote(helper, *, payload, phase, runner):
            received_runners.append(runner)
            assert phase in {"REMOTE_PREFLIGHT", "REMOTE_UPLOAD"}
            child_json = json.dumps(complete_phase_record(phase), sort_keys=True)
            child = runner.run(
                [sys.executable, "-c", f"print({child_json!r})"],
                phase=phase,
                payload=payload,
            )
            assert child["child_returncode"] == 0
            if phase == "REMOTE_UPLOAD":
                raise KeyboardInterrupt()
            return child

        orch.PhaseOwnedRunner = runner_factory
        orch._interactive_auth_available = lambda: True
        orch.local_source_gate = synthetic_source_gate
        orch._call_remote = synthetic_call_remote
        captured = StringIO()
        try:
            with redirect_stdout(captured):
                returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
        finally:
            orch.PhaseOwnedRunner = original_runner_type
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate
            orch._call_remote = original_call_remote
        terminal = json.loads(captured.getvalue())
        assert len(created_runners) == 1
        assert len(received_runners) == 2
        assert received_runners[0] is created_runners[0]
        assert received_runners[1] is created_runners[0]
        assert returncode == 2
        assert terminal["terminal_source"] == "orchestrator_shared_raw_terminal"
        assert terminal["status"] == "HOLD"
        assert terminal["REMOTE_CALL_COUNT"] == 2
        assert terminal["last_started_phase"] == "REMOTE_UPLOAD"
        assert terminal["mutation_capable_phase_started"] is True
        assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == 0
        assert terminal["phase_exit_codes"]["REMOTE_PREFLIGHT"] == 0
        assert terminal["phase_exit_codes"]["REMOTE_UPLOAD"] == 0
        assert "FINAL_TERMINAL" not in terminal["phase_exit_codes"]
        assert terminal["target_state"]["state"] == "NOT_OBSERVED"
        assert terminal["upload_temp_state"]["state"] == "NOT_OBSERVED"
        assert terminal["backup_state"]["state"] == "NOT_OBSERVED"
        assert terminal["rollback_temp_state"]["state"] == "NOT_OBSERVED"
        assert terminal.get("classification") not in {"NO_MUTATION", "DEPLOYED_IDENTITY_VERIFIED"}
        assert_orchestrator_zero_counters(terminal)

    def e33() -> None:
        orch = load_module("e33_orchestrator", ORCH_PATH)
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        orch._interactive_auth_available = lambda: True
        try:
            for exception, expected_kind in ((KeyboardInterrupt(), "OPERATOR_CANCELLATION"), (EOFError(), "EOF")):
                def interrupted_source(exception=exception):
                    raise exception

                orch.local_source_gate = interrupted_source
                captured = StringIO()
                with redirect_stdout(captured):
                    returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
                terminal = json.loads(captured.getvalue())
                assert returncode == 2
                assert terminal["terminal_source"] == "orchestrator_shared_raw_terminal"
                assert terminal["status"] == "HOLD"
                assert terminal["phase"] == "LOCAL_SOURCE_GATE"
                assert terminal["interruption_kind"] == expected_kind
                assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] is None
                assert terminal["phase_exit_code_observed"] is False
                assert terminal["REMOTE_CALL_COUNT"] == 0
                assert terminal["phase_started"] is True
                assert terminal["target_state"]["state"] == "NOT_OBSERVED"
                assert terminal["mutation_capable_phase_started"] is False
                assert_orchestrator_zero_counters(terminal)
        finally:
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate

    def e34() -> None:
        for emission_exception, expected_kind in ((KeyboardInterrupt(), "OPERATOR_CANCELLATION"), (EOFError(), "EOF")):
            orch = load_module(f"e34_orchestrator_{expected_kind.lower()}", ORCH_PATH)
            created_runners: list[Any] = []
            received_runners: list[Any] = []
            emission_calls: list[dict[str, Any]] = []
            original_runner_type = orch.PhaseOwnedRunner
            original_auth_available = orch._interactive_auth_available
            original_source_gate = orch.local_source_gate
            original_call_remote = orch._call_remote
            original_emit_terminal = orch.emit_terminal

            def runner_factory():
                runner = original_runner_type()
                created_runners.append(runner)
                return runner

            def synthetic_source_gate():
                return {
                    "stage_root": "/private/var/folders/e34-terminal-emission",
                    "mapping_payload": b"synthetic mapping payload",
                }

            def synthetic_call_remote(helper, *, payload, phase, runner):
                received_runners.append(runner)
                assert phase in {"REMOTE_PREFLIGHT", "REMOTE_UPLOAD"}
                child_json = json.dumps(complete_phase_record(phase), sort_keys=True)
                child = runner.run(
                    [sys.executable, "-c", f"print({child_json!r})"],
                    phase=phase,
                    payload=payload,
                )
                assert child["child_returncode"] == 0
                if phase == "REMOTE_UPLOAD":
                    raise KeyboardInterrupt()
                return child

            def interrupt_primary(terminal, *args, **kwargs):
                emission_calls.append(terminal)
                if len(emission_calls) == 1:
                    raise emission_exception
                return original_emit_terminal(terminal, *args, **kwargs)

            orch.PhaseOwnedRunner = runner_factory
            orch._interactive_auth_available = lambda: True
            orch.local_source_gate = synthetic_source_gate
            orch._call_remote = synthetic_call_remote
            orch.emit_terminal = interrupt_primary
            captured = StringIO()
            try:
                with redirect_stdout(captured):
                    returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
            finally:
                orch.PhaseOwnedRunner = original_runner_type
                orch._interactive_auth_available = original_auth_available
                orch.local_source_gate = original_source_gate
                orch._call_remote = original_call_remote
                orch.emit_terminal = original_emit_terminal
            terminal = json.loads(captured.getvalue())
            assert returncode == 2
            assert len(created_runners) == 1
            assert len(received_runners) == 2
            assert len(emission_calls) == 2
            assert emission_calls[1]["terminal_delivery_attempt"] == 2
            assert emission_calls[1]["terminal_delivery_fallback"] is True
            assert emission_calls[1]["terminal_delivery_status"] == "FALLBACK_AFTER_INTERRUPTION"
            assert emission_calls[1]["terminal_emission_interruption_kind"] == expected_kind
            assert terminal["terminal_delivery_attempt"] == 2
            assert terminal["terminal_delivery_fallback"] is True
            assert terminal["terminal_delivery_status"] == "FALLBACK_AFTER_INTERRUPTION"
            assert terminal["terminal_emission_interruption_kind"] == expected_kind
            assert terminal["status"] == "HOLD"
            assert terminal["REMOTE_CALL_COUNT"] == 2
            assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == 0
            assert terminal["phase_exit_codes"]["REMOTE_PREFLIGHT"] == 0
            assert terminal["phase_exit_codes"]["REMOTE_UPLOAD"] == 0
            assert terminal["last_started_phase"] == "REMOTE_UPLOAD"
            assert terminal["mutation_capable_phase_started"] is True
            assert terminal.get("classification") not in {"NO_MUTATION", "DEPLOYED_IDENTITY_VERIFIED"}
            assert terminal["target_state"]["state"] == "NOT_OBSERVED"
            assert terminal["collector_state"]["state"] == "NOT_OBSERVED"
            assert "RUNTIME CONFIG LOAD NOT CLAIMED" not in terminal["message"]
            assert_orchestrator_zero_counters(terminal)

    def e35() -> None:
        orch = load_module("e35_orchestrator", ORCH_PATH)
        emission_calls: list[dict[str, Any]] = []
        original_emit_terminal = orch.emit_terminal

        def fail_every_emission(terminal, *args, **kwargs):
            emission_calls.append(terminal)
            raise KeyboardInterrupt()

        orch.emit_terminal = fail_every_emission
        captured = StringIO()
        try:
            try:
                with redirect_stdout(captured):
                    orch.main([])
            except orch.TerminalDeliveryError as exc:
                failure = exc
            else:
                raise AssertionError("terminal delivery unexpectedly escaped without explicit failure")
        finally:
            orch.emit_terminal = original_emit_terminal
        assert len(emission_calls) == 2
        assert failure.attempts == 2
        assert failure.delivery_state == "FAILED_AFTER_FALLBACK"
        assert failure.terminal["status"] == "HOLD"
        assert failure.terminal["terminal_delivery_attempt"] == 2
        assert failure.terminal["terminal_delivery_fallback"] is True
        assert failure.terminal["terminal_delivery_status"] == "FALLBACK_AFTER_INTERRUPTION"
        assert failure.terminal["terminal_delivery_authoritative"] is False
        assert failure.terminal["REMOTE_CALL_COUNT"] == 0
        assert failure.terminal["phase_exit_codes"] == {}
        assert_orchestrator_zero_counters(failure.terminal)
        assert captured.getvalue() == ""

    def e36() -> None:
        """A partial primary write must leave one parseable authoritative fallback."""
        orch = load_module("e36_orchestrator", ORCH_PATH)
        args = type("Args", (), {"execute": True, "confirm": "D2-R7B-I1-CONFIG-ONLY"})()
        created_runners: list[Any] = []
        received_runners: list[Any] = []
        original_runner_type = orch.PhaseOwnedRunner
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        original_call_remote = orch._call_remote
        flow = "direct_execute"

        def runner_factory():
            runner = original_runner_type()
            created_runners.append(runner)
            return runner

        def synthetic_source_gate():
            return {
                "stage_root": "/private/var/folders/e36-actual-flow",
                "mapping_payload": b"synthetic mapping payload",
            }

        def synthetic_call_remote(helper, *, payload, phase, runner):
            received_runners.append(runner)
            if phase == "REMOTE_POSTFLIGHT":
                child_payload = {
                    "status": "HOLD",
                    "phase": "REMOTE_POSTFLIGHT",
                    "classification": "UNKNOWN_OR_UNSAFE",
                    "target_state": {"state": "NOT_OBSERVED"},
                    "upload_temp_state": {"state": "NOT_OBSERVED"},
                    "backup_state": {"state": "NOT_OBSERVED"},
                    "rollback_temp_state": {"state": "NOT_OBSERVED"},
                    "collector_state": {"state": "NOT_OBSERVED"},
                }
            else:
                child_payload = complete_phase_record(phase)
            child_json = json.dumps(child_payload, sort_keys=True)
            child = runner.run(
                [sys.executable, "-c", f"print({child_json!r})"],
                phase=phase,
                payload=payload,
            )
            assert child["child_returncode"] == 0
            if flow == "main_partial_primary" and phase == "REMOTE_UPLOAD":
                raise KeyboardInterrupt()
            return child

        orch.PhaseOwnedRunner = runner_factory
        orch._interactive_auth_available = lambda: True
        orch.local_source_gate = synthetic_source_gate
        orch._call_remote = synthetic_call_remote
        try:
            direct_terminal, direct_returncode = orch.execute(args)
            assert direct_returncode == 2
            assert direct_terminal["REMOTE_CALL_COUNT"] == 4
            assert direct_terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == 0

            flow = "main_partial_primary"
            captured = FaultingTextStream("PARTIAL_JSON_BODY")
            with redirect_stdout(captured):
                returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
        finally:
            orch.PhaseOwnedRunner = original_runner_type
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate
            orch._call_remote = original_call_remote

        assert captured.first_prefix.startswith("{")
        assert len(captured.first_prefix) < len(captured.getvalue())
        records = parse_complete_ndjson_records(captured.getvalue())
        assert records, f"old source stable RED: valid JSON terminal records={len(records)} raw={captured.getvalue()!r}"
        authoritative = [
            record for record in records
            if record.get("terminal_delivery_authoritative") is True
        ]
        assert len(authoritative) == 1, records
        terminal = max(authoritative, key=lambda record: record["terminal_delivery_attempt"])
        assert orch.select_authoritative_terminal(records) == terminal
        assert returncode == 2
        assert terminal["terminal_delivery_attempt"] == 2
        assert terminal["terminal_delivery_fallback"] is True
        assert terminal["terminal_delivery_status"] == "FALLBACK_AFTER_INTERRUPTION"
        assert terminal["terminal_delivery_authoritative"] is True
        assert terminal["terminal_delivery_framing"] == "NDJSON"
        assert terminal["terminal_primary_delivery_interrupted"] is True
        assert terminal["terminal_stream_prefix_may_be_partial"] is True
        assert terminal["status"] == "HOLD"
        assert terminal["REMOTE_CALL_COUNT"] == 2
        assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == 0
        assert terminal["phase_exit_codes"]["REMOTE_PREFLIGHT"] == 0
        assert terminal["phase_exit_codes"]["REMOTE_UPLOAD"] == 0
        assert terminal["last_started_phase"] == "REMOTE_UPLOAD"
        assert terminal["mutation_capable_phase_started"] is True
        assert terminal.get("classification") not in {"NO_MUTATION", "DEPLOYED_IDENTITY_VERIFIED"}
        assert "NO_MUTATION" not in json.dumps(terminal, sort_keys=True)
        assert "DEPLOYED_IDENTITY_VERIFIED" not in json.dumps(terminal, sort_keys=True)
        assert type(terminal["child_started"]) is bool
        assert type(terminal["child_reaped"]) is bool
        assert_orchestrator_zero_counters(terminal)
        assert len(created_runners) == 2
        assert received_runners[-2] is created_runners[-1]
        assert received_runners[-1] is created_runners[-1]

    def e37() -> None:
        """Primary body and body-before-newline faults both recover with two attempts."""
        for fault_point in ("PARTIAL_JSON_BODY", "COMPLETE_JSON_BEFORE_NEWLINE"):
            orch = load_module(f"e37_orchestrator_{fault_point.lower()}", ORCH_PATH)
            original_auth_available = orch._interactive_auth_available
            original_source_gate = orch.local_source_gate
            original_call_remote = orch._call_remote

            def synthetic_source_gate():
                return {
                    "stage_root": f"/private/var/folders/e37-{fault_point.lower()}",
                    "mapping_payload": b"synthetic mapping payload",
                }

            def synthetic_call_remote(helper, *, payload, phase, runner):
                child_json = json.dumps(complete_phase_record(phase), sort_keys=True)
                child = runner.run(
                    [sys.executable, "-c", f"print({child_json!r})"],
                    phase=phase,
                    payload=payload,
                )
                assert child["child_returncode"] == 0
                if phase == "REMOTE_UPLOAD":
                    raise KeyboardInterrupt()
                return child

            orch._interactive_auth_available = lambda: True
            orch.local_source_gate = synthetic_source_gate
            orch._call_remote = synthetic_call_remote
            captured = FaultingTextStream(fault_point)
            try:
                with redirect_stdout(captured):
                    returncode = orch.main(["--execute", "--confirm", "D2-R7B-I1-CONFIG-ONLY"])
            finally:
                orch._interactive_auth_available = original_auth_available
                orch.local_source_gate = original_source_gate
                orch._call_remote = original_call_remote

            records = parse_complete_ndjson_records(captured.getvalue())
            assert returncode == 2
            assert len(records) >= 1, f"{fault_point}: {captured.getvalue()!r}"
            assert captured.json_write_calls == 2, captured.getvalue()
            assert captured.flush_calls >= 1
            authoritative = [
                record for record in records
                if record.get("terminal_delivery_authoritative") is True
            ]
            assert len(authoritative) >= 1, records
            terminal = max(authoritative, key=lambda record: record["terminal_delivery_attempt"])
            assert orch.select_authoritative_terminal(records) == terminal
            assert terminal["terminal_delivery_attempt"] == 2
            assert terminal["terminal_delivery_fallback"] is True
            assert terminal["terminal_delivery_framing"] == "NDJSON"
            assert terminal["terminal_delivery_authoritative"] is True
            assert terminal["status"] == "HOLD"
            assert_orchestrator_zero_counters(terminal)

    def e38() -> None:
        """Local source success, contract failure and interruption freeze observation semantics."""
        orch = load_module("e38_orchestrator", ORCH_PATH)
        args = type("Args", (), {"execute": True, "confirm": "D2-R7B-I1-CONFIG-ONLY"})()
        original_auth_available = orch._interactive_auth_available
        original_source_gate = orch.local_source_gate
        original_call_remote = orch._call_remote

        orch._interactive_auth_available = lambda: True

        def synthetic_success_source_gate():
            return {
                "stage_root": "/private/var/folders/e38-success",
                "mapping_payload": b"synthetic mapping payload",
            }

        def synthetic_success_call_remote(helper, *, payload, phase, runner):
            value = complete_phase_record(phase)
            child_json = json.dumps(value, sort_keys=True)
            return runner.run(
                [sys.executable, "-c", f"print({child_json!r})"],
                phase=phase,
                payload=payload,
            )

        try:
            orch.local_source_gate = synthetic_success_source_gate
            orch._call_remote = synthetic_success_call_remote
            success, success_code = orch.execute(args)
            assert success_code == 0
            assert success["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == 0
            assert success["phase_exit_code_observed"] is True
            assert success["REMOTE_CALL_COUNT"] == 4

            for exception, expected_code, expected_observed in (
                (orch.ContractError("synthetic local source failure"), 2, True),
                (OSError("synthetic local source failure"), 2, True),
                (ValueError("synthetic local source failure"), 2, True),
                (subprocess.SubprocessError("synthetic local source failure"), 2, True),
                (KeyboardInterrupt(), None, False),
                (EOFError(), None, False),
            ):
                def fail_source(exception=exception):
                    raise exception

                orch.local_source_gate = fail_source
                orch._call_remote = lambda **kwargs: (_ for _ in ()).throw(AssertionError("remote call occurred"))
                terminal, returncode = orch.execute(args, runner=orch.PhaseOwnedRunner())
                assert returncode == 2
                assert terminal["phase"] == "LOCAL_SOURCE_GATE"
                assert terminal["phase_exit_codes"]["LOCAL_SOURCE_GATE"] == expected_code
                assert terminal["phase_exit_code_observed"] is expected_observed
                assert terminal["REMOTE_CALL_COUNT"] == 0
                assert terminal["status"] == ("HOLD" if expected_code is None else "HOLD_LOCAL_SOURCE")
        finally:
            orch._interactive_auth_available = original_auth_available
            orch.local_source_gate = original_source_gate
            orch._call_remote = original_call_remote

    def e41() -> None:
        result, terminal = run_orchestrator(fixture)
        records = [json.loads(line) for line in fixture["log"].read_text().splitlines()]
        upload = next(item for item in records if item["phase"] == "remote_upload_exclusive.py")
        assert result.returncode == 0
        assert upload["source_sha256"] == hashlib.sha256((P2_DIR / "remote_upload_exclusive.py").read_bytes()).hexdigest()
        assert terminal["phase_exit_codes"]["REMOTE_UPLOAD"] == 0
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["interruption_source"] == "NONE"

    def e42() -> None:
        result, terminal = run_orchestrator(fixture)
        records = [json.loads(line) for line in fixture["log"].read_text().splitlines()]
        deploy = next(item for item in records if item["phase"] == "remote_deploy.py")
        assert result.returncode == 0
        assert deploy["source_sha256"] == hashlib.sha256((P2_DIR / "remote_deploy.py").read_bytes()).hexdigest()
        assert terminal["phase_exit_codes"]["REMOTE_DEPLOY"] == 0
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["interruption_source"] == "NONE"

    def e43() -> None:
        result, terminal = run_orchestrator(fixture)
        phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
        assert result.returncode == 0
        assert phases == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"]
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["REMOTE_CALL_COUNT"] == 4
        assert all(terminal["phase_exit_codes"][phase] == 0 for phase in ("LOCAL_SOURCE_GATE", "REMOTE_PREFLIGHT", "REMOTE_UPLOAD", "REMOTE_DEPLOY", "REMOTE_POSTFLIGHT"))

    def e44() -> None:
        suffixes = ("empty", "legacy-text", "malformed-json", "multiple-json", "json-list", "json-scalar", "json-trailing-text")
        for phase_prefix, phase, expected_phases in (
            ("remote_upload_exclusive", "REMOTE_UPLOAD", ["remote_preflight.py", "remote_upload_exclusive.py", "remote_postflight.py"]),
            ("remote_deploy", "REMOTE_DEPLOY", ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"]),
        ):
            for suffix in suffixes:
                result, terminal = run_orchestrator(fixture, mode=f"{phase_prefix}-invalid-{suffix}")
                phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
                assert result.returncode == 2
                assert terminal["phase"] == phase
                assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
                assert terminal["interruption_source"] == "INVALID_CHILD_JSON"
                assert terminal["REMOTE_CALL_COUNT"] == (3 if phase == "REMOTE_UPLOAD" else 4)
                assert phases == expected_phases

    def e45() -> None:
        reset_remote(fixture)
        upload = load_module("e45_upload_helper", P2_DIR / "remote_upload_exclusive.py")
        upload.PARENT_PATH = str(fixture["config_dir"])
        upload.UPLOAD_TEMP_PATH = str(fixture["upload"])
        upload.EXPECTED_OWNER = fixture["owner"]
        upload.EXPECTED_GROUP = fixture["group"]
        upload.EXPECTED_PARENT_DEVICE = fixture["device"]
        upload.EXPECTED_FILESYSTEM = fixture["filesystem"]
        upload._filesystem_type = lambda _path, *, pass_fds=(): fixture["filesystem"]
        upload_code, upload_stdout, upload_stderr = invoke_persisted_main(upload, payload=b"invalid-payload")
        assert upload_code == 2
        assert upload_stdout == b""
        assert upload_stderr.startswith(b"HOLD / ")

        reset_remote(fixture)
        deploy = load_module("e45_deploy_helper", P2_DIR / "remote_deploy.py")
        deploy.PARENT_PATH = str(fixture["config_dir"])
        deploy.TARGET_PATH = str(fixture["target"])
        deploy.UPLOAD_TEMP_PATH = str(fixture["upload"])
        deploy.BACKUP_PATH = str(fixture["backup"])
        deploy.EXPECTED_OWNER = fixture["owner"]
        deploy.EXPECTED_GROUP = fixture["group"]
        deploy.EXPECTED_TARGET_DEVICE = fixture["device"]
        deploy.EXPECTED_TARGET_INODE = fixture["target"].stat().st_ino
        deploy.EXPECTED_OLD_BYTES = EXPECTED_OLD_BYTES
        deploy.EXPECTED_OLD_SHA256 = EXPECTED_OLD_SHA256
        deploy.EXPECTED_FILESYSTEM = fixture["filesystem"]
        deploy._filesystem_type = lambda _path: fixture["filesystem"]
        deploy_code, deploy_stdout, deploy_stderr = invoke_persisted_main(deploy)
        assert deploy_code == 2
        assert deploy_stdout == b""
        assert deploy_stderr.startswith(b"HOLD / NO WRITE: ")

        for mode, expected_phases in (
            ("upload-helper-failure", ["remote_preflight.py", "remote_upload_exclusive.py", "remote_postflight.py"]),
            ("deploy-helper-failure", ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"]),
        ):
            result, terminal = run_orchestrator(fixture, mode=mode)
            phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
            assert result.returncode == 2
            assert terminal["status"].startswith("HOLD")
            assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
            assert terminal["REMOTE_CALL_COUNT"] == len(expected_phases)
            assert phases == expected_phases
            assert terminal["retry_count"] == terminal["resume_count"] == 0
            assert terminal["cleanup_count"] == terminal["rollback_count"] == terminal["activation_count"] == 0

    def e46() -> None:
        """Complete JSON objects cannot authorize upload without valid preflight evidence."""
        for variant in ("empty-object", "wrong-status", "missing-field", "additional-field"):
            result, terminal = run_orchestrator(fixture, mode=f"preflight-contract-{variant}")
            phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
            assert result.returncode == 2, variant
            assert phases == ["remote_preflight.py"], (variant, phases)
            assert terminal["status"] == "HOLD_PREFLIGHT_EVIDENCE_INVALID", (variant, terminal)
            assert terminal["phase"] == "REMOTE_PREFLIGHT"
            assert terminal["child_returncode"] == 0
            assert terminal["phase_evidence_valid"] is False
            assert terminal["phase_evidence_error"] == "INVALID_PREFLIGHT_SCHEMA"
            assert terminal["interruption_kind"] is None
            assert terminal["auth_state"] == "NOT_STARTED"
            assert terminal["REMOTE_CALL_COUNT"] == 1
            assert terminal["mutation_capable_phase_started"] is False

    def e47() -> None:
        """Invalid upload evidence cannot authorize deploy and gets one postflight at most."""
        variants = (
            "empty-object", "wrong-phase", "wrong-status", "missing-identity",
            "additional-field", "wrong-path", "wrong-hash", "wrong-bytes", "wrong-mode",
        )
        for variant in variants:
            result, terminal = run_orchestrator(fixture, mode=f"upload-contract-{variant}")
            phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
            assert result.returncode == 2, variant
            assert phases == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_postflight.py"], (variant, phases)
            assert terminal["status"] == "HOLD_UPLOAD_EVIDENCE_INVALID", (variant, terminal)
            assert terminal["phase"] == "REMOTE_UPLOAD"
            assert terminal["child_returncode"] == 0
            assert terminal["phase_evidence_valid"] is False
            assert terminal["phase_evidence_error"] == "INVALID_UPLOAD_SCHEMA"
            assert terminal["interruption_kind"] is None
            assert terminal["auth_state"] == "NOT_STARTED"
            assert terminal["REMOTE_CALL_COUNT"] == 3
            assert terminal["postflight_call_count"] == 1

    def e48() -> None:
        """Invalid deploy evidence and cross-phase inode mismatches cannot authorize PASS."""
        variants = (
            "wrong-phase", "wrong-status", "wrong-operation", "missing-nested-field",
            "additional-nested-field", "upload-source-inode-mismatch", "source-target-inode-mismatch",
        )
        for variant in variants:
            result, terminal = run_orchestrator(fixture, mode=f"deploy-contract-{variant}")
            phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
            assert result.returncode == 2, variant
            assert phases == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"], (variant, phases)
            assert terminal["status"] == "HOLD_DEPLOY_EVIDENCE_INVALID", (variant, terminal)
            assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
            assert terminal["phase"] == "REMOTE_DEPLOY"
            assert terminal["phase_evidence_valid"] is False
            expected_error = "CROSS_PHASE_IDENTITY_MISMATCH" if variant in {
                "upload-source-inode-mismatch", "source-target-inode-mismatch"
            } else "INVALID_DEPLOY_SCHEMA"
            assert terminal["phase_evidence_error"] == expected_error, (variant, terminal)
            assert terminal["REMOTE_CALL_COUNT"] == 4
            assert terminal["postflight_call_count"] == 1
            assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"

    def e49() -> None:
        """Incomplete or semantically invalid postflight records cannot authorize final PASS."""
        variants = (
            "empty-object", "minimal-spoof", "wrong-status", "missing-state-object",
            "additional-field", "lifecycle-nonzero",
        )
        for variant in variants:
            result, terminal = run_orchestrator(fixture, mode=f"postflight-contract-{variant}")
            phases = [json.loads(line)["phase"] for line in fixture["log"].read_text().splitlines()]
            assert result.returncode == 2, variant
            assert phases == ["remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"], (variant, phases)
            assert terminal["status"] == "HOLD_POSTFLIGHT_EVIDENCE_INVALID", (variant, terminal)
            assert terminal["status"] != "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
            assert terminal["phase"] == "REMOTE_POSTFLIGHT"
            assert terminal["phase_evidence_valid"] is False
            assert terminal["phase_evidence_error"] == "INVALID_POSTFLIGHT_SCHEMA"
            assert terminal["REMOTE_CALL_COUNT"] == 4
            assert terminal["postflight_call_count"] == 1

    def e50() -> None:
        """All four actual persisted helper outputs retain the exact success path."""
        result, terminal = run_orchestrator(fixture)
        records = [json.loads(line) for line in fixture["log"].read_text().splitlines()]
        assert result.returncode == 0
        assert [record["phase"] for record in records] == [
            "remote_preflight.py", "remote_upload_exclusive.py", "remote_deploy.py", "remote_postflight.py"
        ]
        for record in records:
            artifact = next(path for path in MANIFEST_BOUND.values() if path.name == record["phase"])
            assert record["source_sha256"] == hashlib.sha256(artifact.read_bytes()).hexdigest()
        assert terminal["status"] == "CONFIG_DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["classification"] == "DEPLOYED_IDENTITY_VERIFIED"
        assert terminal["phase_evidence_valid"] is True
        assert terminal["phase_evidence_error"] is None
        assert terminal["REMOTE_CALL_COUNT"] == 4
        assert terminal["postflight_call_count"] == 1
        assert terminal["message"] == "RUNTIME CONFIG LOAD NOT CLAIMED"

    def e39() -> None:
        assert_persisted_loader_semantics(load_module, "d2_r7b_p2_r3_e39")

    def e40() -> None:
        assert sys.dont_write_bytecode is False
        assert sys.pycache_prefix is None
        assert repository_cache_snapshot() == repository_cache_before

    for label, fn in (("E1", e1), ("E2", e2), ("E3", e3), ("E4", e4), ("E5", e5), ("E6", e6), ("E7", e7), ("E8", e8), ("E9", e9), ("E10", e10), ("E11", e11), ("E12", e12), ("E13", e13), ("E14", e14), ("E15", e15), ("E16", e16), ("E17", e17), ("E18", e18), ("E19", e19), ("E20", e20), ("E21", e21), ("E22", e22), ("E23", e23), ("E24", e24), ("E25", e25), ("E26", e26), ("E27", e27), ("E28", e28), ("E29", e29), ("E30", e30), ("E31", e31), ("E32", e32), ("E33", e33), ("E34", e34), ("E35", e35), ("E36", e36), ("E37", e37), ("E38", e38), ("E39", e39), ("E40", e40), ("E41", e41), ("E42", e42), ("E43", e43), ("E44", e44), ("E45", e45), ("E46", e46), ("E47", e47), ("E48", e48), ("E49", e49), ("E50", e50)):
        case(label, fn)
    print(f"SYNTHETIC_ROOT={fixture['base']}")
    print(f"LOCAL_STAGE_PARENT={fixture['base'] / 'local-stage-parent'}")
    for retained in RETAINED_ROOTS:
        print(f"RETAINED_ROOT={retained}")
    print(f"E1-E50: {'PASS' if all(results) and len(results) == 50 else 'FAIL'} {sum(results)}/{len(results)}")
    return 0 if all(results) and len(results) == 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
