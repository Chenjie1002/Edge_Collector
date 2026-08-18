from __future__ import annotations

import json
from pathlib import Path
import subprocess
import textwrap
import threading

from fastapi.testclient import TestClient

from app.control_api import CONTROL_HTML
from app.control_api import create_control_app
from app.pipeline import Part, SingleLinearRoutePipeline, StationJob, ThreeStationPipeline
from app.runtime_config import load_runtime_config


def test_control_page_renders_station_and_nok_capabilities_from_state() -> None:
    assert 'const stations = ["WS01", "WS02", "WS03"]' not in CONTROL_HTML
    assert "state.topology.station_ids" in CONTROL_HTML
    assert "station.nok_codes" in CONTROL_HTML
    assert "station.allow_force" in CONTROL_HTML
    assert "topology.edges" in CONTROL_HTML
    assert "state.wip[key]" in CONTROL_HTML
    assert "renderFlow" in CONTROL_HTML
    assert "buffer.waiting_unit_id" in CONTROL_HTML
    assert "station.current_cycle.progress_percent" in CONTROL_HTML
    assert "Applied base / jitter" in CONTROL_HTML
    assert "Effective speed / 生效倍率" in CONTROL_HTML
    assert "simulationSpeed" in CONTROL_HTML
    assert "simulationSpeedApplied" in CONTROL_HTML
    assert "downstream_buffer_capacity" in CONTROL_HTML
    assert "buffer.capacity" in CONTROL_HTML
    assert "WIP <strong>${buffer.wip || 0} / ${buffer.capacity ?? \"-\"}</strong>" in CONTROL_HTML
    assert "draft-status" in CONTROL_HTML
    assert "setTimeout(pollState" in CONTROL_HTML
    assert "setInterval" not in CONTROL_HTML


