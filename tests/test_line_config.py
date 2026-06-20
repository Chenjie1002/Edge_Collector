from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

from common.line_config import (
    LineConfigError,
    canonicalize_config,
    compute_config_hash,
    estimate_config_load,
    load_line_config,
    resolve_line_config,
)


ROOT = Path(__file__).resolve().parents[1]
LINES = ROOT / "config" / "lines"


@pytest.mark.parametrize(
    ("filename", "station_count"),
    [
        ("demo_3_station.yaml", 3),
        ("demo_10_station.yaml", 10),
        ("stress_20_station.yaml", 20),
    ],
)
def test_example_line_configs_load(filename: str, station_count: int) -> None:
    config = load_line_config(LINES / filename)

    assert len(config.stations) == station_count
    assert [station.station_order for station in config.stations] == sorted(
        station.station_order for station in config.stations
    )


def test_demo_3_station_preserves_phase1_structure() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")

    assert config.line_id == "LINE_001"
    assert config.plcs[0].plc_id == "PLC_001"
    assert config.plcs[0].runtime_db == 104
    assert [
        (
            station.station_id,
            station.station_order,
            station.station_type,
                station.db_mappings[0].db_number,
                station.cycle_time_s,
                station.effective_nok_rate,
        )
        for station in config.stations
    ] == [
        ("WS01", 10, "screwdriving", 101, 30.4, 0.02),
        ("WS02", 20, "eol_test", 102, 29.8, 0.015),
        ("WS03", 30, "manual_confirm", 103, 29.2, 0.01),
    ]

    with pytest.raises(FrozenInstanceError):
        config.line_id = "CHANGED"  # type: ignore[misc]


def _write_variant(tmp_path: Path, mutate) -> Path:
    raw = yaml.safe_load((LINES / "demo_3_station.yaml").read_text())
    mutate(raw)
    path = tmp_path / "line.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False))
    return path


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["stations"][1].update(
                station_id=raw["stations"][0]["station_id"]
            ),
            "duplicate station_id",
        ),
        (
            lambda raw: raw["stations"][1].update(
                station_order=raw["stations"][0]["station_order"]
            ),
            "duplicate station_order",
        ),
        (
            lambda raw: raw["stations"][0].update(nok_rate=1.1),
            "nok_rate must be between 0 and 1",
        ),
        (
            lambda raw: raw.pop("line_id"),
            "line_id is required",
        ),
        (
            lambda raw: raw["buffers"][0].update(buffer_position=25),
            "buffer_position must be between",
        ),
        (
            lambda raw: raw["plcs"][0].update(max_stations=2),
            "exceeds max_stations",
        ),
        (
            lambda raw: raw["stations"][0].update(payload_template="missing"),
            "payload_template 'missing' does not exist",
        ),
        (
            lambda raw: raw["stations"][0].update(nok_template="eol_test_nok_v1"),
            "is not compatible with station_type",
        ),
        (
            lambda raw: raw["stations"][0].update(cycle_profile="missing"),
            "cycle_profile 'missing' does not exist",
        ),
        (
            lambda raw: raw["stations"][1]["db_mappings"][0].update(db_number=101),
            "DB 101 conflicts",
        ),
        (
            lambda raw: raw["stations"][0].update(cycle_time_s=0),
            "cycle_time_s must be positive",
        ),
        (
            lambda raw: raw["plcs"][0].update(max_db_mappings_per_station=0),
            "max_db_mappings_per_station must be positive",
        ),
    ],
)
def test_invalid_line_configs_fail(tmp_path: Path, mutate, message: str) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


def test_missing_station_type_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0].pop("station_type"),
    )

    with pytest.raises(LineConfigError, match="stations\\[0\\]\\.station_type is required"):
        load_line_config(path)


def test_station_enabled_defaults_to_true(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0].pop("station_enabled"),
    )

    config = load_line_config(path)

    assert config.stations[0].station_enabled is True


def test_payload_template_may_be_null(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0].update(payload_template=None),
    )

    config = load_line_config(path)

    assert config.stations[0].payload_template is None


