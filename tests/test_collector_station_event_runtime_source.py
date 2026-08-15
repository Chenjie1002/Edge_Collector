from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import pytest
import yaml

from collector.app.plc.mapping import (
    RuntimeMappingContractError,
    compute_runtime_mapping_hash,
    load_edge_mapping,
    parse_edge_mapping,
)
from collector.app.plc import mapping as mapping_module
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
    _decode_result,
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


def test_mapping_loader_reads_exact_raw_bytes_once_and_binds_raw_identity(tmp_path: Path) -> None:
    raw_bytes = yaml.safe_dump(mapping_doc(), sort_keys=False, allow_unicode=True).encode("utf-8")
    mapping_path = tmp_path / "mapping.yaml"
    mapping_path.write_bytes(raw_bytes)
    original_read_bytes = Path.read_bytes
    original_read_text = Path.read_text
    read_bytes_count = 0
    read_text_count = 0

    def counted_read(path: Path) -> bytes:
        nonlocal read_bytes_count
        read_bytes_count += 1
        return original_read_bytes(path)

    def counted_text_read(path: Path, *args, **kwargs) -> str:
        nonlocal read_text_count
        read_text_count += 1
        return original_read_text(path, *args, **kwargs)

    with patch.object(Path, "read_bytes", counted_read), patch.object(
        Path,
        "read_text",
        counted_text_read,
    ), patch.object(
        mapping_module.yaml,
        "load",
        wraps=mapping_module.yaml.load,
    ) as yaml_load:
        mapping = load_edge_mapping(mapping_path)

    assert read_bytes_count == 1
    assert read_text_count == 0
    assert yaml_load.call_count == 1
    assert yaml_load.call_args.args[0] == raw_bytes.decode("utf-8")
    assert mapping.mapping_path == str(mapping_path.resolve())
    assert mapping.mapping_content_sha256 == hashlib.sha256(raw_bytes).hexdigest()
    assert mapping.mapping_content_sha256 == mapping.mapping_content_sha256.lower()
    assert len(mapping.mapping_content_sha256) == 64


def test_semantically_same_mapping_bytes_have_distinct_raw_sha_but_same_resolved_hash(tmp_path: Path) -> None:
    raw_bytes = yaml.safe_dump(mapping_doc(), sort_keys=False, allow_unicode=True).encode("utf-8")
    first_path = tmp_path / "first.yaml"
    second_path = tmp_path / "second.yaml"
    first_path.write_bytes(raw_bytes)
    second_path.write_bytes(raw_bytes + b"\n")

    first = load_edge_mapping(first_path)
    second = load_edge_mapping(second_path)

    assert first.mapping_content_sha256 != second.mapping_content_sha256
    assert first.runtime_snapshot.config_hash == second.runtime_snapshot.config_hash


@pytest.mark.parametrize(
    ("filename", "raw_bytes", "exception", "match"),
    [
        ("invalid.yaml", b"line_id: \xff\n", UnicodeDecodeError, None),
        ("malformed.yaml", b"line_id: [\n", yaml.YAMLError, None),
        (
            "duplicate.yaml",
            b"line_id: LINE_001\nline_id: LINE_002\n",
            RuntimeMappingContractError,
            "duplicate YAML mapping key",
        ),
    ],
)
def test_mapping_loader_failure_paths_read_raw_bytes_once_without_alternate_text_read(
    tmp_path: Path,
    filename: str,
    raw_bytes: bytes,
    exception: type[Exception],
    match: str | None,
) -> None:
    mapping_path = tmp_path / filename
    mapping_path.write_bytes(raw_bytes)
    original_read_bytes = Path.read_bytes
    original_read_text = Path.read_text
    read_bytes_count = 0
    read_text_count = 0

    def counted_read(path: Path) -> bytes:
        nonlocal read_bytes_count
        read_bytes_count += 1
        return original_read_bytes(path)

    def counted_text_read(path: Path, *args, **kwargs) -> str:
        nonlocal read_text_count
        read_text_count += 1
        return original_read_text(path, *args, **kwargs)

    with patch.object(Path, "read_bytes", counted_read), patch.object(
        Path,
        "read_text",
        counted_text_read,
    ):
        with pytest.raises(exception, match=match):
            load_edge_mapping(mapping_path)

    assert read_bytes_count == 1
    assert read_text_count == 0


