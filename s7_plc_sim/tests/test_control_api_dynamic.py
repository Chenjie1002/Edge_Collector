from __future__ import annotations

import json
from pathlib import Path
import subprocess
import textwrap
import threading

from fastapi.testclient import TestClient

from app.control_api import CONTROL_HTML
from app.control_api import create_control_app
from app.pipeline import ThreeStationPipeline
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
    assert "setTimeout(pollState" in CONTROL_HTML
    assert "setInterval" not in CONTROL_HTML


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
          "serialHint", "completedHint", "wipLabel", "wip12", "wipHint", "planHint",
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