def test_station_db_mapping_limit_is_enforced(tmp_path: Path) -> None:
    def mutate(raw) -> None:
        raw["plcs"][0]["max_db_mappings_per_station"] = 1
        raw["stations"][0]["db_mappings"].append(
            {
                "mapping_id": "WS01_EXT",
                "db_number": 111,
                "purpose": "payload_ext",
            }
        )

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match="exceeds max_db_mappings_per_station"):
        load_line_config(path)


def test_station_db_cannot_conflict_with_runtime_db(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0]["db_mappings"][0].update(db_number=104),
    )

    with pytest.raises(LineConfigError, match="conflicts with runtime_db"):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda raw: raw.update(unexpected=True), "unexpected"),
        (lambda raw: raw["stations"][0].update(foo=True), r"stations\[0\]\.foo"),
        (lambda raw: raw["plcs"][0].update(unknown_key=True), r"plcs\[0\]\.unknown_key"),
        (lambda raw: raw["buffers"][0].update(unknown_key=True), r"buffers\[0\]\.unknown_key"),
        (
            lambda raw: raw["cycle_profiles"]["normal_screwdriving"].update(
                unknown_key=True
            ),
            r"cycle_profiles\.normal_screwdriving\.unknown_key",
        ),
        (
            lambda raw: raw["payload_templates"]["screwdriving_payload_v1"].update(
                unknown_key=True
            ),
            r"payload_templates\.screwdriving_payload_v1\.unknown_key",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"].update(
                unknown_key=True
            ),
            r"nok_templates\.screwdriving_nok_v1\.unknown_key",
        ),
        (
            lambda raw: raw["stations"][0]["db_mappings"][0].update(
                unknown_key=True
            ),
            r"stations\[0\]\.db_mappings\[0\]\.unknown_key",
        ),
        (
            lambda raw: raw["route_graph"].update(unknown_key=True),
            r"route_graph\.unknown_key",
        ),
        (
            lambda raw: raw["route_graph"]["edges"][0].update(unknown_key=True),
            r"route_graph\.edges\[0\]\.unknown_key",
        ),
        (
            lambda raw: raw["scenario"].update(unknown_key=True),
            r"scenario\.unknown_key",
        ),
        (
            lambda raw: raw["hardware_envelope"].update(unknown_key=True),
            r"hardware_envelope\.unknown_key",
        ),
    ],
)
def test_unknown_fields_fail(tmp_path: Path, mutate, message: str) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["cycle_profiles"]["normal_screwdriving"][
                "simulation"
            ].update(unknown_key=True),
            r"cycle_profiles\.normal_screwdriving\.simulation\.unknown_key",
        ),
        (
            lambda raw: raw["payload_templates"]["screwdriving_payload_v1"][
                "fields"
            ][0].update(unknown_key=True),
            r"payload_templates\.screwdriving_payload_v1\.fields\[0\]\.unknown_key",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"]["codes"][
                0
            ].update(unknown_key=True),
            r"nok_templates\.screwdriving_nok_v1\.codes\[0\]\.unknown_key",
        ),
    ],
)
def test_deeply_nested_unknown_fields_fail(
    tmp_path: Path, mutate, message: str
) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["stations"][0].update(station_type="teleporter"),
            r"stations\[0\]\.station_type",
        ),
        (
            lambda raw: raw["buffers"][0].update(buffer_type="teleporter"),
            r"buffers\[0\]\.buffer_type",
        ),
        (
            lambda raw: raw["cycle_profiles"]["normal_screwdriving"].update(
                mode="turbo"
            ),
            r"cycle_profiles\.normal_screwdriving\.mode",
        ),
    ],
)
def test_invalid_enums_fail(tmp_path: Path, mutate, message: str) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["stations"][0]["db_mappings"][0].update(
                usage="unknown"
            ),
            r"stations\[0\]\.db_mappings\[0\]\.usage",
        ),
        (
            lambda raw: raw["stations"][0]["db_mappings"][0].update(
                direction="write_only"
            ),
            r"stations\[0\]\.db_mappings\[0\]\.direction",
        ),
        (
            lambda raw: raw["stations"][0]["db_mappings"][0].update(
                mapping_type="unknown"
            ),
            r"stations\[0\]\.db_mappings\[0\]\.mapping_type",
        ),
        (
            lambda raw: raw["payload_templates"][
                "screwdriving_payload_v1"
            ].update(template_type="unknown"),
            r"payload_templates\.screwdriving_payload_v1\.template_type",
        ),
        (
            lambda raw: raw["payload_templates"]["screwdriving_payload_v1"][
                "fields"
            ][0].update(field_type="decimal128"),
            r"payload_templates\.screwdriving_payload_v1\.fields\[0\]\.field_type",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"].update(
                template_type="unknown"
            ),
            r"nok_templates\.screwdriving_nok_v1\.template_type",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"]["codes"][
                0
            ].update(category="unknown"),
            r"nok_templates\.screwdriving_nok_v1\.codes\[0\]\.category",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"]["codes"][
                0
            ].update(severity="unknown"),
            r"nok_templates\.screwdriving_nok_v1\.codes\[0\]\.severity",
        ),
        (
            lambda raw: raw["nok_templates"]["screwdriving_nok_v1"]["codes"][
                0
            ].update(mode="unknown"),
            r"nok_templates\.screwdriving_nok_v1\.codes\[0\]\.mode",
        ),
    ],
)
def test_additional_invalid_enums_fail(
    tmp_path: Path, mutate, message: str
) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


