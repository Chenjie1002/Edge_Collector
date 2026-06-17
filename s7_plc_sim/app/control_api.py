from __future__ import annotations

import threading

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.pipeline import ThreeStationPipeline


class StationUpdateRequest(BaseModel):
    base_cycle_s: float | None = Field(default=None, ge=1, le=300)
    jitter_s: float | None = Field(default=None, ge=0, le=60)
    nok_rate: float | None = Field(default=None, ge=0, le=1)
    paused: bool | None = None


class ForceNokRequest(BaseModel):
    nok_code: int


class ProductionPlanRequest(BaseModel):
    mode: str = Field(default="continuous", pattern="^(continuous|duration|quantity|shifts)$")
    duration_hours: float | None = Field(default=None, gt=0, le=168)
    quantity: int | None = Field(default=None, gt=0, le=1000000)
    shift_count: int | None = Field(default=None, gt=0, le=30)
    shift_hours: float | None = Field(default=8.5, gt=0, le=24)


def create_control_app(pipeline: ThreeStationPipeline, lock: threading.RLock) -> FastAPI:
    app = FastAPI(title="V-PLC Control")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/vplc", response_class=HTMLResponse)
    def page() -> str:
        return CONTROL_HTML

    @app.get("/vplc/state")
    def state() -> dict:
        with lock:
            return pipeline.snapshot()

    @app.post("/vplc/stations/{station_id}")
    def update_station(station_id: str, request: StationUpdateRequest) -> dict:
        with lock:
            try:
                return pipeline.update_station(station_id, request.model_dump(exclude_none=True))
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/vplc/stations/{station_id}/force-nok")
    def force_nok(station_id: str, request: ForceNokRequest) -> dict:
        with lock:
            try:
                return pipeline.force_nok(station_id, request.nok_code)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/vplc/reset")
    def reset() -> dict:
        with lock:
            return pipeline.reset()

    @app.post("/vplc/production/start")
    def start_plan(request: ProductionPlanRequest) -> dict:
        with lock:
            try:
                return pipeline.start_plan(request.model_dump(exclude_none=True))
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/vplc/production/stop")
    def stop_plan() -> dict:
        with lock:
            return pipeline.stop_plan("manual_stop")

    return app


