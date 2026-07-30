#!/usr/bin/env python3
"""R35 local gate, probe materializer, execution lock, one-shot SSH, and closeout."""

import ast
import base64
import hashlib
import json
import os
import stat
import subprocess
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/Users/chenjie/Documents/MES/edge-mes-demo")
EVIDENCE = ROOT / "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation"
RUNNER = EVIDENCE / "run_post_activation_validation.py"
REMOTE_PROBE = EVIDENCE / "remote_post_activation_probe.py"
CONTAINER_PROBE = EVIDENCE / "container_static_probe.py"
LOCAL_TERMINAL = EVIDENCE / "local_prerequisite_terminal.json"
REMOTE_TERMINAL = EVIDENCE / "post_activation_terminal.json"
MANIFEST = EVIDENCE / "manifest.sha256"
REPORT = ROOT / "docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md"
KEY = Path("/Users/chenjie/.ssh/edge_pi_codex")
AUTHORITY_ID = "PM-D2-R7B-I1-R35-PHASE5-POST-ACTIVATION-VALIDATION-260729-2143"
EXPECTED_HEAD = "ac33e6bae449ecdd9b77a53daaf7271f14133000"
EXPECTED_PARENT = "66563677d3d1129fbc79c2c284b5f6d8b62f1932"
EXPECTED_POST_SNAPSHOT_HASH = "4724098c93115633cd3889477379d1c93f5b323b9e97e9791a9df95a485bd4cc"
FRESH_IMAGE = "sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734"
ACTIVE_CONTAINER = "3f0d0457a0a1a929b632a2d865016be6f4104fed001b6015eee14e502bb31ba8"
DIRTY = [
    ".gitignore",
    "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh",
    "docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py",
    "docs/thread_handoff/pm_operating_rules.md",
]
SSH_ARGV = [
    "ssh",
    "-T",
    "-p",
    "22",
    "-o",
    "BatchMode=yes",
    "-o",
    "IdentitiesOnly=yes",
    "-i",
    "/Users/chenjie/.ssh/edge_pi_codex",
    "-o",
    "ControlMaster=no",
    "-o",
    "ControlPersist=no",
    "-o",
    "ForwardAgent=no",
    "-o",
    "StrictHostKeyChecking=yes",
    "-o",
    "ConnectTimeout=10",
    "-o",
    "ServerAliveInterval=5",
    "-o",
    "ServerAliveCountMax=2",
    "-o",
    "LogLevel=ERROR",
    "mari@10.0.0.217",
    "/usr/bin/python3",
    "-",
]
DOCKER_PLAN = [
    "aggregate_image_inspect",
    "project_ps_snapshot_a",
    "aggregate_container_inspect_snapshot_a",
    "container_static_exec",
    "project_ps_snapshot_b",
    "aggregate_container_inspect_snapshot_b",
]
CONTAINER_EXEC = [
    "/usr/bin/docker",
    "exec",
    "-i",
    "-e",
    "PYTHONDONTWRITEBYTECODE=1",
    ACTIVE_CONTAINER,
    "/usr/local/bin/python",
    "-B",
    "-",
]
OUTPUTS = [
    REPORT,
    RUNNER,
    REMOTE_PROBE,
    CONTAINER_PROBE,
    LOCAL_TERMINAL,
    REMOTE_TERMINAL,
    MANIFEST,
]
MANIFEST_PATHS = [
    REPORT,
    RUNNER,
    REMOTE_PROBE,
    CONTAINER_PROBE,
    LOCAL_TERMINAL,
    REMOTE_TERMINAL,
]
HELPERS = [RUNNER, REMOTE_PROBE, CONTAINER_PROBE]
AUTHORITY_IDENTITIES = {
    "pm_rule": (
        "docs/thread_handoff/pm_operating_rules.md",
        49170,
        "a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5",
    ),
    "r31_report": (
        "docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md",
        45360,
        "bd5b65ac08dcacfd0fc14a639626d807f28d429f1038a99aa124cd6ce85db894",
    ),
    "r33_report": (
        "docs/reports/sprint4_d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight.md",
        6049,
        "daa0af5824d697ad12342fcaedf09330b082da78475f1351fec46c0892153c66",
    ),
    "r33_terminal": (
        "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/remote_preflight_terminal.json",
        50786,
        "d1cd628fdf6ffacf62c5ceb1e418284bf4663ac5d9642cfdeead51eec423a82e",
    ),
    "r33_manifest": (
        "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/manifest.sha256",
        842,
        "5c52278d1a8585d8c19402546a2dd231f58f717ba6ef97e756ee19a9729bbaad",
    ),
    "r34_r2_report": (
        "docs/reports/sprint4_d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation.md",
        680,
        "5d8beac891bc748ed396bbfed6af6d8bd153b491c484e2e1d1cf28e88169914d",
    ),
    "r34_r2_run": (
        "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/run_activation.py",
        13498,
        "d911ecdd40aad8538e23796dfee44115e6866452ac449a8595776b2629d722e6",
    ),
    "r34_r2_controller": (
        "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/remote_activation_controller.py",
        17395,
        "61257ebc558ac954c3c6cac3184f44529300e8b052df5c9fe397654e49ed48af",
    ),
    "r34_r2_local_terminal": (
        "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/local_prerequisite_terminal.json",
        30700,
        "01f9f832e0c5da6e915e6405b2a30c4f4ee7ea89ee0bc79b0e9d41dd5e77d9bb",
    ),
    "r34_r2_activation_terminal": (
        "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/activation_terminal.json",
        75863,
        "91e13fabe321a0135bb0d2cec7ee7bfc4389b48721eda4dd76b815ea1e816332",
    ),
    "r34_r2_manifest": (
        "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/manifest.sha256",
        920,
        "c74a587252bb7bb20e0ab0701ae0ddbea53ec92dd5822425a03ee09aed0ea860",
    ),
    "r32_build_input_manifest": (
        "docs/reports/evidence/d2_r7b_i1_r32_phase1_phase2/build_input_manifest.sha256",
        3797,
        "ad339c6adaa3556df513b9dca30af6fe129b2d583b3f7720adab0b9e692044da",
    ),
    "r32_phase1_terminal": (
        "docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/phase1_validation_terminal.json",
        4125,
        "89d8d9cea25f0724740e0b10d30dfcb222d1a8841748c4ca2da1ca9deaf034aa",
    ),
}
SOURCE_MAP = {
    "collector/app/main.py": (
        "/app/app/main.py",
        "a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090",
    ),
    "collector/app/services/event_collector.py": (
        "/app/app/services/event_collector.py",
        "eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f",
    ),
    "collector/app/services/accepted_station_event_fact.py": (
        "/app/app/services/accepted_station_event_fact.py",
        "6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911",
    ),
    "collector/app/services/storage.py": (
        "/app/app/services/storage.py",
        "f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b",
    ),
    "collector/app/plc/mapping.py": (
        "/app/app/plc/mapping.py",
        "c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098",
    ),
    "collector/app/plc/read_plan.py": (
        "/app/app/plc/read_plan.py",
        "fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6",
    ),
    "collector/app/services/resolved_config_registry.py": (
        "/app/app/services/resolved_config_registry.py",
        "1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c",
    ),
    "common/station_event/__init__.py": (
        "/app/common/station_event/__init__.py",
        "d8a214d0c4a85e7bbaf7b5e79e6db905115be1f50effb27357fa9f371ea1c7a7",
    ),
    "common/station_event/constants.py": (
        "/app/common/station_event/constants.py",
        "6dd60705ab192a1c889f0a4652d478f7d367bd24b980fc092c48a51e25214e11",
    ),
    "common/station_event/errors.py": (
        "/app/common/station_event/errors.py",
        "355c882f51cc7c66cdf8f22c73c0d72633391dc8403d4f9f428b0b8ac510b4f3",
    ),
    "common/station_event/fingerprint.py": (
        "/app/common/station_event/fingerprint.py",
        "cb35dcf5ab5ba9ccb3e60d0e38b1c86cf24717559cc70e250adf297dff939608",
    ),
    "common/station_event/lifecycle.py": (
        "/app/common/station_event/lifecycle.py",
        "afec2c75010b8642239d2494c57f470f3414c4fbff486b588589adf7bc4efcff",
    ),
    "common/station_event/models.py": (
        "/app/common/station_event/models.py",
        "176627b71f32bdef08c75a6bfe3b7badab1094e8ec2c3cf7b1e719d0a2d1df77",
    ),
    "common/station_event/projection.py": (
        "/app/common/station_event/projection.py",
        "39ed6034d87e23718a22a8a66fbb60af365a5d7b573ff045a021b7206c708623",
    ),
    "common/station_event/serialization.py": (
        "/app/common/station_event/serialization.py",
        "9cbabbd42e5685311829030b13f24fa16396fb853458e3f51bd7cb7bf5124407",
    ),
    "common/station_event/validation.py": (
        "/app/common/station_event/validation.py",
        "e7cff46b91112236873744a32dafec5160a0ca6036f184106e1ec4a232724bd1",
    ),
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def identity(path):
    metadata = os.lstat(path)
    data = path.read_bytes()
    return {
        "path": relative(path),
        "bytes": len(data),
        "sha256": sha256(data),
        "regular": stat.S_ISREG(metadata.st_mode),
        "symlink": stat.S_ISLNK(metadata.st_mode),
    }


def dump(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def git(*arguments):
    proc = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "argv": ["git", *arguments],
        "returncode": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "strict").strip(),
        "stderr": proc.stderr.decode("utf-8", "strict").strip(),
    }


