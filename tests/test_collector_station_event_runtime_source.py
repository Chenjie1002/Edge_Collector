from __future__ import annotations

from dataclasses import replace
from uuid import UUID

import pytest

from collector.app.plc.mapping import (
    RuntimeMappingContractError,
    compute_runtime_mapping_hash,
    parse_edge_mapping,
)
from collector.app.services.decoder_registry import (
    DecoderBinding,
    DecoderRegistrySnapshot,
)
from collector.app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    ResolvedConfigSnapshot,
    build_resolved_config_snapshot_from_mapping,
)
from collector.app.services.station_event_runtime_source import (
    RuntimeSourcePayloadError,
    build_runtime_source_payload,
)


def runtime_decoder_registry_hash() -> str:
    return DecoderRegistrySnapshot(
        registry_snapshot_id="runtime-decoder-registry-2026-06-28",
        registry_content_hash="",
        decoders=(
            DecoderBinding(
                decoder_id="collector.app.plc.decoder.decode_read_plan",
                decoder_version="1.0.0",
                callable_ref="collector.app.plc.decoder.decode_runtime_raw_hex_payload",
                decoder=None,
                payload_template="station_runtime_payload_v1",
            ),
        ),
    ).with_content_hash().registry_content_hash


def mapping_doc() -> dict:
    return {
        "schema_version": "runtime-mapping/v1",
        "config_version": "2026.06.26-slice-a",
        "authoritative_source": "config/mapping.yaml",
        "line_id": "LINE_001",
        "timezone": "Asia/Shanghai",
        "hash_algorithm": "sha256",
        "plc_identity_namespace": "vplc-db104",
        "decoder_registry": {
            "snapshot_id": "runtime-decoder-registry-2026-06-28",
            "content_hash": runtime_decoder_registry_hash(),
        },
        "runtime_defaults": {
            "station_enabled": True,
            "plc_id": "PLC_001",
            "station_type": "assembly",
            "cycle_profile": "normal",
            "payload_template": "station_runtime_payload_v1",
            "nok_template": "station_runtime_nok_v1",
            "raw_policy": "raw_not_provided",
            "decoder_id": "collector.app.plc.decoder.decode_read_plan",
            "decoder_version": "1.0.0",
            "source_namespace": "plc-runtime",
        },
        "route_graph": [
            {"from_station_id": "WS01", "to_station_id": "WS02"},
            {"from_station_id": "WS02", "to_station_id": "WS03"},
        ],
        "plcs": [
            {
                "plc_id": "PLC_001",
                "name": "Virtual S7 Line PLC",
                "host": "s7-plc-sim",
                "port": 1102,
                "rack": 0,
                "slot": 1,
                "connection_timeout_ms": 3000,
                "poll_interval_ms": 500,
                "line_id": "LINE_001",
            }
        ],
        "line": {"line_id": "LINE_001", "db_number": 104, "fields": {}},
        "station_template": {"header": {}},
        "stations": [
            {
                "station_id": "WS01",
                "name": "Screw Station",
                "db_number": 101,
                "station_order": 1,
                "mapping_id": "ws01_runtime_v1",
                "station_type": "screw",
                "cycle_profile": "normal_screwdriving",
                "payload": {
                    "torque": {"address": "DB101.DBD100", "type": "real"},
                },
            },
            {
                "station_id": "WS02",
                "name": "EOL Station",
                "db_number": 102,
                "station_order": 2,
                "mapping_id": "ws02_runtime_v1",
                "station_type": "eol_test",
                "cycle_profile": "normal_eol",
                "upstream_station_id": "WS01",
                "payload": {
                    "current": {"address": "DB102.DBD100", "type": "real"},
                },
            },
            {
                "station_id": "WS03",
                "name": "Label Station",
                "db_number": 103,
                "station_order": 3,
                "mapping_id": "ws03_runtime_v1",
                "station_type": "labeling",
                "cycle_profile": "normal_labeling",
                "upstream_station_id": "WS02",
                "payload": {
                    "serial_no": {"address": "DB103.DBD100", "type": "dint"},
                },
            },
        ],
        "code_tables": {
            "result": {0: "UNKNOWN", 1: "OK", 2: "NOK", 3: "SKIPPED"},
            "nok_codes": {10001: "WS01_TQ_LOW"},
        },
    }