def test_mapping_loader_rejects_final_symlink_without_any_content_read(tmp_path: Path) -> None:
    target_path = tmp_path / "target.yaml"
    target_path.write_bytes(yaml.safe_dump(mapping_doc(), sort_keys=False).encode("utf-8"))
    symlink_path = tmp_path / "mapping-link.yaml"
    symlink_path.symlink_to(target_path)
    original_read_bytes = Path.read_bytes
    original_read_text = Path.read_text
    read_bytes_count = 0
    read_text_count = 0

    def counted_read(path: Path) -> bytes:
        nonlocal read_bytes_count
        read_bytes_count += 1
        return original_read_bytes(path)

    def counted_text_read(path: Path, *args, **kwargs) -> str:
        nonlocal read_text_count
        read_text_count += 1
        return original_read_text(path, *args, **kwargs)

    with patch.object(Path, "read_bytes", counted_read), patch.object(
        Path,
        "read_text",
        counted_text_read,
    ):
        with pytest.raises(RuntimeMappingContractError, match="must not be a symlink"):
            load_edge_mapping(symlink_path)

    assert read_bytes_count == 0
    assert read_text_count == 0


def test_mapping_loader_rejects_non_regular_directory_without_any_content_read(tmp_path: Path) -> None:
    directory_path = tmp_path / "mapping-directory"
    directory_path.mkdir()
    original_read_bytes = Path.read_bytes
    original_read_text = Path.read_text
    read_bytes_count = 0
    read_text_count = 0

    def counted_read(path: Path) -> bytes:
        nonlocal read_bytes_count
        read_bytes_count += 1
        return original_read_bytes(path)

    def counted_text_read(path: Path, *args, **kwargs) -> str:
        nonlocal read_text_count
        read_text_count += 1
        return original_read_text(path, *args, **kwargs)

    with patch.object(Path, "read_bytes", counted_read), patch.object(
        Path,
        "read_text",
        counted_text_read,
    ):
        with pytest.raises(RuntimeMappingContractError, match="not a regular file"):
            load_edge_mapping(directory_path)

    assert read_bytes_count == 0
    assert read_text_count == 0


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


def test_real_mapping_ws01_ws02_ws03_declare_station_level_raw_capable_without_line_wide_default_change() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    raw_mapping = yaml.safe_load(Path("config/mapping.yaml").read_text())

    assert snapshot.station_for("WS01").mapping_id == "ws01_runtime_v1"
    assert snapshot.station_for("WS01").payload_template == "station_runtime_payload_v1"
    assert snapshot.station_for("WS01").raw_policy == "raw_capable"
    assert snapshot.station_for("WS02").mapping_id == "ws02_runtime_v1"
    assert snapshot.station_for("WS02").payload_template == "station_runtime_payload_v1"
    assert snapshot.station_for("WS02").raw_policy == "raw_capable"
    assert snapshot.station_for("WS03").mapping_id == "ws03_runtime_v1"
    assert snapshot.station_for("WS03").payload_template == "station_runtime_payload_v1"
    assert snapshot.station_for("WS03").raw_policy == "raw_capable"
    assert snapshot.config_hash == mapping.runtime_snapshot.config_hash
    assert raw_mapping["runtime_defaults"]["raw_policy"] == "raw_not_provided"