def test_profile_mode_and_simulation_timing_are_preserved() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")
    profiles = {profile.profile_id: profile for profile in config.cycle_profiles}
    profile = profiles["normal_screwdriving"]

    assert profile.mode == "normal"
    assert profile.ideal_cycle_time_s == 30.4
    assert profile.simulation.base_cycle_s == 30.4
    assert profile.simulation.jitter_s >= 0
    assert profile.simulation.cycle_scale == 1.0


def test_stress_profile_is_non_production_and_keeps_production_timing() -> None:
    config = load_line_config(LINES / "stress_20_station.yaml")

    assert config.scenario.scenario_type == "stress"
    assert config.scenario.production is False
    assert {profile.mode for profile in config.cycle_profiles} == {"stress"}
    assert all(profile.ideal_cycle_time_s > 5 for profile in config.cycle_profiles)
    assert all(
        profile.simulation.stress_cycle_time_s == 5
        for profile in config.cycle_profiles
    )
    assert all(
        profile.ideal_cycle_time_s != profile.simulation.stress_cycle_time_s
        for profile in config.cycle_profiles
    )


def test_config_version_resolved_config_and_hash_exist() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")
    resolved = resolve_line_config(config)

    assert config.schema_version == 1
    assert config.config_version
    assert len(config.config_hash) == 64
    assert resolved["config_hash"] == config.config_hash
    assert compute_config_hash(config) == config.config_hash
    assert canonicalize_config(config).startswith("{")


def test_config_version_is_required(tmp_path: Path) -> None:
    path = _write_variant(tmp_path, lambda raw: raw.pop("config_version"))

    with pytest.raises(LineConfigError, match="config_version is required"):
        load_line_config(path)


def test_config_hash_is_stable_for_same_semantic_config(tmp_path: Path) -> None:
    source = yaml.safe_load((LINES / "demo_3_station.yaml").read_text())
    reordered = dict(reversed(list(source.items())))
    first = tmp_path / "first.yaml"
    second = tmp_path / "second.yaml"
    first.write_text(yaml.safe_dump(source, sort_keys=False))
    second.write_text(yaml.safe_dump(reordered, sort_keys=False))

    assert load_line_config(first).config_hash == load_line_config(second).config_hash


def test_config_hash_changes_for_meaningful_change(tmp_path: Path) -> None:
    baseline = load_line_config(LINES / "demo_3_station.yaml")
    path = _write_variant(
        tmp_path,
        lambda raw: raw["scenario"].update(random_seed=raw["scenario"]["random_seed"] + 1),
    )

    assert load_line_config(path).config_hash != baseline.config_hash


