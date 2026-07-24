"""Run non-DB pytest partitions with isolated service import roots."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NON_DB_MARK_EXPRESSION = "not db_backed and not postgres_local"
EXPECTED_TEST_ROOTS = frozenset(
    {
        "tests",
        "collector/tests",
        "api/tests",
        "s7_plc_sim/tests",
    }
)


@dataclass(frozen=True)
class TestPartition:
    name: str
    test_root: str
    pythonpath: str


PARTITIONS = (
    TestPartition(
        name="Root/common tests",
        test_root="tests",
        pythonpath="collector:.",
    ),
    TestPartition(
        name="Collector tests",
        test_root="collector/tests",
        pythonpath="collector:.",
    ),
    TestPartition(
        name="API tests",
        test_root="api/tests",
        pythonpath="api:.",
    ),
    TestPartition(
        name="S7 PLC simulator tests",
        test_root="s7_plc_sim/tests",
        pythonpath="s7_plc_sim:.",
    ),
)


def _validate_partition_contract() -> None:
    actual_test_roots = frozenset(partition.test_root for partition in PARTITIONS)
    if actual_test_roots != EXPECTED_TEST_ROOTS:
        raise RuntimeError(
            "partition contract does not cover exactly the required test roots: "
            f"expected={sorted(EXPECTED_TEST_ROOTS)!r} "
            f"actual={sorted(actual_test_roots)!r}"
        )

    if len(actual_test_roots) != len(PARTITIONS):
        raise RuntimeError("partition contract contains duplicate test roots")

    for partition in PARTITIONS:
        test_root = REPO_ROOT / partition.test_root
        if not test_root.is_dir():
            raise RuntimeError(f"test root is not a directory: {test_root}")


def _validate_venv_interpreter() -> None:
    expected = (REPO_ROOT / ".venv" / "bin" / "python").resolve()
    actual = Path(sys.executable).resolve()
    if actual != expected:
        raise RuntimeError(
            "runner must use the project .venv interpreter: "
            f"expected={expected} actual={actual}"
        )


def _pytest_command(partition: TestPartition) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-m",
        NON_DB_MARK_EXPRESSION,
        "-q",
        partition.test_root,
    ]


def _run_partition(partition: TestPartition) -> int:
    command = _pytest_command(partition)
    display_command = [
        "env",
        f"PYTHONPATH={partition.pythonpath}",
        *command,
    ]

    environment = os.environ.copy()
    environment["PYTHONPATH"] = partition.pythonpath
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    print(f"PARTITION={partition.name}", flush=True)
    print(f"TEST_ROOT={partition.test_root}", flush=True)
    print(f"PYTHONPATH={partition.pythonpath}", flush=True)
    print(f"COMMAND={shlex.join(display_command)}", flush=True)

    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=environment,
            check=False,
            shell=False,
        )
        exit_code = completed.returncode
    except OSError as exc:
        print(f"SUBPROCESS_ERROR={exc}", flush=True)
        exit_code = 2

    print(f"PARTITION_EXIT_CODE={exit_code}", flush=True)
    return exit_code


def main() -> int:
    try:
        _validate_partition_contract()
        _validate_venv_interpreter()
    except RuntimeError as exc:
        print(f"RUNNER_CONTRACT_ERROR={exc}", file=sys.stderr, flush=True)
        print("AGGREGATE_EXIT_CODE=2", flush=True)
        return 2

    exit_codes = []
    for partition in PARTITIONS:
        exit_codes.append(_run_partition(partition))

    aggregate_exit_code = 1 if any(code != 0 for code in exit_codes) else 0
    print(f"PARTITION_EXIT_CODES={exit_codes}", flush=True)
    print(f"AGGREGATE_EXIT_CODE={aggregate_exit_code}", flush=True)
    return aggregate_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
