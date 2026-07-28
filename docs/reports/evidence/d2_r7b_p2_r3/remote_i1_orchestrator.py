#!/usr/bin/env python3
"""Local-only, default-safe D2-R7B I1 execution contract orchestrator."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shlex
import signal
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
P2_DIR = REPO_ROOT / "docs/reports/evidence/d2_r7b_p2_r2"
LOCAL_MATERIALIZER = P2_DIR / "local_materialization.sh"
MANIFEST_PATH = ARTIFACT_DIR / "manifest.sha256"
TRANSPORT_ENDPOINT = "mari@10.0.0.217"
CONFIRMATION_TOKEN = "D2-R7B-I1-CONFIG-ONLY"
EXPECTED_BRANCH = "main"
EXPECTED_COMMIT = "8de5edbb504538a233abbcc80102cb714c9cee65"
EXPECTED_BLOB = "b46a637f23c761d0a4c3fe048b3b7480a3dec2ce"
EXPECTED_NEW_BYTES = 7112
EXPECTED_NEW_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
EXPECTED_OLD_BYTES = 5935
EXPECTED_OLD_SHA256 = "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"
EXPECTED_NEW_FILE = "config/mapping.yaml"
EXPECTED_HOSTNAME = "Pi-5b-Li"
EXPECTED_PRINCIPAL = "mari"
EXPECTED_OWNER = "mari"
EXPECTED_GROUP = "mari"
EXPECTED_DEVICE = 2050
EXPECTED_TARGET_INODE = 550698
EXPECTED_FILESYSTEM = "ext4"
EXPECTED_FILE_MODE = "0644"

HELPERS = {
    "remote_preflight": P2_DIR / "remote_preflight.py",
    "remote_upload": P2_DIR / "remote_upload_exclusive.py",
    "remote_deploy": P2_DIR / "remote_deploy.py",
    "remote_postflight": ARTIFACT_DIR / "remote_postflight.py",
}
MANIFEST_BOUND = {
    "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh": P2_DIR / "local_materialization.sh",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py": P2_DIR / "remote_preflight.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py": P2_DIR / "remote_upload_exclusive.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py": P2_DIR / "remote_deploy.py",
    "docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py": P2_DIR / "remote_rollback.py",
    "docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py": P2_DIR / "test_d2_r7b_contract.py",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py": ARTIFACT_DIR / "remote_i1_orchestrator.py",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py": ARTIFACT_DIR / "remote_postflight.py",
    "docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py": ARTIFACT_DIR / "test_d2_r7b_execution_contract.py",
}
REMOTE_PATHS = {
    "target": "/opt/edge-mes-demo/config/mapping.yaml",
    "upload_temp": "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb",
    "backup": "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
    "rollback_temp": "/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml",
}


class ContractError(RuntimeError):
    pass


class TerminalDeliveryError(RuntimeError):
    """Terminal output was interrupted and its single fallback also failed."""

    def __init__(self, message: str, *, terminal: dict[str, Any], attempts: int) -> None:
        super().__init__(message)
        self.terminal = terminal
        self.attempts = attempts
        self.delivery_state = "FAILED_AFTER_FALLBACK"


def build_remote_command(helper_bytes: bytes, helper_name: str) -> str:
    """Return one SSH command string; helper bytes never use SSH stdin."""
    encoded = base64.b64encode(helper_bytes).decode("ascii")
    bootstrap = f"import base64; exec(compile(base64.b64decode('{encoded}'), {helper_name!r}, 'exec'))"
    return "python3 -c " + shlex.quote(bootstrap)


def _run_git(*args: str) -> str:
    result = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ContractError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def verify_local_baseline() -> dict[str, Any]:
    branch = _run_git("branch", "--show-current")
    head = _run_git("rev-parse", "HEAD")
    origin = _run_git("rev-parse", "origin/main")
    ahead_behind = _run_git("rev-list", "--left-right", "--count", "HEAD...origin/main").split()
    cached = _run_git("diff", "--cached", "--name-only")
    mapping_clean = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--quiet", "--", EXPECTED_NEW_FILE],
        check=False,
    ).returncode == 0
    if branch != EXPECTED_BRANCH or head != EXPECTED_COMMIT or origin != EXPECTED_COMMIT or ahead_behind != ["0", "0"] or cached or not mapping_clean:
        raise ContractError(
            f"baseline drift branch={branch!r} head={head!r} origin={origin!r} ahead_behind={ahead_behind!r} cached={cached!r} mapping_clean={mapping_clean}"
        )
    return {
        "branch": branch,
        "head": head,
        "origin_main": origin,
        "ahead": int(ahead_behind[0]),
        "behind": int(ahead_behind[1]),
        "cached": [],
    }


def verify_composite_manifest(repo_root: Path = REPO_ROOT, manifest_path: Path | None = None) -> dict[str, Any]:
    path = MANIFEST_PATH if manifest_path is None else Path(manifest_path)
    expected = sorted(MANIFEST_BOUND)
    if not path.is_file() or path.is_symlink():
        raise ContractError(f"composite manifest missing or unsafe: {path}")
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line:
            continue
        if "  " not in line:
            raise ContractError(f"manifest line {line_number} is not standard two-space format")
        digest, relative = line.split("  ", 1)
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest) or relative not in MANIFEST_BOUND:
            raise ContractError(f"manifest line {line_number} has an unexpected identity or path")
        records.append({"path": relative, "expected_sha256": digest})
    if [item["path"] for item in records] != expected:
        raise ContractError("composite manifest paths are not the stable nine-file sort")
    for item in records:
        source = repo_root / item["path"]
        resolved = source.resolve()
        if source.is_symlink() or resolved != source or not source.is_file():
            raise ContractError(f"manifest source is missing or unsafe: {item['path']}")
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        item["actual_sha256"] = actual
        item["status"] = "OK" if actual == item["expected_sha256"] else "DRIFT"
        if item["status"] != "OK":
            raise ContractError(f"manifest source drift: {item['path']}")
    return {"ok": True, "count": len(records), "entries": records, "path": str(path)}


def _parse_key_values(stdout: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key] = value
    return fields


def _check_materialized(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ContractError(f"materialized mapping is not regular/non-symlink: {path}")
    realpath = Path(os.path.realpath(path))
    if realpath != path:
        raise ContractError(f"materialized mapping realpath drift: {realpath}")
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    blob = _run_git("hash-object", str(path))
    if len(payload) != EXPECTED_NEW_BYTES or digest != EXPECTED_NEW_SHA256 or blob != EXPECTED_BLOB:
        raise ContractError(f"materialized mapping identity drift bytes={len(payload)} sha256={digest} blob={blob}")
    return {
        "path": str(path),
        "realpath": str(realpath),
        "bytes": len(payload),
        "sha256": digest,
        "blob": blob,
    }


def local_source_gate() -> dict[str, Any]:
    baseline = verify_local_baseline()
    manifest_path = Path(os.environ.get("D2_R7B_MANIFEST_PATH", str(MANIFEST_PATH)))
    manifest = verify_composite_manifest(REPO_ROOT, manifest_path)
    result = subprocess.run(
        [str(LOCAL_MATERIALIZER)],
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ContractError(f"local materialization failed exit={result.returncode}: {result.stderr.strip()}")
    fields = _parse_key_values(result.stdout)
    required = {"TEMP_ROOT", "MATERIALIZED_PATH", "BLOB", "BYTES", "SHA256"}
    if not required.issubset(fields):
        raise ContractError(f"local materialization output missing {sorted(required - fields.keys())}")
    materialized = Path(fields["MATERIALIZED_PATH"])
    identity = _check_materialized(materialized)
    if fields["BLOB"] != EXPECTED_BLOB or fields["BYTES"] != str(EXPECTED_NEW_BYTES) or fields["SHA256"] != EXPECTED_NEW_SHA256:
        raise ContractError("local materialization reported identity drift")
    helper_sources = {
        name: {
            "path": str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
        for name, path in HELPERS.items()
    }
    return {
        "baseline": baseline,
        "manifest": manifest,
        "helper_sources": helper_sources,
        "mapping": identity,
        "mapping_payload": materialized.read_bytes(),
        "stage_root": fields["TEMP_ROOT"],
        "no_auto_cleanup": True,
    }


INTERRUPTION_REAP_SECONDS = 1.0
INTERRUPTION_KINDS = {
    "OPERATOR_CANCELLATION",
    "EOF",
    "PASSWORD_PROMPT_INTERRUPTED",
    "AUTHENTICATION_FAILURE",
    "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN",
}
_Popen = subprocess.Popen


def _not_observed(path: str) -> dict[str, Any]:
    return {"path": path, "state": "NOT_OBSERVED"}


def classify_interruption(*, exception: BaseException | None, returncode: int | None, stdout: bytes = b"", stderr: bytes = b"") -> str | None:
    """Classify only safe local evidence; never retain prompt or credential text."""
    transcript = b" ".join((stdout, stderr)).decode("utf-8", errors="replace").lower()
    if isinstance(exception, EOFError) or " eof" in f" {transcript}" or transcript.startswith("eof"):
        return "EOF"
    if isinstance(exception, KeyboardInterrupt):
        if "password:" in transcript or "password prompt" in transcript:
            return "PASSWORD_PROMPT_INTERRUPTED"
        return "OPERATOR_CANCELLATION"
    if returncode == 255 and any(marker in transcript for marker in ("permission denied", "publickey", "authentication failed")):
        return "AUTHENTICATION_FAILURE"
    if returncode == 255 or exception is not None:
        return "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN"
    return None


def _auth_state(interruption_kind: str | None) -> str:
    if interruption_kind == "PASSWORD_PROMPT_INTERRUPTED":
        return "PROMPT_INTERRUPTED"
    if interruption_kind == "AUTHENTICATION_FAILURE":
        return "AUTHENTICATION_FAILED"
    if interruption_kind == "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN":
        return "UNKNOWN"
    if interruption_kind in {"OPERATOR_CANCELLATION", "EOF"}:
        return "UNKNOWN"
    return "NOT_STARTED"


def _signal_owned_process_group(child: Any, signum: int) -> None:
    """Signal only the process group created by this runner's new session."""
    pid = getattr(child, "pid", None)
    if type(pid) is not int or pid <= 0:
        return
    try:
        os.killpg(pid, signum)
    except (OSError, ProcessLookupError):
        pass