def parse(doc: dict | None = None):
    return parse_edge_mapping(doc or mapping_doc())


def test_mapping_loader_accepts_explicit_contract_fields_and_freezes_computed_hash() -> None:
    mapping = parse()

    assert mapping.config_version == "2026.06.26-slice-a"
    assert mapping.runtime_snapshot.config_hash == compute_runtime_mapping_hash(mapping.runtime_snapshot)
    assert mapping.runtime_snapshot.decoder_registry_snapshot_id == "runtime-decoder-registry-2026-06-28"
    assert mapping.runtime_snapshot.decoder_registry_content_hash == runtime_decoder_registry_hash()
    assert mapping.runtime_snapshot.hash_algorithm == "sha256"
    assert mapping.runtime_snapshot.stations[0].mapping_id == "ws01_runtime_v1"
    assert mapping.runtime_snapshot.stations[0].decoder_id == "collector.app.plc.decoder.decode_read_plan"
    assert mapping.runtime_snapshot.stations[0].decoder_version == "1.0.0"
    assert mapping.runtime_snapshot.stations[1].direct_predecessor_station_id == "WS01"


@pytest.mark.parametrize(
    "missing_field",
    [
        "mapping_id",
        "payload_template",
        "station_type",
        "cycle_profile",
        "raw_policy",
        "decoder_version",
    ],
)
def test_mapping_loader_missing_required_contract_fields_fail_closed(missing_field: str) -> None:
    doc = mapping_doc()
    if missing_field in {"station_type", "cycle_profile"}:
        del doc["runtime_defaults"][missing_field]
        del doc["stations"][0][missing_field]
    elif missing_field in doc["runtime_defaults"]:
        del doc["runtime_defaults"][missing_field]
    else:
        del doc["stations"][0][missing_field]

    with pytest.raises(RuntimeMappingContractError, match=missing_field):
        parse(doc)


@pytest.mark.parametrize("missing_field", ["snapshot_id", "content_hash"])
def test_mapping_loader_missing_decoder_registry_authority_fails_closed(missing_field: str) -> None:
    doc = mapping_doc()
    del doc["decoder_registry"][missing_field]

    with pytest.raises(RuntimeMappingContractError, match=f"decoder_registry.{missing_field}"):
        parse(doc)


def test_mapping_loader_rejects_decoder_registry_hash_mismatch() -> None:
    doc = mapping_doc()
    doc["decoder_registry"]["content_hash"] = "0" * 64

    with pytest.raises(RuntimeMappingContractError, match="decoder_registry.content_hash"):
        parse(doc)


def test_runtime_mapping_hash_is_stable_for_semantic_same_content() -> None:
    left = parse(mapping_doc()).runtime_snapshot
    doc = mapping_doc()
    doc["stations"] = list(reversed(doc["stations"]))
    doc["route_graph"] = list(reversed(doc["route_graph"]))
    right = parse(doc).runtime_snapshot

    assert compute_runtime_mapping_hash(left) == compute_runtime_mapping_hash(right)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("line_id",), "LINE_002"),
        (("config_version",), "2026.06.26-slice-b"),
        (("stations", 0, "station_enabled"), False),
        (("stations", 0, "mapping_id"), "ws01_runtime_v2"),
        (("stations", 0, "nok_template"), "station_runtime_nok_v2"),
        (("stations", 0, "raw_policy"), "raw_required"),
        (("stations", 0, "station_type"), "inspection"),
        (("stations", 0, "cycle_profile"), "fast_screwdriving"),
        (("route_graph", 0, "from_station_id"), "WS03"),
    ],
)
def test_runtime_mapping_hash_changes_for_interpretation_affecting_fields(path: tuple, value) -> None:
    baseline = parse().runtime_snapshot.config_hash
    doc = mapping_doc()
    target = doc
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value

    assert parse(doc).runtime_snapshot.config_hash != baseline


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("stations", 0, "payload_template"), "station_runtime_payload_v2"),
        (("stations", 0, "decoder_id"), "decoder:v2"),
        (("stations", 0, "decoder_version"), "2.0.0"),
        (("decoder_registry", "snapshot_id"), "runtime-decoder-registry-2026-06-29"),
    ],
)
def test_decoder_bound_mapping_changes_without_registry_hash_sync_fail_closed(path: tuple, value) -> None:
    doc = mapping_doc()
    target = doc
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value

    with pytest.raises(RuntimeMappingContractError, match="decoder_registry.content_hash"):
        parse(doc)


