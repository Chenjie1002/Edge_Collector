from __future__ import annotations

import hashlib
import copy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
import yaml

from app.services import deployment_plc
from app.main import app


client = TestClient(app)


def candidate_payload(**overrides: object) -> dict[str, object]:
    return {
        "host": "127.0.0.1",
        "port": 1102,
        "rack": 0,
        "slot": 1,
        "connection_timeout_ms": 3000,
        "poll_interval_ms": 500,
        "line_config": "demo_3_station.yaml",
        **overrides,
    }


def test_active_deployment_config_projects_current_mapping() -> None:
    response = client.get("/api/v2/deployment/plc/active")

    assert response.status_code == 200
    payload = response.json()
    assert payload["authority"] == {
        "kind": "active_runtime_mapping",
        "source": "config/mapping.yaml",
        "config_version": "2026.06.26-slice-a",
        "content_sha256": payload["authority"]["content_sha256"],
    }
    assert payload["line_id"] == "LINE_001"
    assert payload["plc"] == {
        "plc_id": "PLC_001",
        "host": "s7-plc-sim",
        "port": 1102,
        "rack": 0,
        "slot": 1,
        "connection_timeout_ms": 3000,
        "poll_interval_ms": 500,
    }
    assert payload["active_station_ids"] == ["WS01", "WS02", "WS03"]


def test_line_options_classify_valid_configs_without_overclaiming_runtime() -> None:
    response = client.get("/api/v2/deployment/plc/line-options")

    assert response.status_code == 200
    options = {item["file_name"]: item for item in response.json()["items"]}
    assert options["demo_3_station.yaml"]["capability"] == "CURRENTLY_SUPPORTED"
    assert options["demo_3_station.yaml"]["ready_to_activate"] is True
    assert options["demo_10_station.yaml"]["capability"] == (
        "CONFIG_VALID_RUNTIME_NOT_YET_SUPPORTED"
    )
    assert options["demo_10_station.yaml"]["ready_to_activate"] is False
    assert options["stress_20_station.yaml"]["capability"] == (
        "CONFIG_VALID_MULTI_PLC_RUNTIME_NOT_YET_SUPPORTED"
    )
    assert options["stress_20_station.yaml"]["ready_to_activate"] is False