CONTROL_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>V-PLC 控制台</title>
  <style>
    :root {
      --bg: #f4f6f8;
      --surface: #ffffff;
      --surface-2: #eef2f6;
      --line: #d7dde5;
      --text: #17202c;
      --muted: #697386;
      --blue: #1959c8;
      --green: #16815a;
      --red: #bd2b26;
      --amber: #ad6a00;
      --purple: #6c43c9;
      font-family: Inter, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--text); font-size: 14px; }
    header {
      height: 64px; padding: 0 22px; display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid var(--line); background: var(--surface);
    }
    h1 { margin: 0; font-size: 19px; font-weight: 750; letter-spacing: 0; }
    main { width: min(1320px, calc(100vw - 28px)); margin: 18px auto 28px; display: grid; gap: 14px; }
    .topline { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
    .tile, .panel { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }
    .tile { padding: 14px 16px; min-height: 90px; }
    .label { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
    .value { font-size: 27px; line-height: 1.05; font-weight: 760; }
    .hint { margin-top: 8px; color: var(--muted); font-size: 12px; }
    .panel { padding: 16px; }
    .panel-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
    h2 { margin: 0; font-size: 16px; font-weight: 730; }
    table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    th, td { border-bottom: 1px solid var(--line); padding: 10px 8px; text-align: left; vertical-align: middle; }
    th { color: var(--muted); font-size: 12px; font-weight: 650; background: #fbfcfd; }
    td { font-size: 13px; }
    input, select {
      width: 100%; height: 34px; border: 1px solid var(--line); border-radius: 6px;
      padding: 0 8px; font: inherit; background: #fff;
    }
    button {
      height: 34px; border: 1px solid var(--line); border-radius: 6px; background: #fff;
      padding: 0 10px; font: inherit; cursor: pointer; white-space: nowrap;
    }
    button:hover { border-color: #9ca7b7; background: #f8fafc; }
    button.primary { background: var(--blue); color: #fff; border-color: var(--blue); }
    button.danger { color: var(--red); border-color: #f1bab6; }
    .actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .status { display: inline-flex; align-items: center; min-width: 76px; justify-content: center; height: 26px; border-radius: 999px; font-size: 12px; font-weight: 750; }
    .ok { background: #e9f8f1; color: var(--green); }
    .run { background: #eaf1ff; color: var(--blue); }
    .hold { background: #fff5df; color: var(--amber); }
    .bad { background: #fff0ef; color: var(--red); }
    .json { margin: 0; padding: 12px; min-height: 220px; max-height: 360px; overflow: auto; border-radius: 8px; background: #111827; color: #e5e7eb; font-size: 12px; line-height: 1.5; }
    .grid { display: grid; grid-template-columns: 1.4fr 0.9fr; gap: 14px; }
    .compact { width: 90px; }
    .code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .form-grid { display: grid; grid-template-columns: 180px repeat(4, minmax(100px, 1fr)) auto auto; gap: 10px; align-items: end; }
    .field-label { display: grid; gap: 6px; color: var(--muted); font-size: 12px; }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; background: var(--green); box-shadow: 0 0 0 4px #e9f8f1; }
    .dot.off { background: var(--red); box-shadow: 0 0 0 4px #fff0ef; }
    @media (max-width: 960px) { .topline, .grid, .form-grid { grid-template-columns: 1fr; } table { min-width: 980px; } .table-wrap { overflow-x: auto; } }
  </style>
</head>
<body>
  <header>
    <h1>V-PLC 控制台</h1>
    <div class="actions">
      <button onclick="loadState()">刷新</button>
      <button class="danger" onclick="resetPipeline()">重置 WIP / Counter</button>
    </div>
  </header>
  <main>
    <section class="topline">
      <div class="tile"><div class="label">整线状态</div><div class="value" id="lineState">-</div><div class="hint" id="lineHint">-</div></div>
      <div class="tile"><div class="label">模拟倍率</div><div class="value" id="scale">-</div><div class="hint">1.0 表示真实 30s 左右节拍</div></div>
      <div class="tile"><div class="label">总序号</div><div class="value" id="serial">-</div><div class="hint">WS01 投入件累计</div></div>
      <div class="tile"><div class="label">完成件数</div><div class="value" id="completed">-</div><div class="hint">WS03 OK 下线累计</div></div>
      <div class="tile"><div class="label">WIP WS01 -> WS02</div><div class="value" id="wip12">-</div><div class="hint">等待 EOL 的中间件</div></div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>生产计划</h2>
        <span class="hint" id="planHint">-</span>
      </div>
      <div class="form-grid">
        <label class="field-label">模式
          <select id="planMode">
            <option value="continuous">连续生产</option>
            <option value="duration">按小时</option>
            <option value="quantity">按件数</option>
            <option value="shifts">按班次</option>
          </select>
        </label>
        <label class="field-label">小时
          <input id="durationHours" type="number" min="0.1" step="0.1" value="1">
        </label>
        <label class="field-label">件数
          <input id="quantityTarget" type="number" min="1" step="1" value="100">
        </label>
        <label class="field-label">班次数
          <input id="shiftCount" type="number" min="1" step="1" value="1">
        </label>
        <label class="field-label">每班小时
          <input id="shiftHours" type="number" min="0.1" step="0.1" value="8.5">
        </label>
        <button class="primary" onclick="startPlan()">开始</button>
        <button class="danger" onclick="stopPlan()">停止</button>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>工站参数</h2>
        <span class="hint">修改后立即生效，正在加工的当前件会保持其已抽样的节拍。</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="width:76px;">工站</th>
              <th style="width:92px;">状态</th>
              <th style="width:90px;">Counter</th>
              <th>当前 DMC</th>
              <th>最近 DMC</th>
              <th style="width:110px;">基准节拍(s)</th>
              <th style="width:100px;">波动(s)</th>
              <th style="width:96px;">NOK率</th>
              <th style="width:120px;">强制NOK</th>
              <th style="width:180px;">操作</th>
            </tr>
          </thead>
          <tbody id="stationRows"></tbody>
        </table>
      </div>
    </section>
    <section class="grid">
      <div class="panel">
        <div class="panel-head"><h2>最近状态 JSON</h2><span class="hint" id="updatedAt">-</span></div>
        <pre class="json" id="rawJson">{}</pre>
      </div>
      <div class="panel">
        <div class="panel-head"><h2>说明</h2></div>
        <p class="hint">暂停工站会阻止该工站启动下一件，当前正在加工的件仍会完成。</p>
        <p class="hint">强制 NOK 只作用于该工站下一次完成的 cycle，触发后自动清除。</p>
        <p class="hint">Collector 会读取 payload_ready，并写回 read_done；本页用于模拟 PLC 侧参数，不直接写数据库。</p>
      </div>
    </section>
  </main>
  <script>
    const stations = ["WS01", "WS02", "WS03"];
    let currentState = null;

    function resultText(code) {
      if (code === 1) return "OK";
      if (code === 2) return "NOK";
      return "-";
    }

    function statusClass(station) {
      if (station.paused) return "bad";
      if (station.current_dmc) return "run";
      if (station.payload_ready) return "hold";
      return "ok";
    }

    function statusText(station) {
      if (station.paused) return "PAUSED";
      if (station.current_dmc) return "RUNNING";
      if (station.payload_ready) return "READY";
      return "IDLE";
    }

    function nokOptions(stationId) {
      const ranges = {
        WS01: [[10001, "TQ_LOW"], [10002, "TQ_HIGH"], [10003, "ANG_LOW"], [10004, "ANG_HIGH"]],
        WS02: [[20001, "CUR_HIGH"], [20002, "VOLT_LOW"], [20003, "VOLT_HIGH"], [20004, "STALL_CUR"], [20005, "STALL_TIME"]],
        WS03: [[30001, "PRINT_FAIL"], [30002, "VERIFY_FAIL"], [30003, "UPSTREAM_NOK"]],
      };
      return ranges[stationId].map(([code, name]) => `<option value="${code}">${code} ${name}</option>`).join("");
    }

    async function api(path, options = {}) {
      const res = await fetch(path, options);
      if (!res.ok) throw new Error(await res.text());
      return res.json();
    }

    async function loadState() {
      currentState = await api("/vplc/state");
      render(currentState);
    }

    function render(state) {
      const line = state.line;
      document.getElementById("lineState").innerHTML = `<span class="dot ${line.running ? "" : "off"}"></span>${line.running ? "RUN" : "STOP"}`;
      document.getElementById("lineHint").textContent = line.running ? `${line.plan_mode} / 已运行 ${line.elapsed_seconds}s` : (line.stop_reason || "停止");
      document.getElementById("scale").textContent = state.scale.toFixed(2);
      document.getElementById("serial").textContent = state.serial_no;
      document.getElementById("completed").textContent = state.completed_quantity;
      document.getElementById("wip12").textContent = state.wip.ws01_to_ws02;
      document.getElementById("planHint").textContent = planText(line, state.wip.ws02_to_ws03);
      document.getElementById("rawJson").textContent = JSON.stringify(state, null, 2);
      document.getElementById("updatedAt").textContent = new Date().toLocaleTimeString();
      document.getElementById("stationRows").innerHTML = stations.map(id => {
        const station = state.stations[id];
        return `
          <tr>
            <td class="code">${id}</td>
            <td><span class="status ${statusClass(station)}">${statusText(station)}</span></td>
            <td>${station.cycle_counter}</td>
            <td class="code">${station.current_dmc || "-"}</td>
            <td class="code">${station.last_dmc || "-"} ${resultText(station.last_result)}</td>
            <td><input id="${id}-base" type="number" min="1" step="0.1" value="${station.base_cycle_s.toFixed(1)}"></td>
            <td><input id="${id}-jitter" type="number" min="0" step="0.1" value="${station.jitter_s.toFixed(1)}"></td>
            <td><input id="${id}-nok" type="number" min="0" max="1" step="0.001" value="${station.nok_rate.toFixed(3)}"></td>
            <td><select id="${id}-nok-code">${nokOptions(id)}</select></td>
            <td>
              <div class="actions">
                <button class="primary" onclick="saveStation('${id}')">保存</button>
                <button onclick="togglePause('${id}', ${!station.paused})">${station.paused ? "恢复" : "暂停"}</button>
                <button class="danger" onclick="forceNok('${id}')">NOK</button>
              </div>
            </td>
          </tr>`;
      }).join("");
    }

    function planText(line, wip23) {
      const rem = line.remaining_seconds === null ? "无限制" : `剩余 ${line.remaining_seconds}s`;
      const qty = line.target_quantity ? `目标 ${line.target_quantity} 件` : "";
      const shifts = line.target_shifts ? `目标 ${line.target_shifts} 班` : "";
      return `${line.plan_mode} ${rem} ${qty} ${shifts} / WIP WS02->WS03 ${wip23}`;
    }

    async function saveStation(id) {
      currentState = await api(`/vplc/stations/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          base_cycle_s: Number(document.getElementById(`${id}-base`).value),
          jitter_s: Number(document.getElementById(`${id}-jitter`).value),
          nok_rate: Number(document.getElementById(`${id}-nok`).value),
        })
      });
      render(currentState);
    }

    async function togglePause(id, paused) {
      currentState = await api(`/vplc/stations/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paused })
      });
      render(currentState);
    }

    async function forceNok(id) {
      const nokCode = Number(document.getElementById(`${id}-nok-code`).value);
      currentState = await api(`/vplc/stations/${id}/force-nok`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nok_code: nokCode })
      });
      render(currentState);
    }

    async function resetPipeline() {
      if (!confirm("确认重置 WIP 队列和三个工站 counter？")) return;
      currentState = await api("/vplc/reset", { method: "POST" });
      render(currentState);
    }

    async function startPlan() {
      const mode = document.getElementById("planMode").value;
      const payload = { mode };
      if (mode === "duration") payload.duration_hours = Number(document.getElementById("durationHours").value);
      if (mode === "quantity") payload.quantity = Number(document.getElementById("quantityTarget").value);
      if (mode === "shifts") {
        payload.shift_count = Number(document.getElementById("shiftCount").value);
        payload.shift_hours = Number(document.getElementById("shiftHours").value);
      }
      currentState = await api("/vplc/production/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      render(currentState);
    }

    async function stopPlan() {
      currentState = await api("/vplc/production/stop", { method: "POST" });
      render(currentState);
    }

    loadState();
    setInterval(loadState, 2000);
  </script>
</body>
</html>
"""
