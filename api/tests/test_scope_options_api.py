from __future__ import annotations

import hashlib
import importlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import app


MISSING = object()
SCOPE_OPTIONS_PATH = "/api/v2/production/scope-options"


def valid_stations() -> list[dict[str, object]]:
    return [
        {"station_id": "WS01", "name": "Screw Station", "station_order": 1},
        {"station_id": "WS02", "name": "EOL Test Station", "station_order": 2},
        {"station_id": "WS03", "name": "Label Station", "station_order": 3},
    ]


def valid_mapping(
    stations: list[dict[str, object]] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "runtime-mapping/v1",
        "config_version": "2026.06.26-slice-a",
        "authoritative_source": "config/mapping.yaml",
        "line_id": "LINE_001",
        "timezone": "Asia/Shanghai",
        "runtime_defaults": {"station_enabled": True},
        "line": {
            "line_id": "LINE_001",
            "name": "Demo Assembly Line Runtime",
        },
        "stations": deepcopy(stations if stations is not None else valid_stations()),
    }


def write_mapping(path: Path, mapping: dict[str, Any]) -> bytes:
    raw = yaml.safe_dump(mapping, sort_keys=False).encode("utf-8")
    path.write_bytes(raw)
    return raw


def service_module():
    return importlib.import_module("app.services.scope_catalog")


def route_module():
    return importlib.import_module("app.routes.scope_options")


def load_catalog(path: Path) -> dict[str, object]:
    return service_module().load_scope_catalog(path)


def set_field(mapping: dict[str, Any], field: str, value: object) -> None:
    parts = field.split(".")
    container: dict[str, Any] = mapping
    for part in parts[:-1]:
        container = container[part]
    if value is MISSING:
        container.pop(parts[-1], None)
    else:
        container[parts[-1]] = value


def assert_unavailable(path: Path) -> None:
    with pytest.raises(service_module().ScopeCatalogUnavailable):
        load_catalog(path)


def valid_dto() -> dict[str, object]:
    return {
        "contract_version": "production-scope-options/v1",
        "authority": {
            "kind": "active_runtime_mapping",
            "source": "config/mapping.yaml",
            "config_version": "2026.06.26-slice-a",
            "content_sha256": "sha256:catalog-test",
        },
        "timezone": "Asia/Shanghai",
        "utc_offset": "+08:00",
        "lines": [
            {
                "line_id": "LINE_001",
                "name": "Demo Assembly Line Runtime",
                "stations": [
                    {
                        "station_id": "WS01",
                        "name": "Screw Station",
                        "station_order": 1,
                    }
                ],
            }
        ],
    }


def patch_route_loader(monkeypatch: pytest.MonkeyPatch, loader) -> Any:
    route = route_module()
    monkeypatch.setattr(route, "load_scope_catalog", loader)
    return route


def test_service_returns_exact_ordered_dto_and_hashes_exact_mapping_bytes(
    tmp_path: Path,
) -> None:
    path = tmp_path / "mapping.yaml"
    raw = write_mapping(path, valid_mapping())

    result = load_catalog(path)

    assert result == {
        "contract_version": "production-scope-options/v1",
        "authority": {
            "kind": "active_runtime_mapping",
            "source": "config/mapping.yaml",
            "config_version": "2026.06.26-slice-a",
            "content_sha256": f"sha256:{hashlib.sha256(raw).hexdigest()}",
        },
        "timezone": "Asia/Shanghai",
        "utc_offset": "+08:00",
        "lines": [
            {
                "line_id": "LINE_001",
                "name": "Demo Assembly Line Runtime",
                "stations": valid_stations(),
            }
        ],
    }


def test_service_preserves_source_station_order_without_alphabetizing(
    tmp_path: Path,
) -> None:
    stations = [
        {"station_id": "Z_STATION", "name": "Zulu", "station_order": 1},
        {"station_id": "A_STATION", "name": "Alpha", "station_order": 2},
    ]
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping(stations))

    result = load_catalog(path)

    assert [station["station_id"] for station in result["lines"][0]["stations"]] == [
        "Z_STATION",
        "A_STATION",
    ]