def test_valid_candidate_is_ready_without_changing_active_mapping() -> None:
    response = client.post(
        "/api/v2/deployment/plc/validate",
        json={
            "host": "127.0.0.1",
            "port": 1102,
            "rack": 0,
            "slot": 1,
            "connection_timeout_ms": 3000,
            "poll_interval_ms": 500,
            "line_config": "demo_3_station.yaml",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["validation_state"] == "VALID"
    assert payload["ready_to_activate"] is True
    assert payload["candidate_hash"].startswith("sha256:")
    assert payload["active_mapping_hash"].startswith("sha256:")
    assert payload["candidate_hash"] != payload["active_mapping_hash"]


def test_invalid_candidate_returns_field_level_errors() -> None:
    response = client.post(
        "/api/v2/deployment/plc/validate",
        json={
            "host": " ",
            "port": 70000,
            "rack": -1,
            "slot": 99,
            "connection_timeout_ms": 10,
            "poll_interval_ms": 0,
            "line_config": "demo_10_station.yaml",
        },
    )

    assert response.status_code == 422
    fields = {item["field"] for item in response.json()["errors"]}
    assert {"host", "port", "rack", "slot", "connection_timeout_ms", "poll_interval_ms"} <= fields
    assert response.json()["ready_to_activate"] is False


def test_missing_line_config_returns_field_level_error() -> None:
    response = client.post(
        "/api/v2/deployment/plc/validate",
        json=candidate_payload(line_config="missing.yaml"),
    )

    assert response.status_code == 422
    assert response.json()["errors"] == [
        {
            "field": "line_config",
            "message": "Selected line configuration is not available or valid.",
        }
    ]


def test_valid_10_station_candidate_is_not_ready_to_activate() -> None:
    response = client.post(
        "/api/v2/deployment/plc/validate",
        json=candidate_payload(line_config="demo_10_station.yaml"),
    )

    assert response.status_code == 200
    assert response.json()["validation_state"] == "VALID_RUNTIME_NOT_SUPPORTED"
    assert response.json()["ready_to_activate"] is False
    assert response.json()["warnings"][0]["field"] == "line_config"


def test_candidate_identity_is_deterministic_for_same_semantic_content() -> None:
    first = client.post("/api/v2/deployment/plc/validate", json=candidate_payload()).json()
    second = client.post("/api/v2/deployment/plc/validate", json=candidate_payload()).json()

    assert first["candidate_hash"] == second["candidate_hash"]
    changed = client.post(
        "/api/v2/deployment/plc/validate",
        json=candidate_payload(host="10.0.0.50"),
    ).json()
    assert changed["candidate_hash"] != first["candidate_hash"]


class ReadOnlyClient:
    def __init__(self, *, failure: Exception | None = None) -> None:
        self.failure = failure
        self.calls: list[tuple[str, object]] = []

    def set_param(self, parameter: object, value: int) -> None:
        self.calls.append(("set_param", value))

    def connect(self, host: str, rack: int, slot: int, *, tcp_port: int) -> None:
        self.calls.append(("connect", (host, rack, slot, tcp_port)))
        if self.failure:
            raise self.failure

    def db_read(self, db_number: int, start: int, size: int) -> bytearray:
        self.calls.append(("db_read", (db_number, start, size)))
        return bytearray(size)

    def disconnect(self) -> None:
        self.calls.append(("disconnect", None))

    def __getattr__(self, name: str) -> object:
        if name in {"db_write", "write_area", "write_multi_vars"}:
            raise AssertionError(f"read-only test attempted forbidden operation: {name}")
        raise AttributeError(name)


def test_read_only_test_connection_connects_reads_and_disconnects_without_write() -> None:
    fake = ReadOnlyClient()

    result = deployment_plc.test_connection(
        candidate_payload(),
        client_factory=lambda: fake,
    )

    assert result["status"] == "CONNECTED_AND_READABLE"
    assert result["read_only"] is True
    assert result["writes_performed"] is False
    assert result["operations"] == ["connect", "db_read", "disconnect"]
    assert [call[0] for call in fake.calls] == ["set_param", "connect", "db_read", "disconnect"]


def test_connection_failure_is_safe_and_still_disconnects() -> None:
    fake = ReadOnlyClient(failure=TimeoutError("timed out"))

    result = deployment_plc.test_connection(
        candidate_payload(),
        client_factory=lambda: fake,
    )

    assert result["status"] == "TIMEOUT"
    assert result["read_only"] is True
    assert result["writes_performed"] is False
    assert fake.calls[-1][0] == "disconnect"


def test_candidate_save_and_load_leave_active_mapping_bytes_unchanged(tmp_path: Path) -> None:
    mapping_path = Path("config/mapping.yaml")
    before = hashlib.sha256(mapping_path.read_bytes()).hexdigest()

    saved = deployment_plc.save_candidate(
        candidate_payload(last_connection_test={"status": "CONNECTED_AND_READABLE", "read_only": True}),
        store_path=tmp_path,
    )
    loaded = deployment_plc.load_candidate(saved["candidate_id"], store_path=tmp_path)

    after = hashlib.sha256(mapping_path.read_bytes()).hexdigest()
    assert saved["status"] == "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION"
    assert loaded["candidate_hash"] == saved["candidate_hash"]
    assert loaded["last_connection_test"] == {
        "read_only": True,
        "status": "CONNECTED_AND_READABLE",
    }
    assert before == after


def test_candidate_route_retrieves_saved_artifact_without_active_mutation(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("DEPLOYMENT_CONFIG_DIR", str(tmp_path))
    response = client.post("/api/v2/deployment/plc/candidates", json=candidate_payload())

    assert response.status_code == 200
    candidate_id = response.json()["candidate_id"]
    retrieved = client.get(f"/api/v2/deployment/plc/candidates/{candidate_id}")

    assert retrieved.status_code == 200
    assert retrieved.json()["candidate_id"] == candidate_id
    assert retrieved.json()["status"] == "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION"


def _write_active_overlay(root: Path, baseline: Path, **plc_overrides: object) -> Path:
    document = yaml.safe_load(baseline.read_text(encoding="utf-8"))
    document["plcs"][0].update(plc_overrides)
    destination = root / "active" / "mapping.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return destination


def test_valid_active_overlay_becomes_effective_and_reports_overlay_authority(tmp_path: Path) -> None:
    baseline = Path("config/mapping.yaml")
    overlay = _write_active_overlay(tmp_path, baseline, connection_timeout_ms=2500)

    result = deployment_plc.load_active_deployment_config(
        mapping_path=baseline,
        store_path=tmp_path,
    )

    assert result["plc"]["connection_timeout_ms"] == 2500
    assert result["authority"]["source"] == "active/mapping.yaml"
    assert result["authority"]["content_sha256"] == f"sha256:{hashlib.sha256(overlay.read_bytes()).hexdigest()}"


def test_invalid_active_overlay_fails_closed_instead_of_falling_back(tmp_path: Path) -> None:
    destination = tmp_path / "active" / "mapping.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("plcs: [", encoding="utf-8")

    try:
        deployment_plc.load_active_deployment_config(
            mapping_path=Path("config/mapping.yaml"),
            store_path=tmp_path,
        )
    except deployment_plc.DeploymentConfigUnavailable as exc:
        assert "active mapping" in str(exc)
    else:
        raise AssertionError("invalid active overlay must fail closed")


def test_activation_requires_fresh_server_test_and_does_not_mutate_on_failure(tmp_path: Path) -> None:
    baseline = Path("config/mapping.yaml")
    saved = deployment_plc.save_candidate(
        candidate_payload(
            host="s7-plc-sim",
            connection_timeout_ms=2500,
            last_connection_test={
                "status": "CONNECTED_AND_READABLE",
                "read_only": True,
                "writes_performed": False,
            },
        ),
        mapping_path=baseline,
        store_path=tmp_path,
    )
    before = hashlib.sha256(baseline.read_bytes()).hexdigest()
    fake = ReadOnlyClient(failure=TimeoutError("timed out"))

    result = deployment_plc.activate_candidate(
        saved["candidate_id"],
        mapping_path=baseline,
        store_path=tmp_path,
        client_factory=lambda: fake,
    )

    assert result["status"] == "FRESH_TEST_FAILED"
    assert result["fresh_connection_test"]["status"] == "TIMEOUT"
    assert result["writes_performed"] is False
    assert not (tmp_path / "active" / "mapping.yaml").exists()
    assert hashlib.sha256(baseline.read_bytes()).hexdigest() == before


def test_activation_overlays_only_connectivity_fields_and_rollback_restores_previous_mapping(
    tmp_path: Path,
) -> None:
    baseline = Path("config/mapping.yaml")
    saved = deployment_plc.save_candidate(
        candidate_payload(
            host="s7-plc-sim",
            port=1102,
            rack=0,
            slot=1,
            connection_timeout_ms=2500,
            poll_interval_ms=500,
        ),
        mapping_path=baseline,
        store_path=tmp_path,
    )
    fake = ReadOnlyClient()
    baseline_document = yaml.safe_load(baseline.read_text(encoding="utf-8"))
    baseline_hash = hashlib.sha256(baseline.read_bytes()).hexdigest()

    activated = deployment_plc.activate_candidate(
        saved["candidate_id"],
        mapping_path=baseline,
        store_path=tmp_path,
        client_factory=lambda: fake,
    )

    active_path = tmp_path / "active" / "mapping.yaml"
    active_document = yaml.safe_load(active_path.read_text(encoding="utf-8"))
    expected_document = copy.deepcopy(baseline_document)
    expected_document["plcs"][0].update(
        {
            "connection_timeout_ms": 2500,
        }
    )
    for key in set(baseline_document["plcs"][0]) - {
        "host",
        "port",
        "rack",
        "slot",
        "connection_timeout_ms",
        "poll_interval_ms",
    }:
        assert active_document["plcs"][0][key] == expected_document["plcs"][0][key]
    baseline_without_plc_fields = copy.deepcopy(baseline_document)
    active_without_plc_fields = copy.deepcopy(active_document)
    for document in (baseline_without_plc_fields, active_without_plc_fields):
        for field in (
            "host",
            "port",
            "rack",
            "slot",
            "connection_timeout_ms",
            "poll_interval_ms",
        ):
            document["plcs"][0].pop(field, None)
    assert active_without_plc_fields == baseline_without_plc_fields
    assert activated["active_mapping_hash"] != f"sha256:{baseline_hash}"
    assert activated["changed_fields"] == ["connection_timeout_ms"]
    assert Path(activated["backup_path"]).is_file()
    assert Path(activated["activation_record_path"]).is_file()
    assert hashlib.sha256(baseline.read_bytes()).hexdigest() == baseline_hash

    rolled_back = deployment_plc.rollback_activation(
        activated["activation_id"],
        mapping_path=baseline,
        store_path=tmp_path,
    )

    assert rolled_back["status"] == "ROLLED_BACK"
    assert rolled_back["active_mapping_hash"] == f"sha256:{baseline_hash}"
    assert not active_path.exists()


def test_stale_candidate_is_rejected_before_fresh_test_or_mutation(tmp_path: Path) -> None:
    baseline = Path("config/mapping.yaml")
    saved = deployment_plc.save_candidate(
        candidate_payload(host="s7-plc-sim"),
        mapping_path=baseline,
        store_path=tmp_path,
    )
    _write_active_overlay(tmp_path, baseline, connection_timeout_ms=2500)
    fake = ReadOnlyClient()

    result = deployment_plc.activate_candidate(
        saved["candidate_id"],
        mapping_path=baseline,
        store_path=tmp_path,
        client_factory=lambda: fake,
    )

    assert result["status"] == "STALE_CANDIDATE"
    assert fake.calls == []


def test_active_overlay_and_candidate_artifacts_reject_symlinks(tmp_path: Path) -> None:
    active = tmp_path / "active" / "mapping.yaml"
    active.parent.mkdir(parents=True, exist_ok=True)
    active.symlink_to(Path("config/mapping.yaml").resolve())
    with pytest.raises(deployment_plc.DeploymentConfigUnavailable):
        deployment_plc.load_active_deployment_config(
            mapping_path=Path("config/mapping.yaml"),
            store_path=tmp_path,
        )

    candidate = tmp_path / "candidates" / "candidate-link.json"
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.symlink_to(Path("config/mapping.yaml").resolve())
    with pytest.raises(deployment_plc.DeploymentConfigUnavailable):
        deployment_plc.load_candidate("candidate-link", store_path=tmp_path)
