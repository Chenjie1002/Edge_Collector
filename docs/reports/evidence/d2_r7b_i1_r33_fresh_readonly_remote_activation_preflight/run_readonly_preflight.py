#!/usr/bin/env python3
"""R33 exact local runner.  It owns the sole structured SSH child."""
import ast
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

AUTHORITY_ID = "PM-D2-R7B-I1-R33-FRESH-READONLY-REMOTE-ACTIVATION-PREFLIGHT-260729-2001"
ROOT = Path("/Users/chenjie/Documents/MES/edge-mes-demo")
EVIDENCE = ROOT / "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight"
RUNNER = EVIDENCE / "run_readonly_preflight.py"
PROBE = EVIDENCE / "remote_readonly_probe.py"
LOCAL = EVIDENCE / "local_prerequisite_terminal.json"
REMOTE = EVIDENCE / "remote_preflight_terminal.json"
REPORT = ROOT / "docs/reports/sprint4_d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight.md"
MANIFEST = EVIDENCE / "manifest.sha256"
KEY = Path("/Users/chenjie/.ssh/edge_pi_codex")
EXPECTED_DIRTY = [".gitignore", "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh", "docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256", "docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256", "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py", "docs/thread_handoff/pm_operating_rules.md"]
IDENTITIES = {"docs/thread_handoff/chatgpt_pm_handoff_260729-1945.md": (13999, "ad474117600b2f9444d6a5dfa96f9a719bbb03777b161fb40960c53ff45c4a89"), "docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md": (8525, "d4dcd835cf1152bd4585226f6bcb86533040e5481539dd669c53c170a7531df3"), "docs/reports/sprint4_d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution.md": (8429, "0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff"), "docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md": (45360, "bd5b65ac08dcacfd0fc14a639626d807f28d429f1038a99aa124cd6ce85db894"), "config/mapping.yaml": (7112, "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"), "docker-compose.yml": (5698, "c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66")}


def digest(path):
    data = path.read_bytes()
    s = os.lstat(path)
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "regular": stat.S_ISREG(s.st_mode), "symlink": stat.S_ISLNK(s.st_mode)}


def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {"argv": ["git", *args], "returncode": p.returncode, "stdout": p.stdout.decode("utf-8", "strict").strip(), "stderr": p.stderr.decode("utf-8", "strict").strip()}


def process_audit():
    terms = ["PM-" + "D2-R7B-I1-R33-FRESH-READONLY-REMOTE-ACTIVATION-PREFLIGHT-260729-2001", "run_" + "readonly_preflight.py", "remote_" + "readonly_probe.py"]
    text = subprocess.run(["ps", "-ax", "-o", "pid=,ppid=,command="], stdout=subprocess.PIPE, check=True).stdout.decode("utf-8", "strict")
    rows = []
    for line in text.splitlines():
        fields = line.strip().split(None, 2)
        if len(fields) == 3:
            rows.append((int(fields[0]), int(fields[1]), line, fields[2]))
    parents = {pid: ppid for pid, ppid, _, _ in rows}
    ancestors = {os.getpid()}
    current = os.getpid()
    while current in parents and parents[current] not in ancestors and parents[current] > 0:
        current = parents[current]
        ancestors.add(current)
    found = []
    for pid, _, line, command_text in rows:
        if pid not in ancestors and any(term in command_text for term in terms):
            found.append(line)
    return {"matches": found, "pass": not found, "self_and_ancestor_pids_excluded": sorted(ancestors)}