@pytest.mark.parametrize(
    ("table", "key", "value"),
    [
        ("result", 2, "SCRAP"),
        ("nok_codes", 10001, "WS01_TQ_HIGH"),
    ],
)
def test_runtime_mapping_hash_changes_for_interpretation_code_tables(table: str, key: int, value: str) -> None:
    baseline = parse().runtime_snapshot.config_hash
    doc = mapping_doc()
    doc["code_tables"][table][key] = value

    assert parse(doc).runtime_snapshot.config_hash != baseline


def test_registry_builds_resolved_config_snapshot_from_runtime_mapping_snapshot() -> None:
    snapshot = build_resolved_config_snapshot_from_mapping(parse().runtime_snapshot)

    assert isinstance(snapshot, ResolvedConfigSnapshot)
    assert snapshot.config_hash == parse().runtime_snapshot.config_hash
    assert snapshot.content_hash_matches()
    assert snapshot.decoder_registry_snapshot_id == "runtime-decoder-registry-2026-06-28"
    assert snapshot.decoder_registry_content_hash == runtime_decoder_registry_hash()
    assert snapshot.decoder_registry is not None
    assert snapshot.decoder_registry.content_hash_matches()
    assert snapshot.station_for("WS02").decoder_version == "1.0.0"
    assert snapshot.station_for("WS02").payload_template == "station_runtime_payload_v1"
    assert snapshot.route_graph.edges[0].from_station_id == "WS01"


def test_registry_rejects_tampered_runtime_mapping_snapshot_hash_content() -> None:
    mapping = parse().runtime_snapshot
    tampered = replace(
        mapping,
        stations=(
            replace(mapping.stations[0], station_type="tampered"),
            mapping.stations[1],
            mapping.stations[2],
        ),
    )

    with pytest.raises(ValueError, match="CONFIG_HASH_MISMATCH"):
        build_resolved_config_snapshot_from_mapping(tampered)


def test_registry_lookup_rejects_duck_typed_unknown_snapshot_without_self_check() -> None:
    good = build_resolved_config_snapshot_from_mapping(parse().runtime_snapshot)

    class DuckSnapshot:
        config_hash = good.config_hash
        status = "found"

    registry = InMemoryResolvedConfigRegistry({good.config_hash: DuckSnapshot()})

    result = registry.lookup_resolved_config(good.config_hash)

    assert result.status == "hash_mismatch"


def test_source_builder_emits_deterministic_source_event_id_and_excludes_runtime_clock_identity() -> None:
    station = parse().runtime_snapshot.station_for("WS01")
    base = {
        "station_status": 1,
        "cycle_counter": 42,
        "cycle_valid": True,
        "result": 1,
        "unit_id": "UNIT-42",
        "station_dmc": "DMC-42",
        "plc_start_time": "2026-06-26T10:00:00+08:00",
        "plc_end_time": "2026-06-26T10:00:30+08:00",
        "nok_code_count": 0,
    }

    first = build_runtime_source_payload(
        decoded_fields=base,
        raw_bytes=None,
        station_snapshot=station,
        resolved_config_hash=parse().runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=parse().code_tables,
    )
    second = build_runtime_source_payload(
        decoded_fields=base,
        raw_bytes=None,
        station_snapshot=station,
        resolved_config_hash=parse().runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:59:59Z",
        code_tables=parse().code_tables,
    )

    assert first["source_event_id"] == second["source_event_id"]
    assert first["event_id"] == second["event_id"]
    assert first["event_id"] != first["source_event_id"]
    assert UUID(first["event_id"]).version == 4
    assert "retry_count" not in first
    assert "created_at" not in first
    assert first["event_ts"] == "2026-06-26T02:00:30Z"
    assert first["observed_at"] != second["observed_at"]