def _terminate_owned_child(child: Any) -> None:
    _signal_owned_process_group(child, signal.SIGTERM)


def _close_owned_stdin(child: Any) -> bool:
    stream = getattr(child, "stdin", None)
    if stream is None:
        return False
    try:
        stream.close()
    except (OSError, ValueError):
        pass
    return True


def _reap_owned_child(child: Any) -> tuple[bool, bytes, bytes, int | None]:
    try:
        stdout, stderr = child.communicate(timeout=INTERRUPTION_REAP_SECONDS)
        return True, stdout or b"", stderr or b"", child.returncode
    except subprocess.TimeoutExpired:
        _signal_owned_process_group(child, signal.SIGKILL)
        try:
            stdout, stderr = child.communicate(timeout=INTERRUPTION_REAP_SECONDS)
            return True, stdout or b"", stderr or b"", child.returncode
        except subprocess.TimeoutExpired:
            return False, b"", b"", None
        except (OSError, subprocess.SubprocessError):
            return False, b"", b"", None
    except (OSError, subprocess.SubprocessError):
        return False, b"", b"", None


class PhaseOwnedRunner:
    """Own one SSH child from creation through bounded drain and reap."""

    def __init__(self) -> None:
        self.remote_call_count = 0
        self.last_started_phase: str | None = None
        self.mutation_capable_phase_started = False
        self.last_child_lifecycle: dict[str, Any] | None = None
        self.phase_exit_codes: dict[str, int | None] = {}

    def record_phase(self, phase: str, phase_exit_code: int | None) -> None:
        if phase == "FINAL_TERMINAL":
            raise ValueError("FINAL_TERMINAL is not an execution phase")
        self.phase_exit_codes[phase] = phase_exit_code

    def _record_outcome(self, outcome: dict[str, Any]) -> dict[str, Any]:
        phase = outcome["phase"]
        self.phase_exit_codes[phase] = outcome.get("phase_exit_code")
        if outcome.get("child_started"):
            self.last_started_phase = phase
            if phase in {"REMOTE_UPLOAD", "REMOTE_DEPLOY"}:
                self.mutation_capable_phase_started = True
        self.last_child_lifecycle = {
            key: outcome.get(key)
            for key in (
                "phase", "child_started", "child_pid", "child_reaped", "child_returncode",
                "child_signal", "phase_exit_code", "phase_exit_code_observed",
                "interruption_kind", "interruption_source", "auth_state", "status",
            )
        }
        return outcome

    def run(self, command: list[str], *, phase: str, payload: bytes | None) -> dict[str, Any]:
        stdin = subprocess.PIPE if payload is not None else None
        try:
            child = _Popen(
                command,
                cwd=REPO_ROOT,
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return self._record_outcome({
                "phase": phase,
                "child_started": False,
                "child_pid": None,
                "child_reaped": True,
                "child_returncode": None,
                "child_signal": None,
                "phase_exit_code": None,
                "phase_exit_code_observed": False,
                "interruption_kind": "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN",
                "interruption_source": "CHILD_CREATE_ERROR",
                "auth_state": "UNKNOWN",
                "status": "HOLD_UNKNOWN_REMOTE_STATE",
                "stdout": b"",
                "stderr": str(exc).encode("utf-8", errors="replace"),
            })

        self.remote_call_count += 1
        child_pid = getattr(child, "pid", None)
        try:
            stdout, stderr = child.communicate(input=payload)
            returncode = child.returncode
            interruption_kind = classify_interruption(exception=None, returncode=returncode, stdout=stdout or b"", stderr=stderr or b"")
            return self._record_outcome({
                "phase": phase,
                "child_started": True,
                "child_pid": child_pid,
                "child_reaped": True,
                "child_returncode": returncode,
                "child_signal": -returncode if isinstance(returncode, int) and returncode < 0 else None,
                "phase_exit_code": returncode if isinstance(returncode, int) else None,
                "phase_exit_code_observed": isinstance(returncode, int),
                "interruption_kind": interruption_kind,
                "interruption_source": "CHILD_RETURN_CODE" if interruption_kind else "NONE",
                "auth_state": _auth_state(interruption_kind),
                "status": "OK" if returncode == 0 else "HOLD",
                "stdout": stdout or b"",
                "stderr": stderr or b"",
            })
        except (KeyboardInterrupt, EOFError, BrokenPipeError) as exc:
            _close_owned_stdin(child)
            _terminate_owned_child(child)
            reaped, stdout, stderr, returncode = _reap_owned_child(child)
            interruption_kind = classify_interruption(
                exception=exc,
                returncode=returncode,
                stdout=stdout,
                stderr=stderr,
            )
            if interruption_kind is None:
                interruption_kind = "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN"
            return self._record_outcome({
                "phase": phase,
                "child_started": True,
                "child_pid": child_pid,
                "child_reaped": reaped,
                "child_returncode": returncode,
                "child_signal": -returncode if isinstance(returncode, int) and returncode < 0 else None,
                "phase_exit_code": returncode if reaped and isinstance(returncode, int) else None,
                "phase_exit_code_observed": reaped and isinstance(returncode, int),
                "interruption_kind": interruption_kind,
                "interruption_source": "PARENT_INTERRUPT" if isinstance(exc, KeyboardInterrupt) else "INPUT_STREAM",
                "auth_state": _auth_state(interruption_kind),
                "status": "HOLD_UNKNOWN_REMOTE_STATE" if not reaped else "HOLD_INTERRUPTED",
                "stdout": stdout,
                "stderr": stderr,
            })
        except subprocess.TimeoutExpired:
            _close_owned_stdin(child)
            _terminate_owned_child(child)
            reaped, stdout, stderr, returncode = _reap_owned_child(child)
            return self._record_outcome({
                "phase": phase,
                "child_started": True,
                "child_pid": child_pid,
                "child_reaped": reaped,
                "child_returncode": returncode,
                "child_signal": -returncode if isinstance(returncode, int) and returncode < 0 else None,
                "phase_exit_code": returncode if reaped and isinstance(returncode, int) else None,
                "phase_exit_code_observed": reaped and isinstance(returncode, int),
                "interruption_kind": "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN",
                "interruption_source": "BOUNDED_WAIT_TIMEOUT",
                "auth_state": "UNKNOWN",
                "status": "HOLD_UNKNOWN_REMOTE_STATE",
                "stdout": stdout,
                "stderr": stderr,
            })
        except (OSError, subprocess.SubprocessError) as exc:
            _close_owned_stdin(child)
            _terminate_owned_child(child)
            reaped, stdout, stderr, returncode = _reap_owned_child(child)
            return self._record_outcome({
                "phase": phase,
                "child_started": True,
                "child_pid": child_pid,
                "child_reaped": reaped,
                "child_returncode": returncode,
                "child_signal": -returncode if isinstance(returncode, int) and returncode < 0 else None,
                "phase_exit_code": returncode if reaped and isinstance(returncode, int) else None,
                "phase_exit_code_observed": reaped and isinstance(returncode, int),
                "interruption_kind": "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN",
                "interruption_source": "CHILD_IO_ERROR",
                "auth_state": "UNKNOWN",
                "status": "HOLD_UNKNOWN_REMOTE_STATE",
                "stdout": stdout,
                "stderr": stderr or str(exc).encode("utf-8", errors="replace"),
            })


def _public_child_outcome(outcome: dict[str, Any]) -> dict[str, Any]:
    return {
        key: outcome.get(key)
        for key in (
            "phase", "child_started", "child_pid", "child_reaped", "child_returncode",
            "child_signal", "phase_exit_code", "phase_exit_code_observed",
            "interruption_kind", "interruption_source", "auth_state", "status",
        )
    }


def _base_terminal(*, status: str, phase: str, message: str, remote_call_count: int, phase_exit_codes: dict[str, int | None], local_source: dict[str, Any] | None = None, stage_root: str | None = None, child: dict[str, Any] | None = None, interruption_kind: str | None = None, interruption_source: str = "NONE", auth_state: str = "NOT_STARTED", mutation_capable_phase_started: bool = False, last_started_phase: str | None = None, last_child_lifecycle: dict[str, Any] | None = None, postflight_attempted: bool = False, postflight_completed: bool = False, postflight_call_count: int = 0, postflight_terminal: dict[str, Any] | None = None, phase_evidence_valid: bool | None = None, phase_evidence_error: str | None = None) -> dict[str, Any]:
    public_local_source = {} if local_source is None else {
        key: value for key, value in local_source.items() if key != "mapping_payload"
    }
    if local_source is not None and "mapping_payload" in local_source:
        public_local_source["mapping_payload_bytes"] = len(local_source["mapping_payload"])
    child_data = child or {}
    phase_exit_code = child_data.get("phase_exit_code")
    terminal = {
        "task": "D2-R7B-I1",
        "endpoint": TRANSPORT_ENDPOINT,
        "status": status,
        "phase": phase,
        "message": message,
        "terminal_source": "orchestrator_shared_raw_terminal",
        "raw_orchestrator_terminal_available": True,
        "terminal_delivery_attempt": 0,
        "terminal_delivery_fallback": False,
        "terminal_delivery_status": "PENDING",
        "terminal_delivery_authoritative": False,
        "terminal_delivery_framing": "NDJSON",
        "terminal_primary_delivery_interrupted": False,
        "terminal_stream_prefix_may_be_partial": False,
        "terminal_emission_interruption_kind": None,
        "last_started_phase": last_started_phase,
        "last_owned_child_lifecycle": last_child_lifecycle,
        "local_source": public_local_source,
        "interruption_kind": interruption_kind,
        "interruption_source": interruption_source,
        "auth_state": auth_state,
        "phase_started": True,
        "mutation_capable_phase_started": mutation_capable_phase_started,
        "child_started": bool(child_data.get("child_started", False)),
        "child_pid": child_data.get("child_pid"),
        "child_reaped": child_data.get("child_reaped", True),
        "child_returncode": child_data.get("child_returncode"),
        "child_signal": child_data.get("child_signal"),
        "phase_exit_codes": dict(phase_exit_codes),
        "phase_exit_code_observed": bool(
            child_data["phase_exit_code_observed"]
            if "phase_exit_code_observed" in child_data
            else phase_exit_codes.get(phase) is not None
        ),
        "target_state": _not_observed(REMOTE_PATHS["target"]),
        "upload_temp_state": _not_observed(REMOTE_PATHS["upload_temp"]),
        "backup_state": _not_observed(REMOTE_PATHS["backup"]),
        "rollback_temp_state": _not_observed(REMOTE_PATHS["rollback_temp"]),
        "collector_state": {"state": "NOT_OBSERVED"},
        "exact_artifact_paths": {
            **REMOTE_PATHS,
            "local_materializer": str(LOCAL_MATERIALIZER),
            "composite_manifest": str(Path(os.environ.get("D2_R7B_MANIFEST_PATH", str(MANIFEST_PATH)))),
            **{f"{name}_source": str(path) for name, path in HELPERS.items()},
        },
        "postflight_attempted": postflight_attempted,
        "postflight_completed": postflight_completed,
        "postflight_call_count": postflight_call_count,
        "postflight_terminal": postflight_terminal,
        "phase_evidence_valid": phase_evidence_valid,
        "phase_evidence_error": phase_evidence_error,
        "retry_count": 0,
        "resume_count": 0,
        "cleanup_count": 0,
        "rollback_count": 0,
        "restart_count_by_task": 0,
        "activation_count": 0,
        "local_stage_root": stage_root,
        "next_authority": "PM intake -> focused Reliability final re-review",
        "REMOTE_CALL_COUNT": int(remote_call_count),
    }
    return terminal


def _attach_postflight(terminal: dict[str, Any], postflight: dict[str, Any] | None, postflight_outcome: dict[str, Any]) -> None:
    if postflight:
        for key in ("target_state", "upload_temp_state", "backup_state", "rollback_temp_state", "collector_state"):
            if key in postflight:
                terminal[key] = postflight[key]
        if "classification" in postflight:
            terminal["classification"] = postflight["classification"]
    terminal["postflight_terminal"] = {
        **({} if postflight is None else postflight),
        "child_lifecycle": _public_child_outcome(postflight_outcome),
    }


def _call_remote(helper: Path, *, payload: bytes | None, phase: str, runner: PhaseOwnedRunner) -> dict[str, Any]:
    command = build_remote_command(helper.read_bytes(), helper.name)
    return runner.run(["ssh", TRANSPORT_ENDPOINT, command], phase=phase, payload=payload)


def _decode_json(stdout: bytes) -> dict[str, Any] | None:
    text = stdout.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    try:
        value = json.loads(text)
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def _normalize_invalid_child_json(outcome: dict[str, Any]) -> dict[str, Any]:
    if outcome.get("child_returncode") != 0 or _decode_json(outcome.get("stdout", b"")) is not None:
        return outcome
    normalized = dict(outcome)
    normalized["interruption_kind"] = None
    normalized["interruption_source"] = "INVALID_CHILD_JSON"
    normalized["auth_state"] = "NOT_STARTED"
    normalized["status"] = "HOLD_UNKNOWN_REMOTE_STATE"
    return normalized


def _phase_expectations() -> dict[str, Any]:
    synthetic_root = os.environ.get("D2_R7B_SYNTHETIC_ROOT")
    synthetic = bool(synthetic_root and os.environ.get("D2_R7B_TEST_INTERACTIVE_TTY") == "1")
    if not synthetic:
        return {
            "hostname": EXPECTED_HOSTNAME,
            "principal": EXPECTED_PRINCIPAL,
            "owner": EXPECTED_OWNER,
            "group": EXPECTED_GROUP,
            "device": EXPECTED_DEVICE,
            "target_inode": EXPECTED_TARGET_INODE,
            "filesystem": EXPECTED_FILESYSTEM,
            "old_sha256": EXPECTED_OLD_SHA256,
            **REMOTE_PATHS,
        }
    root = Path(str(synthetic_root))
    target = root / "config" / "mapping.yaml"
    device_text = os.environ.get("D2_R7B_SYNTHETIC_DEVICE", "")
    if not target.is_file() or target.is_symlink() or not device_text.isdigit():
        raise ContractError("synthetic phase-evidence fixture is incomplete")
    return {
        "hostname": EXPECTED_HOSTNAME,
        "principal": os.environ.get("D2_R7B_SYNTHETIC_OWNER", ""),
        "owner": os.environ.get("D2_R7B_SYNTHETIC_OWNER", ""),
        "group": os.environ.get("D2_R7B_SYNTHETIC_GROUP", ""),
        "device": int(device_text),
        "target_inode": target.stat().st_ino,
        "filesystem": os.environ.get("D2_R7B_SYNTHETIC_FILESYSTEM", ""),
        "old_sha256": os.environ.get("D2_R7B_SYNTHETIC_OLD_SHA256", ""),
        "target": str(target),
        "upload_temp": str(root / "config" / Path(REMOTE_PATHS["upload_temp"]).name),
        "backup": str(root / "config" / Path(REMOTE_PATHS["backup"]).name),
        "rollback_temp": str(root / "config" / Path(REMOTE_PATHS["rollback_temp"]).name),
    }


def _has_exact_keys(value: Any, keys: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == keys


def _positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _regular_file_record_valid(
    value: Any,
    *,
    path: str,
    state: str | None,
    expected_bytes: int,
    expected_sha256: str,
    expectations: dict[str, Any],
    inode_key: str = "inode",
) -> bool:
    keys = {"path", "realpath", "bytes", "sha256", "device", inode_key, "owner", "group", "mode"}
    if state is not None:
        keys |= {"state", "exists", "exact_realpath"}
    if not _has_exact_keys(value, keys):
        return False
    if state is not None and (value["state"] != state or value["exists"] is not True or value["exact_realpath"] is not True):
        return False
    return (
        value["path"] == path
        and value["realpath"] == path
        and type(value["bytes"]) is int
        and value["bytes"] == expected_bytes
        and value["sha256"] == expected_sha256
        and type(value["device"]) is int
        and value["device"] == expectations["device"]
        and _positive_int(value[inode_key])
        and value["owner"] == expectations["owner"]
        and value["group"] == expectations["group"]
        and value["mode"] == EXPECTED_FILE_MODE
    )


def _absent_record_valid(value: Any, *, path: str) -> bool:
    return (
        _has_exact_keys(value, {"path", "state", "exists", "realpath"})
        and value["path"] == path
        and value["state"] == "ABSENT"
        and value["exists"] is False
        and value["realpath"] is None
    )


def _collector_record_valid(value: Any) -> bool:
    if not _has_exact_keys(value, {"state", "observed", "expected", "command", "exit_code"}):
        return False
    if value["state"] not in {"UNCHANGED", "DRIFT"} or type(value["exit_code"]) is not int:
        return False
    state_keys = {"id", "name", "image", "configured_image", "running", "started_at", "restart_count", "mount"}
    if not _has_exact_keys(value["observed"], state_keys) or not _has_exact_keys(value["expected"], state_keys):
        return False
    mount_keys = {"source", "destination", "type", "rw"}
    return _has_exact_keys(value["observed"]["mount"], mount_keys) and _has_exact_keys(value["expected"]["mount"], mount_keys)


def _validate_preflight(value: dict[str, Any] | None, expectations: dict[str, Any]) -> tuple[bool, str | None]:
    keys = {"status", "transport_endpoint", "hostname", "principal", "target_device", "target_inode", "parent_device", "filesystem"}
    valid = (
        _has_exact_keys(value, keys)
        and value["status"] == "PASS"
        and value["transport_endpoint"] == TRANSPORT_ENDPOINT
        and value["hostname"] == expectations["hostname"]
        and value["principal"] == expectations["principal"]
        and type(value["target_device"]) is int
        and value["target_device"] == expectations["device"]
        and _positive_int(value["target_inode"])
        and value["target_inode"] == expectations["target_inode"]
        and type(value["parent_device"]) is int
        and value["parent_device"] == expectations["device"]
        and value["filesystem"] == expectations["filesystem"]
    )
    if valid:
        return True, None
    return False, "INVALID_CHILD_JSON" if value is None else "INVALID_PREFLIGHT_SCHEMA"


def _validate_upload(value: dict[str, Any] | None, expectations: dict[str, Any]) -> tuple[bool, str | None]:
    keys = {"status", "phase", "path", "realpath", "bytes", "sha256", "device", "inode", "owner", "group", "mode"}
    valid = (
        _has_exact_keys(value, keys)
        and value["status"] == "PASS"
        and value["phase"] == "REMOTE_UPLOAD"
        and _regular_file_record_valid(
            {key: value[key] for key in keys - {"status", "phase"}},
            path=expectations["upload_temp"],
            state=None,
            expected_bytes=EXPECTED_NEW_BYTES,
            expected_sha256=EXPECTED_NEW_SHA256,
            expectations=expectations,
        )
    )
    if valid:
        return True, None
    return False, "INVALID_CHILD_JSON" if value is None else "INVALID_UPLOAD_SCHEMA"


def _validate_deploy(
    value: dict[str, Any] | None,
    expectations: dict[str, Any],
    accepted_upload: dict[str, Any],
) -> tuple[bool, str | None]:
    top_keys = {"status", "phase", "operation", "source_upload_temp", "target", "backup"}
    source_keys = {"state", "path", "realpath", "bytes", "sha256", "device", "inode", "owner", "group", "mode"}
    target_keys = {"path", "realpath", "bytes", "sha256", "device", "inode_before", "inode_after", "owner", "group", "mode"}
    backup_keys = {"path", "realpath", "bytes", "sha256", "device", "inode", "owner", "group", "mode"}
    structural = (
        _has_exact_keys(value, top_keys)
        and _has_exact_keys(value["source_upload_temp"], source_keys)
        and _has_exact_keys(value["target"], target_keys)
        and _has_exact_keys(value["backup"], backup_keys)
    )
    if not structural:
        return False, "INVALID_CHILD_JSON" if value is None else "INVALID_DEPLOY_SCHEMA"
    source = value["source_upload_temp"]
    target = value["target"]
    backup = value["backup"]
    semantic = (
        value["status"] == "PASS"
        and value["phase"] == "REMOTE_DEPLOY"
        and value["operation"] == "ATOMIC_REPLACE_WITH_BACKUP"
        and source["state"] == "CONSUMED_BY_ATOMIC_REPLACE"
        and _regular_file_record_valid(
            {key: source[key] for key in source_keys - {"state"}},
            path=expectations["upload_temp"], state=None,
            expected_bytes=EXPECTED_NEW_BYTES, expected_sha256=EXPECTED_NEW_SHA256,
            expectations=expectations,
        )
        and _regular_file_record_valid(
            {key: target[key] for key in target_keys - {"inode_before"}},
            path=expectations["target"], state=None, inode_key="inode_after",
            expected_bytes=EXPECTED_NEW_BYTES, expected_sha256=EXPECTED_NEW_SHA256,
            expectations=expectations,
        )
        and _positive_int(target["inode_before"])
        and target["inode_before"] == expectations["target_inode"]
        and target["inode_before"] != target["inode_after"]
        and _regular_file_record_valid(
            backup,
            path=expectations["backup"], state=None,
            expected_bytes=EXPECTED_OLD_BYTES, expected_sha256=expectations["old_sha256"],
            expectations=expectations,
        )
    )
    if not semantic:
        return False, "INVALID_DEPLOY_SCHEMA"
    if source["inode"] != accepted_upload["inode"] or source["inode"] != target["inode_after"]:
        return False, "CROSS_PHASE_IDENTITY_MISMATCH"
    return True, None


def _postflight_file_state_valid(
    value: Any,
    *,
    path: str,
    new_state: str,
    expectations: dict[str, Any],
) -> bool:
    state = value.get("state") if isinstance(value, dict) else None
    if state == "ABSENT":
        return _absent_record_valid(value, path=path)
    if state == new_state:
        expected_bytes = EXPECTED_NEW_BYTES if new_state == "NEW_EXACT" else EXPECTED_OLD_BYTES
        expected_sha256 = EXPECTED_NEW_SHA256 if new_state == "NEW_EXACT" else expectations["old_sha256"]
        return _regular_file_record_valid(
            value, path=path, state=new_state, expected_bytes=expected_bytes,
            expected_sha256=expected_sha256, expectations=expectations,
        )
    return False


def _validate_postflight(
    value: dict[str, Any] | None,
    expectations: dict[str, Any],
    *,
    child_returncode: int | None,
) -> tuple[bool, str | None]:
    keys = {
        "status", "phase", "classification", "target_state", "upload_temp_state",
        "backup_state", "rollback_temp_state", "collector_state", "exact_artifact_paths",
        "task_lifecycle_actions", "message",
    }
    if not _has_exact_keys(value, keys):
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    paths = value["exact_artifact_paths"]
    actions = value["task_lifecycle_actions"]
    if not _has_exact_keys(paths, {"target", "upload_temp", "backup", "rollback_temp"}) or paths != {
        key: expectations[key] for key in ("target", "upload_temp", "backup", "rollback_temp")
    }:
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    if not _has_exact_keys(actions, {"cleanup_count", "rollback_count", "restart_count_by_task", "activation_count"}):
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    if any(type(actions[key]) is not int or actions[key] != 0 for key in actions):
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    if value["phase"] != "REMOTE_POSTFLIGHT" or not _collector_record_valid(value["collector_state"]):
        return False, "INVALID_POSTFLIGHT_SCHEMA"

    classification = value["classification"]
    target = value["target_state"]
    upload = value["upload_temp_state"]
    backup = value["backup_state"]
    rollback = value["rollback_temp_state"]
    if classification == "DEPLOYED_IDENTITY_VERIFIED":
        valid = (
            child_returncode == 0
            and value["status"] == "PASS"
            and value["message"] == "RUNTIME CONFIG LOAD NOT CLAIMED"
            and _postflight_file_state_valid(target, path=expectations["target"], new_state="NEW_EXACT", expectations=expectations)
            and _absent_record_valid(upload, path=expectations["upload_temp"])
            and _postflight_file_state_valid(backup, path=expectations["backup"], new_state="OLD_EXACT", expectations=expectations)
            and _absent_record_valid(rollback, path=expectations["rollback_temp"])
            and value["collector_state"]["state"] == "UNCHANGED"
        )
        return (True, None) if valid else (False, "INVALID_POSTFLIGHT_SCHEMA")

    if classification not in {"NO_MUTATION", "UPLOAD_STAGED_NO_REPLACEMENT", "BACKUP_CREATED_NO_REPLACEMENT"}:
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    if child_returncode != 2 or value["status"] != "HOLD" or value["message"] != "POSTFLIGHT DID NOT PROVE DEPLOYED IDENTITY":
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    if value["collector_state"]["state"] not in {"UNCHANGED", "DRIFT"}:
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    relations = {
        "NO_MUTATION": ("OLD_EXACT", "ABSENT", "ABSENT", "ABSENT"),
        "UPLOAD_STAGED_NO_REPLACEMENT": ("OLD_EXACT", "NEW_EXACT", "ABSENT", "ABSENT"),
        "BACKUP_CREATED_NO_REPLACEMENT": ("OLD_EXACT", "ABSENT", "OLD_EXACT", "ABSENT"),
    }
    observed = (target.get("state"), upload.get("state"), backup.get("state"), rollback.get("state"))
    if observed != relations[classification]:
        return False, "INVALID_POSTFLIGHT_SCHEMA"
    valid_states = (
        _postflight_file_state_valid(target, path=expectations["target"], new_state="OLD_EXACT", expectations=expectations)
        and _postflight_file_state_valid(upload, path=expectations["upload_temp"], new_state="NEW_EXACT", expectations=expectations)
        and _postflight_file_state_valid(backup, path=expectations["backup"], new_state="OLD_EXACT", expectations=expectations)
        and _absent_record_valid(rollback, path=expectations["rollback_temp"])
    )
    return (True, None) if valid_states else (False, "INVALID_POSTFLIGHT_SCHEMA")


def _interactive_auth_available() -> bool:
    if sys.stdin.isatty():
        return True
    return bool(os.environ.get("D2_R7B_SYNTHETIC_ROOT") and os.environ.get("D2_R7B_TEST_INTERACTIVE_TTY") == "1")


def _dry_run_terminal() -> dict[str, Any]:
    return _base_terminal(
        status="DRY_RUN",
        phase="FINAL_TERMINAL",
        message="DRY_RUN",
        remote_call_count=0,
        phase_exit_codes={},
    )


def _phase_snapshot(runner: PhaseOwnedRunner) -> dict[str, int | None]:
    return dict(runner.phase_exit_codes)


def _terminal_with_delivery(
    terminal: dict[str, Any],
    *,
    attempt: int,
    fallback: bool,
    delivery_status: str,
    interruption_kind: str | None,
) -> dict[str, Any]:
    emitted = dict(terminal)
    emitted["terminal_delivery_attempt"] = attempt
    emitted["terminal_delivery_fallback"] = fallback
    emitted["terminal_delivery_status"] = delivery_status
    emitted["terminal_delivery_authoritative"] = True
    emitted["terminal_delivery_framing"] = "NDJSON"
    emitted["terminal_primary_delivery_interrupted"] = fallback
    emitted["terminal_stream_prefix_may_be_partial"] = fallback
    emitted["terminal_emission_interruption_kind"] = interruption_kind
    return emitted


def serialize_terminal_record(terminal: dict[str, Any]) -> str:
    """Return one complete newline-delimited JSON terminal record."""
    fallback = bool(terminal.get("terminal_delivery_fallback", False))
    emitted = _terminal_with_delivery(
        terminal,
        attempt=2 if fallback else 1,
        fallback=fallback,
        delivery_status=("FALLBACK_AFTER_INTERRUPTION" if fallback else "PRIMARY"),
        interruption_kind=terminal.get("terminal_emission_interruption_kind") if fallback else None,
    )
    return json.dumps(emitted, sort_keys=True) + "\n"


def emit_terminal_record(terminal: dict[str, Any], *, force_new_record_boundary: bool) -> None:
    """Deliver one NDJSON record and flush within the same delivery attempt."""
    if force_new_record_boundary:
        sys.stdout.write("\n")
    sys.stdout.write(serialize_terminal_record(terminal))
    sys.stdout.flush()


def select_authoritative_terminal(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Select the unique highest-attempt authoritative member of complete records."""
    candidates = [
        record for record in records
        if record.get("terminal_delivery_authoritative") is True
        and record.get("terminal_delivery_framing") == "NDJSON"
        and type(record.get("terminal_delivery_attempt")) is int
    ]
    if not candidates:
        return None
    highest_attempt = max(record["terminal_delivery_attempt"] for record in candidates)
    highest = [record for record in candidates if record["terminal_delivery_attempt"] == highest_attempt]
    if len(highest) != 1:
        raise ValueError("authoritative terminal selection is ambiguous")
    return highest[0]


def emit_terminal(terminal: dict[str, Any], *, force_new_record_boundary: bool = False) -> None:
    """Serialize and emit exactly one terminal attempt."""
    emit_terminal_record(terminal, force_new_record_boundary=force_new_record_boundary)


def _terminal_emission_fallback(
    terminal: dict[str, Any],
    *,
    runner: PhaseOwnedRunner,
    interruption_kind: str,
) -> dict[str, Any]:
    """Build one deterministic, fail-closed fallback from the same execution context."""
    fallback = dict(terminal)
    fallback.update({
        "status": "HOLD",
        "phase": "FINAL_TERMINAL",
        "message": "HOLD / TERMINAL EMISSION INTERRUPTED",
        "terminal_source": "orchestrator_shared_raw_terminal",
        "raw_orchestrator_terminal_available": True,
        "terminal_delivery_attempt": 2,
        "terminal_delivery_fallback": True,
        "terminal_delivery_status": "FALLBACK_AFTER_INTERRUPTION",
        "terminal_delivery_authoritative": True,
        "terminal_delivery_framing": "NDJSON",
        "terminal_primary_delivery_interrupted": True,
        "terminal_stream_prefix_may_be_partial": True,
        "terminal_emission_interruption_kind": interruption_kind,
        "REMOTE_CALL_COUNT": int(runner.remote_call_count),
        "phase_exit_codes": _phase_snapshot(runner),
        "last_started_phase": runner.last_started_phase,
        "mutation_capable_phase_started": runner.mutation_capable_phase_started,
        "interruption_kind": interruption_kind,
        "interruption_source": "TERMINAL_EMISSION",
        "auth_state": _auth_state(interruption_kind),
        "target_state": _not_observed(REMOTE_PATHS["target"]),
        "upload_temp_state": _not_observed(REMOTE_PATHS["upload_temp"]),
        "backup_state": _not_observed(REMOTE_PATHS["backup"]),
        "rollback_temp_state": _not_observed(REMOTE_PATHS["rollback_temp"]),
        "collector_state": {"state": "NOT_OBSERVED"},
        "postflight_completed": False,
    })
    fallback.pop("classification", None)
    lifecycle = runner.last_child_lifecycle
    if lifecycle is not None:
        fallback["last_owned_child_lifecycle"] = dict(lifecycle)
        for key in (
            "child_started", "child_pid", "child_reaped", "child_returncode",
            "child_signal", "phase_exit_code_observed",
        ):
            if key in lifecycle:
                fallback[key] = lifecycle[key]
    fallback["postflight_terminal"] = {
        "status": "HOLD",
        "phase": "REMOTE_POSTFLIGHT",
        "classification": "UNKNOWN_OR_UNSAFE",
        "message": "TERMINAL EMISSION INTERRUPTED",
    }
    for key in ("retry_count", "resume_count", "cleanup_count", "rollback_count", "activation_count", "restart_count_by_task"):
        fallback[key] = 0
    return fallback


def _postflight_once(*, runner: PhaseOwnedRunner, expectations: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], bool, bool, str | None]:
    outcome = _call_remote(HELPERS["remote_postflight"], payload=None, phase="REMOTE_POSTFLIGHT", runner=runner)
    parsed = _decode_json(outcome["stdout"])
    valid, error = _validate_postflight(parsed, expectations, child_returncode=outcome.get("child_returncode"))
    completed = bool(outcome["child_reaped"] and valid)
    if not valid:
        classification = "UNKNOWN_OR_UNSAFE" if outcome["child_started"] else "NOT_OBSERVED"
        parsed = {
            "status": "HOLD",
            "phase": "REMOTE_POSTFLIGHT",
            "classification": classification,
            "target_state": _not_observed(REMOTE_PATHS["target"]),
            "upload_temp_state": _not_observed(REMOTE_PATHS["upload_temp"]),
            "backup_state": _not_observed(REMOTE_PATHS["backup"]),
            "rollback_temp_state": _not_observed(REMOTE_PATHS["rollback_temp"]),
            "collector_state": {"state": classification},
            "message": "POSTFLIGHT OBSERVATION INCOMPLETE",
        }
    return outcome, parsed, completed, valid, error


def _terminal_for_phase(*, outcome: dict[str, Any], status: str, phase: str, message: str, runner: PhaseOwnedRunner, phase_exit_codes: dict[str, int | None], local_source: dict[str, Any] | None = None, stage_root: str | None = None, mutation_capable_phase_started: bool = False, postflight_attempted: bool = False, postflight_completed: bool = False, postflight_call_count: int = 0, postflight_terminal: dict[str, Any] | None = None, phase_evidence_valid: bool | None = None, phase_evidence_error: str | None = None) -> dict[str, Any]:
    return _base_terminal(
        status=status,
        phase=phase,
        message=message,
        remote_call_count=runner.remote_call_count,
        phase_exit_codes=phase_exit_codes,
        local_source=local_source,
        stage_root=stage_root,
        child=outcome,
        interruption_kind=outcome.get("interruption_kind"),
        interruption_source=outcome.get("interruption_source", "NONE"),
        auth_state=outcome.get("auth_state", "NOT_STARTED"),
        mutation_capable_phase_started=mutation_capable_phase_started,
        last_started_phase=runner.last_started_phase,
        last_child_lifecycle=runner.last_child_lifecycle,
        postflight_attempted=postflight_attempted,
        postflight_completed=postflight_completed,
        postflight_call_count=postflight_call_count,
        postflight_terminal=postflight_terminal,
        phase_evidence_valid=phase_evidence_valid,
        phase_evidence_error=phase_evidence_error,
    )


def execute(args: argparse.Namespace, *, runner: PhaseOwnedRunner | None = None) -> tuple[dict[str, Any], int]:
    if not args.execute and args.confirm is None:
        return _dry_run_terminal(), 0
    if not args.execute or args.confirm != CONFIRMATION_TOKEN:
        terminal = _base_terminal(
            status="HOLD_REMOTE_EXECUTION_NOT_CONFIRMED",
            phase="FINAL_TERMINAL",
            message="HOLD / REMOTE EXECUTION NOT CONFIRMED",
            remote_call_count=0,
            phase_exit_codes={},
        )
        return terminal, 2
    if not _interactive_auth_available():
        terminal = _base_terminal(
            status="HOLD_INTERACTIVE_AUTHENTICATION_UNAVAILABLE",
            phase="FINAL_TERMINAL",
            message="HOLD / INTERACTIVE AUTHENTICATION UNAVAILABLE",
            remote_call_count=0,
            phase_exit_codes={},
        )
        return terminal, 2

    runner = PhaseOwnedRunner() if runner is None else runner
    try:
        local_source = local_source_gate()
    except (ContractError, OSError, ValueError, subprocess.SubprocessError) as exc:
        runner.record_phase("LOCAL_SOURCE_GATE", 2)
        terminal = _base_terminal(
            status="HOLD_LOCAL_SOURCE",
            phase="LOCAL_SOURCE_GATE",
            message=f"HOLD_LOCAL_SOURCE: {exc}",
            remote_call_count=runner.remote_call_count,
            phase_exit_codes=_phase_snapshot(runner),
        )
        return terminal, 2
    except (KeyboardInterrupt, EOFError) as exc:
        interruption_kind = classify_interruption(exception=exc, returncode=None)
        runner.record_phase("LOCAL_SOURCE_GATE", None)
        terminal = _base_terminal(
            status="HOLD",
            phase="LOCAL_SOURCE_GATE",
            message="HOLD_LOCAL_SOURCE: LOCAL INTERRUPTION",
            remote_call_count=runner.remote_call_count,
            phase_exit_codes=_phase_snapshot(runner),
            interruption_kind=interruption_kind,
            interruption_source="PARENT_INTERRUPT",
            auth_state=_auth_state(interruption_kind),
        )
        return terminal, 2

    runner.record_phase("LOCAL_SOURCE_GATE", 0)
    stage_root = local_source["stage_root"]
    expectations = _phase_expectations()

    preflight = _normalize_invalid_child_json(_call_remote(HELPERS["remote_preflight"], payload=None, phase="REMOTE_PREFLIGHT", runner=runner))
    if not preflight["child_reaped"]:
        terminal = _terminal_for_phase(
            outcome=preflight,
            status="HOLD_UNKNOWN_REMOTE_STATE",
            phase="REMOTE_PREFLIGHT",
            message="PREFLIGHT CHILD NOT REAPED; STOPPED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
        )
        return terminal, 2
    if preflight["child_returncode"] != 0 or preflight.get("interruption_kind"):
        status = "HOLD_PREFLIGHT_INTERRUPTED" if preflight.get("interruption_kind") else "HOLD_PREFLIGHT"
        terminal = _terminal_for_phase(
            outcome=preflight,
            status=status,
            phase="REMOTE_PREFLIGHT",
            message="HOLD_PREFLIGHT",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
        )
        return terminal, 2
    preflight_json = _decode_json(preflight["stdout"])
    preflight_valid, preflight_error = _validate_preflight(preflight_json, expectations)
    if not preflight_valid:
        terminal = _terminal_for_phase(
            outcome=preflight,
            status="HOLD_PREFLIGHT_EVIDENCE_INVALID",
            phase="REMOTE_PREFLIGHT",
            message="PREFLIGHT PHASE EVIDENCE INVALID; UPLOAD NOT STARTED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            phase_evidence_valid=False,
            phase_evidence_error=preflight_error,
        )
        return terminal, 2

    upload = _normalize_invalid_child_json(_call_remote(HELPERS["remote_upload"], payload=local_source["mapping_payload"], phase="REMOTE_UPLOAD", runner=runner))
    if not upload["child_reaped"]:
        terminal = _terminal_for_phase(
            outcome=upload,
            status="HOLD_UNKNOWN_REMOTE_STATE",
            phase="REMOTE_UPLOAD",
            message="UPLOAD CHILD NOT REAPED; STOPPED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
        )
        return terminal, 2
    if upload["child_returncode"] != 0 or upload.get("interruption_kind"):
        postflight_outcome, postflight_json, postflight_completed, _, _ = _postflight_once(runner=runner, expectations=expectations)
        classification = postflight_json.get("classification")
        if upload.get("interruption_kind"):
            status = "HOLD_UPLOAD_INTERRUPTED"
            message = "UPLOAD INTERRUPTED; READ-ONLY POSTFLIGHT COMPLETED"
        elif classification == "PARTIAL_DEPLOYMENT":
            status = "HOLD_PARTIAL_DEPLOYMENT"
            message = "UPLOAD FAILED; READ-ONLY POSTFLIGHT COMPLETED"
        elif classification == "UNKNOWN_OR_UNSAFE":
            status = "HOLD_UNKNOWN_REMOTE_STATE"
            message = "UPLOAD FAILED; READ-ONLY POSTFLIGHT COMPLETED"
        else:
            status = "HOLD_UPLOAD_FAILED_NO_REPLACEMENT"
            message = "UPLOAD FAILED; READ-ONLY POSTFLIGHT COMPLETED"
        terminal = _terminal_for_phase(
            outcome=upload,
            status=status,
            phase="REMOTE_UPLOAD",
            message=message,
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
            postflight_attempted=True,
            postflight_completed=postflight_completed,
            postflight_call_count=1,
            postflight_terminal=postflight_json,
        )
        _attach_postflight(terminal, postflight_json, postflight_outcome)
        return terminal, 2
    upload_json = _decode_json(upload["stdout"])
    upload_valid, upload_error = _validate_upload(upload_json, expectations)
    if not upload_valid:
        postflight_outcome, postflight_json, postflight_completed, _, _ = _postflight_once(runner=runner, expectations=expectations)
        terminal = _terminal_for_phase(
            outcome=upload,
            status="HOLD_UPLOAD_EVIDENCE_INVALID",
            phase="REMOTE_UPLOAD",
            message="UPLOAD PHASE EVIDENCE INVALID; DEPLOY NOT STARTED; READ-ONLY POSTFLIGHT COMPLETED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
            postflight_attempted=True,
            postflight_completed=postflight_completed,
            postflight_call_count=1,
            postflight_terminal=postflight_json,
            phase_evidence_valid=False,
            phase_evidence_error=upload_error,
        )
        _attach_postflight(terminal, postflight_json, postflight_outcome)
        return terminal, 2

    deploy = _normalize_invalid_child_json(_call_remote(HELPERS["remote_deploy"], payload=None, phase="REMOTE_DEPLOY", runner=runner))
    if not deploy["child_reaped"]:
        terminal = _terminal_for_phase(
            outcome=deploy,
            status="HOLD_UNKNOWN_REMOTE_STATE",
            phase="REMOTE_DEPLOY",
            message="DEPLOY CHILD NOT REAPED; STOPPED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
        )
        return terminal, 2

    deploy_json = _decode_json(deploy["stdout"])
    deploy_valid, deploy_error = _validate_deploy(deploy_json, expectations, upload_json)
    postflight_outcome, postflight_json, postflight_completed, postflight_valid, postflight_error = _postflight_once(runner=runner, expectations=expectations)
    classification = postflight_json.get("classification")
    if deploy.get("interruption_kind"):
        status = "HOLD_DEPLOY_INTERRUPTED"
        message = "DEPLOY INTERRUPTED; READ-ONLY POSTFLIGHT COMPLETED"
    elif postflight_outcome.get("interruption_kind"):
        status = "HOLD_POSTFLIGHT_INTERRUPTED"
        message = "POSTFLIGHT INTERRUPTED; NO SECOND POSTFLIGHT"
    elif deploy["child_returncode"] == 0 and not deploy_valid:
        terminal = _terminal_for_phase(
            outcome=deploy,
            status="HOLD_DEPLOY_EVIDENCE_INVALID",
            phase="REMOTE_DEPLOY",
            message="DEPLOYED STATE OBSERVED BUT DEPLOY HELPER EVIDENCE INVALID",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
            postflight_attempted=True,
            postflight_completed=postflight_completed,
            postflight_call_count=1,
            postflight_terminal=postflight_json,
            phase_evidence_valid=False,
            phase_evidence_error=deploy_error,
        )
        _attach_postflight(terminal, postflight_json, postflight_outcome)
        return terminal, 2
    elif not postflight_valid:
        terminal = _terminal_for_phase(
            outcome=postflight_outcome,
            status="HOLD_POSTFLIGHT_EVIDENCE_INVALID",
            phase="REMOTE_POSTFLIGHT",
            message="POSTFLIGHT PHASE EVIDENCE INVALID; NO SECOND POSTFLIGHT",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
            postflight_attempted=True,
            postflight_completed=False,
            postflight_call_count=1,
            postflight_terminal=postflight_json,
            phase_evidence_valid=False,
            phase_evidence_error=postflight_error,
        )
        _attach_postflight(terminal, postflight_json, postflight_outcome)
        return terminal, 2
    elif deploy["child_returncode"] == 0 and postflight_outcome["child_returncode"] == 0 and classification == "DEPLOYED_IDENTITY_VERIFIED":
        terminal = _terminal_for_phase(
            outcome=postflight_outcome,
            status="CONFIG_DEPLOYED_IDENTITY_VERIFIED",
            phase="FINAL_TERMINAL",
            message="RUNTIME CONFIG LOAD NOT CLAIMED",
            runner=runner,
            phase_exit_codes=_phase_snapshot(runner),
            local_source=local_source,
            stage_root=stage_root,
            mutation_capable_phase_started=True,
            postflight_attempted=True,
            postflight_completed=postflight_completed,
            postflight_call_count=1,
            postflight_terminal=postflight_json,
            phase_evidence_valid=True,
            phase_evidence_error=None,
        )
        _attach_postflight(terminal, postflight_json, postflight_outcome)
        return terminal, 0
    elif deploy["child_returncode"] != 0 and classification == "NO_MUTATION":
        status = "HOLD_DEPLOY_FAILED_NO_REPLACEMENT"
        message = "DEPLOYMENT NOT PROMOTED TO SUCCESS"
    elif deploy["child_returncode"] != 0 and classification in {"DEPLOYED_IDENTITY_VERIFIED", "PARTIAL_DEPLOYMENT"}:
        status = "HOLD_PARTIAL_DEPLOYMENT"
        message = "DEPLOYMENT NOT PROMOTED TO SUCCESS"
    elif deploy["child_returncode"] != 0:
        status = "HOLD_UNKNOWN_REMOTE_STATE" if classification == "UNKNOWN_OR_UNSAFE" else "HOLD_DEPLOY_FAILED_NO_REPLACEMENT"
        message = "DEPLOYMENT NOT PROMOTED TO SUCCESS"
    else:
        status = "HOLD_PARTIAL_OR_UNKNOWN"
        message = "DEPLOYMENT NOT PROMOTED TO SUCCESS"
    terminal = _terminal_for_phase(
        outcome=postflight_outcome if postflight_outcome.get("interruption_kind") else deploy,
        status=status,
        phase="REMOTE_DEPLOY" if deploy.get("interruption_kind") else "REMOTE_POSTFLIGHT",
        message=message,
        runner=runner,
        phase_exit_codes=_phase_snapshot(runner),
        local_source=local_source,
        stage_root=stage_root,
        mutation_capable_phase_started=True,
        postflight_attempted=True,
        postflight_completed=postflight_completed,
        postflight_call_count=1,
        postflight_terminal=postflight_json,
    )
    _attach_postflight(terminal, postflight_json, postflight_outcome)
    return terminal, 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args(argv)
    runner = PhaseOwnedRunner()
    try:
        terminal, exit_code = execute(args, runner=runner)
    except (ContractError, OSError, ValueError, subprocess.SubprocessError) as exc:
        terminal = _base_terminal(
            status="HOLD_UNKNOWN_REMOTE_STATE",
            phase="FINAL_TERMINAL",
            message=f"HOLD / UNEXPECTED EXECUTION CONTRACT ERROR: {exc}",
            remote_call_count=runner.remote_call_count,
            phase_exit_codes=dict(runner.phase_exit_codes),
            child=runner.last_child_lifecycle,
            mutation_capable_phase_started=runner.mutation_capable_phase_started,
            last_started_phase=runner.last_started_phase,
            last_child_lifecycle=runner.last_child_lifecycle,
        )
        exit_code = 2
    except (KeyboardInterrupt, EOFError) as exc:
        interruption_kind = classify_interruption(exception=exc, returncode=None)
        terminal = _base_terminal(
            status="HOLD",
            phase="FINAL_TERMINAL",
            message="HOLD / PARENT INTERRUPTION",
            remote_call_count=runner.remote_call_count,
            phase_exit_codes=dict(runner.phase_exit_codes),
            child=runner.last_child_lifecycle,
            interruption_kind=interruption_kind,
            interruption_source="PARENT_INTERRUPT",
            auth_state=_auth_state(interruption_kind),
            mutation_capable_phase_started=runner.mutation_capable_phase_started,
            last_started_phase=runner.last_started_phase,
            last_child_lifecycle=runner.last_child_lifecycle,
        )
        exit_code = 2
    try:
        emit_terminal(terminal)
    except (KeyboardInterrupt, EOFError) as exc:
        interruption_kind = classify_interruption(exception=exc, returncode=None)
        fallback = _terminal_emission_fallback(
            terminal,
            runner=runner,
            interruption_kind=interruption_kind or "AUTHENTICATION_OR_INTERRUPTION_UNKNOWN",
        )
        try:
            emit_terminal(fallback, force_new_record_boundary=True)
        except (KeyboardInterrupt, EOFError) as fallback_exc:
            failed_fallback = dict(fallback)
            failed_fallback["terminal_delivery_authoritative"] = False
            raise TerminalDeliveryError(
                "terminal delivery failed after one primary and one fallback attempt",
                terminal=failed_fallback,
                attempts=2,
            ) from fallback_exc
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