def validate_remote(value):
    required = {"schema_version": str, "authority_id": str, "status": str, "classification": str, "observed": dict, "assertions": dict, "mutation_audit": dict, "command_audit": list}
    if not isinstance(value, dict) or any(not isinstance(value.get(k), t) for k, t in required.items()):
        return False, "REMOTE_SCHEMA_INVALID"
    if value["authority_id"] != AUTHORITY_ID or value["status"] not in ("PASS", "HOLD"):
        return False, "REMOTE_SCHEMA_INVALID"
    if any(not isinstance(v, int) or v != 0 for v in value["mutation_audit"].values()):
        return False, "REMOTE_MUTATION_AUDIT_NONZERO"
    if len(value["command_audit"]) > 11 or any(not isinstance(x, dict) or not isinstance(x.get("argv"), list) for x in value["command_audit"]):
        return False, "DOCKER_COMMAND_BUDGET_EXCEEDED"
    return True, value["classification"]


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def local_prerequisite():
    assertions, observed = {}, {}
    facts = {name: git(*cmd) for name, cmd in {"root": ("rev-parse", "--show-toplevel"), "branch": ("rev-parse", "--abbrev-ref", "HEAD"), "head": ("rev-parse", "HEAD"), "origin_main": ("rev-parse", "origin/main"), "head_parent": ("rev-parse", "HEAD^"), "ahead_behind": ("rev-list", "--left-right", "--count", "HEAD...origin/main"), "dirty": ("diff", "--name-only"), "cached": ("diff", "--cached", "--name-only"), "diff_check": ("diff", "--check"), "cached_check": ("diff", "--cached", "--check")}.items()}
    observed["git"] = facts
    assertions["baseline"] = facts["root"]["stdout"] == str(ROOT) and facts["branch"]["stdout"] == "main" and facts["head"]["stdout"] == "ac33e6bae449ecdd9b77a53daaf7271f14133000" and facts["origin_main"]["stdout"] == "ac33e6bae449ecdd9b77a53daaf7271f14133000" and facts["head_parent"]["stdout"] == "66563677d3d1129fbc79c2c284b5f6d8b62f1932" and facts["ahead_behind"]["stdout"] == "0\t0"
    assertions["tracked_dirty_set"] = facts["dirty"]["stdout"].splitlines() == EXPECTED_DIRTY
    assertions["cached_index_empty"] = facts["cached"]["stdout"] == ""
    assertions["diff_checks"] = all(facts[k]["returncode"] == 0 and facts[k]["stdout"] == "" for k in ("diff_check", "cached_check"))
    identities = {p: digest(ROOT / p) for p in IDENTITIES}
    observed["authority_inputs"] = identities
    assertions["authority_input_identities"] = all(x["regular"] and not x["symlink"] and x["bytes"] == IDENTITIES[p][0] and x["sha256"] == IDENTITIES[p][1] for p, x in identities.items())
    key = os.lstat(KEY)
    observed["ssh_key_metadata"] = {"regular": stat.S_ISREG(key.st_mode), "symlink": stat.S_ISLNK(key.st_mode), "uid": key.st_uid, "mode": format(stat.S_IMODE(key.st_mode), "04o")}
    assertions["ssh_key_metadata"] = observed["ssh_key_metadata"] == {"regular": True, "symlink": False, "uid": 501, "mode": "0600"}
    observed["process_audit"] = process_audit()
    assertions["no_task_owned_process"] = observed["process_audit"]["pass"]
    outputs = {str(p.relative_to(ROOT)): ("ABSENT" if not os.path.lexists(p) else "PRESENT") for p in (REPORT, LOCAL, REMOTE, MANIFEST)}
    observed["remaining_output_preconditions"] = outputs
    assertions["remaining_outputs_absent"] = all(v == "ABSENT" for v in outputs.values())
    helpers = {"runner": digest(RUNNER), "probe": digest(PROBE)}
    observed["helpers_preliminary"] = helpers
    try:
        for path in (RUNNER, PROBE):
            ast.parse(path.read_bytes().decode("utf-8", "strict"), filename=str(path))
        assertions["helper_ast_syntax"] = True
    except (SyntaxError, UnicodeDecodeError):
        assertions["helper_ast_syntax"] = False
    assertions["local_schema_self_check"] = validate_remote({"schema_version": "x", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": "x", "observed": {}, "assertions": {}, "mutation_audit": {"x": 0}, "command_audit": []})[0]
    assertions["mapping_clean_relative_head"] = git("diff", "--quiet", "HEAD", "--", "config/mapping.yaml")["returncode"] == 0
    return observed, assertions, helpers


def main():
    observed, assertions, helper_before = local_prerequisite()
    local = {"schema_version": "d2-r7b-i1-r33-local-prerequisite/v1", "authority_id": AUTHORITY_ID, "project_root": str(ROOT), "observed": observed, "assertions": assertions, "remote_call_budget": {"structured_ssh_calls": 1, "retry": 0, "resume": 0, "supplemental_ssh": 0}, "remote_authority_consumption": "NOT_CONSUMED", "local_mutation_audit": {"git_mutations": 0, "docker_commands": 0, "cleanup": 0, "extra_artifacts": 0}}
    if not all(assertions.values()):
        local.update({"status": "HOLD", "classification": "LOCAL_PREREQUISITE_FAILED"})
        remote = {"schema_version": "d2-r7b-i1-r33-remote-preflight/v1", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": "REMOTE_NOT_OBSERVED", "observed": {}, "assertions": {}, "mutation_audit": {"filesystem_writes": 0, "docker_mutations": 0, "collector_lifecycle": 0, "protected_service_lifecycle": 0, "network_calls_other_than_authorized_ssh": 0}, "command_audit": [], "structured_ssh_calls": 0}
        write(LOCAL, local); write(REMOTE, remote); print(json.dumps({"status": "HOLD", "classification": local["classification"]})); return
    probe_bytes = PROBE.read_bytes()
    ssh = ["ssh", "-T", "-p", "22", "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-i", str(KEY), "-o", "ControlMaster=no", "-o", "ControlPersist=no", "-o", "ForwardAgent=no", "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=2", "-o", "LogLevel=ERROR", "mari@10.0.0.217", "/usr/bin/python3", "-"]
    child = subprocess.run(ssh, input=probe_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    capture = {"returncode": child.returncode, "stdout_bytes": len(child.stdout), "stdout_sha256": hashlib.sha256(child.stdout).hexdigest(), "stderr_bytes": len(child.stderr), "stderr_sha256": hashlib.sha256(child.stderr).hexdigest()}
    local["remote_authority_consumption"] = "CONSUMED"
    local["ssh_capture"] = capture
    try:
        parsed = json.loads(child.stdout.decode("utf-8", "strict"))
        valid, classification = validate_remote(parsed)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed, valid, classification = None, False, "REMOTE_UTF8_OR_JSON_INVALID"
    if child.returncode != 0:
        valid, classification = False, "SSH_FAILED"
    if child.stderr:
        valid, classification = False, "SSH_STDERR_NONEMPTY"
    if not valid:
        remote = {"schema_version": "d2-r7b-i1-r33-remote-preflight/v1", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": classification, "observed": {}, "assertions": {}, "mutation_audit": {"filesystem_writes": 0, "docker_mutations": 0, "collector_lifecycle": 0, "protected_service_lifecycle": 0, "network_calls_other_than_authorized_ssh": 0}, "command_audit": [], "structured_ssh_calls": 1, "ssh_capture": capture}
    else:
        remote = parsed
        remote["structured_ssh_calls"] = 1
        remote["ssh_capture"] = capture
    helper_after = {"runner": digest(RUNNER), "probe": digest(PROBE)}
    local["helpers_final"] = helper_after
    local["assertions"]["helpers_unchanged_after_execution"] = helper_before == helper_after
    local["status"] = "PASS" if valid and remote.get("status") == "PASS" and all(local["assertions"].values()) else "HOLD"
    local["classification"] = "ACTIVATION_ELIGIBLE" if local["status"] == "PASS" else classification
    write(LOCAL, local); write(REMOTE, remote)
    print(json.dumps({"status": local["status"], "classification": local["classification"], "structured_ssh_calls": 1}))


if __name__ == "__main__":
    main()
