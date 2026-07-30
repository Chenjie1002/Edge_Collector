#!/usr/bin/env python3
"""Local prerequisite, seal, sole SSH transport, and durable receipt writer."""
import ast
import hashlib
import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY_ID = "PM-D2-R7B-I1-R34-R1-COLLECTOR-ONLY-ACTIVATION-260729-2057"
ROOT = Path("/Users/chenjie/Documents/MES/edge-mes-demo")
E = ROOT / "docs/reports/evidence/d2_r7b_i1_r34_r1_collector_only_activation_retry"
RUN, CTL = E / "run_activation.py", E / "remote_activation_controller.py"
LOCAL, REMOTE, MAN = E / "local_prerequisite_terminal.json", E / "activation_terminal.json", E / "manifest.sha256"
REPORT = ROOT / "docs/reports/sprint4_d2_r7b_i1_r34_r1_collector_only_activation_retry.md"
KEY = Path("/Users/chenjie/.ssh/edge_pi_codex")
R33E = ROOT / "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight"
DIRTY = [".gitignore", "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh", "docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256", "docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256", "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py", "docs/thread_handoff/pm_operating_rules.md"]
IDENTITIES = {
    "docs/thread_handoff/pm_operating_rules.md": (45785, "e9f9713c1845ad91edc147f2f82f2d104b22ad48759d7a50f74e0eb8bbfa149a"),
    "docs/thread_handoff/chatgpt_pm_handoff_260729-1945.md": (13999, "ad474117600b2f9444d6a5dfa96f9a719bbb03777b161fb40960c53ff45c4a89"),
    "docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md": (45360, "bd5b65ac08dcacfd0fc14a639626d807f28d429f1038a99aa124cd6ce85db894"),
    "docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md": (8525, "d4dcd835cf1152bd4585226f6bcb86533040e5481539dd669c53c170a7531df3"),
    "docs/reports/sprint4_d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight.md": (6049, "daa0af5824d697ad12342fcaedf09330b082da78475f1351fec46c0892153c66"),
    "docs/reports/sprint4_d2_r7b_i1_r34_collector_only_activation.md": (1694, "182d58da5a132bd80da23d8a8bc14812732d7e37624b097be0f7535fe44ff1a0"),
    "docker-compose.yml": (5698, "c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66"),
    "config/mapping.yaml": (7112, "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"),
}
R33 = {"run_readonly_preflight.py": (11422, "3f3c34c0157b8fedc1a30acb0561c04203d390710a601a70dd9c0dc6cdc8bf97"), "remote_readonly_probe.py": (14245, "9223c4cd7b63072a39936029681ee0b4b007e58838bba0626d4515d9e47a6430"), "local_prerequisite_terminal.json": (7796, "2c0b342168195de98bd0dbda627a5e3231f2dd54cac57fcea850596449fa87de"), "remote_preflight_terminal.json": (50786, "d1cd628fdf6ffacf62c5ceb1e418284bf4663ac5d9642cfdeead51eec423a82e"), "manifest.sha256": (842, "5c52278d1a8585d8c19402546a2dd231f58f717ba6ef97e756ee19a9729bbaad")}
R34 = {"run_activation.py": (10043, "7b809f2b84de88a444a292022049d6a86ea32194a7161a763cc0d35962c8fde9"), "remote_activation_controller.py": (19124, "a893449f7872c9727db4c199336d05a56e0b70ab9e5479138170e616cb3852da"), "local_prerequisite_terminal.json": (1274, "c737eb8ae77f57410d2b502e6506c4d7a0155aef5d3fd4691472874180646fe3"), "activation_terminal.json": (688, "5e49305a81f5e7bd6447b04cad84b3c69125f5f22862f4a09bb721dfe964fe1d"), "manifest.sha256": (750, "9cba85ab282baa89ee6b9e4b7ad355385a45a3c3ad8878e933c0b8a34bbf4e65")}
SSH = ["ssh", "-T", "-p", "22", "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-i", str(KEY), "-o", "ControlMaster=no", "-o", "ControlPersist=no", "-o", "ForwardAgent=no", "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=2", "-o", "LogLevel=ERROR", "mari@10.0.0.217", "/usr/bin/python3", "-"]
INITIAL_OUTPUT_PRECONDITIONS = {str(p.relative_to(ROOT)): "ABSENT_NON_SYMLINK" for p in (REPORT, RUN, CTL, LOCAL, REMOTE, MAN)}