def test_service_filters_disabled_stations_and_honors_station_override(
    tmp_path: Path,
) -> None:
    stations = valid_stations()
    stations[0]["station_enabled"] = False
    stations[2]["station_enabled"] = True
    mapping = valid_mapping(stations)
    mapping["runtime_defaults"]["station_enabled"] = False
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    result = load_catalog(path)

    assert [station["station_id"] for station in result["lines"][0]["stations"]] == [
        "WS03",
    ]


def test_service_rejects_all_disabled_stations(tmp_path: Path) -> None:
    stations = valid_stations()
    for station in stations:
        station["station_enabled"] = False
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping(stations))

    assert_unavailable(path)


@pytest.mark.parametrize(
    ("path_kind", "prepare"),
    [
        ("missing", lambda tmp_path: tmp_path / "missing.yaml"),
        ("directory", lambda tmp_path: tmp_path / "mapping.yaml"),
    ],
)
def test_service_rejects_missing_and_non_regular_paths(
    tmp_path: Path,
    path_kind: str,
    prepare,
) -> None:
    path = prepare(tmp_path)
    if path_kind == "directory":
        path.mkdir()

    assert_unavailable(path)


def test_service_rejects_symlink_path(tmp_path: Path) -> None:
    real_path = tmp_path / "real-mapping.yaml"
    link_path = tmp_path / "mapping.yaml"
    write_mapping(real_path, valid_mapping())
    link_path.symlink_to(real_path)

    assert_unavailable(link_path)


def test_service_converts_unreadable_file_to_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping())
    original_read_bytes = Path.read_bytes

    def deny_read(candidate: Path) -> bytes:
        if candidate == path:
            raise PermissionError("permission denied")
        return original_read_bytes(candidate)

    monkeypatch.setattr(Path, "read_bytes", deny_read)

    assert_unavailable(path)


@pytest.mark.parametrize(
    "raw",
    [
        b"\xff\xfe\xfd",
        b"line: [\n",
        b"!!python/object/apply:os.system ['echo unsafe']\n",
    ],
    ids=["invalid-utf8", "invalid-yaml", "unsafe-yaml"],
)
def test_service_rejects_invalid_utf8_invalid_yaml_and_unsafe_yaml(
    tmp_path: Path,
    raw: bytes,
) -> None:
    path = tmp_path / "mapping.yaml"
    path.write_bytes(raw)

    assert_unavailable(path)