def real_runtime_decoded_fields() -> dict[str, object]:
    return {
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


@pytest.mark.parametrize(
    ("result_code", "expected"),
    ((0, "unknown"), (1, "ok"), (2, "nok"), (3, "skip")),
)
def test_runtime_result_code_table_canonicalizes_skipped_to_skip(
    result_code: int,
    expected: str,
) -> None:
    mapping = load_edge_mapping("config/mapping.yaml")

    assert _decode_result(result_code, mapping.code_tables) == expected


@pytest.mark.parametrize("station_id", ("WS02", "WS03"))
def test_downstream_skipped_result_builds_canonical_skip_source_payload(
    station_id: str,
) -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for(station_id)
    decoded_fields = {**real_runtime_decoded_fields(), "result": 3}

    payload = build_runtime_source_payload(
        decoded_fields=decoded_fields,
        raw_bytes=b"\x03\x00",
        station_snapshot=station,
        resolved_config_hash=snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert payload["result"] == "skip"
    assert payload["result"] != "skipped"


def test_real_mapping_ws01_raw_capable_source_builder_emits_raw_hex_without_replacing_normalized_payload() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS01")

    payload = build_runtime_source_payload(
        decoded_fields=real_runtime_decoded_fields(),
        raw_bytes=b"\x01\x02\xfe\xff",
        station_snapshot=station,
        resolved_config_hash=snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert station.raw_policy == "raw_capable"
    assert payload["raw_payload"] == {"raw_hex": "0102feff"}
    assert payload["payload"]["station_status"] == 1
    assert payload["unit_id"] == "UNIT-42"
    assert payload["config_hash"] == mapping.runtime_snapshot.config_hash


def test_real_mapping_ws01_raw_capable_missing_raw_fails_closed_without_downgrade() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS01")

    assert station.raw_policy == "raw_capable"
    with pytest.raises(RuntimeSourcePayloadError, match="RAW_EVIDENCE_MISSING"):
        build_runtime_source_payload(
            decoded_fields=real_runtime_decoded_fields(),
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=mapping.code_tables,
        )


def test_real_mapping_ws02_raw_capable_source_builder_emits_raw_hex_without_replacing_normalized_payload() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS02")

    payload = build_runtime_source_payload(
        decoded_fields=real_runtime_decoded_fields(),
        raw_bytes=b"\x10\x20\x30\x40",
        station_snapshot=station,
        resolved_config_hash=snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert station.raw_policy == "raw_capable"
    assert payload["raw_payload"] == {"raw_hex": "10203040"}
    assert payload["payload"]["station_status"] == 1
    assert payload["unit_id"] == "UNIT-42"
    assert payload["config_hash"] == mapping.runtime_snapshot.config_hash


def test_real_mapping_ws02_raw_capable_missing_raw_fails_closed_without_downgrade() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS02")

    assert station.raw_policy == "raw_capable"
    with pytest.raises(RuntimeSourcePayloadError, match="RAW_EVIDENCE_MISSING"):
        build_runtime_source_payload(
            decoded_fields=real_runtime_decoded_fields(),
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=mapping.code_tables,
        )


def test_real_mapping_ws03_raw_capable_source_builder_emits_raw_hex_without_replacing_normalized_payload() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS03")

    payload = build_runtime_source_payload(
        decoded_fields=real_runtime_decoded_fields(),
        raw_bytes=b"\x03\x30\x40\x50",
        station_snapshot=station,
        resolved_config_hash=snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert station.raw_policy == "raw_capable"
    assert payload["raw_payload"] == {"raw_hex": "03304050"}
    assert payload["payload"]["station_status"] == 1
    assert payload["unit_id"] == "UNIT-42"
    assert payload["config_hash"] == mapping.runtime_snapshot.config_hash


def test_real_mapping_ws03_raw_capable_missing_raw_fails_closed_without_downgrade() -> None:
    mapping = load_edge_mapping("config/mapping.yaml")
    snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    station = snapshot.station_for("WS03")

    assert station.raw_policy == "raw_capable"
    with pytest.raises(RuntimeSourcePayloadError, match="RAW_EVIDENCE_MISSING"):
        build_runtime_source_payload(
            decoded_fields=real_runtime_decoded_fields(),
            raw_bytes=None,
            station_snapshot=station,
            resolved_config_hash=snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=mapping.code_tables,
        )


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


def test_source_builder_empty_raw_bytes_keeps_explicit_empty_raw_hex() -> None:
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
        raw_bytes=b"",
        station_snapshot=station,
        resolved_config_hash=mapping.runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert payload["raw_payload"] == {"raw_hex": ""}


def test_source_builder_accepts_bytes_like_raw_without_mutating_normalized_payload() -> None:
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
        raw_bytes=memoryview(b"\x01\x02\x03"),
        station_snapshot=station,
        resolved_config_hash=mapping.runtime_snapshot.config_hash,
        plc_boot_id="BOOT-1",
        observed_at="2026-06-26T02:00:31Z",
        code_tables=mapping.code_tables,
    )

    assert payload["raw_payload"] == {"raw_hex": "010203"}
    assert payload["payload"]["station_status"] == 1


def test_source_builder_wrong_type_raw_bytes_fails_before_adapter_side_effects() -> None:
    mapping = parse()
    station = replace(mapping.runtime_snapshot.station_for("WS01"), raw_policy="raw_capable")

    with pytest.raises(TypeError):
        build_runtime_source_payload(
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
            raw_bytes=object(),
            station_snapshot=station,
            resolved_config_hash=mapping.runtime_snapshot.config_hash,
            plc_boot_id="BOOT-1",
            observed_at="2026-06-26T02:00:31Z",
            code_tables=mapping.code_tables,
        )


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