def test_control_page_distinguishes_waiting_transfer_from_running() -> None:
    assert "WAITING_TRANSFER" in CONTROL_HTML
    assert "station.status_reason" in CONTROL_HTML
    assert "station.waiting_transfer" in CONTROL_HTML

    script = CONTROL_HTML.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    node_program = textwrap.dedent(
        """
        (() => {
          const vm = require("node:vm");
          const source = __SOURCE__;
          const document = { getElementById: () => null, querySelectorAll: () => [] };
          const context = {
            console,
            document,
            window: { location: { protocol: "http:", hostname: "localhost" } },
            fetch: () => new Promise(() => {}),
            setTimeout: () => 0,
          };
          vm.runInNewContext(source, context);
          const station = {
            status: "WAITING_TRANSFER",
            waiting_transfer: true,
            status_reason: "downstream buffer full / waiting transfer",
            paused: false,
            current_dmc: "SUB-HELD",
            payload_ready: false,
          };
          if (context.statusText(station) !== "WAITING_TRANSFER") throw new Error("waiting transfer status was hidden as running");
          if (context.statusClass(station) !== "hold") throw new Error("waiting transfer status is not a hold state");
          process.stdout.write("CONTROL_WAITING_TRANSFER_OK\\n");
        })();
        """
    ).replace("__SOURCE__", json.dumps(script))
    result = subprocess.run(["node", "-"], input=node_program, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_control_page_back_link_derives_dashboard_from_current_browser_host() -> None:
    assert "返回 Edge MES" in CONTROL_HTML
    assert "window.location.hostname" in CONTROL_HTML
    assert ":3001/" in CONTROL_HTML
    assert "127.0.0.1" not in CONTROL_HTML
    assert "10.0.0.218" not in CONTROL_HTML


def _linear_mapping() -> dict[str, object]:
    station_ids = ["WS01", "WS02", "WS03"]
    return {
        "line_id": "LINE_TEST",
        "entry_station_id": "WS01",
        "terminal_station_id": "WS03",
        "route_graph": [
            {"from_station_id": left, "to_station_id": right}
            for left, right in zip(station_ids, station_ids[1:])
        ],
        "execution_profile": {"mode": "normal", "cycle_scale": 1.0},
        "stations": [
            {
                "station_id": station_id,
                "station_order": index,
                "db_number": 100 + index,
                "cycle_time_s": 1.0,
                "jitter_s": 0.0,
                "nok_rate": 0.0,
                "payload_template": "generic_status_v1",
                "nok_codes": [11001],
            }
            for index, station_id in enumerate(station_ids, start=1)
        ],
    }


def test_buffer_capacity_endpoint_applies_audits_and_rejects_unsafe_lowering() -> None:
    audit = _AuditRecorder()
    pipeline = SingleLinearRoutePipeline.from_mapping(_linear_mapping(), audit_recorder=audit)
    client = TestClient(create_control_app(pipeline, threading.RLock()))

    response = client.post(
        "/vplc/stations/WS01",
        json={"downstream_buffer_capacity": 2, "reason": "operator buffer tuning"},
    )

    assert response.status_code == 200
    assert response.json()["buffers"][0]["capacity"] == 2
    assert client.get("/vplc/state").json()["buffers"][0]["capacity"] == 2
    assert audit.changes[-1]["parameter_name"] == "downstream_buffer_capacity"
    assert audit.changes[-1]["old_value"] == 1
    assert audit.changes[-1]["new_value"] == 2

    pipeline.edge_queues[("WS01", "WS02")].extend(
        [
            Part(serial_no=1, unit_id="U-1", child_dmc="SUB-1"),
            Part(serial_no=2, unit_id="U-2", child_dmc="SUB-2"),
        ]
    )
    lowering = client.post(
        "/vplc/stations/WS01",
        json={"downstream_buffer_capacity": 1, "reason": "unsafe lower buffer"},
    )
    assert lowering.status_code == 400
    assert "current WIP" in lowering.json()["detail"]
    assert len(pipeline.edge_queues[("WS01", "WS02")]) == 2
    assert client.get("/vplc/state").json()["buffers"][0]["capacity"] == 2


def test_buffer_capacity_endpoint_rejects_invalid_integer_bounds() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(_linear_mapping())
    client = TestClient(create_control_app(pipeline, threading.RLock()))

    for invalid in (0, -1, 101, 1.5, "2"):
        response = client.post(
            "/vplc/stations/WS01",
            json={"downstream_buffer_capacity": invalid, "reason": "invalid buffer test"},
        )
        assert response.status_code in (400, 422), invalid
    assert client.get("/vplc/state").json()["buffers"][0]["capacity"] == 1


class _AuditRecorder:
    def __init__(self) -> None:
        self.changes: list[dict[str, object]] = []
        self.snapshots: list[dict[str, object]] = []

    def record_change(self, payload: dict[str, object]) -> None:
        self.changes.append(payload)

    def record_snapshot(self, payload: dict[str, object]) -> None:
        self.snapshots.append(payload)


def test_normal_profile_api_update_returns_and_persists_all_runtime_values() -> None:
    config = load_runtime_config(Path(__file__).resolve().parents[2] / "config" / "vplc.yaml")
    assert config.profile == "normal"
    assert config.allow_runtime_cycle_edit is True
    audit = _AuditRecorder()
    pipeline = ThreeStationPipeline(
        scale=config.cycle_scale,
        profile=config.profile,
        allow_runtime_cycle_edit=config.allow_runtime_cycle_edit,
        station_parameters=config.station_dict(),
        config_source=config.source,
        config_hash=config.config_hash,
        audit_recorder=audit,
    )
    client = TestClient(create_control_app(pipeline, threading.RLock()))

    response = client.post(
        "/vplc/stations/WS01",
        json={
            "base_cycle_s": 42.5,
            "jitter_s": 2.25,
            "nok_rate": 0.125,
            "reason": "normal profile runtime tuning",
        },
        headers={"X-VPLC-Actor": "operator"},
    )

    assert response.status_code == 200
    returned = response.json()["stations"]["WS01"]
    assert returned["base_cycle_s"] == 42.5
    assert returned["jitter_s"] == 2.25
    assert returned["nok_rate"] == 0.125
    persisted = client.get("/vplc/state").json()["stations"]["WS01"]
    assert persisted["base_cycle_s"] == 42.5
    assert persisted["jitter_s"] == 2.25
    assert persisted["nok_rate"] == 0.125
    assert {item["parameter_name"] for item in audit.changes} >= {
        "base_cycle_s",
        "jitter_s",
        "nok_rate",
    }
    assert all(item["reason"] == "normal profile runtime tuning" for item in audit.changes)


def test_runtime_speed_endpoint_updates_future_jobs_and_preserves_inflight_job() -> None:
    audit = _AuditRecorder()
    pipeline = ThreeStationPipeline(
        scale=1.0,
        profile="normal",
        allow_runtime_cycle_edit=True,
        audit_recorder=audit,
        station_parameters={
            "WS01": {"base_cycle_s": 40.0, "jitter_s": 0.0, "nok_rate": 0.0},
            "WS02": {"base_cycle_s": 30.0, "jitter_s": 0.0, "nok_rate": 0.0},
            "WS03": {"base_cycle_s": 30.0, "jitter_s": 0.0, "nok_rate": 0.0},
        },
    )
    station = pipeline.stations["WS01"]
    started_mono = 100.0
    station.current_job = StationJob(
        part=Part(serial_no=1, unit_id="U-INFLIGHT", child_dmc="SUB-INFLIGHT"),
        started_at=pipeline.plan.started_at,
        finish_monotonic=started_mono + 17.5,
        cycle_time_s=17.5,
    )
    client = TestClient(create_control_app(pipeline, threading.RLock()))

    response = client.post(
        "/vplc/simulation/speed",
        json={"speed_multiplier": 10, "reason": "operator demo speed"},
        headers={"X-VPLC-Actor": "operator"},
    )

    assert response.status_code == 200
    assert response.json()["speed_multiplier"] == 10.0
    assert response.json()["scale"] == 0.1
    assert client.get("/vplc/state").json()["speed_multiplier"] == 10.0
    assert station.current_job is not None
    assert station.current_job.finish_monotonic == started_mono + 17.5

    station.current_job = None
    pipeline._start_station(
        station,
        Part(serial_no=2, unit_id="U-FUTURE", child_dmc="SUB-FUTURE"),
        pipeline.plan.started_at,
        200.0,
    )
    assert station.current_job is not None
    assert station.current_job.cycle_time_s == 4.0
    assert audit.changes[-1]["parameter_name"] == "simulation_speed_multiplier"
    assert audit.changes[-1]["old_value"] == 1.0
    assert audit.changes[-1]["new_value"] == 10.0
    assert audit.snapshots[-1]["snapshot_type"] == "runtime_speed_update"


def test_runtime_speed_endpoint_rejects_non_preset_multiplier() -> None:
    client = TestClient(create_control_app(ThreeStationPipeline(), threading.RLock()))

    response = client.post(
        "/vplc/simulation/speed",
        json={"speed_multiplier": 3, "reason": "unsupported demo speed"},
    )

    assert response.status_code == 400
    assert "1, 2, 5, 10, 20" in response.json()["detail"]


def test_control_page_speed_action_and_unsaved_indicator_have_runtime_behavior() -> None:
    script = CONTROL_HTML.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    node_program = textwrap.dedent(
        """
        (async () => {
        const vm = require("node:vm");
        const source = __SOURCE__;
        const elements = new Map([
          ["simulationSpeed", { id: "simulationSpeed", value: "1", dataset: {}, disabled: false }],
          ["simulationSpeedApplied", { id: "simulationSpeedApplied", textContent: "", dataset: {} }],
          ["simulationSpeedDraftStatus", { id: "simulationSpeedDraftStatus", hidden: true, dataset: {} }],
        ]);
        const document = {
          activeElement: null,
          getElementById(id) { return elements.get(id) || null; },
          querySelectorAll() { return []; },
        };
        let request;
        const context = {
          console,
          document,
          prompt: () => "speed test",
          fetch: async (path, options) => {
            request = { path, options };
            return { ok: true, json: async () => ({ speed_multiplier: 10, scale: 0.1 }) };
          },
          setTimeout: () => 0,
        };
        vm.runInNewContext(source, context);
        const speed = elements.get("simulationSpeed");
        speed.value = "10";
        context.markSpeedDirty(speed);
        if (elements.get("simulationSpeedDraftStatus").hidden) throw new Error("speed draft is not marked before apply");
        await context.applySimulationSpeed();
        if (!request || request.path !== "/vplc/simulation/speed") throw new Error("speed endpoint was not called");
        const payload = JSON.parse(request.options.body);
        if (payload.speed_multiplier !== 10 || payload.reason !== "speed test") throw new Error("speed payload is incomplete");
        if (elements.get("simulationSpeedApplied").textContent !== "10×") throw new Error("speed readback was not rendered");
        process.stdout.write("CONTROL_SPEED_RUNTIME_OK\\n");
        })().catch((error) => {
          console.error(error && (error.stack || error.message) || error);
          process.exitCode = 1;
        });
        """
    ).replace("__SOURCE__", json.dumps(script))
    result = subprocess.run(["node", "-"], input=node_program, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_control_page_runtime_preserves_focused_and_dirty_inputs_and_sends_three_values() -> None:
    script = CONTROL_HTML.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    node_program = textwrap.dedent(
        """
        (async () => {
        const vm = require("node:vm");
        const source = __SOURCE__;

        class FakeElement {
          constructor(id) {
            this.id = id;
            this._innerHTML = "";
            this.textContent = "";
            this.value = "";
            this.dataset = {};
            this.disabled = false;
            this.inputs = [];
          }

          set innerHTML(value) {
            this._innerHTML = String(value);
            if (this.id !== "stationRows") return;
            this.inputs = [];
            for (const tag of this._innerHTML.match(/<input\\b[^>]*>/g) || []) {
              const attr = (name) => {
                const match = tag.match(new RegExp(name + '="([^"]*)"'));
                return match ? match[1] : "";
              };
              const id = attr("id");
              if (!id) continue;
              const suffix = id.match(/-(base|jitter|nok)$/)?.[1] || "";
              const field = attr("data-field") || ({base: "base_cycle_s", jitter: "jitter_s", nok: "nok_rate"}[suffix] || "");
              const station = attr("data-station") || id.slice(0, -(suffix.length + 1));
              if (!field || !station) continue;
              const input = new FakeElement(id);
              input.value = attr("value");
              input.dataset.station = station;
              input.dataset.field = field;
              input.dataset.dirty = attr("data-dirty") || "false";
              input.disabled = /\\sdisabled(?:\\s|>)/.test(tag);
              this.inputs.push(input);
            }
          }

          get innerHTML() {
            return this._innerHTML;
          }

          focus() {
            document.activeElement = this;
          }
        }

        const staticIds = [
        "lineState", "lineHint", "scale", "profileHint", "serial", "completed",
        "terminalOk", "terminalNok", "serialHint", "completedHint", "wipLabel", "wip12", "wipHint", "planHint",
          "lineFlow", "rawJson", "updatedAt", "stationRows",
        ];
        const elements = new Map(staticIds.map((id) => [id, new FakeElement(id)]));
        const document = {
          activeElement: null,
          getElementById(id) {
            if (elements.has(id)) return elements.get(id);
            return elements.get("stationRows").inputs.find((input) => input.id === id) || null;
          },
          querySelectorAll(selector) {
            if (selector === "input[data-station][data-field]") return elements.get("stationRows").inputs;
            return [];
          },
        };

        const station = (id, base, jitter, nok) => ({
          station_id: id,
          base_cycle_s: base,
          jitter_s: jitter,
          nok_rate: nok,
          paused: false,
          cycle_counter: 0,
          current_dmc: "",
          current_cycle: null,
          last_dmc: "",
          last_result: 0,
          last_nok_codes: [],
          last_end_time: null,
          payload_ready: false,
          pending_forced_nok_count: 0,
          pending_forced_nok_codes: [],
          allow_force: true,
          nok_codes: [10001],
        });
        const makeState = (base, jitter, nok) => ({
          scale: 1,
          profile: "normal",
          allow_runtime_cycle_edit: true,
          serial_no: 0,
          completed_quantity: 0,
          topology: {
            station_ids: ["WS01", "WS02", "WS03"],
            edges: [
              {from_station_id: "WS01", to_station_id: "WS02"},
              {from_station_id: "WS02", to_station_id: "WS03"},
            ],
            entry_station_id: "WS01",
            terminal_station_id: "WS03",
          },
          wip: {ws01_to_ws02: 0, ws02_to_ws03: 0},
          buffers: [],
          line: {
            running: true,
            plan_mode: "continuous",
            elapsed_seconds: 1,
            stop_reason: "",
            remaining_seconds: null,
            target_quantity: null,
            target_shifts: null,
          },
          stations: {
            WS01: station("WS01", base, jitter, nok),
            WS02: station("WS02", 29.8, 1.0, 0.015),
            WS03: station("WS03", 29.2, 0.9, 0.01),
          },
        });

        const state1 = makeState(30.4, 1.2, 0.02);
        const state2 = makeState(30.4, 1.2, 0.02);
        let capturedPayload = null;
        const context = {
          console,
          document,
          fetch: () => new Promise(() => {}),
          setTimeout: () => 0,
          prompt: () => "operator edit",
          confirm: () => true,
        };
        vm.runInNewContext(source, context);
        context.render(state1);
        const baseInput = document.getElementById("WS01-base");
        const jitterInput = document.getElementById("WS01-jitter");
        const nokInput = document.getElementById("WS01-nok");
        if (!baseInput || !jitterInput || !nokInput) throw new Error("runtime station inputs missing");
        if (baseInput.disabled || jitterInput.disabled || nokInput.disabled) throw new Error("normal inputs are disabled");

        baseInput.value = "42.5";
        baseInput.focus();
        context.fetch = async (path, options = {}) => {
          if (path === "/vplc/state") return {ok: true, json: async () => state2};
          if (options.method === "POST") {
            capturedPayload = JSON.parse(options.body);
            return {ok: true, json: async () => state2};
          }
          throw new Error("unexpected request " + path);
        };
        await context.loadState();
        const focusedAfterPoll = document.getElementById("WS01-base");
        if (focusedAfterPoll.value !== "42.5") throw new Error("focused value overwritten by polling");
        if (document.activeElement !== focusedAfterPoll) throw new Error("focused input lost focus during polling");

        if (typeof context.markInputDirty !== "function") throw new Error("dirty-input runtime contract missing");
        context.markInputDirty(focusedAfterPoll);
        const dirtyInput = document.getElementById("WS01-nok");
        dirtyInput.value = "0.333";
        context.markInputDirty(dirtyInput);
        document.activeElement = null;
        await context.loadState();
        const dirtyAfterPoll = document.getElementById("WS01-nok");
        if (dirtyAfterPoll.value !== "0.333") throw new Error("dirty value overwritten by polling");

        await context.saveStation("WS01");
        if (!capturedPayload) throw new Error("save payload was not sent");
        for (const key of ["base_cycle_s", "jitter_s", "nok_rate", "reason"]) {
          if (!(key in capturedPayload)) throw new Error("save payload missing " + key);
        }
        if (capturedPayload.base_cycle_s !== 42.5 || capturedPayload.jitter_s !== 1.2 || capturedPayload.nok_rate !== 0.333) {
          throw new Error("save payload values do not match protected inputs");
        }
        if (document.getElementById("WS01-nok").value !== "0.020") {
          throw new Error("returned state was hidden by stale draft");
        }
        process.stdout.write("CONTROL_HTML_RUNTIME_OK\\n");
        })().catch((error) => {
          console.error(error && (error.stack || error.message) || error);
          process.exitCode = 1;
        });
        """
    ).replace("__SOURCE__", json.dumps(script))
    result = subprocess.run(
        ["node", "-"],
        input=node_program,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_control_page_polling_keeps_editable_nodes_selection_and_mode_semantics() -> None:
    script = CONTROL_HTML.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    node_program = textwrap.dedent(
        """
        (async () => {
        const vm = require("node:vm");
        const source = __SOURCE__;

        const setDataAttribute = (element, name, value) => {
          if (!name.startsWith("data-")) return;
          const key = name.slice(5).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
          element.dataset[key] = value;
        };

        class FakeElement {
          constructor(tagName = "div", id = "") {
            this.tagName = tagName.toUpperCase();
            this.id = id;
            this._innerHTML = "";
            this.textContent = "";
            this.value = "";
            this.dataset = {};
            this.style = {};
            this.hidden = false;
            this.disabled = false;
            this.children = [];
            this.parentElement = null;
            this.selectionStart = 0;
            this.selectionEnd = 0;
            this.selectedIndex = 0;
            this.options = [];
          }

          _attributes(raw) {
            const attributes = {};
            for (const match of raw.matchAll(/([a-zA-Z_:][-a-zA-Z0-9_:]*)="([^"]*)"/g)) {
              attributes[match[1]] = match[2];
            }
            return attributes;
          }

          _applyAttributes(raw) {
            const attributes = this._attributes(raw);
            for (const [name, value] of Object.entries(attributes)) {
              if (name === "id") this.id = value;
              if (name === "value") this.value = value;
              if (name === "disabled") this.disabled = true;
              setDataAttribute(this, name, value);
            }
            if (/\\sdisabled(?:\\s|>)/.test(raw)) this.disabled = true;
          }

          _parseControls(html) {
            for (const match of html.matchAll(/<input\\b([^>]*)>/g)) {
              const input = new FakeElement("input");
              input._applyAttributes(match[1]);
              input.selectionStart = input.value.length;
              input.selectionEnd = input.value.length;
              this.appendChild(input);
            }
            for (const match of html.matchAll(/<select\\b([^>]*)>([\\s\\S]*?)<\\/select>/g)) {
              const select = new FakeElement("select");
              select._applyAttributes(match[1]);
              select._setOptions(match[2]);
              this.appendChild(select);
            }
            const livePattern = /<(?:span|strong|div)\\b([^>]*(?:id="[^"]+"|data-live="[^"]+")[^>]*)>([\\s\\S]*?)<\\/(?:span|strong|div)>/g;
            for (const match of html.matchAll(livePattern)) {
              const live = new FakeElement("span");
              live._applyAttributes(match[1]);
              live.textContent = match[2].replace(/<[^>]+>/g, "").trim();
              this.appendChild(live);
            }
          }

          _setOptions(html) {
            this._innerHTML = String(html);
            this.options = [];
            for (const match of html.matchAll(/<option\\b([^>]*)>([\\s\\S]*?)<\\/option>/g)) {
              const attributes = this._attributes(match[1]);
              this.options.push({ value: attributes.value || "", text: match[2] });
            }
            if (!this.value || !this.options.some((option) => option.value === this.value)) {
              this.value = this.options[0]?.value || "";
            }
            this.selectedIndex = Math.max(0, this.options.findIndex((option) => option.value === this.value));
          }

          set innerHTML(value) {
            this._innerHTML = String(value);
            if (this.tagName === "SELECT") {
              this._setOptions(this._innerHTML);
              return;
            }
            this.children = [];
            if (this.id !== "stationRows") return;
            const rowPattern = /<tr\\b[^>]*data-station-row="([^"]+)"[^>]*>([\\s\\S]*?)<\\/tr>/g;
            for (const match of this._innerHTML.matchAll(rowPattern)) {
              const row = new FakeElement("tr");
              row.dataset.stationRow = match[1];
              row._parseControls(match[2]);
              this.appendChild(row);
            }
            if (!this.children.length) this._parseControls(this._innerHTML);
          }

          get innerHTML() {
            return this._innerHTML;
          }

          appendChild(child) {
            child.parentElement = this;
            this.children.push(child);
            return child;
          }

          remove() {
            if (!this.parentElement) return;
            this.parentElement.children = this.parentElement.children.filter((child) => child !== this);
            this.parentElement = null;
          }

          matches(selector) {
            if (selector === "input[data-station][data-field]") {
              return this.tagName === "INPUT" && this.dataset.station && this.dataset.field;
            }
            if (selector === "select[data-station][data-field]") {
              return this.tagName === "SELECT" && this.dataset.station && this.dataset.field;
            }
            if (selector === "tr[data-station-row]") {
              return this.tagName === "TR" && this.dataset.stationRow;
            }
            if (selector === "[data-station-row]") return Boolean(this.dataset.stationRow);
            if (selector.startsWith('[data-live="')) {
              const value = selector.match(/data-live="([^"]+)"/)?.[1];
              return this.dataset.live === value;
            }
            return false;
          }

          querySelectorAll(selector) {
            const matches = [];
            for (const child of this.children) {
              if (child.matches(selector)) matches.push(child);
              matches.push(...child.querySelectorAll(selector));
            }
            return matches;
          }

          querySelector(selector) {
            return this.querySelectorAll(selector)[0] || null;
          }

          focus() {
            document.activeElement = this;
          }

          setSelectionRange(start, end) {
            this.selectionStart = start;
            this.selectionEnd = end;
          }

          addEventListener() {}
        }

        const staticIds = [
        "lineState", "lineHint", "scale", "profileHint", "serial", "completed",
        "terminalOk", "terminalNok", "serialHint", "completedHint", "wipLabel", "wip12", "wipHint", "planHint",
          "planMode", "continuousPlanHint", "durationPlanField", "quantityPlanField",
          "shiftsPlanField", "durationHours", "quantityTarget", "shiftCount", "shiftHours",
          "startPlanButton", "planRunningState", "lineFlow", "rawJson", "updatedAt", "stationRows",
        ];
        const elements = new Map(staticIds.map((id) => [id, new FakeElement(id === "planMode" ? "select" : "div", id)]));
        elements.get("planMode").value = "continuous";
        for (const [id, value] of [["durationHours", "1"], ["quantityTarget", "100"], ["shiftCount", "1"], ["shiftHours", "8.5"]]) {
          const input = new FakeElement("input", id);
          input.value = value;
          input.selectionStart = value.length;
          input.selectionEnd = value.length;
          elements.set(id, input);
        }

        const findById = (element, id) => {
          if (element.id === id) return element;
          for (const child of element.children) {
            const match = findById(child, id);
            if (match) return match;
          }
          return null;
        };
        const document = {
          activeElement: null,
          getElementById(id) {
            return findById(elements.get("stationRows"), id) || elements.get(id) || null;
          },
          querySelectorAll(selector) {
            const stationRows = elements.get("stationRows");
            if (selector === "input[data-station][data-field]" || selector === "select[data-station][data-field]") {
              return stationRows.querySelectorAll(selector);
            }
            return [];
          },
        };

        const station = (id, base, jitter, nok, progress, status = "RUNNING") => ({
          station_id: id,
          base_cycle_s: base,
          jitter_s: jitter,
          nok_rate: nok,
          paused: status === "PAUSED",
          cycle_counter: progress,
          current_dmc: status === "IDLE" ? "" : `DMC-${progress}`,
          current_cycle: status === "IDLE" ? null : {
            unit_id: `U-${progress}`,
            dmc: `DMC-${progress}`,
            progress_percent: progress,
            elapsed_seconds: progress,
            planned_cycle_seconds: 100,
            remaining_seconds: 100 - progress,
          },
          last_dmc: `LAST-${progress}`,
          last_result: 1,
          last_nok_codes: [],
          last_end_time: null,
          payload_ready: false,
          pending_forced_nok_count: 0,
          pending_forced_nok_codes: [],
          allow_force: true,
          nok_codes: [10001, 10002],
        });
        const makeState = (progress, wip, planMode = "continuous") => ({
          scale: 1,
          profile: "normal",
          allow_runtime_cycle_edit: true,
          serial_no: progress,
          completed_quantity: progress - 1,
          topology: {
            station_ids: ["WS01", "WS02", "WS03"],
            edges: [
              {from_station_id: "WS01", to_station_id: "WS02"},
              {from_station_id: "WS02", to_station_id: "WS03"},
            ],
            entry_station_id: "WS01",
            terminal_station_id: "WS03",
          },
          wip: {ws01_to_ws02: wip, ws02_to_ws03: 0},
          buffers: [{
            from_station_id: "WS01",
            to_station_id: "WS02",
                wip,
                status: wip ? "WAITING" : "EMPTY",
                capacity: 1,
                waiting_unit_id: wip ? "U-WAITING" : null,
            waiting_dmc: wip ? "DMC-WAITING" : null,
          }],
          line: {
            running: true,
            external_running: true,
            plan_active: true,
            plan_mode: planMode,
            elapsed_seconds: progress,
            stop_reason: "",
            remaining_seconds: planMode === "duration" ? 7200 : null,
            target_quantity: planMode === "quantity" ? 100 : null,
            target_shifts: planMode === "shifts" ? 2 : null,
            shift_hours: planMode === "shifts" ? 8.5 : null,
          },
          stations: {
            WS01: station("WS01", 30.4, 1.2, 0.02, progress, progress === 10 ? "IDLE" : "RUNNING"),
            WS02: station("WS02", 29.8, 1.0, 0.015, 0, "IDLE"),
            WS03: station("WS03", 29.2, 0.9, 0.01, 0, "IDLE"),
          },
        });

        const states = [makeState(10, 0), makeState(20, 1), makeState(30, 2)];
        let stateIndex = 0;
        let capturedPayload = null;
        const context = {
          console,
          document,
          fetch: async (path, options = {}) => {
            if (path === "/vplc/state") return {ok: true, json: async () => states[Math.min(stateIndex++, states.length - 1)]};
            if (options.method === "POST") {
              capturedPayload = JSON.parse(options.body);
              return {ok: true, json: async () => states[states.length - 1]};
            }
            throw new Error("unexpected request " + path);
          },
          setTimeout: () => 0,
          prompt: () => "operator edit",
          confirm: () => true,
        };
        vm.runInNewContext(source, context);
        context.render(states[0]);

        const baseInput = document.getElementById("WS01-base");
        const jitterInput = document.getElementById("WS01-jitter");
        const nokInput = document.getElementById("WS01-nok");
        const codeSelect = document.getElementById("WS01-nok-code");
        const countInput = document.getElementById("WS01-nok-count");
        const planMode = document.getElementById("planMode");
        const durationInput = document.getElementById("durationHours");
        if (!baseInput || !jitterInput || !nokInput || !codeSelect || !countInput || !planMode || !durationInput) {
          throw new Error("editable controls missing: " + JSON.stringify({base: !!baseInput, jitter: !!jitterInput, nok: !!nokInput, code: !!codeSelect, count: !!countInput, mode: !!planMode, duration: !!durationInput}));
        }

        baseInput.value = "42.5";
        baseInput.focus();
        baseInput.setSelectionRange(1, 3);
        context.markInputDirty(baseInput);
        jitterInput.value = "2.75";
        jitterInput.setSelectionRange(0, 2);
        context.markInputDirty(jitterInput);
        nokInput.value = "0.333";
        nokInput.setSelectionRange(2, 5);
        context.markInputDirty(nokInput);
        codeSelect.value = "10002";
        context.markInputDirty(codeSelect);
        countInput.value = "3";
        countInput.focus();
        countInput.setSelectionRange(0, 1);
        context.markInputDirty(countInput);
        const draftStatus = document.getElementById("WS01-draft-status");
        if (!draftStatus || draftStatus.hidden || draftStatus.textContent !== "Unsaved / 未保存") throw new Error("station draft status is not visible");

                planMode.value = "duration";
            planMode.dataset.dirty = "true";
            durationInput.value = "2.5";
            durationInput.focus();
            durationInput.setSelectionRange(0, 3);
            durationInput.dataset.dirty = "true";

        const identities = {baseInput, jitterInput, nokInput, codeSelect, countInput, planMode, durationInput};
        const selections = {
          baseInput: [baseInput.selectionStart, baseInput.selectionEnd],
          jitterInput: [jitterInput.selectionStart, jitterInput.selectionEnd],
          nokInput: [nokInput.selectionStart, nokInput.selectionEnd],
          countInput: [countInput.selectionStart, countInput.selectionEnd],
          durationInput: [durationInput.selectionStart, durationInput.selectionEnd],
        };
        for (let poll = 0; poll < 3; poll += 1) {
          await context.loadState();
          for (const [name, element] of Object.entries(identities)) {
            if (document.getElementById(element.id) !== element) throw new Error(name + " DOM node replaced during polling");
          }
          if (baseInput.value !== "42.5" || jitterInput.value !== "2.75" || nokInput.value !== "0.333") {
            throw new Error("station draft overwritten during polling");
          }
          if (codeSelect.value !== "10002" || countInput.value !== "3") throw new Error("force NOK draft overwritten during polling");
          if (planMode.value !== "duration" || durationInput.value !== "2.5") throw new Error("production plan draft overwritten during polling");
          for (const [name, [start, end]] of Object.entries(selections)) {
            const element = identities[name];
            if (element.selectionStart !== start || element.selectionEnd !== end) throw new Error(name + " caret/selection moved during polling");
          }
        }
            if (document.getElementById("WS01-status").textContent !== "RUNNING") throw new Error("live station status did not update");
            if (!document.getElementById("lineFlow").innerHTML.includes("30%")) throw new Error("live cycle progress did not update");
            if (!document.getElementById("lineFlow").innerHTML.includes("WIP <strong>2 / 1</strong>")) throw new Error("live buffer state did not update");
            if (!document.getElementById("lineFlow").innerHTML.includes("1×")) throw new Error("effective speed is missing from line flow");

        if (typeof context.clearPlanDrafts !== "function") throw new Error("plan draft reset contract missing");
        context.clearPlanDrafts();
        const continuousState = makeState(31, 2, "continuous");
        context.render(continuousState);
        if (!document.getElementById("durationPlanField").hidden || !document.getElementById("quantityPlanField").hidden || !document.getElementById("shiftsPlanField").hidden) {
          throw new Error("continuous mode exposes irrelevant plan fields");
        }
        if (document.getElementById("continuousPlanHint").hidden) throw new Error("continuous mode copy is hidden");
        if (document.getElementById("startPlanButton").textContent !== "开始连续生产") throw new Error("continuous start copy missing");
        if (document.getElementById("planRunningState").textContent !== "CONTINUOUS / Running until manual stop") throw new Error("continuous running state copy missing");
        planMode.value = "continuous";
        context.renderPlanMode("continuous");
        await context.startPlan();
        if (!capturedPayload || JSON.stringify(capturedPayload) !== JSON.stringify({mode: "continuous"})) {
          throw new Error("continuous start sent irrelevant duration/quantity/shift fields");
        }

        context.renderPlanMode("duration");
        if (document.getElementById("durationPlanField").hidden || !document.getElementById("quantityPlanField").hidden || !document.getElementById("shiftsPlanField").hidden) throw new Error("duration mode fields are not isolated");
        if (!context.planText({plan_active: true, plan_mode: "duration", remaining_seconds: 7200, target_quantity: null, target_shifts: null, shift_hours: null}, [{label: "WS01 -> WS02", value: 0}]).includes("2.0 h")) throw new Error("duration plan does not show positive hours");
        if (!context.planText({plan_active: true, plan_mode: "quantity", remaining_seconds: null, target_quantity: 100, target_shifts: null, shift_hours: null}, []).includes("100 pcs")) throw new Error("quantity plan does not show pcs");
        if (!context.planText({plan_active: true, plan_mode: "shifts", remaining_seconds: 61200, target_quantity: null, target_shifts: 2, shift_hours: 8.5}, []).includes("2 shifts")) throw new Error("shift plan does not show shift count");
        process.stdout.write("CONTROL_HTML_STABLE_CONTROLS_OK\\n");
        })().catch((error) => {
          console.error(error && (error.stack || error.message) || error);
          process.exitCode = 1;
        });
        """
    ).replace("__SOURCE__", json.dumps(script))
    result = subprocess.run(
        ["node", "-"],
        input=node_program,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    assert "Production Plan / 生产计划" in CONTROL_HTML
    assert "Simulation / 模拟设置" in CONTROL_HTML
    assert "Station Controls / 工站控制" in CONTROL_HTML
    assert "1× = nominal cycle" in CONTROL_HTML
    assert "future jobs" in CONTROL_HTML
    assert "0.02 = 2%" in CONTROL_HTML
    assert "持续运行，直到手动点击“停止”" in CONTROL_HTML
    assert "开始连续生产" in CONTROL_HTML
    assert "CONTINUOUS / Running until manual stop" in CONTROL_HTML