@pytest.mark.parametrize("raw", [b"[]\n", b"null\n", b"plain scalar\n"])
def test_service_requires_mapping_root(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "mapping.yaml"
    path.write_bytes(raw)

    assert_unavailable(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("authoritative_source", MISSING, id="authority-missing"),
        pytest.param("authoritative_source", " ", id="authority-blank"),
        pytest.param("authoritative_source", 7, id="authority-wrong-type"),
        pytest.param("config_version", MISSING, id="version-missing"),
        pytest.param("config_version", " ", id="version-blank"),
        pytest.param("config_version", 7, id="version-wrong-type"),
        pytest.param("line_id", MISSING, id="root-line-missing"),
        pytest.param("line_id", " ", id="root-line-blank"),
        pytest.param("line_id", 7, id="root-line-wrong-type"),
        pytest.param("timezone", MISSING, id="timezone-missing"),
        pytest.param("timezone", " ", id="timezone-blank"),
        pytest.param("timezone", 7, id="timezone-wrong-type"),
    ],
)
def test_service_rejects_missing_blank_or_wrong_type_root_fields(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    mapping = valid_mapping()
    set_field(mapping, field, value)
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


def test_service_requires_exact_authoritative_source(tmp_path: Path) -> None:
    mapping = valid_mapping()
    mapping["authoritative_source"] = "config/other.yaml"
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("line", MISSING, id="line-missing"),
        pytest.param("line", [], id="line-wrong-type"),
        pytest.param("line.line_id", MISSING, id="nested-line-missing"),
        pytest.param("line.line_id", " ", id="nested-line-blank"),
        pytest.param("line.line_id", 7, id="nested-line-wrong-type"),
        pytest.param("line.name", MISSING, id="line-name-missing"),
        pytest.param("line.name", " ", id="line-name-blank"),
        pytest.param("line.name", 7, id="line-name-wrong-type"),
    ],
)
def test_service_rejects_invalid_nested_line_fields(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    mapping = valid_mapping()
    set_field(mapping, field, value)
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


def test_service_rejects_root_and_nested_line_mismatch(tmp_path: Path) -> None:
    mapping = valid_mapping()
    mapping["line"]["line_id"] = "LINE_999"
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


def test_service_rejects_unsupported_timezone(tmp_path: Path) -> None:
    mapping = valid_mapping()
    mapping["timezone"] = "UTC"
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("runtime_defaults", MISSING, id="runtime-defaults-missing"),
        pytest.param("runtime_defaults", [], id="runtime-defaults-wrong-type"),
        pytest.param(
            "runtime_defaults.station_enabled",
            MISSING,
            id="station-enabled-missing",
        ),
        pytest.param(
            "runtime_defaults.station_enabled",
            "true",
            id="station-enabled-string",
        ),
        pytest.param(
            "runtime_defaults.station_enabled",
            1,
            id="station-enabled-integer",
        ),
    ],
)
def test_service_requires_real_boolean_runtime_default(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    mapping = valid_mapping()
    set_field(mapping, field, value)
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


@pytest.mark.parametrize(
    "stations",
    [
        pytest.param(MISSING, id="stations-missing"),
        pytest.param({}, id="stations-wrong-type"),
        pytest.param([], id="stations-empty"),
        pytest.param(["not-a-mapping"], id="station-entry-wrong-type"),
    ],
)
def test_service_requires_nonempty_station_mapping_list(
    tmp_path: Path,
    stations: object,
) -> None:
    mapping = valid_mapping()
    if stations is MISSING:
        mapping.pop("stations")
    else:
        mapping["stations"] = stations
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("station_id", MISSING, id="station-id-missing"),
        pytest.param("station_id", " ", id="station-id-blank"),
        pytest.param("station_id", 7, id="station-id-wrong-type"),
        pytest.param("name", MISSING, id="station-name-missing"),
        pytest.param("name", " ", id="station-name-blank"),
        pytest.param("name", 7, id="station-name-wrong-type"),
        pytest.param("station_order", MISSING, id="station-order-missing"),
        pytest.param("station_order", "1", id="station-order-string"),
        pytest.param("station_order", True, id="station-order-boolean"),
        pytest.param("station_order", 0, id="station-order-zero"),
        pytest.param("station_order", -1, id="station-order-negative"),
        pytest.param("station_enabled", "true", id="station-enabled-string"),
        pytest.param("station_enabled", 1, id="station-enabled-integer"),
        pytest.param("station_enabled", None, id="station-enabled-null"),
    ],
)
def test_service_rejects_invalid_station_fields(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    mapping = valid_mapping()
    set_field(mapping["stations"][0], field, value)
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    assert_unavailable(path)


def test_service_rejects_duplicate_station_ids(tmp_path: Path) -> None:
    stations = valid_stations()
    stations[1]["station_id"] = stations[0]["station_id"]
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping(stations))

    assert_unavailable(path)


def test_service_rejects_duplicate_station_orders(tmp_path: Path) -> None:
    stations = valid_stations()
    stations[1]["station_order"] = stations[0]["station_order"]
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping(stations))

    assert_unavailable(path)


def test_service_rejects_non_increasing_source_station_order(tmp_path: Path) -> None:
    stations = valid_stations()
    stations[0]["station_order"] = 2
    stations[1]["station_order"] = 1
    path = tmp_path / "mapping.yaml"
    write_mapping(path, valid_mapping(stations))

    assert_unavailable(path)


