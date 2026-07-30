from __future__ import annotations

import json
import hashlib
import os
import tempfile
import threading
import unittest
from contextlib import nullcontext
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zoneinfo import ZoneInfo

from snap7 import util
import yaml

from app import main as collector_main
from app.plc.mapping import RuntimeMappingContractError, StationMapping, load_edge_mapping
from app.plc.read_plan import ReadPlan, build_read_plans
from app.services import event_collector as event_collector_module
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"
DEFAULT_CONTEXT = object()
DEFAULT_MAPPING = object()
FROZEN_MAPPING_CONTENT_SHA256 = "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"
FROZEN_RESOLVED_CONFIG_HASH = "0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38"


class FakeClient:
    def __init__(
        self,
        fail_writes: int = 0,
        reads: dict[int, bytes | bytearray] | None = None,
        events: list[str] | None = None,
    ) -> None:
        self.fail_writes = fail_writes
        self.writes: list[tuple[int, int, bytes]] = []
        self.reads = reads or {}
        self.events = events
        self.write_attempts = 0

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        self.write_attempts += 1
        if self.events is not None:
            self.events.append("ack_write_attempt")
        if self.fail_writes > 0:
            self.fail_writes -= 1
            if self.events is not None:
                self.events.append("ack_write_failed")
            raise RuntimeError("simulated ACK write failure")
        self.writes.append((db_number, start, bytes(data)))
        if self.events is not None:
            self.events.append("ack_write")

    def get_connected(self) -> bool:
        return True

    def db_read(self, db_number: int, start: int, size: int) -> bytearray:
        data = bytearray(self.reads[db_number])
        return data[start : start + size]


class FakeTransaction:
    def __init__(self, storage: "FakeStorage") -> None:
        self.storage = storage

    def __enter__(self) -> "FakeTransaction":
        self.storage._transaction_snapshot = (
            self.storage.max_counter,
            list(self.storage.accepted_facts),
            dict(self.storage.persisted_cycles),
        )
        self.storage.events.append("begin")
        return self

    def __exit__(self, exc_type, exc, _tb) -> bool:
        if exc_type is not None:
            self.storage.rollback()
            return False
        self.storage.events.append("commit")
        self.storage._transaction_snapshot = None
        return False


class FakeStorage:
    def __init__(self, *, max_counter: int | None = None, fail_persist: bool = False) -> None:
        self.max_counter = max_counter
        self.fail_persist = fail_persist
        self.persist_calls = 0
        self.accepted_fact_calls = 0
        self.accepted_facts: list[object] = []
        self.persisted_cycles: dict[tuple[str, str, str, int], dict] = {}
        self.ack_ok_calls = 0
        self.ack_failed_calls = 0
        self.errors: list[dict] = []
        self.runtime_updates: list[dict] = []
        self.events: list[str] = []
        self._transaction_snapshot: tuple[int | None, list[object], dict[tuple[str, str, str, int], dict]] | None = None

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        self.runtime_updates.append(kwargs)

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return self.max_counter

    def persist_cycle(self, **_kwargs) -> int:
        raise AssertionError("internal-commit persist_cycle must not be called in atomic path")

    def persist_cycle_no_commit(self, **kwargs) -> int:
        self.persist_calls += 1
        self.events.append("persist_cycle")
        if self.fail_persist:
            raise RuntimeError("simulated database failure")
        self.max_counter = max(self.max_counter or 0, int(kwargs["cycle_counter"]))
        key = (
            str(kwargs["plc_id"]),
            kwargs["station"].station_id,
            str(kwargs["plc_boot_id"]),
            int(kwargs["cycle_counter"]),
        )
        self.persisted_cycles[key] = kwargs
        return 41

    def transaction(self) -> FakeTransaction:
        return FakeTransaction(self)

    def insert_accepted_station_event_fact_no_commit(self, fact) -> str:
        self.accepted_fact_calls += 1
        self.events.append("accepted_fact")
        for existing in self.accepted_facts:
            if existing.fact_key == fact.fact_key:
                if existing.content_fingerprint != fact.content_fingerprint:
                    raise ValueError("accepted station-event fact conflict: fact_key content differs")
                return "existing"
            if existing.source_identity == fact.source_identity:
                if existing.content_fingerprint != fact.content_fingerprint:
                    raise ValueError("accepted station-event fact conflict: source identity content differs")
                return "existing"
        self.accepted_facts.append(fact)
        return "inserted"

    def rollback(self) -> None:
        self.events.append("rollback")
        if self._transaction_snapshot is not None:
            self.max_counter, accepted_facts, persisted_cycles = self._transaction_snapshot
            self.accepted_facts = accepted_facts
            self.persisted_cycles = persisted_cycles
            self._transaction_snapshot = None

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok_calls += 1
        self.events.append("ack_ok")

    def mark_cycle_ack_failed(self, **kwargs) -> None:
        self.ack_failed_calls += 1
        self.events.append("ack_failed")

    def insert_collector_error(self, **kwargs) -> None:
        self.errors.append(kwargs)