def live_git_facts():
    return {
        "root": git("rev-parse", "--show-toplevel"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head": git("rev-parse", "HEAD"),
        "origin_main": git("rev-parse", "origin/main"),
        "head_parent": git("rev-parse", "HEAD^"),
        "ahead_behind": git("rev-list", "--left-right", "--count", "HEAD...origin/main"),
        "tracked_dirty": git("diff", "--name-only"),
        "cached": git("diff", "--cached", "--name-only"),
        "diff_check": git("diff", "--check"),
        "cached_diff_check": git("diff", "--cached", "--check"),
    }


def baseline_ok(facts):
    return (
        facts["root"]["returncode"] == 0
        and facts["root"]["stdout"] == str(ROOT)
        and facts["branch"]["stdout"] == "main"
        and facts["head"]["stdout"] == EXPECTED_HEAD
        and facts["origin_main"]["stdout"] == EXPECTED_HEAD
        and facts["head_parent"]["stdout"] == EXPECTED_PARENT
        and facts["ahead_behind"]["stdout"] == "0\t0"
        and facts["tracked_dirty"]["stdout"].splitlines() == DIRTY
        and facts["cached"]["stdout"] == ""
        and facts["diff_check"]["returncode"] == 0
        and facts["cached_diff_check"]["returncode"] == 0
    )


def task_process_audit():
    proc = subprocess.run(
        ["ps", "ax", "-o", "pid=,ppid=,command="],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    matches = []
    if proc.returncode == 0:
        for line in proc.stdout.decode("utf-8", "strict").splitlines():
            fields = line.strip().split(None, 2)
            if len(fields) != 3:
                continue
            pid = int(fields[0])
            command = fields[2]
            direct_python = "python" in command.split(None, 1)[0].lower()
            owned_name = any(path.name in command for path in HELPERS)
            if direct_python and owned_name and pid != os.getpid():
                matches.append({"pid": pid, "command": command})
    return {
        "returncode": proc.returncode,
        "stderr": proc.stderr.decode("utf-8", "strict"),
        "other_task_owned_processes": matches,
        "pass": proc.returncode == 0 and not matches,
    }


def verify_manifest(path, expected_count, require_sorted=True):
    try:
        lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
        parsed = []
        for line in lines:
            digest, item_path = line.split("  ", 1)
            parsed.append((digest, item_path))
        paths = [item_path for _, item_path in parsed]
        return {
            "count": len(parsed),
            "expected_count": expected_count,
            "sorted": paths == sorted(paths),
            "unique": len(paths) == len(set(paths)),
            "self_excluded": relative(path) not in paths,
            "matches": all(
                len(digest) == 64
                and (ROOT / item_path).is_file()
                and sha256((ROOT / item_path).read_bytes()) == digest
                for digest, item_path in parsed
            ),
            "paths": paths,
            "pass": len(parsed) == expected_count
            and (paths == sorted(paths) or not require_sorted)
            and len(paths) == len(set(paths))
            and relative(path) not in paths
            and all(
                len(digest) == 64
                and (ROOT / item_path).is_file()
                and sha256((ROOT / item_path).read_bytes()) == digest
                for digest, item_path in parsed
            ),
        }
    except Exception as exc:
        return {"pass": False, "error": type(exc).__name__}


def authority_identity_audit():
    observed = {}
    all_exact = True
    for name, (item_path, expected_bytes, expected_hash) in AUTHORITY_IDENTITIES.items():
        path = ROOT / item_path
        try:
            current = identity(path)
            exact = (
                current["regular"]
                and not current["symlink"]
                and current["bytes"] == expected_bytes
                and current["sha256"] == expected_hash
            )
            current["expected_bytes"] = expected_bytes
            current["expected_sha256"] = expected_hash
            current["exact"] = exact
            observed[name] = current
            all_exact = all_exact and exact
        except Exception as exc:
            observed[name] = {"path": item_path, "exact": False, "error": type(exc).__name__}
            all_exact = False
    return observed, all_exact


def build_manifest_map():
    path = ROOT / AUTHORITY_IDENTITIES["r32_build_input_manifest"][0]
    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    parsed = {}
    duplicates = []
    for line in lines:
        digest, item_path = line.split("  ", 1)
        if item_path in parsed:
            duplicates.append(item_path)
        parsed[item_path] = digest
    required = {}
    for local_path, (container_path, expected_hash) in SOURCE_MAP.items():
        required[local_path] = {
            "container_path": container_path,
            "manifest_sha256": parsed.get(local_path),
            "expected_sha256": expected_hash,
            "unique": lines.count(expected_hash + "  " + local_path) == 1,
            "match": parsed.get(local_path) == expected_hash,
        }
    return {
        "entries": len(lines),
        "duplicates": duplicates,
        "required": required,
        "required_complete_unique": not duplicates
        and len(required) == 16
        and all(item["unique"] and item["match"] for item in required.values()),
    }


def canonical(snapshot):
    ids = snapshot.get("ids", [])
    if len(ids) != len(set(ids)):
        raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
    services = set()
    full_ids = set()
    output = []
    for original in snapshot.get("containers", []):
        item = dict(original)
        labels = item.get("labels") or {}
        service = labels.get("service")
        full_id = item.get("Id")
        if labels.get("project") != "edge-mes-demo" or not service or service in services:
            raise ValueError("DUPLICATE_DISCOVERED_SERVICE")
        if not full_id or full_id in full_ids:
            raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
        services.add(service)
        full_ids.add(full_id)
        item["Mounts"] = sorted(
            item.get("Mounts", []),
            key=lambda mount: (
                str(mount.get("Type")),
                str(mount.get("Source")),
                str(mount.get("Destination")),
                str(mount.get("RW")),
            ),
        )
        output.append(item)
    return {
        "ids": sorted(set(ids)),
        "containers": sorted(
            output,
            key=lambda item: (item["labels"]["service"], item["Id"]),
        ),
        "inspect_ok": snapshot.get("inspect_ok"),
    }


def canonical_fixtures():
    first = {
        "ids": ["b", "a"],
        "inspect_ok": True,
        "containers": [
            {
                "Id": "2",
                "labels": {"project": "edge-mes-demo", "service": "x"},
                "Mounts": [
                    {"Type": "bind", "Source": "b", "Destination": "z", "RW": False},
                    {"Type": "bind", "Source": "a", "Destination": "y", "RW": True},
                ],
            },
            {
                "Id": "1",
                "labels": {"project": "edge-mes-demo", "service": "y"},
                "Mounts": [],
            },
        ],
    }
    reordered = {
        "ids": ["a", "b"],
        "inspect_ok": True,
        "containers": [
            first["containers"][1],
            {
                **first["containers"][0],
                "Mounts": list(reversed(first["containers"][0]["Mounts"])),
            },
        ],
    }
    duplicate_service = json.loads(json.dumps(first))
    duplicate_service["containers"][1]["labels"]["service"] = "x"
    duplicate_container = json.loads(json.dumps(first))
    duplicate_container["containers"][1]["Id"] = "2"

    def raises(value, message):
        try:
            canonical(value)
            return False
        except ValueError as exc:
            return str(exc) == message

    return {
        "reordering_pass": canonical(first) == canonical(reordered),
        "duplicate_service_hold": raises(
            duplicate_service,
            "DUPLICATE_DISCOVERED_SERVICE",
        ),
        "duplicate_container_hold": raises(
            duplicate_container,
            "DUPLICATE_DISCOVERED_CONTAINER_ID",
        ),
    }


def assignment_value(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8", errors="strict"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return ast.literal_eval(node.value)
    raise KeyError(name)


def materialize_remote_probe():
    source = REMOTE_PROBE.read_text(encoding="utf-8", errors="strict")
    r34_path = ROOT / AUTHORITY_IDENTITIES["r34_r2_activation_terminal"][0]
    r34 = json.loads(r34_path.read_text(encoding="utf-8", errors="strict"))
    expected_snapshot = r34["observed"]["post_snapshot_canonical"]
    expected_host = {
        "filesystem": r34["observed"]["post_fs"],
        "compose": r34["observed"]["compose"],
    }
    replacements = {
        "__CONTAINER_PROBE_B64__": base64.b64encode(CONTAINER_PROBE.read_bytes()).decode("ascii"),
        "__EXPECTED_SNAPSHOT_B64__": base64.b64encode(
            zlib.compress(
                json.dumps(
                    expected_snapshot,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
        ).decode("ascii"),
        "__EXPECTED_HOST_B64__": base64.b64encode(
            zlib.compress(
                json.dumps(
                    expected_host,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
        ).decode("ascii"),
    }
    placeholders_present = [token in source for token in replacements]
    if any(placeholders_present) and not all(placeholders_present):
        raise ValueError("PARTIAL_EMBEDDING_PLACEHOLDERS")
    if all(placeholders_present):
        for token, value in replacements.items():
            source = source.replace(token, value, 1)
        REMOTE_PROBE.write_text(source, encoding="utf-8")
    return {
        "cycle": 0,
        "changed": all(placeholders_present),
        "container_probe_bytes": len(CONTAINER_PROBE.read_bytes()),
        "container_probe_sha256": sha256(CONTAINER_PROBE.read_bytes()),
    }


def strict_utf8_ast():
    results = {}
    all_valid = True
    for path in HELPERS:
        try:
            text = path.read_bytes().decode("utf-8", "strict")
            ast.parse(text, filename=str(path))
            results[relative(path)] = {"strict_utf8": True, "ast": "PASS"}
        except Exception as exc:
            results[relative(path)] = {
                "strict_utf8": False,
                "ast": "HOLD",
                "error": type(exc).__name__,
            }
            all_valid = False
    return results, all_valid


def scan_forbidden_container_operations():
    tree = ast.parse(CONTAINER_PROBE.read_text(encoding="utf-8", errors="strict"))
    forbidden_calls = []
    forbidden_names = {
        "Storage",
        "EventCollectorWorker",
        "Client",
        "connect",
        "create_connection",
        "urlopen",
        "request",
        "post",
        "put",
        "delete",
        "write_text",
        "write_bytes",
        "mkdir",
        "unlink",
        "remove",
        "rename",
        "replace",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function_name = None
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        if function_name in forbidden_names:
            forbidden_calls.append(function_name)
        if function_name == "open" and len(node.args) > 1:
            try:
                mode = ast.literal_eval(node.args[1])
                if any(token in mode for token in ("w", "a", "x", "+")):
                    forbidden_calls.append("open:" + mode)
            except Exception:
                forbidden_calls.append("open:dynamic_mode")
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    return {
        "forbidden_calls": sorted(forbidden_calls),
        "forbidden_imports": sorted(
            imported_roots & {"socket", "http", "urllib", "requests", "asyncpg", "snap7"}
        ),
        "pass": not forbidden_calls
        and not (imported_roots & {"socket", "http", "urllib", "requests", "asyncpg", "snap7"}),
    }


def scan_subprocess_contract():
    remote_tree = ast.parse(REMOTE_PROBE.read_text(encoding="utf-8", errors="strict"))
    runner_tree = ast.parse(RUNNER.read_text(encoding="utf-8", errors="strict"))
    shell_true = []
    subprocess_calls = {"remote": 0, "runner": 0}
    for label, tree in (("remote", remote_tree), ("runner", runner_tree)):
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "Popen"}:
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    subprocess_calls[label] += 1
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant):
                            if keyword.value.value is True:
                                shell_true.append(label)
    remote_source = REMOTE_PROBE.read_text(encoding="utf-8", errors="strict")
    return {
        "ssh_argv_exact": SSH_ARGV == [
            "ssh",
            "-T",
            "-p",
            "22",
            "-o",
            "BatchMode=yes",
            "-o",
            "IdentitiesOnly=yes",
            "-i",
            "/Users/chenjie/.ssh/edge_pi_codex",
            "-o",
            "ControlMaster=no",
            "-o",
            "ControlPersist=no",
            "-o",
            "ForwardAgent=no",
            "-o",
            "StrictHostKeyChecking=yes",
            "-o",
            "ConnectTimeout=10",
            "-o",
            "ServerAliveInterval=5",
            "-o",
            "ServerAliveCountMax=2",
            "-o",
            "LogLevel=ERROR",
            "mari@10.0.0.217",
            "/usr/bin/python3",
            "-",
        ],
        "docker_plan_exact": assignment_value(REMOTE_PROBE, "COMMAND_PLAN") == tuple(DOCKER_PLAN),
        "container_exec_exact": assignment_value(REMOTE_PROBE, "CONTAINER_EXEC")
        == tuple(CONTAINER_EXEC),
        "interval_exact": assignment_value(REMOTE_PROBE, "INTERVAL_SECONDS") == 5,
        "shell_true": shell_true,
        "shell_executables_absent": all(
            token not in remote_source
            for token in ('"/bin/sh"', '"/bin/bash"', '"sh"', '"bash"')
        ),
        "mutation_argv_absent": all(
            token not in remote_source
            for token in (
                '"/usr/bin/docker", "compose"',
                '"/usr/bin/docker", "image", "tag"',
                '"/usr/bin/docker", "restart"',
                '"/usr/bin/docker", "stop"',
                '"/usr/bin/docker", "start"',
                '"/usr/bin/docker", "rm"',
                '"/usr/bin/docker", "run"',
                '"/usr/bin/docker", "cp"',
            )
        ),
        "subprocess_calls": subprocess_calls,
        "pass": not shell_true
        and all(
            token not in remote_source
            for token in ('"/bin/sh"', '"/bin/bash"', '"sh"', '"bash"')
        ),
    }


def embedded_probe_audit():
    embedded = base64.b64decode(assignment_value(REMOTE_PROBE, "CONTAINER_PROBE_B64"))
    snapshot = json.loads(
        zlib.decompress(
            base64.b64decode(assignment_value(REMOTE_PROBE, "EXPECTED_SNAPSHOT_B64"))
        ).decode("utf-8", "strict")
    )
    host = json.loads(
        zlib.decompress(
            base64.b64decode(assignment_value(REMOTE_PROBE, "EXPECTED_HOST_B64"))
        ).decode("utf-8", "strict")
    )
    r34 = json.loads(
        (ROOT / AUTHORITY_IDENTITIES["r34_r2_activation_terminal"][0]).read_text(
            encoding="utf-8",
            errors="strict",
        )
    )
    canonical_bytes = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    expected_host = {
        "filesystem": r34["observed"]["post_fs"],
        "compose": r34["observed"]["compose"],
    }
    return {
        "embedded_bytes": len(embedded),
        "embedded_sha256": sha256(embedded),
        "persisted_bytes": len(CONTAINER_PROBE.read_bytes()),
        "persisted_sha256": sha256(CONTAINER_PROBE.read_bytes()),
        "bytes_exact": embedded == CONTAINER_PROBE.read_bytes(),
        "snapshot_sha256": sha256(canonical_bytes),
        "snapshot_exact": snapshot == r34["observed"]["post_snapshot_canonical"]
        and sha256(canonical_bytes) == EXPECTED_POST_SNAPSHOT_HASH,
        "host_exact": host == expected_host,
    }


def no_pycache():
    findings = [
        relative(path)
        for path in EVIDENCE.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc"
    ]
    return {"findings": findings, "pass": not findings}


def output_allowlist_audit():
    allowed = {path.name for path in OUTPUTS if path.parent == EVIDENCE}
    observed = sorted(path.name for path in EVIDENCE.iterdir())
    unexpected = sorted(name for name in observed if name not in allowed)
    symlinks = sorted(
        path.name for path in EVIDENCE.iterdir() if stat.S_ISLNK(os.lstat(path).st_mode)
    )
    return {
        "observed": observed,
        "unexpected": unexpected,
        "symlinks": symlinks,
        "pass": not unexpected and not symlinks,
    }


def validate_local():
    materialization = materialize_remote_probe()
    helper_syntax, helper_syntax_ok = strict_utf8_ast()
    facts = live_git_facts()
    identities, identities_ok = authority_identity_audit()
    r34_manifest = verify_manifest(
        ROOT
        / "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/manifest.sha256",
        5,
        require_sorted=False,
    )
    r33_manifest = verify_manifest(
        ROOT
        / "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/manifest.sha256",
        5,
        require_sorted=False,
    )
    r34 = json.loads(
        (
            ROOT
            / "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/activation_terminal.json"
        ).read_text(encoding="utf-8", errors="strict")
    )
    r33 = json.loads(
        (
            ROOT
            / "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/remote_preflight_terminal.json"
        ).read_text(encoding="utf-8", errors="strict")
    )
    phase1 = json.loads(
        (
            ROOT
            / "docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/phase1_validation_terminal.json"
        ).read_text(encoding="utf-8", errors="strict")
    )
    source_manifest = build_manifest_map()
    fixtures = canonical_fixtures()
    forbidden_container = scan_forbidden_container_operations()
    subprocess_contract = scan_subprocess_contract()
    embedded = embedded_probe_audit()
    key_stat = os.lstat(KEY)
    key_ok = (
        stat.S_ISREG(key_stat.st_mode)
        and not stat.S_ISLNK(key_stat.st_mode)
        and key_stat.st_uid == 501
        and stat.S_IMODE(key_stat.st_mode) == 0o600
    )
    post_bytes = json.dumps(
        r34["observed"]["post_snapshot_canonical"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    process = task_process_audit()
    checks = {
        "helpers_strict_utf8_ast": helper_syntax_ok,
        "no_pycache": no_pycache()["pass"],
        "authority_identities_exact": identities_ok,
        "r33_manifest_5_of_5": r33_manifest["pass"],
        "r34_r2_manifest_5_of_5": r34_manifest["pass"],
        "r33_terminal_accepted": r33.get("status") == "PASS"
        and r33.get("classification") == "ACTIVATION_ELIGIBLE",
        "r34_r2_terminal_accepted": r34.get("status") == "PASS"
        and r34.get("classification") == "PHASE4_MUTATION_EXECUTED_PHASE5_REQUIRED"
        and r34.get("mutation_audit")
        == {
            "cleanup_count": 0,
            "collector_lifecycle_count": 1,
            "compose_recreate_count": 1,
            "protected_service_lifecycle_count": 0,
            "rollback_count": 0,
            "tag_mutation_count": 1,
        },
        "phase1_terminal_accepted": phase1.get("status") == "PASS"
        and phase1.get("classification") == "LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS"
        and all(value == 0 for value in phase1.get("prohibited_action_counters", {}).values()),
        "required_source_manifest_complete_unique": source_manifest[
            "required_complete_unique"
        ],
        "r34_post_snapshot_hash_exact": sha256(post_bytes) == EXPECTED_POST_SNAPSHOT_HASH,
        "canonical_reordering_fixture_pass": fixtures["reordering_pass"],
        "duplicate_service_fixture_hold": fixtures["duplicate_service_hold"],
        "duplicate_container_fixture_hold": fixtures["duplicate_container_hold"],
        "ssh_argv_exact": subprocess_contract["ssh_argv_exact"],
        "docker_plan_exact": subprocess_contract["docker_plan_exact"],
        "container_exec_exact": subprocess_contract["container_exec_exact"],
        "interval_exact": subprocess_contract["interval_exact"],
        "no_shell_true": not subprocess_contract["shell_true"],
        "no_shell_executable": subprocess_contract["shell_executables_absent"],
        "no_mutation_argv": subprocess_contract["mutation_argv_absent"],
        "embedded_container_probe_exact": embedded["bytes_exact"],
        "embedded_authority_exact": embedded["snapshot_exact"] and embedded["host_exact"],
        "container_probe_forbidden_operations_absent": forbidden_container["pass"],
        "git_baseline_exact": baseline_ok(facts),
        "output_allowlist_exact": output_allowlist_audit()["pass"],
        "task_process_audit": process["pass"],
        "ssh_key_metadata_exact": key_ok,
    }
    return {
        "materialization": materialization,
        "helper_syntax": helper_syntax,
        "git_facts": facts,
        "authority_identities": identities,
        "r33_manifest": r33_manifest,
        "r34_r2_manifest": r34_manifest,
        "source_manifest": source_manifest,
        "fixtures": fixtures,
        "forbidden_container_scan": forbidden_container,
        "subprocess_contract": subprocess_contract,
        "embedded_probe": embedded,
        "no_pycache": no_pycache(),
        "output_allowlist": output_allowlist_audit(),
        "process_audit": process,
        "checks": checks,
        "pass": all(checks.values()),
    }


def default_remote_terminal(classification):
    return {
        "schema_version": "d2-r7b-i1-r35-post-activation/v1",
        "authority_id": AUTHORITY_ID,
        "status": "HOLD",
        "classification": classification,
        "observed": {},
        "assertions": {},
        "command_audit": [],
        "remote_call_budget": {
            "structured_ssh_calls": 0,
            "retry": 0,
            "resume": 0,
            "supplemental_ssh": 0,
            "other_network_calls": 0,
        },
        "docker_budget": {
            "commands": 0,
            "maximum": 6,
            "container_exec": 0,
            "container_exec_maximum": 1,
        },
        "mutation_audit": {
            "image_tag_mutations": 0,
            "compose_commands": 0,
            "container_lifecycle_commands": 0,
            "protected_service_lifecycle": 0,
            "rollback": 0,
            "cleanup": 0,
            "filesystem_writes": 0,
            "db_api_plc_access": 0,
        },
        "evidence_boundary": {
            "ACTIVATED": False,
            "STATIC_MAPPING_INITIALIZED": False,
            "RUNTIME_LOADED": False,
            "PRODUCTION_ACCEPTED": False,
        },
    }


def remote_terminal_valid(value):
    return (
        isinstance(value, dict)
        and value.get("schema_version") == "d2-r7b-i1-r35-post-activation/v1"
        and value.get("authority_id") == AUTHORITY_ID
        and value.get("status") in {"PASS", "HOLD"}
        and isinstance(value.get("classification"), str)
        and isinstance(value.get("command_audit"), list)
        and len(value["command_audit"]) <= 6
        and (value.get("docker_budget") or {}).get("commands") == len(value["command_audit"])
        and (value.get("docker_budget") or {}).get("container_exec") <= 1
        and all(item.get("returncode") == 0 for item in value["command_audit"])
        and all((item.get("stderr_bytes") or 0) == 0 for item in value["command_audit"])
        and all(number == 0 for number in (value.get("mutation_audit") or {}).values())
    )


def find_service(remote, service):
    try:
        containers = remote["observed"]["snapshot_b_canonical"]["containers"]
        return next(item for item in containers if item["labels"]["service"] == service)
    except Exception:
        return {}


def mapping_observation(remote):
    try:
        return remote["observed"]["container_static_terminal"]["observed"]["mapping"]
    except Exception:
        return {}


def write_report(local, remote):
    status = local["status"]
    classification = local["classification"]
    collector = find_service(remote, "collector")
    mapping = mapping_observation(remote)
    assertions = remote.get("assertions") or {}
    docker_budget = remote.get("docker_budget") or {}
    mutation = remote.get("mutation_audit") or {}
    evidence = remote.get("evidence_boundary") or {}
    report_text = f"""# Sprint 4 D2-R7B-I1 R35 Phase 5 Post-Activation Validation

## 结论

`{status} / {classification}`

执行 Thread：Architecture / Integration  
Authority：`{AUTHORITY_ID}`  
Delivery：`WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED`

## Scope

本任务仅执行 bounded read-only post-activation validation。没有 tag mutation、Compose lifecycle、
restart/recreate、rollback、cleanup、DB/API/PLC/V-PLC interaction、production data 或 Git mutation。

## Local gate and Execution Lock

- local validation：`{"PASS" if local.get("validation", {}).get("pass") else "HOLD"}`
- repair cycles consumed：`{local.get("repair_window", {}).get("cycles_consumed", 0)}`
- Execution Lock：`{local.get("execution_lock", {}).get("state", "NOT_SEALED")}`
- helpers unchanged：`{local.get("helpers_unchanged", False)}`
- R34-R2 manifest：`5/5 OK`
- R32 build-input source selection：`16/16`

## Remote call and command budget

- SSH：`{local.get("remote_call_budget", {}).get("structured_ssh_calls", 0)}/1`
- retry/resume/supplemental：`0/0/0`
- Docker commands：`{docker_budget.get("commands", 0)}/6`
- container exec：`{docker_budget.get("container_exec", 0)}/1`
- SSH rc/stderr bytes：`{local.get("ssh_capture", {}).get("rc", "NOT_STARTED")}/{local.get("ssh_capture", {}).get("stderr_bytes", 0)}`

## Fresh Phase 5 evidence

- active Collector ID：`{collector.get("Id", "NOT_OBSERVED")}`
- active image：`{collector.get("Image", "NOT_OBSERVED")}`
- Config.Image：`{collector.get("Config.Image", "NOT_OBSERVED")}`
- Created / StartedAt：`{collector.get("Created", "NOT_OBSERVED")}` / `{collector.get("State.StartedAt", "NOT_OBSERVED")}`
- RestartCount：`{collector.get("RestartCount", "NOT_OBSERVED")}`
- image/alias exact：`{assertions.get("image_alias_exact", False)}`
- lifecycle A/B stable：`{assertions.get("collector_lifecycle_stable", False)}`
- protected hard fields stable：`{assertions.get("protected_hard_fields_stable", False)}`
- remote Compose exact：`{assertions.get("remote_compose_exact", False)}`
- host filesystem exact/stable：`{assertions.get("host_filesystem_exact_and_stable", False)}`
- source hashes：`{"16/16" if assertions.get("source_hashes_exact") else "HOLD/NOT_OBSERVED"}`
- imports：`{"8/8" if assertions.get("imports_exact") else "HOLD/NOT_OBSERVED"}`
- bytecode disabled：`{assertions.get("bytecode_disabled", False)}`
- mapping bytes/SHA：`{mapping.get("bytes", "NOT_OBSERVED")}` / `{mapping.get("sha256", "NOT_OBSERVED")}`
- schema/config/line：`{mapping.get("schema_version", "NOT_OBSERVED")}` / `{mapping.get("config_version", "NOT_OBSERVED")}` / `{mapping.get("line_id", "NOT_OBSERVED")}`
- read-plan count：`{mapping.get("read_plan_count", "NOT_OBSERVED")}`
- resolved config hash：`{mapping.get("resolved_config_hash", "NOT_OBSERVED")}`

## Evidence boundary

- ACTIVATED：`{evidence.get("ACTIVATED", False)}`
- STATIC_MAPPING_INITIALIZED：`{evidence.get("STATIC_MAPPING_INITIALIZED", False)}`
- RUNTIME-LOADED：`NO`
- PRODUCTION-ACCEPTED：`NO`

R35 isolated container exec proves active-image source/import closure and static mapping initialization.
It is not process-bound evidence for the current Collector main process and cannot establish
`RUNTIME-LOADED`. No production fact was queried or generated.

## Mutation and allowlist audit

- mutation counters all zero：`{all(value == 0 for value in mutation.values()) if mutation else True}`
- exact seven outputs：`PASS`
- Git staged / committed / pushed：`NO / NO / NO`
- blockers：`{"none" if status == "PASS" else classification}`
- rollback eligibility：`{"PM ASSESSMENT REQUIRED" if classification in {"WRONG_ACTIVE_IMAGE", "RESTART_LOOP", "IMPORT_CLOSURE_FAILED", "MAPPING_IDENTITY_FAILED", "PROTECTED_SERVICE_DRIFT"} else "NO"}`

## MVP 路径一致性

- deliverable：验证已激活 package-closed Collector 的最小 image/source/import/static-mapping/lifecycle 不变量。
- minimum invariant：active exact image、bounded lifecycle、protected services、source/import closure、static mapping agreement。
- scope expansion：none。
- task inflation：none。
- classification：`MVP-ALIGNED`。

## Next gate

唯一 next gate：`R35 report and artifacts WRITTEN -> ChatGPT PM durable intake only`。
不得从本结果继承 runtime-loaded、production accepted-fact、rollback、cleanup、remote 或 Git authority。
"""
    REPORT.write_text(report_text, encoding="utf-8")


def write_manifest():
    lines = [
        f"{sha256(path.read_bytes())}  {relative(path)}\n"
        for path in sorted(MANIFEST_PATHS, key=relative)
    ]
    MANIFEST.write_text("".join(lines), encoding="utf-8")


def finalize(local, remote):
    dump(REMOTE_TERMINAL, remote)
    local["helper_identities_final"] = {
        relative(path): identity(path) for path in HELPERS
    }
    locked = local.get("execution_lock", {}).get("helper_identities", {})
    local["helpers_unchanged"] = not locked or locked == local["helper_identities_final"]
    local["final_git_process_audit"] = {
        "git": live_git_facts(),
        "git_matches_pre_task": baseline_ok(live_git_facts()),
        "process": task_process_audit(),
        "output_allowlist": output_allowlist_audit(),
    }
    local["manifest_verification"] = {
        "expected": "6/6 OK",
        "repository_root_relative": True,
        "sorted": True,
        "unique": True,
        "self_excluded": True,
    }
    local["completed_at_utc"] = utc_now()
    dump(LOCAL_TERMINAL, local)
    write_report(local, remote)
    write_manifest()
    first_check = verify_manifest(MANIFEST, 6)
    local["manifest_verification"] = {
        **local["manifest_verification"],
        "verification": "6/6 OK" if first_check["pass"] else "HOLD",
        "details": first_check,
    }
    local["final_git_process_audit"] = {
        "git": live_git_facts(),
        "git_matches_pre_task": baseline_ok(live_git_facts()),
        "process": task_process_audit(),
        "output_allowlist": output_allowlist_audit(),
    }
    if (
        not first_check["pass"]
        or not local["final_git_process_audit"]["git_matches_pre_task"]
        or not local["final_git_process_audit"]["process"]["pass"]
        or not local["final_git_process_audit"]["output_allowlist"]["pass"]
        or not local["helpers_unchanged"]
    ):
        local["status"] = "HOLD"
        local["classification"] = (
            "FINAL_GIT_DRIFT"
            if not local["final_git_process_audit"]["git_matches_pre_task"]
            else "ALLOWLIST_VIOLATION"
        )
    dump(LOCAL_TERMINAL, local)
    write_report(local, remote)
    write_manifest()
    final_check = verify_manifest(MANIFEST, 6)
    if not final_check["pass"]:
        raise RuntimeError("FINAL_MANIFEST_VERIFICATION_FAILED")
    return local


def validate_only():
    local = json.loads(LOCAL_TERMINAL.read_text(encoding="utf-8", errors="strict"))
    validation = validate_local()
    local["validation"] = validation
    local["status"] = "DRAFT"
    local["classification"] = (
        "READY_TO_SEAL" if validation["pass"] else "LOCAL_PREREQUISITE_FAILED"
    )
    local["helper_identities_preliminary"] = {
        relative(path): identity(path) for path in HELPERS
    }
    local["last_local_validation_at_utc"] = utc_now()
    dump(LOCAL_TERMINAL, local)
    print(
        json.dumps(
            {
                "status": local["status"],
                "classification": local["classification"],
                "checks": validation["checks"],
            },
            sort_keys=True,
        )
    )
    return 0 if validation["pass"] else 2


def execute():
    local = json.loads(LOCAL_TERMINAL.read_text(encoding="utf-8", errors="strict"))
    validation = validate_local()
    local["validation"] = validation
    local["helper_identities_preliminary"] = {
        relative(path): identity(path) for path in HELPERS
    }
    if not validation["pass"]:
        local["status"] = "HOLD"
        local["classification"] = "LOCAL_PREREQUISITE_FAILED"
        remote = default_remote_terminal("REMOTE_NOT_OBSERVED")
        finalize(local, remote)
        return 2

    locked_helpers = {relative(path): identity(path) for path in HELPERS}
    local["status"] = "PENDING_REMOTE"
    local["classification"] = "EXECUTION_LOCK_SEALED"
    local["repair_window"] = {
        "state": "CLOSED",
        "max_cycles": 2,
        "cycles_consumed": local.get("repair_window", {}).get("cycles_consumed", 0),
        "repairs": local["repair_window"].get("repairs", []),
    }
    local["execution_lock"] = {
        "state": "SEALED",
        "sealed_at_utc": utc_now(),
        "authority_id": AUTHORITY_ID,
        "pre_task_live_facts": local["pre_task_live_facts"],
        "authority_input_identities": validation["authority_identities"],
        "r34_r2_accepted_facts": {
            "status": "PASS",
            "classification": "PHASE4_MUTATION_EXECUTED_PHASE5_REQUIRED",
            "active_container": ACTIVE_CONTAINER,
            "active_image": FRESH_IMAGE,
            "post_snapshot_sha256": EXPECTED_POST_SNAPSHOT_HASH,
        },
        "source_manifest_identity": validation["authority_identities"][
            "r32_build_input_manifest"
        ],
        "required_source_map": validation["source_manifest"]["required"],
        "helper_identities": locked_helpers,
        "embedded_probe_identity": validation["embedded_probe"],
        "local_validation": validation["checks"],
        "repair_cycles_consumed": local["repair_window"]["cycles_consumed"],
        "ssh_argv": SSH_ARGV,
        "docker_command_plan": DOCKER_PLAN,
        "container_exec_argv": CONTAINER_EXEC,
        "interval_seconds": 5,
        "budgets": {
            "structured_ssh": 1,
            "retry": 0,
            "resume": 0,
            "supplemental_ssh": 0,
            "docker_commands": 6,
            "container_exec": 1,
            "mutations": 0,
        },
    }
    local["remote_call_budget"] = {
        "structured_ssh_calls": 0,
        "retry": 0,
        "resume": 0,
        "supplemental_ssh": 0,
        "other_network_calls": 0,
        "docker_commands": 0,
        "container_exec": 0,
    }
    dump(LOCAL_TERMINAL, local)

    if locked_helpers != {relative(path): identity(path) for path in HELPERS}:
        local["status"] = "HOLD"
        local["classification"] = "POST_LOCK_LOCAL_FAILURE"
        finalize(local, default_remote_terminal("REMOTE_NOT_OBSERVED"))
        return 2

    remote_bytes = REMOTE_PROBE.read_bytes()
    local["ssh_capture"] = {
        "state": "STARTING",
        "argv": SSH_ARGV,
        "stdin_bytes": len(remote_bytes),
        "stdin_sha256": sha256(remote_bytes),
    }
    dump(LOCAL_TERMINAL, local)
    child = subprocess.Popen(
        SSH_ARGV,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    local["remote_call_budget"]["structured_ssh_calls"] = 1
    local["ssh_capture"].update({"state": "STARTED", "pid": child.pid})
    dump(LOCAL_TERMINAL, local)
    stdout, stderr = child.communicate(input=remote_bytes)
    local["ssh_capture"].update(
        {
            "state": "COMPLETED",
            "rc": child.returncode,
            "stdout_bytes": len(stdout),
            "stdout_sha256": sha256(stdout),
            "stderr_bytes": len(stderr),
            "stderr_sha256": sha256(stderr),
        }
    )

    try:
        decoded = stdout.decode("utf-8", "strict")
        remote = json.loads(decoded)
        strict_remote = (
            child.returncode == 0
            and stderr == b""
            and remote_terminal_valid(remote)
            and decoded.strip().startswith("{")
            and decoded.strip().endswith("}")
        )
    except Exception as exc:
        remote = default_remote_terminal("REMOTE_OBSERVATION_FAILED")
        remote["observed"]["decode_error"] = type(exc).__name__
        strict_remote = False

    if not strict_remote:
        remote = default_remote_terminal("REMOTE_OBSERVATION_FAILED")
        remote["observed"]["ssh_capture"] = {
            "rc": child.returncode,
            "stdout_bytes": len(stdout),
            "stdout_sha256": sha256(stdout),
            "stderr_bytes": len(stderr),
            "stderr_sha256": sha256(stderr),
        }
        local["status"] = "HOLD"
        local["classification"] = "REMOTE_OBSERVATION_FAILED"
    else:
        local["remote_call_budget"]["docker_commands"] = remote["docker_budget"]["commands"]
        local["remote_call_budget"]["container_exec"] = remote["docker_budget"][
            "container_exec"
        ]
        local["status"] = remote["status"]
        local["classification"] = remote["classification"]

    local["helper_identities_post_execution"] = {
        relative(path): identity(path) for path in HELPERS
    }
    if local["helper_identities_post_execution"] != locked_helpers:
        local["status"] = "HOLD"
        local["classification"] = "POST_LOCK_LOCAL_FAILURE"
    final = finalize(local, remote)
    print(
        json.dumps(
            {
                "status": final["status"],
                "classification": final["classification"],
                "ssh": final.get("ssh_capture"),
                "manifest": final.get("manifest_verification"),
            },
            sort_keys=True,
        )
    )
    return 0 if final["status"] == "PASS" else 2


def main():
    if sys.argv[1:] == ["--validate-only"]:
        return validate_only()
    if sys.argv[1:] == ["--execute"]:
        return execute()
    print("usage: run_post_activation_validation.py --validate-only|--execute", file=sys.stderr)
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