def test_service_does_not_leak_unknown_or_forbidden_mapping_fields(
    tmp_path: Path,
) -> None:
    mapping = valid_mapping()
    mapping.update(
        {
            "plc_address": "DB104.DBW0",
            "credentials": "secret",
            "absolute_path": "/private/secret/mapping.yaml",
            "payload": {"raw_hex": "0001"},
            "nok": {"code": "NOK-1"},
            "database": "postgresql://secret",
            "unknown_config_field": "must-not-leak",
        }
    )
    mapping["stations"][0].update(
        {
            "plc_address": "DB101.DBW0",
            "payload": {"raw_hex": "0002"},
        }
    )
    path = tmp_path / "mapping.yaml"
    write_mapping(path, mapping)

    serialized = json.dumps(load_catalog(path), sort_keys=True)

    for forbidden in (
        "plc_address",
        "credentials",
        "absolute_path",
        "raw_hex",
        "NOK-1",
        "postgresql://secret",
        "must-not-leak",
    ):
        assert forbidden not in serialized


def test_route_returns_exact_dto_and_calls_loader_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0
    expected = valid_dto()

    def loader() -> dict[str, object]:
        nonlocal calls
        calls += 1
        return expected

    patch_route_loader(monkeypatch, loader)

    response = TestClient(app).get(SCOPE_OPTIONS_PATH)

    assert response.status_code == 200
    assert response.json() == expected
    assert calls == 1


@pytest.mark.parametrize(
    "params",
    [
        {"unexpected": "blocked"},
        [("unexpected", "one"), ("unexpected", "two")],
        [("line_id", "LINE_001"), ("line_id", "LINE_001")],
    ],
    ids=["unknown-query", "duplicate-unknown-query", "duplicate-query"],
)
def test_route_rejects_any_query_parameter_with_stable_422(
    monkeypatch: pytest.MonkeyPatch,
    params,
) -> None:
    calls = 0

    def loader() -> dict[str, object]:
        nonlocal calls
        calls += 1
        return valid_dto()

    patch_route_loader(monkeypatch, loader)

    response = TestClient(app, raise_server_exceptions=False).get(
        SCOPE_OPTIONS_PATH,
        params=params,
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "unsupported scope-options request"}
    assert calls == 0


def test_route_rejects_nonempty_body_with_stable_422(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def loader() -> dict[str, object]:
        nonlocal calls
        calls += 1
        return valid_dto()

    patch_route_loader(monkeypatch, loader)

    response = TestClient(app, raise_server_exceptions=False).request(
        "GET",
        SCOPE_OPTIONS_PATH,
        content=b"{}",
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "unsupported scope-options request"}
    assert calls == 0


def test_route_maps_unavailable_catalog_without_raw_exception_or_path_leakage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = route_module()
    error = route.ScopeCatalogUnavailable(
        "cannot read /private/secret/mapping.yaml: permission denied"
    )

    def loader() -> dict[str, object]:
        raise error

    monkeypatch.setattr(route, "load_scope_catalog", loader)

    response = TestClient(app, raise_server_exceptions=False).get(SCOPE_OPTIONS_PATH)

    assert response.status_code == 503
    assert response.json() == {"detail": "Scope catalog is not available."}
    assert "/private/secret/mapping.yaml" not in response.text
    assert "permission denied" not in response.text


def test_route_does_not_access_database_or_leak_forbidden_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = importlib.import_module("app.db")
    db_calls = 0

    def fail_db(*args, **kwargs):
        nonlocal db_calls
        db_calls += 1
        raise AssertionError("scope-options must not access the database")

    monkeypatch.setattr(database, "get_conn", fail_db)
    patch_route_loader(monkeypatch, lambda: valid_dto())

    payload = TestClient(app).get(SCOPE_OPTIONS_PATH).json()

    assert db_calls == 0
    assert set(payload) == {
        "contract_version",
        "authority",
        "timezone",
        "utc_offset",
        "lines",
    }
    assert "raw_payload" not in json.dumps(payload)
    assert "absolute_path" not in json.dumps(payload)


def test_scope_options_route_is_registered_exactly_once_as_get() -> None:
    routes = [
        (route.path, tuple(sorted(route.methods or ())))
        for route in app.routes
        if route.path == SCOPE_OPTIONS_PATH
    ]

    assert routes == [(SCOPE_OPTIONS_PATH, ("GET",))]
