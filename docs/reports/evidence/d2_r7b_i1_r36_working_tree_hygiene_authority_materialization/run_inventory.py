#!/usr/bin/env python3
"""R36 working-tree inventory and authority-materialization artifact generator."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "edge-mes/r36-authority-materialization/v1"
AUTHORITY_ID = "PM-D2-R7B-I1-R36-WORKTREE-HYGIENE-AUTHORITY-MATERIALIZATION-260729-2221"
EXPECTED_ROOT = Path("/Users/chenjie/Documents/MES/edge-mes-demo")
EXPECTED_BRANCH = "main"
EXPECTED_HEAD = "ac33e6bae449ecdd9b77a53daaf7271f14133000"
EXPECTED_PARENT = "66563677d3d1129fbc79c2c284b5f6d8b62f1932"
EXPECTED_GITIGNORE_BEFORE = {
    "bytes": 891,
    "sha256": "a302455543639fa197b725008240dc24c460505b9f09a0a4cd662bb6ba0bb442",
}
EXPECTED_GITIGNORE_AFTER = {
    "bytes": 1002,
    "sha256": "b23d176a4e84628fd1afdb849fa6b8761c291664610c8cff35c60175852f133c",
}
EXPECTED_PM_RULE = {
    "bytes": 49170,
    "sha256": "a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5",
}
EXPECTED_TRACKED_DIRTY = [
    ".gitignore",
    "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh",
    "docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py",
    "docs/thread_handoff/pm_operating_rules.md",
]
BATCH_C_PATHS = [
    "docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh",
    "docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256",
    "docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py",
]
IGNORE_RULES_ADDED = [
    "# Frontend dependencies and build output",
    "frontend/node_modules/",
    "frontend/.next/",
    "frontend/tsconfig.tsbuildinfo",
]
BROAD_IGNORE_RULES_FORBIDDEN = [
    "frontend/",
    "docs/",
    "docs/reports/",
    "docs/thread_handoff/",
    "frontend/next-env.d.ts",
]
PRE_IGNORE_FACTS = {
    "all_untracked": 13877,
    "frontend_node_modules": 12252,
    "frontend_next": 1277,
    "docs_reports": 307,
    "docs_thread_handoff": 38,
    "remaining_frontend": 2,
    "remaining_top_level_docs": 1,
    "status_entry_counts": {" M": 6, "??": 13877},
    "raw_porcelain_bytes": 1046501,
    "raw_porcelain_sha256": "286424545a431a0baf8900e39c1fdc4c9cfe4e587ab3e5c63856048463571085",
    "sorted_untracked_nul_sha256": "3e5469c0f5f44cb642c222ef7f4744fc4d8d8f60b79db72b7f187cf94b6f5fb4",
}
POST_IGNORE_FACTS = {
    "all_untracked": 347,
    "status_entry_counts": {" M": 6, "??": 347},
    "raw_porcelain_bytes": 32278,
    "raw_porcelain_sha256": "93c94ab4033eb8d6425118672537daf35d5ddfbdcffeb3aee2a390d9abb49520",
    "sorted_untracked_nul_sha256": "1c36f320808fd7585089cd116ee45cff9f2bc8f9736900f8212fdc21560656d7",
}

REPORT_PATH = "docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md"
EVIDENCE_DIR = "docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization"
RUNNER_PATH = f"{EVIDENCE_DIR}/run_inventory.py"
TERMINAL_PATH = f"{EVIDENCE_DIR}/inventory_terminal.json"
INVENTORY_PATH = f"{EVIDENCE_DIR}/untracked_durable_inventory.tsv"
NOISE_PATH = f"{EVIDENCE_DIR}/generated_noise_summary.json"
PLAN_PATH = f"{EVIDENCE_DIR}/authority_materialization_plan.json"
MANIFEST_PATH = f"{EVIDENCE_DIR}/manifest.sha256"
TASK_OUTPUT_PATHS = {
    REPORT_PATH,
    RUNNER_PATH,
    TERMINAL_PATH,
    INVENTORY_PATH,
    NOISE_PATH,
    PLAN_PATH,
    MANIFEST_PATH,
}

AUTHORITY_SEEDS = [
    ".gitignore",
    "docs/thread_handoff/pm_operating_rules.md",
    "docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md",
    "docs/reports/evidence/d2_r7b_i1_r32_phase1_phase2/manifest.sha256",
    "docs/reports/evidence/d2_r7b_i1_r32_phase1_phase2/build_input_manifest.sha256",
    "docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/manifest.sha256",
    "docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/phase1_validation_terminal.json",
    "docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md",
    "docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256",
    "docs/reports/sprint4_d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation.md",
    "docs/reports/sprint4_d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight.md",
    "docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/manifest.sha256",
    "docs/reports/sprint4_d2_r7b_i1_r34_collector_only_activation.md",
    "docs/reports/evidence/d2_r7b_i1_r34_collector_only_activation/manifest.sha256",
    "docs/reports/sprint4_d2_r7b_i1_r34_r1_collector_only_activation_retry.md",
    "docs/reports/evidence/d2_r7b_i1_r34_r1_collector_only_activation_retry/manifest.sha256",
    "docs/reports/sprint4_d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation.md",
    "docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation/manifest.sha256",
    "docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md",
    "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/manifest.sha256",
]

ALLOWED_CLASSIFICATIONS = {
    "CURRENT_AUTHORITY_KEEP_AND_COMMIT",
    "GOVERNANCE_KEEP_AND_COMMIT",
    "TRACKED_DIRTY_RECONCILIATION_REQUIRED",
    "HISTORICAL_DOC_ARCHIVE_REVIEW",
    "LOCAL_ONLY_REVIEW",
    "GENERATED_FILE_REVIEW",
    "UNCLASSIFIED_BLOCKER",
}
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")


class InventoryError(RuntimeError):
    """Fail-closed local inventory error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(root: Path, args: list[str], allowed_returncodes: set[int] | None = None) -> subprocess.CompletedProcess[bytes]:
    allowed = {0} if allowed_returncodes is None else allowed_returncodes
    cp = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )
    if cp.returncode not in allowed:
        raise InventoryError(
            f"git command failed: argv={['git', *args]!r} rc={cp.returncode} stderr={cp.stderr.decode('utf-8', 'replace')!r}"
        )
    return cp


