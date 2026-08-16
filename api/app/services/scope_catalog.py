from __future__ import annotations

import hashlib
import stat
from pathlib import Path
from typing import Any

import yaml


DEFAULT_MAPPING_PATH = Path("/app/config/mapping.yaml")


class ScopeCatalogUnavailable(Exception):
    pass


def _unavailable(detail: str) -> None:
    raise ScopeCatalogUnavailable(detail)


def _required_mapping(value: object, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _unavailable(f"{field_name} must be a mapping")
    return value


def _required_text(value: object, field_name: str) -> str:
    if type(value) is not str or not value.strip():
        _unavailable(f"{field_name} must be a nonblank string")
    return value


def _required_bool(value: object, field_name: str) -> bool:
    if type(value) is not bool:
        _unavailable(f"{field_name} must be a boolean")
    return value


def _required_positive_int(value: object, field_name: str) -> int:
    if type(value) is not int or value <= 0:
        _unavailable(f"{field_name} must be a positive integer")
    return value


def read_mapping_document(
    mapping_path: Path = DEFAULT_MAPPING_PATH,
) -> tuple[dict[str, Any], str]:
    """Read the active mapping once with the same identity checks as scope-options."""
    try:
        path = Path(mapping_path)
        path_stat = path.lstat()
        if not stat.S_ISREG(path_stat.st_mode) or stat.S_ISLNK(path_stat.st_mode):
            _unavailable("mapping path is not a regular file")

        raw_bytes = path.read_bytes()
        content_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        document = yaml.safe_load(raw_bytes.decode("utf-8"))
        root = _required_mapping(document, "mapping root")
        return root, content_sha256
    except ScopeCatalogUnavailable:
        raise
    except Exception as exc:
        raise ScopeCatalogUnavailable("scope catalog is unavailable") from exc


def load_scope_catalog(mapping_path: Path = DEFAULT_MAPPING_PATH) -> dict[str, object]:
    try:
        root, content_sha256 = read_mapping_document(mapping_path)

        authoritative_source = _required_text(
            root.get("authoritative_source"),
            "authoritative_source",
        )
        if authoritative_source != "config/mapping.yaml":
            _unavailable("authoritative_source is unsupported")

        config_version = _required_text(
            root.get("config_version"),
            "config_version",
        )
        root_line_id = _required_text(root.get("line_id"), "line_id")
        timezone = _required_text(root.get("timezone"), "timezone")
        if timezone != "Asia/Shanghai":
            _unavailable("timezone is unsupported")

        runtime_defaults = _required_mapping(
            root.get("runtime_defaults"),
            "runtime_defaults",
        )
        default_station_enabled = _required_bool(
            runtime_defaults.get("station_enabled"),
            "runtime_defaults.station_enabled",
        )

        line = _required_mapping(root.get("line"), "line")
        nested_line_id = _required_text(line.get("line_id"), "line.line_id")
        line_name = _required_text(line.get("name"), "line.name")
        if root_line_id != nested_line_id:
            _unavailable("root and nested line_id do not match")

        stations = root.get("stations")
        if not isinstance(stations, list) or not stations:
            _unavailable("stations must be a nonempty list")

        enabled_stations: list[dict[str, object]] = []
        seen_station_ids: set[str] = set()
        seen_station_orders: set[int] = set()
        previous_station_order: int | None = None

        for index, raw_station in enumerate(stations):
            station = _required_mapping(raw_station, f"stations[{index}]")
            station_id = _required_text(
                station.get("station_id"),
                f"stations[{index}].station_id",
            )
            station_name = _required_text(
                station.get("name"),
                f"stations[{index}].name",
            )
            station_order = _required_positive_int(
                station.get("station_order"),
                f"stations[{index}].station_order",
            )
            if station_id in seen_station_ids:
                _unavailable("duplicate station_id")
            if station_order in seen_station_orders:
                _unavailable("duplicate station_order")
            if (
                previous_station_order is not None
                and station_order <= previous_station_order
            ):
                _unavailable("station_order is not strictly increasing")
            seen_station_ids.add(station_id)
            seen_station_orders.add(station_order)
            previous_station_order = station_order

            station_enabled = default_station_enabled
            if "station_enabled" in station:
                station_enabled = _required_bool(
                    station["station_enabled"],
                    f"stations[{index}].station_enabled",
                )
            if station_enabled:
                enabled_stations.append(
                    {
                        "station_id": station_id,
                        "name": station_name,
                        "station_order": station_order,
                    }
                )

        if not enabled_stations:
            _unavailable("no enabled stations")

        return {
            "contract_version": "production-scope-options/v1",
            "authority": {
                "kind": "active_runtime_mapping",
                "source": authoritative_source,
                "config_version": config_version,
                "content_sha256": f"sha256:{content_sha256}",
            },
            "timezone": timezone,
            "utc_offset": "+08:00",
            "lines": [
                {
                    "line_id": root_line_id,
                    "name": line_name,
                    "stations": enabled_stations,
                }
            ],
        }
    except ScopeCatalogUnavailable:
        raise
    except Exception as exc:
        raise ScopeCatalogUnavailable("scope catalog is unavailable") from exc