def test_seed_global_nok_and_station_override_are_preserved() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")
    stations = {station.station_id: station for station in config.stations}

    assert config.scenario.random_seed == 20260620
    assert config.scenario.global_nok_rate == 0.01
    assert stations["WS01"].nok_rate == 0.02
    assert stations["WS01"].effective_nok_rate == 0.02
    assert stations["WS03"].nok_rate is None
    assert stations["WS03"].effective_nok_rate == 0.01


def test_explicit_null_station_nok_rate_uses_global_fallback(
    tmp_path: Path,
) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0].update(nok_rate=None),
    )

    config = load_line_config(path)

    assert config.stations[0].nok_rate is None
    assert (
        config.stations[0].effective_nok_rate
        == config.scenario.global_nok_rate
    )
    assert (
        resolve_line_config(config)["stations"][0]["effective_nok_rate"]
        == config.scenario.global_nok_rate
    )


def test_buffer_enabled_and_tracking_mode_are_preserved(tmp_path: Path) -> None:
    def mutate(raw) -> None:
        raw["buffers"][0].update(
            enabled=False,
            tracking_mode="unit_id",
        )

    path = _write_variant(tmp_path, mutate)
    config = load_line_config(path)

    assert config.buffers[0].enabled is False
    assert config.buffers[0].tracking_mode == "unit_id"
    resolved_buffer = resolve_line_config(config)["buffers"][0]
    assert resolved_buffer["enabled"] is False
    assert resolved_buffer["tracking_mode"] == "unit_id"


def test_invalid_buffer_tracking_mode_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["buffers"][0].update(tracking_mode="telepathy"),
    )

    with pytest.raises(
        LineConfigError,
        match=r"buffers\[0\]\.tracking_mode",
    ):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["scenario"].update(global_nok_rate=1.1),
            "scenario.global_nok_rate",
        ),
        (
            lambda raw: raw["stations"][0].update(nok_rate=-0.1),
            r"stations\[0\]\.nok_rate",
        ),
    ],
)
def test_invalid_nok_rates_fail(tmp_path: Path, mutate, message: str) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


def test_21_stations_fail_even_when_declared_limit_is_raised(tmp_path: Path) -> None:
    def mutate(raw) -> None:
        raw["plcs"][0]["max_stations"] = 21
        station = dict(raw["stations"][-1])
        station["station_id"] = "WS21"
        station["station_order"] = 210
        station["db_mappings"] = [dict(station["db_mappings"][0])]
        station["db_mappings"][0].update(
            mapping_id="WS21_MAIN", db_number=121, station_id="WS21"
        )
        raw["stations"].extend(
            [
                {
                    **station,
                    "station_id": f"WS{number:02d}",
                    "station_order": number * 10,
                    "db_mappings": [
                        {
                            **station["db_mappings"][0],
                            "mapping_id": f"WS{number:02d}_MAIN",
                            "station_id": f"WS{number:02d}",
                            "db_number": 120 + number,
                        }
                    ],
                }
                for number in range(4, 22)
            ]
        )
        raw["route_graph"]["terminal_station_id"] = "WS21"
        raw["route_graph"]["edges"].extend(
            {
                "from_station_id": f"WS{number - 1:02d}",
                "to_station_id": f"WS{number:02d}",
            }
            for number in range(4, 22)
        )

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match="hard maximum 20"):
        load_line_config(path)


def test_five_db_mappings_fail_even_when_declared_limit_is_raised(
    tmp_path: Path,
) -> None:
    def mutate(raw) -> None:
        raw["plcs"][0]["max_db_mappings_per_station"] = 5
        base = raw["stations"][0]["db_mappings"][0]
        raw["stations"][0]["db_mappings"] = [
            {
                **base,
                "mapping_id": f"WS01_{index}",
                "db_number": 110 + index,
            }
            for index in range(5)
        ]

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match="hard maximum 4"):
        load_line_config(path)