def strict_text(data: bytes, label: str) -> str:
    try:
        return data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise InventoryError(f"{label}: strict UTF-8 decode failed") from exc


def normalize_repo_path(value: str) -> str:
    if not value or "\x00" in value or "\t" in value or "\n" in value or "\r" in value:
        raise InventoryError(f"invalid repository path characters: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != value or value.startswith("./"):
        raise InventoryError(f"non-normalized repository path: {value!r}")
    return value


def parse_nul_paths(data: bytes, label: str) -> list[str]:
    result: list[str] = []
    for raw in data.split(b"\0"):
        if not raw:
            continue
        result.append(normalize_repo_path(strict_text(raw, label)))
    return result


def parse_porcelain(data: bytes) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for raw in data.split(b"\0"):
        if not raw:
            continue
        if len(raw) < 4 or raw[2:3] != b" ":
            raise InventoryError(f"unsupported porcelain record: {raw[:80]!r}")
        status_code = raw[:2].decode("ascii", "strict")
        path = normalize_repo_path(strict_text(raw[3:], "porcelain path"))
        entries.append((status_code, path))
    return entries


def file_identity(root: Path, repo_path: str) -> dict[str, Any]:
    repo_path = normalize_repo_path(repo_path)
    path = root / repo_path
    try:
        st = path.lstat()
    except FileNotFoundError as exc:
        raise InventoryError(f"required path absent: {repo_path}") from exc
    if stat.S_ISLNK(st.st_mode):
        target = os.readlink(path)
        payload = os.fsencode(target)
        return {
            "path": repo_path,
            "bytes": len(payload),
            "sha256": sha256_bytes(payload),
            "file_type": "symlink",
            "symlink": True,
        }
    if stat.S_ISREG(st.st_mode):
        digest = hashlib.sha256()
        byte_count = 0
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                byte_count += len(chunk)
        if byte_count != st.st_size:
            raise InventoryError(f"size changed while hashing: {repo_path}")
        return {
            "path": repo_path,
            "bytes": byte_count,
            "sha256": digest.hexdigest(),
            "file_type": "regular",
            "symlink": False,
        }
    if stat.S_ISDIR(st.st_mode):
        return {
            "path": repo_path,
            "bytes": 0,
            "sha256": sha256_bytes(b""),
            "file_type": "directory",
            "symlink": False,
        }
    return {
        "path": repo_path,
        "bytes": st.st_size,
        "sha256": sha256_bytes(b""),
        "file_type": "special",
        "symlink": False,
    }


def assert_regular_exact(root: Path, repo_path: str, expected: dict[str, Any]) -> dict[str, Any]:
    identity = file_identity(root, repo_path)
    if identity["file_type"] != "regular" or identity["symlink"]:
        raise InventoryError(f"identity is not a regular non-symlink file: {repo_path}")
    if identity["bytes"] != expected["bytes"] or identity["sha256"] != expected["sha256"]:
        raise InventoryError(f"identity drift: {repo_path}")
    return identity


def parse_manifest(root: Path, manifest_path: str) -> list[dict[str, str]]:
    identity = file_identity(root, manifest_path)
    if identity["file_type"] != "regular" or identity["symlink"]:
        raise InventoryError(f"AUTHORITY_MANIFEST_INVALID: non-regular manifest {manifest_path}")
    text = strict_text((root / manifest_path).read_bytes(), manifest_path)
    members: list[dict[str, str]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = MANIFEST_LINE.fullmatch(line)
        if match is None:
            raise InventoryError(f"AUTHORITY_MANIFEST_INVALID: {manifest_path}:{line_number}")
        expected_sha, member_path = match.groups()
        member_path = normalize_repo_path(member_path)
        if member_path == manifest_path or member_path in seen:
            raise InventoryError(f"AUTHORITY_MANIFEST_INVALID: duplicate/self member {member_path}")
        seen.add(member_path)
        identity = file_identity(root, member_path)
        if identity["file_type"] != "regular" or identity["symlink"] or identity["sha256"] != expected_sha:
            raise InventoryError(f"AUTHORITY_MANIFEST_INVALID: member mismatch {member_path}")
        members.append({"path": member_path, "sha256": expected_sha})
    if not members:
        raise InventoryError(f"AUTHORITY_MANIFEST_INVALID: empty manifest {manifest_path}")
    return members


def build_authority_closure(root: Path) -> dict[str, Any]:
    closure: set[str] = set()
    provenance: dict[str, set[str]] = {}
    queue: deque[str] = deque()
    for seed in AUTHORITY_SEEDS:
        seed = normalize_repo_path(seed)
        file_identity(root, seed)
        closure.add(seed)
        provenance.setdefault(seed, set()).add(f"DIRECT_SEED:{seed}")
        if seed.endswith("manifest.sha256"):
            queue.append(seed)
    parsed_manifests: set[str] = set()
    reference_edges: dict[str, list[str]] = {}
    verified_members = 0
    while queue:
        manifest_path = queue.popleft()
        if manifest_path in parsed_manifests:
            continue
        parsed_manifests.add(manifest_path)
        members = parse_manifest(root, manifest_path)
        reference_edges[manifest_path] = [member["path"] for member in members]
        for member in members:
            member_path = member["path"]
            verified_members += 1
            closure.add(member_path)
            provenance.setdefault(member_path, set()).add(f"MANIFEST_MEMBER:{manifest_path}")
            if member_path.endswith("manifest.sha256") and member_path not in parsed_manifests:
                queue.append(member_path)
    return {
        "paths": sorted(closure),
        "provenance": {key: sorted(value) for key, value in sorted(provenance.items())},
        "manifest_paths": sorted(parsed_manifests),
        "reference_edges": {key: value for key, value in sorted(reference_edges.items())},
        "verified_members": verified_members,
    }


def check_git_baseline(root: Path) -> dict[str, Any]:
    actual_root = Path(strict_text(run_git(root, ["rev-parse", "--show-toplevel"]).stdout, "root").strip())
    branch = strict_text(run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout, "branch").strip()
    head = strict_text(run_git(root, ["rev-parse", "HEAD"]).stdout, "HEAD").strip()
    origin_main = strict_text(run_git(root, ["rev-parse", "origin/main"]).stdout, "origin/main").strip()
    parent = strict_text(run_git(root, ["rev-parse", "HEAD^"]).stdout, "HEAD^").strip()
    counts = strict_text(run_git(root, ["rev-list", "--left-right", "--count", "HEAD...origin/main"]).stdout, "ahead/behind").split()
    if len(counts) != 2:
        raise InventoryError("WORKTREE_BASELINE_DRIFT: invalid ahead/behind")
    ahead, behind = (int(value) for value in counts)
    dirty = sorted(parse_nul_paths(run_git(root, ["diff", "--name-only", "-z"]).stdout, "tracked dirty"))
    cached = sorted(parse_nul_paths(run_git(root, ["diff", "--cached", "--name-only", "-z"]).stdout, "cached"))
    run_git(root, ["diff", "--check"])
    run_git(root, ["diff", "--cached", "--check"])
    if (
        actual_root != EXPECTED_ROOT
        or branch != EXPECTED_BRANCH
        or head != EXPECTED_HEAD
        or origin_main != EXPECTED_HEAD
        or parent != EXPECTED_PARENT
        or ahead != 0
        or behind != 0
        or dirty != EXPECTED_TRACKED_DIRTY
        or cached
    ):
        raise InventoryError("WORKTREE_BASELINE_DRIFT")
    return {
        "root": str(actual_root),
        "branch": branch,
        "head": head,
        "origin_main": origin_main,
        "head_parent": parent,
        "ahead": ahead,
        "behind": behind,
        "tracked_dirty": dirty,
        "cached": cached,
        "diff_check": "PASS",
        "cached_diff_check": "PASS",
    }


def check_gitignore(root: Path) -> dict[str, Any]:
    identity = assert_regular_exact(root, ".gitignore", EXPECTED_GITIGNORE_AFTER)
    text = strict_text((root / ".gitignore").read_bytes(), ".gitignore")
    block = "\n".join(IGNORE_RULES_ADDED) + "\n"
    if text.count(block) != 1 or not text.endswith(block):
        raise InventoryError("GITIGNORE_SCOPE_VIOLATION")
    lines = text.splitlines()
    if any(rule in lines for rule in BROAD_IGNORE_RULES_FORBIDDEN):
        raise InventoryError("GITIGNORE_SCOPE_VIOLATION")
    results: dict[str, Any] = {}
    expected_ignored = {
        "frontend/node_modules": True,
        "frontend/.next": True,
        "frontend/tsconfig.tsbuildinfo": True,
        "frontend/next-env.d.ts": False,
    }
    for target, should_ignore in expected_ignored.items():
        cp = run_git(root, ["check-ignore", "-v", "--", target], allowed_returncodes={0, 1})
        ignored = cp.returncode == 0
        results[target] = {
            "ignored": ignored,
            "returncode": cp.returncode,
            "rule": strict_text(cp.stdout, f"check-ignore {target}").rstrip("\n"),
            "stderr_bytes": len(cp.stderr),
        }
        if ignored != should_ignore or cp.stderr:
            raise InventoryError("GITIGNORE_SCOPE_VIOLATION")
    return {
        **identity,
        "before": EXPECTED_GITIGNORE_BEFORE,
        "ignore_rules_added": IGNORE_RULES_ADDED,
        "exact_block_occurrences": text.count(block),
        "exact_block_is_suffix": text.endswith(block),
        "broad_ignore_rule_absent": True,
        "git_check_ignore_results": results,
    }


def capture_untracked(root: Path) -> dict[str, Any]:
    cp = run_git(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    entries = parse_porcelain(cp.stdout)
    status_counts = Counter(status_code for status_code, _ in entries)
    untracked_all = sorted(path for status_code, path in entries if status_code == "??")
    task_outputs_present = sorted(path for path in untracked_all if path in TASK_OUTPUT_PATHS)
    untracked = sorted(path for path in untracked_all if path not in TASK_OUTPUT_PATHS)
    digest_payload = b"".join(path.encode("utf-8") + b"\0" for path in untracked)
    if len(untracked) != POST_IGNORE_FACTS["all_untracked"]:
        raise InventoryError("POST_IGNORE_COUNT_MISMATCH")
    if sha256_bytes(digest_payload) != POST_IGNORE_FACTS["sorted_untracked_nul_sha256"]:
        raise InventoryError("FINAL_GIT_DRIFT")
    if "frontend/next-env.d.ts" not in untracked:
        raise InventoryError("GITIGNORE_SCOPE_VIOLATION")
    return {
        "entries": entries,
        "status_entry_counts_live": dict(sorted(status_counts.items())),
        "untracked_all": untracked_all,
        "untracked": untracked,
        "task_outputs_present": task_outputs_present,
        "non_task_untracked_count": len(untracked),
        "non_task_sorted_untracked_nul_sha256": sha256_bytes(digest_payload),
    }


def capture_generated_groups(root: Path) -> dict[str, Any]:
    cp = run_git(
        root,
        [
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
            "-z",
            "--",
            "frontend/node_modules",
            "frontend/.next",
            "frontend/tsconfig.tsbuildinfo",
        ],
    )
    paths = sorted(parse_nul_paths(cp.stdout, "ignored generated path"))
    groups = {
        "frontend/node_modules": [path for path in paths if path.startswith("frontend/node_modules/")],
        "frontend/.next": [path for path in paths if path.startswith("frontend/.next/")],
        "frontend/tsconfig.tsbuildinfo": [path for path in paths if path == "frontend/tsconfig.tsbuildinfo"],
    }
    expected = {
        "frontend/node_modules": PRE_IGNORE_FACTS["frontend_node_modules"],
        "frontend/.next": PRE_IGNORE_FACTS["frontend_next"],
        "frontend/tsconfig.tsbuildinfo": 1,
    }
    counts = {key: len(value) for key, value in groups.items()}
    if (
        counts["frontend/node_modules"] < expected["frontend/node_modules"]
        or counts["frontend/.next"] != expected["frontend/.next"]
        or counts["frontend/tsconfig.tsbuildinfo"] != expected["frontend/tsconfig.tsbuildinfo"]
    ):
        raise InventoryError("FINAL_GIT_DRIFT")
    return {
        "paths_count": len(paths),
        "groups": {
            key: {
                "path_prefix": key,
                "captured_visible_file_count_before_rule": expected[key],
                "live_ignored_discovery_file_count": counts[key],
                "classification": "GENERATED_NOISE_IGNORED",
                "discovery_note": (
                    "Live git ls-files --ignored may also include package-internal paths that "
                    "were already ignored before the new root rule; the frozen before/after "
                    "status captures are visibility-reduction authority."
                ),
            }
            for key in sorted(groups)
        },
    }


def validate_r35(root: Path) -> dict[str, Any]:
    expected = {
        "docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md": {
            "bytes": 3002,
            "sha256": "133c303e6a556b4be9e2c9535a10ff3b5a9dd06bf5b6f3fca1f272d707b75ee0",
        },
        "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/local_prerequisite_terminal.json": {
            "bytes": 52496,
            "sha256": "41c28d5c22e9c934c4edfeea0b07a1a84ec893b2ce9918d2bb17f2808afc7ce7",
        },
        "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/post_activation_terminal.json": {
            "bytes": 72307,
            "sha256": "135e66854fc032ceddc81ce6fa0cf28b51c90efd081f7f6c15e9e9299295e618",
        },
        "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/manifest.sha256": {
            "bytes": 973,
            "sha256": "51e172a2c5bc3f9671187dc560565c9423368741fd67281b57329edd2795d244",
        },
    }
    identities = {path: assert_regular_exact(root, path, identity) for path, identity in expected.items()}
    local = json.loads(
        strict_text(
            (root / "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/local_prerequisite_terminal.json").read_bytes(),
            "R35 local terminal",
        )
    )
    post = json.loads(
        strict_text(
            (root / "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/post_activation_terminal.json").read_bytes(),
            "R35 post terminal",
        )
    )
    manifest_members = parse_manifest(
        root, "docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/manifest.sha256"
    )
    semantic_pass = (
        local.get("status") == "PASS"
        and local.get("classification") == "ACTIVATED"
        and local.get("manifest_verification", {}).get("verification") == "6/6 OK"
        and post.get("status") == "PASS"
        and post.get("classification") == "ACTIVATED"
        and post.get("evidence_boundary", {}).get("ACTIVATED") is True
        and post.get("evidence_boundary", {}).get("STATIC_MAPPING_INITIALIZED") is True
        and post.get("evidence_boundary", {}).get("RUNTIME_LOADED") is False
        and post.get("evidence_boundary", {}).get("PRODUCTION_ACCEPTED") is False
        and len(manifest_members) == 6
    )
    if not semantic_pass:
        raise InventoryError("AUTHORITY_CLOSURE_AMBIGUOUS")
    return {
        "identities": identities,
        "status": "PASS",
        "classification": "ACTIVATED",
        "STATIC_MAPPING_INITIALIZED": True,
        "RUNTIME_LOADED": False,
        "PRODUCTION_ACCEPTED": False,
        "manifest_verification": "6/6 OK",
    }


def classify_path(path: str, closure: dict[str, Any]) -> tuple[str, str, str]:
    if path in closure["paths"]:
        references = closure["provenance"].get(path, ["DIRECT_AUTHORITY_SEED"])
        return (
            "CURRENT_AUTHORITY_KEEP_AND_COMMIT",
            "Path is an exact current authority seed or a verified member of an accepted seed manifest.",
            ";".join(references),
        )
    if path == "frontend/next-env.d.ts":
        return (
            "GENERATED_FILE_REVIEW",
            "Next.js generated declaration remains visible and unignored; this task makes no keep-or-ignore decision.",
            "frontend/package.json;frontend/tsconfig.json;R36 Batch E",
        )
    if path.startswith("docs/reports/") or path.startswith("docs/thread_handoff/") or (
        path.startswith("docs/") and "/" not in path[len("docs/") :]
    ):
        return (
            "HISTORICAL_DOC_ARCHIVE_REVIEW",
            "Durable-looking documentation or execution evidence is outside the verified current authority closure and requires human review.",
            "R36 Batch D;not in accepted manifest closure",
        )
    return (
        "UNCLASSIFIED_BLOCKER",
        "No frozen classification rule applies; deletion or inferred purpose is forbidden.",
        "R36 fail-closed classification boundary",
    )


def build_inventory(root: Path, untracked: list[str], closure: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in untracked:
        identity = file_identity(root, path)
        classification, reason, authority_reference = classify_path(path, closure)
        if identity["file_type"] not in {"regular", "symlink"}:
            classification = "UNCLASSIFIED_BLOCKER"
            reason = "Non-file untracked object requires explicit PM classification."
            authority_reference = "R36 fail-closed file-type boundary"
        if classification not in ALLOWED_CLASSIFICATIONS:
            raise InventoryError(f"invalid classification: {classification}")
        rows.append(
            {
                "path": path,
                "bytes": identity["bytes"],
                "sha256": identity["sha256"],
                "file_type": identity["file_type"],
                "symlink": str(identity["symlink"]).lower(),
                "classification": classification,
                "reason": reason,
                "authority_reference": authority_reference,
            }
        )
    rows.sort(key=lambda item: item["path"])
    paths = [row["path"] for row in rows]
    if len(paths) != len(set(paths)) or paths != sorted(paths):
        raise InventoryError("DUPLICATE_CLASSIFICATION")
    if len(rows) != POST_IGNORE_FACTS["all_untracked"]:
        raise InventoryError("INVENTORY_COVERAGE_INCOMPLETE")
    if any(row["classification"] == "UNCLASSIFIED_BLOCKER" for row in rows):
        raise InventoryError("UNCLASSIFIED_BLOCKER")
    return rows


def total_bytes(root: Path, paths: list[str]) -> int:
    return sum(int(file_identity(root, path)["bytes"]) for path in paths)


def batch(root: Path, batch_id: str, paths: list[str], reason: str, title: str) -> dict[str, Any]:
    exact_paths = sorted(paths)
    if len(exact_paths) != len(set(exact_paths)):
        raise InventoryError(f"BATCH_OVERLAP: duplicate within {batch_id}")
    return {
        "batch_id": batch_id,
        "exact_paths": exact_paths,
        "path_count": len(exact_paths),
        "total_bytes": total_bytes(root, exact_paths),
        "classification_reason": reason,
        "proposed_commit_title": title,
        "stage_authority_required": True,
        "commit_authority_required": True,
        "push_authority_required": True,
    }


def build_plan(
    root: Path,
    rows: list[dict[str, Any]],
    closure: dict[str, Any],
    tracked: set[str],
    tracked_dirty: set[str],
) -> dict[str, Any]:
    row_by_path = {row["path"]: row for row in rows}
    batch_a_paths = [".gitignore", "docs/thread_handoff/pm_operating_rules.md"]
    batch_b_paths = sorted(set(closure["paths"]) - set(batch_a_paths))
    batch_d_paths = sorted(
        row["path"] for row in rows if row["classification"] == "HISTORICAL_DOC_ARCHIVE_REVIEW"
    )
    batch_e_paths = sorted(
        row["path"]
        for row in rows
        if row["classification"] in {"LOCAL_ONLY_REVIEW", "GENERATED_FILE_REVIEW"}
    )
    batches = [
        batch(
            root,
            "A",
            batch_a_paths,
            "Governance and exact frontend generated-noise ignore rules; both are pre-existing tracked dirty paths.",
            "Materialize repository governance and frontend ignore rules",
        ),
        batch(
            root,
            "B",
            batch_b_paths,
            "Exact verified R31-R35 activation authority closure, including manifest-bound direct source authority; no directory-similarity expansion.",
            "Materialize current Collector activation authority chain",
        ),
        batch(
            root,
            "C",
            BATCH_C_PATHS,
            "Four pre-existing tracked dirty artifacts require independent reconciliation and are not automatically merged into governance or current authority.",
            "Reconcile pre-existing D2-R7B tracked dirty artifacts",
        ),
        batch(
            root,
            "D",
            batch_d_paths,
            "Untracked reports, handoffs, and execution/review evidence outside the current authority closure require human archive/keep review; nothing is safe to delete.",
            "Review historical documentation and evidence for archival",
        ),
        batch(
            root,
            "E",
            batch_e_paths,
            "Generated or local-only remaining untracked paths require a separate keep/ignore decision; this task does not delete or ignore them.",
            "Review generated and local-only repository artifacts",
        ),
    ]
    membership: dict[str, list[str]] = {}
    for item in batches:
        for path in item["exact_paths"]:
            membership.setdefault(path, []).append(item["batch_id"])
    overlaps = {path: ids for path, ids in membership.items() if len(ids) != 1}
    if overlaps:
        raise InventoryError("BATCH_OVERLAP")
    inventory_batch_membership = {
        path: membership.get(path, []) for path in sorted(row_by_path)
    }
    uncovered = [path for path, ids in inventory_batch_membership.items() if len(ids) != 1]
    if uncovered:
        raise InventoryError("INVENTORY_COVERAGE_INCOMPLETE")
    authority_identities = {path: file_identity(root, path) for path in closure["paths"]}
    closure_tracked = sorted(path for path in closure["paths"] if path in tracked)
    closure_untracked = sorted(path for path in closure["paths"] if path not in tracked)
    closure_dirty = sorted(path for path in closure["paths"] if path in tracked_dirty)
    plan = {
        "schema_version": SCHEMA_VERSION,
        "authority_id": AUTHORITY_ID,
        "status": "READY_FOR_PM_GIT_CLOSEOUT_PLANNING",
        "safe_to_delete_claims": 0,
        "authority_closure": {
            "seeds": AUTHORITY_SEEDS,
            "exact_paths": closure["paths"],
            "path_count": len(closure["paths"]),
            "total_bytes": sum(identity["bytes"] for identity in authority_identities.values()),
            "manifest_paths": closure["manifest_paths"],
            "manifest_count": len(closure["manifest_paths"]),
            "verified_manifest_members": closure["verified_members"],
            "all_members_exist_and_match": True,
            "reference_edges": closure["reference_edges"],
            "provenance": closure["provenance"],
            "tracked_paths": closure_tracked,
            "tracked_path_count": len(closure_tracked),
            "untracked_paths": closure_untracked,
            "untracked_path_count": len(closure_untracked),
            "tracked_dirty_paths": closure_dirty,
            "tracked_dirty_path_count": len(closure_dirty),
            "selection_rule": "exact seeds plus recursively verified manifest members only; no directory-similarity inference",
        },
        "batches": batches,
        "batch_overlap": {
            "count": 0,
            "paths": [],
            "disjoint": True,
        },
        "inventory_batch_coverage": {
            "inventory_paths": len(row_by_path),
            "covered_exactly_once": len(row_by_path),
            "uncovered": [],
            "duplicate_membership": [],
            "pass": True,
        },
        "review_actions": {
            "D": {
                path: (
                    "ARCHIVE_REVIEW_REQUIRED"
                    if path.startswith("docs/")
                    else "KEEP_REVIEW_REQUIRED"
                )
                for path in batch_d_paths
            },
            "E": {path: "KEEP_REVIEW_REQUIRED" for path in batch_e_paths},
        },
        "authority_non_inheritance": (
            "All A-E stage, commit, and push actions require future exact authorization. "
            "This plan grants no Git, delete, move, cleanup, remote, runtime, or production authority."
        ),
    }
    if "SAFE_TO_DELETE" in json.dumps(plan, ensure_ascii=False):
        raise InventoryError("AUTHORITY_CLOSURE_AMBIGUOUS")
    return plan


def render_tsv(rows: list[dict[str, Any]]) -> str:
    columns = [
        "path",
        "bytes",
        "sha256",
        "file_type",
        "symlink",
        "classification",
        "reason",
        "authority_reference",
    ]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, dialect="excel-tab", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


def output_identity_from_bytes(path: str, payload: bytes) -> dict[str, Any]:
    return {
        "path": path,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def write_exclusive(root: Path, repo_path: str, payload: bytes) -> None:
    repo_path = normalize_repo_path(repo_path)
    path = root / repo_path
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise InventoryError(f"OUTPUT_PATH_PREEXISTS: {repo_path}") from exc
    try:
        view = memoryview(payload)
        written = 0
        while written < len(view):
            count = os.write(fd, view[written:])
            if count <= 0:
                raise InventoryError(f"short write: {repo_path}")
            written += count
        os.fsync(fd)
    finally:
        os.close(fd)


def runner_identity(root: Path) -> dict[str, Any]:
    return file_identity(root, RUNNER_PATH)


def validate_execution_lock(root: Path) -> dict[str, Any]:
    terminal_path = root / TERMINAL_PATH
    terminal = json.loads(strict_text(terminal_path.read_bytes(), TERMINAL_PATH))
    lock = terminal.get("execution_lock", {})
    if lock.get("state") != "SEALED" or lock.get("authority_id") != AUTHORITY_ID:
        raise InventoryError("EXECUTION_LOCK_INVALID")
    current_runner = runner_identity(root)
    locked_runner = terminal.get("runner_identities", {}).get("locked")
    if locked_runner != current_runner:
        raise InventoryError("EXECUTION_LOCK_INVALID")
    if terminal.get("repair_cycles", {}).get("consumed", 99) > 2:
        raise InventoryError("LOCAL_REPAIR_BUDGET_EXHAUSTED")
    return terminal


def build_artifacts(root: Path, require_sealed: bool) -> dict[str, Any]:
    git_facts = check_git_baseline(root)
    gitignore = check_gitignore(root)
    assert_regular_exact(root, "docs/thread_handoff/pm_operating_rules.md", EXPECTED_PM_RULE)
    r35 = validate_r35(root)
    capture = capture_untracked(root)
    generated = capture_generated_groups(root)
    closure = build_authority_closure(root)
    tracked = set(parse_nul_paths(run_git(root, ["ls-files", "-z"]).stdout, "tracked path"))
    rows = build_inventory(root, capture["untracked"], closure)
    plan = build_plan(root, rows, closure, tracked, set(git_facts["tracked_dirty"]))
    classification_counts = dict(sorted(Counter(row["classification"] for row in rows).items()))
    noise = {
        "schema_version": SCHEMA_VERSION,
        "authority_id": AUTHORITY_ID,
        "captured_before_ignore": PRE_IGNORE_FACTS,
        "captured_after_ignore_before_outputs": POST_IGNORE_FACTS,
        "ignore_rules_added": IGNORE_RULES_ADDED,
        "generated_groups": generated["groups"],
        "file_counts": {
            "before_ignore": PRE_IGNORE_FACTS["all_untracked"],
            "after_ignore_before_outputs": POST_IGNORE_FACTS["all_untracked"],
            "removed_from_status_visibility": 13530,
            "live_ignored_generated_group_count": generated["paths_count"],
            "live_non_task_untracked": capture["non_task_untracked_count"],
        },
        "status_entry_counts": {
            "before_ignore": PRE_IGNORE_FACTS["status_entry_counts"],
            "after_ignore_before_outputs": POST_IGNORE_FACTS["status_entry_counts"],
            "live_with_task_outputs": capture["status_entry_counts_live"],
        },
        "git_check_ignore_results": gitignore["git_check_ignore_results"],
        "next_env_d_ts_result": {
            "path": "frontend/next-env.d.ts",
            "ignored": False,
            "remains_untracked": "frontend/next-env.d.ts" in capture["untracked"],
            "classification": "GENERATED_FILE_REVIEW",
        },
        "broad_ignore_rule_absent": gitignore["broad_ignore_rule_absent"],
        "exact_ignore_block_once": gitignore["exact_block_occurrences"] == 1,
        "generated_noise_conclusion": (
            "frontend/node_modules and frontend/.next are generated dependency/build noise; "
            "frontend/tsconfig.tsbuildinfo is generated compiler state. Exactly 13,530 files "
            "were removed from Git status visibility by the narrow rules."
        ),
        "delete_move_actions": 0,
        "no_delete_or_move": True,
        "classification_counts_for_remaining_untracked": classification_counts,
    }
    tsv_bytes = render_tsv(rows).encode("utf-8")
    noise_bytes = (json.dumps(noise, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    plan_bytes = (json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payloads = {
        INVENTORY_PATH: tsv_bytes,
        NOISE_PATH: noise_bytes,
        PLAN_PATH: plan_bytes,
    }
    if require_sealed:
        terminal = validate_execution_lock(root)
        for path in payloads:
            if (root / path).exists() or (root / path).is_symlink():
                raise InventoryError(f"OUTPUT_PATH_PREEXISTS: {path}")
        for path, payload in payloads.items():
            write_exclusive(root, path, payload)
        post_runner = runner_identity(root)
        if post_runner != terminal["runner_identities"]["locked"]:
            raise InventoryError("POST_LOCK_LOCAL_FAILURE")
    return {
        "git_facts": git_facts,
        "gitignore": gitignore,
        "r35": r35,
        "capture": {
            key: value
            for key, value in capture.items()
            if key not in {"entries", "untracked_all", "untracked"}
        },
        "generated": generated,
        "closure": {
            "path_count": len(closure["paths"]),
            "manifest_count": len(closure["manifest_paths"]),
            "verified_members": closure["verified_members"],
        },
        "inventory": {
            "row_count": len(rows),
            "classification_counts": classification_counts,
            "unique_paths": len({row["path"] for row in rows}),
            "unclassified": classification_counts.get("UNCLASSIFIED_BLOCKER", 0),
        },
        "plan": {
            "batch_counts": {item["batch_id"]: item["path_count"] for item in plan["batches"]},
            "batch_overlap": plan["batch_overlap"],
            "coverage": plan["inventory_batch_coverage"],
        },
        "payload_identities": {
            path: output_identity_from_bytes(path, payload) for path, payload in payloads.items()
        },
        "write_performed": require_sealed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="run complete read-only local validation without creating final inventory artifacts",
    )
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if root != EXPECTED_ROOT:
        raise InventoryError("WORKTREE_BASELINE_DRIFT")
    if not args.self_check:
        validate_execution_lock(root)
    result = build_artifacts(root, require_sealed=not args.self_check)
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": "SELF_CHECK" if args.self_check else "FINAL_INVENTORY_EXECUTION",
                "authority_id": AUTHORITY_ID,
                "inventory": result["inventory"],
                "closure": result["closure"],
                "plan": result["plan"],
                "payload_identities": result["payload_identities"],
                "write_performed": result["write_performed"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InventoryError as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        raise SystemExit(2)