def test_source_builder_normalized_only_runtime_path_depends_on_raw_not_provided_policy() -> None:
    mapping = parse()
    station = mapping.runtime_snapshot.station_for("WS01")

    payload = build_runtime_source_payload(
        decoded_fields={
            "station_status": 1,
            "cycle_counter": 42,
            "cycle_valid": True,
            "result": 1,
            "unit_id": "UNIT-42",
            "station_dmc": "DMC-42",
            "plc_start_time": "2026-06-26T10:00:00+08:00",
            "plc_end_time": "2026-06-26T10:00:30+08:00",
            "nok_code_count": 0,
        },
        raw_bytes=None,
        station_snapshot=station,
        resolved_config_hash=mapping.runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert station.raw_policy == "raw_not_provided"
    assert "raw_payload" not in payload
    assert payload["payload"]["station_status"] == 1
    assert payload["config_hash"] == mapping.runtime_snapshot.config_hash


def test_source_builder_emits_raw_hex_from_station_read_plan_bytes() -> None:
    mapping = parse()
    station = replace(mapping.runtime_snapshot.station_for("WS01"), raw_policy="raw_capable")

    payload = build_runtime_source_payload(
        decoded_fields={
            "station_status": 1,
            "cycle_counter": 42,
            "cycle_valid": True,
            "result": 1,
            "unit_id": "UNIT-42",
            "station_dmc": "DMC-42",
            "plc_start_time": "2026-06-26T10:00:00+08:00",
            "plc_end_time": "2026-06-26T10:00:30+08:00",
            "nok_code_count": 0,
        },
        raw_bytes=b"\x01\x02\xfe\xff",
        station_snapshot=station,
        resolved_config_hash=mapping.runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert payload["raw_payload"] == {"raw_hex": "0102feff"}
    assert payload["payload"]["station_status"] == 1


@pytest.mark.parametrize("raw_policy", ["raw_required", "raw_capable", "unexpected_policy"])
def test_source_builder_missing_raw_fails_closed_unless_snapshot_declares_no_raw(raw_policy: str) -> None:
    mapping = parse()
    station = replace(mapping.runtime_snapshot.station_for("WS01"), raw_policy=raw_policy)

    with pytest.raises(RuntimeSourcePayloadError, match="RAW_EVIDENCE_MISSING"):
        build_runtime_source_payload(
            decoded_fields={
                "cycle_counter": 42,
                "cycle_valid": True,
                "result": 1,
                "unit_id": "UNIT-42",
                "station_dmc": "DMC-42",
                "plc_start_time": "2026-06-26T10:00:00+08:00",
                "plc_end_time": "2026-06-26T10:00:30+08:00",
                "nok_code_count": 0,
            },
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=mapping.runtime_snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=mapping.code_tables,
        )


def test_source_builder_station_nok_identity_appends_detail_fields() -> None:
    station = parse().runtime_snapshot.station_for("WS01")
    payload = build_runtime_source_payload(
        decoded_fields={
            "cycle_counter": 42,
            "cycle_valid": True,
            "result": 2,
            "unit_id": "UNIT-42",
            "station_dmc": "DMC-42",
            "plc_start_time": "2026-06-26T10:00:00+08:00",
            "plc_end_time": "2026-06-26T10:00:30+08:00",
            "nok_code_count": 1,
            "nok_codes_1": 10001,
        },
        raw_bytes=None,
        station_snapshot=station,
        resolved_config_hash=parse().runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=parse().code_tables,
        event_type="station_nok",
        parent_event_id="PARENT-EVENT-42",
        parent_fact_key="sha256:" + "1" * 64,
        detail_role="primary",
    )

    assert payload["event_type"] == "station_nok"
    assert payload["parent_event_id"] == "PARENT-EVENT-42"
    assert payload["parent_fact_key"] == "sha256:" + "1" * 64
    assert payload["detail_role"] == "primary"
    assert payload["nok_code"] == 10001
    assert payload["nok_origin"] == "plc"


def test_source_builder_station_nok_requires_authoritative_parent_event_id() -> None:
    station = parse().runtime_snapshot.station_for("WS01")

    with pytest.raises(RuntimeSourcePayloadError, match="NOK_PARENT_CONTEXT_MISSING"):
        build_runtime_source_payload(
            decoded_fields={
                "cycle_counter": 42,
                "cycle_valid": True,
                "result": 2,
                "unit_id": "UNIT-42",
                "station_dmc": "DMC-42",
                "plc_start_time": "2026-06-26T10:00:00+08:00",
                "plc_end_time": "2026-06-26T10:00:30+08:00",
                "nok_code_count": 1,
                "nok_codes_1": 10001,
            },
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=parse().runtime_snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=parse().code_tables,
            event_type="station_nok",
            parent_fact_key="sha256:" + "1" * 64,
            detail_role="primary",
        )


def test_source_builder_station_nok_source_identity_includes_parent_event_id() -> None:
    station = parse().runtime_snapshot.station_for("WS01")
    base_kwargs = {
        "decoded_fields": {
            "cycle_counter": 42,
            "cycle_valid": True,
            "result": 2,
            "unit_id": "UNIT-42",
            "station_dmc": "DMC-42",
            "plc_start_time": "2026-06-26T10:00:00+08:00",
            "plc_end_time": "2026-06-26T10:00:30+08:00",
            "nok_code_count": 1,
            "nok_codes_1": 10001,
        },
        "raw_bytes": None,
        "station_snapshot": station,
        "resolved_config_hash": parse().runtime_snapshot.config_hash,
        "plc_boot_id": "BOOT-1",
        "observed_at": "2026-06-26T02:00:31Z",
        "code_tables": parse().code_tables,
        "event_type": "station_nok",
        "parent_fact_key": "sha256:" + "1" * 64,
        "detail_role": "primary",
    }

    first = build_runtime_source_payload(parent_event_id="PARENT-EVENT-42", **base_kwargs)
    second = build_runtime_source_payload(parent_event_id="PARENT-EVENT-43", **base_kwargs)

    assert first["source_event_id"] != second["source_event_id"]
    assert first["event_id"] != second["event_id"]


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("raw_policy", "raw_required", "RAW_EVIDENCE_MISSING"),
        ("payload_template", "other_template", "PAYLOAD_TEMPLATE_MISMATCH"),
        ("station_type", "other_type", "STATION_TYPE_MISMATCH"),
        ("cycle_profile", "other_profile", "CYCLE_PROFILE_MISMATCH"),
    ],
)
def test_source_builder_policy_and_lineage_mismatches_reject_before_projection(field: str, value: str, match: str) -> None:
    station = parse().runtime_snapshot.station_for("WS01")
    station = replace(station, **{field: value})

    with pytest.raises(RuntimeSourcePayloadError, match=match):
        build_runtime_source_payload(
            decoded_fields={
                "cycle_counter": 42,
                "cycle_valid": True,
                "result": 1,
                "unit_id": "UNIT-42",
                "station_dmc": "DMC-42",
                "plc_start_time": "2026-06-26T10:00:00+08:00",
                "plc_end_time": "2026-06-26T10:00:30+08:00",
                "nok_code_count": 0,
                "payload_template": "station_runtime_payload_v1",
                "station_type": "screw",
                "cycle_profile": "normal_screwdriving",
            },
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=parse().runtime_snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=parse().code_tables,
        )