def test_station_references_unknown_plc_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path, lambda raw: raw["stations"][0].update(plc_id="PLC_UNKNOWN")
    )

    with pytest.raises(LineConfigError, match="PLC_UNKNOWN.*does not exist"):
        load_line_config(path)


def test_db_mapping_references_unknown_plc_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0]["db_mappings"][0].update(
            plc_id="PLC_UNKNOWN"
        ),
    )

    with pytest.raises(LineConfigError, match="PLC_UNKNOWN.*does not exist"):
        load_line_config(path)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("poll_interval_ms", None, "poll_interval_ms"),
        ("poll_interval_ms", 0, "poll_interval_ms"),
        ("read_size_bytes", 0, "read_size_bytes"),
    ],
)
def test_mapping_load_fields_are_required_and_validated(
    tmp_path: Path, field: str, value, message: str
) -> None:
    def mutate(raw) -> None:
        mapping = raw["stations"][0]["db_mappings"][0]
        if value is None:
            mapping.pop(field)
        else:
            mapping[field] = value

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


def test_runtime_db_reserved_conflict_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["stations"][0]["db_mappings"][0].update(
            db_number=104, usage="runtime"
        ),
    )

    with pytest.raises(LineConfigError, match="runtime_db"):
        load_line_config(path)


def test_reserved_nok_code_in_random_pool_fails(tmp_path: Path) -> None:
    def mutate(raw) -> None:
        code = raw["nok_templates"]["manual_confirm_nok_v1"]["codes"][-1]
        code.update(mode="random_simulated_nok", allow_random=True)

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match="reserved.*random"):
        load_line_config(path)


def test_forced_nok_code_must_be_explicitly_marked(tmp_path: Path) -> None:
    def mutate(raw) -> None:
        code = raw["nok_templates"]["screwdriving_nok_v1"]["codes"][0]
        code.update(mode="forced_test_nok", allow_force=False)

    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match="forced_test_nok.*allow_force"):
        load_line_config(path)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda raw: raw["buffers"][0].update(from_station_id="UNKNOWN"),
            r"buffers\[0\]\.from_station_id",
        ),
        (
            lambda raw: raw["stations"][1].update(station_enabled=False),
            r"buffers\[0\].*disabled",
        ),
        (
            lambda raw: raw["stations"][0].update(station_enabled=False),
            "route_graph.entry_station_id.*enabled",
        ),
        (
            lambda raw: raw["stations"][-1].update(station_enabled=False),
            "route_graph.terminal_station_id.*enabled",
        ),
    ],
)
def test_route_and_buffer_invalid_references_fail(
    tmp_path: Path, mutate, message: str
) -> None:
    path = _write_variant(tmp_path, mutate)

    with pytest.raises(LineConfigError, match=message):
        load_line_config(path)


def test_route_entry_and_terminal_are_valid() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")

    assert config.route_graph.entry_station_id == "WS01"
    assert config.route_graph.terminal_station_id == "WS03"


def test_stress_config_exposes_hardware_and_load_summary() -> None:
    config = load_line_config(LINES / "stress_20_station.yaml")
    summary = estimate_config_load(config)

    assert config.hardware_envelope.target_hardware_class == "raspberry_pi_5"
    assert config.hardware_envelope.intended_load_class == "stress"
    assert summary.station_count == 20
    assert summary.mapping_count >= 20
    assert summary.reads_per_second > 0
    assert summary.estimated_read_bytes_per_second > 0
    assert summary.estimated_event_rate_per_second > 0
    assert summary.estimated_payload_bytes_per_second > 0


def test_invalid_hardware_envelope_fails(tmp_path: Path) -> None:
    path = _write_variant(
        tmp_path,
        lambda raw: raw["hardware_envelope"].update(
            target_hardware_class="quantum_edge"
        ),
    )

    with pytest.raises(LineConfigError, match="hardware_envelope.target_hardware_class"):
        load_line_config(path)