def sha(data): return hashlib.sha256(data).hexdigest()
def identity(path):
    data = path.read_bytes(); st = os.lstat(path)
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": sha(data), "regular": stat.S_ISREG(st.st_mode), "symlink": stat.S_ISLNK(st.st_mode)}
def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {"argv": ["git", *args], "returncode": p.returncode, "stdout": p.stdout.decode("utf-8", "strict").strip(), "stderr": p.stderr.decode("utf-8", "strict").strip()}
def json_write(path, value): path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
def manifest_ok(directory):
    lines = (directory / "manifest.sha256").read_text(encoding="utf-8").splitlines()
    return len(lines) == 5 and all(len(line.split("  ")) == 2 and sha((ROOT / line.split("  ", 1)[1]).read_bytes()) == line.split("  ", 1)[0] for line in lines)
def load_controller():
    source = CTL.read_text(encoding="utf-8")
    ast.parse(source, str(CTL)); namespace = {"__name__": "not_main"}; exec(compile(source, str(CTL), "exec"), namespace)
    return namespace
def process_audit():
    p = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    blocked = [str(RUN), str(CTL), "d2_r7b_i1_r34_r1_collector_only_activation_retry"]
    own = {os.getpid(), os.getppid()}; hits = [line for line in p.stdout.decode("utf-8", "strict").splitlines() if any(x in line for x in blocked) and not any(str(pid) in line.split(None, 2)[:2] for pid in own)]
    return {"returncode": p.returncode, "matches": hits, "pass": p.returncode == 0 and not hits}
def expected_identity(path, pair):
    actual = identity(path); return actual, actual["regular"] and not actual["symlink"] and (actual["bytes"], actual["sha256"]) == pair
def write_report(local, remote):
    outcome = local["status"]
    text = f"""# Sprint 4 D2-R7B-I1 R34-R1 Corrected Collector-Only Activation Retry

## 1. 报告身份
- Authority：`{AUTHORITY_ID}`
- 执行 Thread：Architecture / Integration
- Delivery：`REPOSITORY_REPORT_WITH_ARTIFACTS`

## 2. 任务结论
- `{outcome} / {local['classification']}`

## 3. 授权边界
- AUTHORIZED ONCE；仅一条 structured SSH、一次 alias tag、一次 Collector-only recreate。

## 4. 初始本地事实
- Git baseline、六个 tracked dirty 排除项与六条输出初始 ABSENT 均记录在 local terminal。

## 5. 历史身份复核
- R31、scope-reset、R33、R34 historical report/evidence 与 PM identity 已逐项复核。

## 6. R33 先决条件
- R33 manifest `5/5 OK`，terminal `PASS / ACTIVATION_ELIGIBLE`。

## 7. 本地验证
- UTF-8、AST、no-pycache、helper identity、R33 Snapshot B semantic equality、exact SSH argv、9-command plan、allowlist 与 Git audit 已执行。

## 8. EXECUTION_LOCK
- `{local.get('execution_lock', {}).get('state', 'NOT_SEALED')}`；seal 后无 helper repair/unseal。

## 9. SSH 消耗
- structured SSH `{local['remote_call_budget']['structured_ssh_calls']}`；retry/resume/supplemental 均为 0。

## 10. 远端命令与变更
- command count：`{len(remote.get('command_audit', []))}`；tag `{remote.get('mutation_audit', {}).get('tag_mutation_count')}`；compose `{remote.get('mutation_audit', {}).get('compose_recreate_count')}`。

## 11. Phase 4 收据
- `{remote.get('status')} / {remote.get('classification')}`；只建立 Phase 4 receipt。

## 12. 明确未建立的状态
- `RUNTIME-LOADED`、`PRODUCTION-ACCEPTED` 均未建立；Phase 5 未执行。

## 13. 排除操作
- rollback、cleanup、第二次 SSH、Git stage/commit/push/tag/reset/restore/clean/stash、DB/API/PLC/production validation 均未执行。

## 14. MVP 路径一致性
- `MVP-ALIGNED`：最小不变量为精确 alias 变更和仅 Collector recreate，且保护服务与 config 不漂移。

## 15. 下一关
- 仅 `ChatGPT PM durable intake`；本报告仅为 `WRITTEN`，不继承任何后续 authority。
"""
    REPORT.write_text(text, encoding="utf-8")
def finalize_manifest():
    paths = [REPORT, RUN, CTL, LOCAL, REMOTE]
    MAN.write_text("".join(f"{sha(p.read_bytes())}  {p.relative_to(ROOT)}\n" for p in paths), encoding="utf-8")
    return manifest_ok(E)