def make_runtime() -> StationRuntime:
    station = StationMapping(
        station_id="WS01",
        name="Screw Station",
        db_number=101,
        upstream_station_id=None,
        dmc_role="child_dmc",
        fields=(),
    )
    return StationRuntime(
        station=station,
        plan=ReadPlan(scope="WS01", db_number=101, read_start=0, read_size=64, fields=()),
    )


def make_worker(storage: FakeStorage, client: FakeClient) -> EventCollectorWorker:
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.client = client
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.timezone = ZoneInfo("Asia/Shanghai")
    worker.mapping = type("Mapping", (), {"code_tables": {}})()
    worker._adapt_station_runtime_payload = lambda *args, **kwargs: accepted_adapter_decision()
    if client.events is None:
        client.events = storage.events
    return worker


def ready_payload(counter: int = 5, *, read_done: bool = False) -> dict[str, object]:
    return {
        "station_status": 1,
        "cycle_counter": counter,
        "payload_ready": True,
        "read_done": read_done,
        "ack_timeout": False,
        "cycle_valid": True,
        "result": 1,
        "nok_code_count": 0,
        "station_dmc": "SUB-000005",
        "unit_id": "U-20260618-000005",
    }


def accepted_adapter_decision() -> SimpleNamespace:
    return SimpleNamespace(
        disposition="accepted",
        final_error_code=None,
        normalized_event={
            "line_id": "LINE_001",
            "plc_id": "PLC_001",
            "station_id": "WS01",
            "station_type": "screw",
            "profile_id": "normal_screwdriving",
            "config_hash": "a" * 64,
            "config_version": "2026.06.20-1",
            "event_type": "station_result",
            "result": "ok",
            "unit_id": "U-20260618-000005",
            "dmc": "SUB-000005",
            "cycle_counter": 5,
            "event_ts": "2026-06-26T10:00:30Z",
            "correlation": {
                "source_event_id": "PLC_001:WS01:5:station_result",
                "fact_key": "sha256:" + "1" * 64,
            },
        },
        fact_key="sha256:" + "1" * 64,
        content_fingerprint="sha256:" + "2" * 64,
        projection_metadata=SimpleNamespace(production_outcome="ok", defect_detail=None),
    )


class EventCollectorReliabilityTest(unittest.TestCase):
    def test_reads_boot_identity_from_db104_mapping(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        runtime_db = bytearray(64)
        util.set_int(runtime_db, 0, 1)
        util.set_dint(runtime_db, 4, 25)
        util.set_dint(runtime_db, 8, 3)
        runtime_db[12] = 36
        runtime_db[13] = len(BOOT_ID)
        runtime_db[14 : 14 + len(BOOT_ID)] = BOOT_ID.encode("ascii")
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.mapping = mapping
        worker.line_plan = {plan.scope: plan for plan in build_read_plans(mapping)}["line"]
        worker.client = FakeClient(reads={104: runtime_db})

        self.assertEqual(BOOT_ID, worker._read_plc_boot_id())

    def test_invalid_db104_identity_is_rejected(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        runtime_db = bytearray(64)
        util.set_int(runtime_db, 0, 1)
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.mapping = mapping
        worker.line_plan = {plan.scope: plan for plan in build_read_plans(mapping)}["line"]
        worker.client = FakeClient(reads={104: runtime_db})

        with self.assertRaises(ValueError):
            worker._read_plc_boot_id()

    def test_database_failure_never_writes_ack_and_is_logged(self) -> None:
        storage = FakeStorage(fail_persist=True)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

        self.assertEqual([], client.writes)
        self.assertEqual(0, storage.ack_ok_calls)
        self.assertEqual("STORAGE_WRITE_FAILED", storage.errors[-1]["error_type"])

    def test_ack_write_failure_is_marked_then_retried_on_same_payload(self) -> None:
        storage = FakeStorage()
        client = FakeClient(fail_writes=1)
        worker = make_worker(storage, client)
        runtime = make_runtime()
        data = bytearray(64)

        worker._process_station(runtime, data, ready_payload(), BOOT_ID)
        worker._process_station(runtime, data, ready_payload(), BOOT_ID)

        self.assertEqual(2, storage.persist_calls)
        self.assertEqual(2, storage.accepted_fact_calls)
        self.assertEqual(1, len(storage.accepted_facts))
        self.assertEqual(1, len({fact.source_identity for fact in storage.accepted_facts}))
        self.assertEqual(1, len({fact.fact_key for fact in storage.accepted_facts}))
        self.assertEqual(1, len(storage.persisted_cycles))
        self.assertEqual(1, storage.ack_failed_calls)
        self.assertEqual(1, storage.ack_ok_calls)
        self.assertEqual(1, len(client.writes))
        self.assertEqual(2, client.write_attempts)
        self.assertEqual("ACK_WRITE_FAILED", storage.errors[-1]["error_type"])
        self.assertEqual(
            [
                "begin",
                "accepted_fact",
                "persist_cycle",
                "commit",
                "ack_write_attempt",
                "ack_write_failed",
                "ack_failed",
                "begin",
                "accepted_fact",
                "persist_cycle",
                "commit",
                "ack_write_attempt",
                "ack_write",
                "ack_ok",
            ],
            storage.events,
        )

    def test_counter_reset_is_logged_without_persist_or_ack(self) -> None:
        storage = FakeStorage(max_counter=8)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(make_runtime(), bytearray(64), ready_payload(counter=1), BOOT_ID)

        self.assertEqual(0, storage.persist_calls)
        self.assertEqual([], client.writes)
        self.assertEqual("PLC_COUNTER_RESET", storage.errors[-1]["error_type"])
        self.assertEqual("COUNTER_RESET", storage.runtime_updates[-1]["collector_state"])

    def test_existing_read_done_repairs_database_ack_status_without_second_write(self) -> None:
        storage = FakeStorage(max_counter=5)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(
            make_runtime(),
            bytearray(64),
            ready_payload(counter=5, read_done=True),
            BOOT_ID,
        )

        self.assertEqual([], client.writes)
        self.assertEqual(0, client.write_attempts)
        self.assertEqual(1, storage.persist_calls)
        self.assertEqual(1, storage.accepted_fact_calls)
        self.assertEqual(1, len(storage.accepted_facts))
        self.assertEqual(1, storage.ack_ok_calls)
        self.assertEqual(
            ["begin", "accepted_fact", "persist_cycle", "commit", "ack_ok"],
            storage.events,
        )


class RuntimeLoadedObservabilityTest(unittest.TestCase):
    def startup_context(self, *, pid: int | None = None):
        from app.services.event_collector import CollectorStartupContext

        return CollectorStartupContext(
            collector_main_started_at_utc="2026-07-30T04:56:00Z",
            process_pid=os.getpid() if pid is None else pid,
        )

    def construct_worker(
        self,
        *,
        context=DEFAULT_CONTEXT,
        mapping=DEFAULT_MAPPING,
        logger=None,
        mapping_path: str = "config/mapping.yaml",
    ):
        if mapping is DEFAULT_MAPPING:
            mapping = load_edge_mapping("config/mapping.yaml")
        if context is DEFAULT_CONTEXT:
            context = self.startup_context()
        storage = FakeStorage()
        client = FakeClient()
        storage_constructor_calls: list[str] = []
        client_constructor_calls: list[str] = []

        def storage_factory(_dsn: str) -> FakeStorage:
            storage_constructor_calls.append("storage_construct")
            return storage

        def client_factory() -> FakeClient:
            client_constructor_calls.append("snap7_client_construct")
            return client

        self._storage_constructor_calls = storage_constructor_calls
        self._snap7_client_constructor_calls = client_constructor_calls
        logger_patch = patch.object(event_collector_module.logger, "info")
        logger_mock = logger_patch.start() if logger is None else logger
        self._runtime_logger = logger_mock
        self._constructor_storage = storage
        try:
            loader_patch = (
                patch.object(event_collector_module, "load_edge_mapping", return_value=mapping)
                if mapping is not None
                else nullcontext()
            )
            with patch.object(event_collector_module, "Storage", side_effect=storage_factory), patch.object(
                event_collector_module.snap7.client,
                "Client",
                side_effect=client_factory,
            ), patch.object(
                event_collector_module,
                "build_accepted_station_event_fact",
            ) as accepted_fact_builder, loader_patch:
                self._accepted_fact_builder = accepted_fact_builder
                worker = EventCollectorWorker(
                    dsn="postgresql://unused",
                    host="unused-host",
                    port=1102,
                    mapping_path=mapping_path,
                    startup_context=context,
                )
        finally:
            if logger is None:
                logger_patch.stop()
        return worker, logger_mock, storage, client

    def independent_expected_runtime_record(self, mapping) -> dict[str, object]:
        raw_mapping_bytes = Path("config/mapping.yaml").read_bytes()
        raw_mapping_sha256 = hashlib.sha256(raw_mapping_bytes).hexdigest()
        self.assertEqual(FROZEN_MAPPING_CONTENT_SHA256, raw_mapping_sha256)
        self.assertNotEqual(FROZEN_MAPPING_CONTENT_SHA256, FROZEN_RESOLVED_CONFIG_HASH)
        return {
            "evidence_schema_version": "edge-mes/collector-runtime-loaded/v1",
            "event_type": "collector_runtime_loaded",
            "mapping_path": str(Path("config/mapping.yaml").resolve()),
            "mapping_content_sha256": raw_mapping_sha256,
            "mapping_schema_version": "runtime-mapping/v1",
            "config_version": "2026.06.26-slice-a",
            "line_id": "LINE_001",
            "read_plan_count": 1 + len(mapping.stations),
            "resolved_config_hash": FROZEN_RESOLVED_CONFIG_HASH,
            "collector_main_started_at_utc": "2026-07-30T04:56:00Z",
            "process_pid": os.getpid(),
        }

    def assert_worker_constructor_failure_has_no_runtime_side_effects(
        self,
        *,
        exception: type[Exception],
        mapping=DEFAULT_MAPPING,
        mapping_path: str = "config/mapping.yaml",
    ) -> None:
        with patch.object(EventCollectorWorker, "run_forever") as run_forever, patch.object(
            threading,
            "Thread",
        ) as thread_constructor:
            with self.assertRaises(exception):
                self.construct_worker(mapping=mapping, mapping_path=mapping_path)

        runtime_loaded_messages = [
            call.args[0]
            for call in self._runtime_logger.call_args_list
            if call.args
            and isinstance(call.args[0], str)
            and call.args[0].startswith("collector_runtime_loaded_json=")
        ]
        self.assertEqual([], runtime_loaded_messages)
        self.assertEqual([], self._storage_constructor_calls)
        self.assertEqual([], self._snap7_client_constructor_calls)
        self.assertEqual(0, self._accepted_fact_builder.call_count)
        self.assertEqual([], self._constructor_storage.events)
        self.assertEqual(0, run_forever.call_count)
        self.assertEqual(0, thread_constructor.call_count)

    def test_worker_emits_one_exact_record_before_constructor_returns(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        expected_record = self.independent_expected_runtime_record(mapping)
        worker, logger, _storage, _client = self.construct_worker(mapping=mapping)

        self.assertIsNotNone(worker)
        self.assertEqual([], self._storage_constructor_calls)
        self.assertEqual(1, logger.call_count)
        self.assertEqual(1, len(logger.call_args.args))
        application_message = logger.call_args.args[0]
        prefix = "collector_runtime_loaded_json="
        self.assertTrue(application_message.startswith(prefix))
        payload = application_message[len(prefix) :]
        self.assertEqual(application_message, prefix + payload)
        decoder = json.JSONDecoder()
        record, end = decoder.raw_decode(payload)
        self.assertEqual(len(payload), end)
        self.assertEqual(record, json.loads(payload))
        self.assertEqual(
            {
                "evidence_schema_version",
                "event_type",
                "mapping_path",
                "mapping_content_sha256",
                "mapping_schema_version",
                "config_version",
                "line_id",
                "read_plan_count",
                "resolved_config_hash",
                "collector_main_started_at_utc",
                "process_pid",
            },
            set(record),
        )
        self.assertEqual(expected_record, record)
        expected_payload = json.dumps(
            expected_record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        self.assertEqual(expected_payload, payload)
        self.assertEqual(prefix + expected_payload, application_message)
        self.assertIsInstance(record["read_plan_count"], int)
        self.assertNotIsInstance(record["read_plan_count"], bool)
        self.assertGreater(record["read_plan_count"], 0)
        self.assertEqual(1 + len(mapping.stations), record["read_plan_count"])
        self.assertEqual(4, record["read_plan_count"])
        self.assertIsInstance(record["process_pid"], int)
        self.assertNotIsInstance(record["process_pid"], bool)
        self.assertGreater(record["process_pid"], 0)
        self.assertEqual(os.getpid(), record["process_pid"])
        self.assertEqual(FROZEN_MAPPING_CONTENT_SHA256, record["mapping_content_sha256"])
        self.assertEqual(FROZEN_RESOLVED_CONFIG_HASH, record["resolved_config_hash"])
        swapped_expected = dict(expected_record)
        swapped_expected["mapping_content_sha256"] = FROZEN_RESOLVED_CONFIG_HASH
        swapped_expected["resolved_config_hash"] = FROZEN_MAPPING_CONTENT_SHA256
        constant_expected = dict(expected_record)
        constant_expected["mapping_content_sha256"] = "0" * 64
        constant_expected["resolved_config_hash"] = "0" * 64
        self.assertNotEqual(expected_record, swapped_expected)
        self.assertNotEqual(expected_record, constant_expected)
        self.assertNotEqual(record, swapped_expected)
        self.assertNotEqual(record, constant_expected)
        self.assertNotIn("production", application_message.lower())
        self.assertNotIn("ack", application_message.lower())
        self.assertNotIn("read_done", application_message.lower())

    def test_disabled_configured_station_remains_in_read_plan_count(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        disabled_station = replace(mapping.stations[0], station_enabled=False)
        mapping = replace(mapping, stations=(disabled_station, *mapping.stations[1:]))

        _worker, logger, _storage, _client = self.construct_worker(mapping=mapping)

        record = json.loads(logger.call_args.args[0].split("=", 1)[1])
        self.assertEqual(len(build_read_plans(mapping)), record["read_plan_count"])

    def test_duplicate_plan_scope_fails_before_success_emission(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        plans = build_read_plans(mapping)

        with patch.object(event_collector_module, "build_read_plans", return_value=[plans[0], *plans]):
            with self.assertRaises(ValueError):
                self.construct_worker(mapping=mapping)

    def test_missing_plan_scope_fails_before_success_emission(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        plans = build_read_plans(mapping)

        with patch.object(
            event_collector_module,
            "build_read_plans",
            return_value=[plan for plan in plans if plan.scope != "WS02"],
        ):
            with self.assertRaises(ValueError):
                self.construct_worker(mapping=mapping)

    def test_extra_plan_scope_and_scope_multiset_mismatch_fail_closed(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        plans = build_read_plans(mapping)
        cases = [
            [*plans, replace(plans[-1], scope="EXTRA")],
            [plans[0], replace(plans[1], scope="EXTRA"), *plans[2:]],
        ]

        for generated_plans in cases:
            with self.subTest(scopes=[plan.scope for plan in generated_plans]):
                with patch.object(
                    event_collector_module,
                    "build_read_plans",
                    return_value=generated_plans,
                ):
                    with self.assertRaises(ValueError):
                        self.construct_worker(mapping=mapping)

    def test_duplicate_configured_station_id_fails_before_dict_conversion(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        duplicate_station = replace(mapping.stations[1], station_id=mapping.stations[0].station_id)
        mapping = replace(mapping, stations=(mapping.stations[0], duplicate_station, *mapping.stations[2:]))

        with self.assertRaises(ValueError):
            self.construct_worker(mapping=mapping)

    def test_constructor_validation_failure_has_no_plc_db_ack_or_read_done_side_effect(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        plans = build_read_plans(mapping)
        storage = FakeStorage()
        client = FakeClient()

        with patch.object(event_collector_module, "Storage", return_value=storage), patch.object(
            event_collector_module.snap7.client,
            "Client",
            return_value=client,
        ), patch.object(event_collector_module, "load_edge_mapping", return_value=mapping), patch.object(
            event_collector_module,
            "build_read_plans",
            return_value=[plans[0], *plans],
        ):
            with self.assertRaises(ValueError):
                EventCollectorWorker(
                    dsn="postgresql://unused",
                    host="unused-host",
                    port=1102,
                    mapping_path="config/mapping.yaml",
                    startup_context=self.startup_context(),
                )

        self.assertEqual([], storage.events)
        self.assertEqual([], client.writes)
        self.assertEqual(0, client.write_attempts)

    def test_constructor_failure_paths_make_zero_storage_constructor_calls(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        plans = build_read_plans(mapping)
        cases = [
            ("scope", patch.object(event_collector_module, "build_read_plans", return_value=[plans[0], *plans])),
            ("line", None),
        ]
        mismatched_plc = dict(mapping.plcs[0])
        mismatched_plc["line_id"] = "LINE_OTHER"

        for name, plan_patch in cases:
            with self.subTest(name=name):
                failing_mapping = (
                    replace(mapping, plcs=(mismatched_plc,)) if name == "line" else mapping
                )
                context_manager = plan_patch if plan_patch is not None else nullcontext()
                with context_manager, self.assertRaises(ValueError):
                    self.construct_worker(mapping=failing_mapping)
                self.assertEqual([], self._storage_constructor_calls)

    def test_loader_and_resolved_identity_failures_have_no_worker_runtime_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            invalid_utf8 = temp_path / "invalid.yaml"
            invalid_utf8.write_bytes(b"line_id: \xff\n")
            malformed_yaml = temp_path / "malformed.yaml"
            malformed_yaml.write_bytes(b"line_id: [\n")
            duplicate_key = temp_path / "duplicate.yaml"
            duplicate_key.write_bytes(b"line_id: LINE_001\nline_id: LINE_002\n")

            for mapping_path, exception in (
                (invalid_utf8, UnicodeDecodeError),
                (malformed_yaml, yaml.YAMLError),
                (duplicate_key, RuntimeMappingContractError),
            ):
                with self.subTest(mapping_path=mapping_path.name):
                    self.assert_worker_constructor_failure_has_no_runtime_side_effects(
                        exception=exception,
                        mapping=None,
                        mapping_path=str(mapping_path),
                    )

        valid_mapping = load_edge_mapping("config/mapping.yaml")
        tampered_runtime_snapshot = replace(
            valid_mapping.runtime_snapshot,
            config_hash="0" * 64,
        )
        tampered_mapping = replace(valid_mapping, runtime_snapshot=tampered_runtime_snapshot)
        self.assert_worker_constructor_failure_has_no_runtime_side_effects(
            exception=ValueError,
            mapping=tampered_mapping,
        )

    def test_canonical_snapshot_line_and_selected_routing_line_must_match(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        mismatched_plc = dict(mapping.plcs[0])
        mismatched_plc["line_id"] = "LINE_OTHER"
        mapping = replace(mapping, plcs=(mismatched_plc,))

        with self.assertRaises(ValueError):
            self.construct_worker(mapping=mapping)

    def test_missing_or_ambiguous_routing_selection_fails_closed(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        missing_line = dict(mapping.plcs[0])
        missing_line.pop("line_id")
        empty_line = dict(mapping.plcs[0])
        empty_line["line_id"] = ""
        for plcs in ((), (mapping.plcs[0], mapping.plcs[0]), (missing_line,), (empty_line,)):
            with self.subTest(plcs=len(plcs)):
                with self.assertRaises(ValueError):
                    self.construct_worker(mapping=replace(mapping, plcs=plcs))

    def test_startup_context_is_mandatory_pid_bound_and_single_use(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")

        with self.assertRaises(ValueError):
            self.construct_worker(context=None, mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)
        with self.assertRaises(ValueError):
            self.construct_worker(context=self.startup_context(pid=os.getpid() + 1), mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)

        context = self.startup_context()
        self.construct_worker(context=context, mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)
        with self.assertRaises(ValueError):
            self.construct_worker(context=context, mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)

    def test_constructor_failure_consumes_context_and_prevents_retry(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        mismatched_plc = dict(mapping.plcs[0])
        mismatched_plc["line_id"] = "LINE_OTHER"
        failing_mapping = replace(mapping, plcs=(mismatched_plc,))
        context = self.startup_context()

        with self.assertRaises(ValueError):
            self.construct_worker(context=context, mapping=failing_mapping)
        self.assertEqual([], self._storage_constructor_calls)
        with self.assertRaises(ValueError):
            self.construct_worker(context=context, mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)

    def test_serialization_or_logger_failure_propagates_without_success_record(self) -> None:
        context = self.startup_context()
        mapping = load_edge_mapping("config/mapping.yaml")
        with patch.object(event_collector_module.json, "dumps", side_effect=RuntimeError("serialize")):
            with self.assertRaises(RuntimeError):
                self.construct_worker(context=context, mapping=mapping)
        self.assertEqual([], self._storage_constructor_calls)

        context = self.startup_context()
        with patch.object(event_collector_module.logger, "info", side_effect=RuntimeError("log")):
            with self.assertRaises(RuntimeError):
                self.construct_worker(context=context, logger=event_collector_module.logger.info)
        self.assertEqual([], self._storage_constructor_calls)

    def test_main_passes_one_context_and_emits_before_thread_start(self) -> None:
        events: list[str] = []

        class FakeEventWorker:
            def __init__(self, **kwargs) -> None:
                context = kwargs["startup_context"]
                self.assert_context(context)
                events.append("record")

            @staticmethod
            def assert_context(context) -> None:
                assert context.process_pid == os.getpid()
                assert context.collector_main_started_at_utc.endswith("Z")

            def run_forever(self) -> None:
                raise AssertionError("run_forever must not run in this test")

        class FakeThread:
            def __init__(self, **_kwargs) -> None:
                events.append("thread_construct")

            def start(self) -> None:
                events.append("thread_start")

        class StopSource:
            def read(self):
                raise SystemExit()

        def storage_factory(_dsn: str) -> FakeStorage:
            events.append("legacy_storage_construct")
            return FakeStorage()

        with patch.object(collector_main, "load_config", return_value={"collector": {}}), patch.object(
            collector_main, "event_collector_enabled", return_value=True
        ), patch.object(collector_main, "EventCollectorWorker", FakeEventWorker), patch.object(
            collector_main, "threading"
        ) as threading_module, patch.object(collector_main, "SimulatorSource", return_value=StopSource()), patch.object(
            collector_main, "Storage", side_effect=storage_factory
        ), patch.object(collector_main, "EventDetector", return_value=object()), patch.object(
            collector_main, "database_url", return_value="unused"
        ), patch.object(collector_main, "snap7_host", return_value="unused"), patch.object(
            collector_main, "snap7_port", return_value=1102
        ), patch.object(collector_main.logger, "info"):
            threading_module.Thread = FakeThread
            with self.assertRaises(SystemExit):
                collector_main.main()

        self.assertEqual(
            ["record", "thread_construct", "thread_start", "legacy_storage_construct"],
            events,
        )

    def test_constructor_failure_prevents_main_thread_start(self) -> None:
        class FailingEventWorker:
            def __init__(self, **_kwargs) -> None:
                raise RuntimeError("constructor failed")

        class FakeThread:
            started = False

            def __init__(self, **_kwargs) -> None:
                pass

            def start(self) -> None:
                FakeThread.started = True

        storage_constructor_calls: list[str] = []

        def storage_factory(_dsn: str) -> FakeStorage:
            storage_constructor_calls.append("legacy_storage_construct")
            return FakeStorage()

        with patch.object(collector_main, "load_config", return_value={"collector": {}}), patch.object(
            collector_main, "event_collector_enabled", return_value=True
        ), patch.object(collector_main, "EventCollectorWorker", FailingEventWorker), patch.object(
            collector_main.threading, "Thread", FakeThread
        ), patch.object(collector_main, "SimulatorSource", return_value=object()), patch.object(
            collector_main, "Storage", side_effect=storage_factory
        ), patch.object(collector_main, "EventDetector", return_value=object()), patch.object(
            collector_main, "database_url", return_value="unused"
        ), patch.object(collector_main, "snap7_host", return_value="unused"), patch.object(
            collector_main, "snap7_port", return_value=1102
        ):
            with self.assertRaises(RuntimeError):
                collector_main.main()

        self.assertFalse(FakeThread.started)
        self.assertEqual([], storage_constructor_calls)

    def test_run_forever_constructs_storage_once_before_first_poll(self) -> None:
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.dsn = "postgresql://unused"
        worker.host = "unused-host"
        worker.port = 1102
        worker.station_runtimes = []
        events: list[str] = []

        def storage_factory(_dsn: str) -> FakeStorage:
            events.append("storage_construct")
            return FakeStorage()

        def poll_once() -> None:
            events.append("poll_once")
            raise KeyboardInterrupt()

        worker.poll_once = poll_once
        with patch.object(event_collector_module, "Storage", side_effect=storage_factory), patch.object(
            event_collector_module.logger, "info"
        ):
            with self.assertRaises(KeyboardInterrupt):
                worker.run_forever()

        self.assertEqual(["storage_construct", "poll_once"], events)

    def test_run_forever_storage_failure_is_not_retried_or_reemitted(self) -> None:
        worker, _logger, _storage, _client = self.construct_worker()
        storage_constructor_calls: list[str] = []

        def failing_storage_factory(_dsn: str) -> FakeStorage:
            storage_constructor_calls.append("storage_construct")
            raise RuntimeError("storage initialization failed")

        with patch.object(event_collector_module, "Storage", side_effect=failing_storage_factory), patch.object(
            event_collector_module.logger, "info"
        ) as logger:
            with self.assertRaisesRegex(RuntimeError, "storage initialization failed"):
                worker.run_forever()

        self.assertEqual(["storage_construct"], storage_constructor_calls)
        runtime_loaded_messages = [
            call.args[0]
            for call in logger.call_args_list
            if call.args and isinstance(call.args[0], str) and call.args[0].startswith("collector_runtime_loaded_json=")
        ]
        self.assertEqual([], runtime_loaded_messages)

    def test_disabled_event_collector_does_not_receive_startup_context(self) -> None:
        class UnexpectedEventWorker:
            def __init__(self, **_kwargs) -> None:
                raise AssertionError("disabled collector must not construct worker")

        class StopSource:
            def read(self):
                raise SystemExit()

        with patch.object(collector_main, "load_config", return_value={"collector": {}}), patch.object(
            collector_main, "event_collector_enabled", return_value=False
        ), patch.object(collector_main, "EventCollectorWorker", UnexpectedEventWorker), patch.object(
            collector_main, "SimulatorSource", return_value=StopSource()
        ), patch.object(collector_main, "Storage", return_value=FakeStorage()), patch.object(
            collector_main, "EventDetector", return_value=object()
        ), patch.object(collector_main, "database_url", return_value="unused"):
            with self.assertRaises(SystemExit):
                collector_main.main()


if __name__ == "__main__":
    unittest.main()