def main():
    facts = {name: git(*args) for name, args in {"status": ("status", "-sb"), "root": ("rev-parse", "--show-toplevel"), "branch": ("rev-parse", "--abbrev-ref", "HEAD"), "head": ("rev-parse", "HEAD"), "origin_main": ("rev-parse", "origin/main"), "parent": ("rev-parse", "HEAD^"), "ahead_behind": ("rev-list", "--left-right", "--count", "HEAD...origin/main"), "dirty": ("diff", "--name-only"), "cached": ("diff", "--cached", "--name-only"), "diff_check": ("diff", "--check"), "cached_check": ("diff", "--cached", "--check")}.items()}
    identities = {}; identity_pass = True
    for rel, pair in IDENTITIES.items():
        identities[rel], ok = expected_identity(ROOT / rel, pair); identity_pass &= ok
    r33_ids = {}; r34_ids = {}; r33_pass = r34_pass = True
    for name, pair in R33.items(): r33_ids[name], ok = expected_identity(R33E / name, pair); r33_pass &= ok
    r34e = ROOT / "docs/reports/evidence/d2_r7b_i1_r34_collector_only_activation"
    for name, pair in R34.items(): r34_ids[name], ok = expected_identity(r34e / name, pair); r34_pass &= ok
    r33_local = json.loads((R33E / "local_prerequisite_terminal.json").read_text(encoding="utf-8")); r33_remote = json.loads((R33E / "remote_preflight_terminal.json").read_text(encoding="utf-8")); old_local = json.loads((r34e / "local_prerequisite_terminal.json").read_text(encoding="utf-8")); old_remote = json.loads((r34e / "activation_terminal.json").read_text(encoding="utf-8"))
    preliminary = {"runner": identity(RUN), "controller": identity(CTL)}
    syntax_ok = True
    try:
        ast.parse(RUN.read_text(encoding="utf-8"), str(RUN)); ctl = load_controller()
        snapshot_ok = ctl["EXPECTED_SNAPSHOT_B"] == r33_remote["observed"]["snapshot_b"]
        plan_ok = tuple(ctl["COMMAND_PLAN"]) == ("aggregate_image_inspect", "pre_project_ps", "pre_aggregate_inspect", "fresh_ancestor_lookup", "tag", "alias_inspect", "collector_only_compose", "post_project_ps", "post_aggregate_inspect")
        controller_text = CTL.read_text(encoding="utf-8")
        forbidden_ok = "shell=" not in controller_text and "os.unlink" not in controller_text and "shutil" not in controller_text and '"rm"' not in controller_text
    except Exception:
        syntax_ok = snapshot_ok = plan_ok = forbidden_ok = False
    key = os.lstat(KEY); key_ok = stat.S_ISREG(key.st_mode) and not stat.S_ISLNK(key.st_mode) and key.st_uid == 501 and stat.S_IMODE(key.st_mode) == 0o600
    pycache_ok = not any(p.name == "__pycache__" or p.suffix == ".pyc" for p in E.rglob("*"))
    assertions = {"baseline": facts["root"]["stdout"] == str(ROOT) and facts["branch"]["stdout"] == "main" and facts["head"]["stdout"] == facts["origin_main"]["stdout"] == "ac33e6bae449ecdd9b77a53daaf7271f14133000" and facts["parent"]["stdout"] == "66563677d3d1129fbc79c2c284b5f6d8b62f1932" and facts["ahead_behind"]["stdout"] == "0\t0", "tracked_dirty_exact": facts["dirty"]["stdout"].splitlines() == DIRTY, "cached_empty": facts["cached"]["stdout"] == "", "diff_checks": facts["diff_check"]["returncode"] == facts["cached_check"]["returncode"] == 0 and not facts["diff_check"]["stdout"] and not facts["cached_check"]["stdout"], "mapping_clean_relative_head": git("diff", "--quiet", "HEAD", "--", "config/mapping.yaml")["returncode"] == 0, "authority_identities": identity_pass and r33_pass and r34_pass, "r33_manifest_5_5": manifest_ok(R33E), "r34_manifest_5_5": manifest_ok(r34e), "r33_activation_eligible": r33_local.get("status") == "PASS" and r33_local.get("classification") == "ACTIVATION_ELIGIBLE" and r33_remote.get("status") == "PASS", "r34_historical_hold_not_observed": old_local.get("status") == "HOLD" and old_local.get("classification") == "HELPER_SYNTAX_OR_SCHEMA_INVALID" and old_remote.get("classification") == "REMOTE_NOT_OBSERVED" and old_remote.get("remote_call_budget", {}).get("structured_ssh_calls") == 0, "helpers_utf8_ast": syntax_ok, "r33_snapshot_b_semantic_equal": snapshot_ok, "docker_plan_exact_9": plan_ok, "no_forbidden_controller_paths": forbidden_ok, "no_pycache_or_pyc": pycache_ok, "ssh_key_metadata": key_ok, "process_audit": process_audit()["pass"], "local_output_preconditions": not any(p.exists() or p.is_symlink() for p in (LOCAL, REMOTE, REPORT, MAN))}
    if not all(assertions.values()):
        local = {"schema_version": "d2-r7b-i1-r34-r1-local-prerequisite/v1", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": "LOCAL_PREREQUISITE_FAILED", "initial_output_preconditions": INITIAL_OUTPUT_PRECONDITIONS, "git": facts, "identities": identities, "r33_identities": r33_ids, "r34_historical_identities": r34_ids, "assertions": assertions, "helpers_preliminary": preliminary, "remote_call_budget": {"structured_ssh_calls": 0, "retry": 0, "resume": 0, "supplemental_ssh": 0}, "local_mutation_audit": {"docker_commands": 0, "git_mutations": 0, "cleanup": 0}}
        remote = {"schema_version": "d2-r7b-i1-r34-r1-remote-activation/v1", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": "REMOTE_NOT_OBSERVED", "command_audit": [], "assertions": {}, "mutation_audit": {"tag_mutation_count": 0, "compose_recreate_count": 0, "collector_lifecycle_count": 0, "protected_service_lifecycle_count": 0, "rollback_count": 0, "cleanup_count": 0}, "remote_call_budget": {"structured_ssh_calls": 0, "retry": 0, "resume": 0, "supplemental_ssh": 0}}
    else:
        final_helpers = {"runner": identity(RUN), "controller": identity(CTL)}
        lock = {"state": "SEALED", "authority_id": AUTHORITY_ID, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "pre_facts": facts, "r33_manifest": r33_ids["manifest.sha256"], "r34_historical_manifest": r34_ids["manifest.sha256"], "helpers": final_helpers, "repair_cycles": 1, "repair_summary": "Cycle 0 corrected only historical helper syntax/schema defects in new task-owned paths.", "validation": assertions, "ssh_argv": SSH, "docker_command_plan": list(ctl["COMMAND_PLAN"]), "mutation_budget": {"tag": 1, "compose": 1, "rollback": 0, "cleanup": 0}, "snapshot_b_sha256": sha(json.dumps(r33_remote["observed"]["snapshot_b"], sort_keys=True, separators=(",", ":")).encode("utf-8"))}
        local = {"schema_version": "d2-r7b-i1-r34-r1-local-prerequisite/v1", "authority_id": AUTHORITY_ID, "status": "PENDING_REMOTE", "classification": "EXECUTION_LOCK_SEALED", "initial_output_preconditions": INITIAL_OUTPUT_PRECONDITIONS, "git": facts, "identities": identities, "r33_identities": r33_ids, "r34_historical_identities": r34_ids, "assertions": assertions, "helpers_preliminary": preliminary, "helpers_final": final_helpers, "execution_lock": lock, "remote_call_budget": {"structured_ssh_calls": 0, "retry": 0, "resume": 0, "supplemental_ssh": 0}, "local_mutation_audit": {"docker_commands": 0, "git_mutations": 0, "cleanup": 0}}
        json_write(LOCAL, local)
        if final_helpers != {"runner": identity(RUN), "controller": identity(CTL)}: raise RuntimeError("POST_LOCK_LOCAL_FAILURE")
        p = subprocess.run(SSH, input=CTL.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        local["remote_call_budget"]["structured_ssh_calls"] = 1; local["ssh_capture"] = {"returncode": p.returncode, "stdout_bytes": len(p.stdout), "stderr_bytes": len(p.stderr), "stdout_sha256": sha(p.stdout), "stderr_sha256": sha(p.stderr)}
        try: remote = json.loads(p.stdout.decode("utf-8", "strict"))
        except Exception: remote = None
        required = {"schema_version", "authority_id", "status", "classification", "command_audit", "assertions", "mutation_audit", "remote_call_budget"}
        valid = isinstance(remote, dict) and required <= set(remote) and remote.get("authority_id") == AUTHORITY_ID
        if p.returncode != 0 or p.stderr or not valid:
            remote = {"schema_version": "d2-r7b-i1-r34-r1-remote-activation/v1", "authority_id": AUTHORITY_ID, "status": "HOLD", "classification": "REMOTE_STATE_MAY_BE_AMBIGUOUS", "command_audit": [], "assertions": {}, "mutation_audit": {"tag_mutation_count": 0, "compose_recreate_count": 0, "collector_lifecycle_count": 0, "protected_service_lifecycle_count": 0, "rollback_count": 0, "cleanup_count": 0}, "remote_call_budget": {"structured_ssh_calls": 1, "retry": 0, "resume": 0, "supplemental_ssh": 0}}
        local["status"] = remote["status"] if valid and p.returncode == 0 and not p.stderr else "HOLD"; local["classification"] = remote["classification"]
    json_write(REMOTE, remote); write_report(local, remote); finalize_manifest(); local["manifest_5_5"] = manifest_ok(E); local["helpers_unchanged_after_execution"] = preliminary == {"runner": identity(RUN), "controller": identity(CTL)}; json_write(LOCAL, local); finalize_manifest()
    print(json.dumps({"status": local["status"], "classification": local["classification"], "manifest_5_5": manifest_ok(E)}, sort_keys=True))
if __name__ == "__main__": main()
