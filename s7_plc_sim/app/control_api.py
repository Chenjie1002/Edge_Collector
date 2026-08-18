from __future__ import annotations

import threading
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, StrictInt

from app.pipeline import ThreeStationPipeline


class StationUpdateRequest(BaseModel):
    base_cycle_s: float | None = Field(default=None, ge=1, le=300)
    jitter_s: float | None = Field(default=None, ge=0, le=60)
    nok_rate: float | None = Field(default=None, ge=0, le=1)
    downstream_buffer_capacity: StrictInt | None = Field(default=None, ge=1, le=100)
    paused: bool | None = None
    reason: str = Field(min_length=1, max_length=500)


class ForceNokRequest(BaseModel):
    nok_code: int
    count: int = Field(default=1, ge=1, le=100)
    reason: str = Field(min_length=1, max_length=500)


class ProductionPlanRequest(BaseModel):
    mode: str = Field(default="continuous", pattern="^(continuous|duration|quantity|shifts)$")
    duration_hours: float | None = Field(default=None, gt=0, le=168)
    quantity: int | None = Field(default=None, gt=0, le=1000000)
    shift_count: int | None = Field(default=None, gt=0, le=30)
    shift_hours: float | None = Field(default=8.5, gt=0, le=24)


class SimulationSpeedRequest(BaseModel):
    speed_multiplier: float = Field(ge=1, le=20)
    reason: str = Field(min_length=1, max_length=500)


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

    @app.post("/vplc/simulation/speed")
    def update_simulation_speed(update: SimulationSpeedRequest, request: Request) -> dict:
        with lock:
            try:
                return pipeline.set_simulation_speed(
                    update.speed_multiplier,
                    audit_context={
                        "reason": update.reason,
                        "actor": request.headers.get("X-VPLC-Actor", "anonymous"),
                        "client_ip": request.client.host if request.client else None,
                        "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
                        "source": "API",
                    },
                )
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/vplc/stations/{station_id}")
    def update_station(station_id: str, update: StationUpdateRequest, request: Request) -> dict:
        with lock:
            try:
                params = update.model_dump(exclude_none=True)
                reason = str(params.pop("reason"))
                return pipeline.update_station(
                    station_id,
                    params,
                    audit_context={
                        "reason": reason,
                        "actor": request.headers.get("X-VPLC-Actor", "anonymous"),
                        "client_ip": request.client.host if request.client else None,
                        "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
                        "source": "API",
                    },
                )
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/vplc/audit/changes")
    def audit_changes(limit: int = 100) -> dict:
        recorder = pipeline.audit_recorder
        return {"items": recorder.recent_changes(limit) if recorder else []}

    @app.get("/vplc/audit/snapshots")
    def audit_snapshots(limit: int = 100) -> dict:
        recorder = pipeline.audit_recorder
        return {"items": recorder.recent_snapshots(limit) if recorder else []}

    @app.post("/vplc/stations/{station_id}/force-nok")
    def force_nok(station_id: str, force: ForceNokRequest, request: Request) -> dict:
        with lock:
            try:
                return pipeline.force_nok(
                    station_id,
                    force.nok_code,
                    count=force.count,
                    audit_context={
                        "reason": force.reason,
                        "actor": request.headers.get("X-VPLC-Actor", "anonymous"),
                        "client_ip": request.client.host if request.client else None,
                        "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
                        "source": "API",
                    },
                )
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.delete("/vplc/stations/{station_id}/force-nok")
    def clear_forced_nok(station_id: str, request: Request, reason: str) -> dict:
        with lock:
            try:
                return pipeline.clear_forced_nok(
                    station_id,
                    audit_context={
                        "reason": reason,
                        "actor": request.headers.get("X-VPLC-Actor", "anonymous"),
                        "client_ip": request.client.host if request.client else None,
                        "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
                        "source": "API",
                    },
                )
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
    a.product-back { color: var(--blue); text-decoration: none; font-weight: 700; white-space: nowrap; }
    a.product-back:hover { text-decoration: underline; }
    main { width: min(1320px, calc(100vw - 28px)); margin: 18px auto 28px; display: grid; gap: 14px; }
    .topline { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 12px; }
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
    .plan-grid { display: grid; grid-template-columns: minmax(160px, 1.1fr) repeat(4, minmax(140px, 1fr)) auto auto; gap: 10px; align-items: end; }
    .plan-field, .plan-mode-copy { min-width: 0; }
    .plan-mode-copy { min-height: 34px; display: flex; align-items: center; padding: 0 10px; border: 1px dashed #aab5c5; border-radius: 6px; color: var(--blue); background: #f5f8ff; font-size: 13px; font-weight: 650; }
    .plan-mode-copy[hidden], .plan-field[hidden] { display: none; }
    .unit { color: var(--muted); font-size: 12px; }
    .field-note { color: var(--muted); font-size: 11px; line-height: 1.35; }
    .simulation-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
    .simulation-card { min-height: 72px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfd; }
    .simulation-card strong { display: block; margin-top: 5px; font-size: 18px; }
    .simulation-speed-control { display: grid; grid-template-columns: minmax(180px, 0.9fr) minmax(180px, 1fr) auto; gap: 12px; align-items: end; margin-top: 12px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfd; }
    .simulation-speed-readback { min-height: 34px; display: flex; align-items: center; gap: 8px; color: var(--muted); }
    .simulation-speed-readback strong { color: var(--text); font-size: 18px; }
    .draft-status { display: inline-flex; align-items: center; min-height: 22px; padding: 0 8px; border-radius: 999px; background: #fff5df; color: var(--amber); font-size: 11px; font-weight: 750; }
    .draft-status[hidden] { display: none; }
    .simulation-explain { margin: 12px 0 0; color: var(--muted); font-size: 12px; }
    .station-list { display: grid; gap: 12px; }
    .station-card { padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfd; }
    .station-card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; margin-bottom: 12px; }
    .station-card-title { display: flex; align-items: center; gap: 10px; font-size: 16px; font-weight: 760; }
    .station-live-meta { display: grid; grid-template-columns: repeat(4, minmax(90px, 1fr)); gap: 8px 14px; color: var(--muted); font-size: 12px; }
    .station-live-meta strong { display: block; margin-top: 3px; color: var(--text); font-size: 13px; overflow-wrap: anywhere; }
    .station-groups { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; }
    .control-group { min-width: 0; padding: 10px; border: 1px solid var(--line); border-radius: 7px; background: var(--surface); }
    .control-group h3 { margin: 0 0 9px; color: var(--muted); font-size: 12px; font-weight: 750; }
    .control-fields { display: grid; gap: 8px; }
    .control-fields.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .control-group .actions { align-items: start; }
    .control-group button { flex: 1 1 120px; }
    .live-value { min-height: 20px; overflow-wrap: anywhere; }
    .readonly { color: var(--muted); }
    .field-label { display: grid; gap: 6px; color: var(--muted); font-size: 12px; }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; background: var(--green); box-shadow: 0 0 0 4px #e9f8f1; }
    .dot.off { background: var(--red); box-shadow: 0 0 0 4px #fff0ef; }
    .flow-strip { display: flex; align-items: stretch; gap: 10px; overflow-x: auto; padding: 2px 1px 6px; }
    .flow-node { min-width: 188px; flex: 1 0 188px; border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: var(--surface); }
    .flow-node.buffer { min-width: 150px; flex-basis: 150px; background: var(--surface-2); border-style: dashed; }
    .flow-node-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 10px; }
    .flow-node-title { font-weight: 760; }
    .flow-runtime-badge { flex: 0 0 auto; min-width: 138px; display: grid; gap: 4px; align-self: center; padding: 10px 12px; border: 1px solid #b9ccef; border-radius: 8px; background: #f5f8ff; color: var(--muted); font-size: 11px; }
    .flow-runtime-badge strong { color: var(--blue); font-size: 18px; }
    .flow-runtime-badge small { color: var(--muted); }
    .flow-meta { display: grid; gap: 5px; color: var(--muted); font-size: 12px; }
    .flow-meta strong { color: var(--text); font-weight: 700; overflow-wrap: anywhere; }
    .cycle-track { height: 8px; margin-top: 10px; border-radius: 999px; background: #dfe5ec; overflow: hidden; }
    .cycle-fill { height: 100%; border-radius: inherit; background: var(--blue); transition: width 160ms linear; }
    .flow-arrow { flex: 0 0 18px; align-self: center; color: var(--muted); font-weight: 800; text-align: center; }
    @media (max-width: 960px) {
      .topline, .grid, .simulation-grid { grid-template-columns: 1fr; }
      .simulation-speed-control { grid-template-columns: 1fr; }
      .plan-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .station-card-head { display: grid; }
      .station-live-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .station-groups { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 620px) {
      .plan-grid, .station-groups { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>V-PLC 控制台</h1>
    <div class="actions">
      <a class="product-back" id="productBack" href="/">← 返回 Edge MES</a>
      <button onclick="loadState()">刷新</button>
      <button class="danger" onclick="resetPipeline()">重置 WIP / Counter</button>
    </div>
  </header>
  <main>
    <section class="topline">
      <div class="tile"><div class="label">整线状态</div><div class="value" id="lineState">-</div><div class="hint" id="lineHint">-</div></div>
      <div class="tile"><div class="label">Profile / 模拟倍率</div><div class="value" id="scale">-</div><div class="hint" id="profileHint">1.0 表示真实 30s 左右节拍</div></div>
      <div class="tile"><div class="label">总序号</div><div class="value" id="serial">-</div><div class="hint" id="serialHint">入口站投入件累计</div></div>
      <div class="tile"><div class="label">终点完成</div><div class="value" id="completed">-</div><div class="hint" id="completedHint">OK + NOK terminal completion</div></div>
      <div class="tile"><div class="label">OK</div><div class="value" id="terminalOk">-</div><div class="hint">终点合格累计</div></div>
      <div class="tile"><div class="label">NOK</div><div class="value" id="terminalNok">-</div><div class="hint">终点不合格累计</div></div>
      <div class="tile"><div class="label" id="wipLabel">首段 WIP</div><div class="value" id="wip12">-</div><div class="hint" id="wipHint">-</div></div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>产线流动</h2>
        <span class="hint">真实 topology / edge queue / current cycle，只读轮询</span>
      </div>
      <div class="flow-strip" id="lineFlow" aria-label="V-PLC topology flow"></div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>Production Plan / 生产计划</h2>
        <span class="hint" id="planHint">-</span>
      </div>
      <div class="plan-grid">
        <label class="field-label">Mode / 模式
          <select id="planMode" onfocus="rememberInput(this)" onchange="markPlanControlDirty(this); renderPlanMode(this.value)">
            <option value="continuous">连续生产</option>
            <option value="duration">按小时</option>
            <option value="quantity">按件数</option>
            <option value="shifts">按班次</option>
          </select>
        </label>
        <div class="plan-mode-copy" id="continuousPlanHint" data-plan-mode-field="continuous">
          持续运行，直到手动点击“停止”
        </div>
        <label class="field-label plan-field" id="durationPlanField" data-plan-mode-field="duration" hidden>Duration / 时长
          <input id="durationHours" type="number" min="0.1" step="0.1" value="1" onfocus="rememberInput(this)" oninput="markPlanControlDirty(this)">
          <span class="unit">h</span>
        </label>
        <label class="field-label plan-field" id="quantityPlanField" data-plan-mode-field="quantity" hidden>Quantity / 目标件数
          <input id="quantityTarget" type="number" min="1" step="1" value="100" onfocus="rememberInput(this)" oninput="markPlanControlDirty(this)">
          <span class="unit">pcs</span>
        </label>
        <label class="field-label plan-field" id="shiftsPlanField" data-plan-mode-field="shifts" hidden>Shifts / 班次
          <input id="shiftCount" type="number" min="1" step="1" value="1" onfocus="rememberInput(this)" oninput="markPlanControlDirty(this)">
          <span class="unit">shifts</span>
        </label>
        <label class="field-label plan-field" id="shiftHoursPlanField" data-plan-mode-field="shifts" hidden>Hours per shift / 每班小时
          <input id="shiftHours" type="number" min="0.1" step="0.1" value="8.5" onfocus="rememberInput(this)" oninput="markPlanControlDirty(this)">
          <span class="unit">h / shift</span>
        </label>
        <div class="plan-mode-copy readonly" id="planRunningState">-</div>
        <button class="primary" id="startPlanButton" onclick="startPlan()">开始生产</button>
        <button class="danger" onclick="stopPlan()">停止</button>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>Simulation / 模拟设置</h2>
        <span class="hint">Profile supplies startup defaults; runtime speed is writable for future jobs.</span>
      </div>
      <div class="simulation-grid">
        <div class="simulation-card"><div class="label">Profile</div><strong id="simulationProfile">-</strong></div>
        <div class="simulation-card"><div class="label">Cycle scale / 模拟倍率</div><strong id="simulationScale">-</strong></div>
        <div class="simulation-card"><div class="label">Authority / 权限</div><strong id="simulationAuthority">-</strong></div>
      </div>
      <div class="simulation-speed-control">
        <label class="field-label">Simulation speed / 运行倍率
          <select id="simulationSpeed" onfocus="rememberInput(this)" onchange="markSpeedDirty(this)">
            <option value="1">1×</option>
            <option value="2">2×</option>
            <option value="5">5×</option>
            <option value="10">10×</option>
            <option value="20">20×</option>
          </select>
        </label>
        <div class="simulation-speed-readback">
          <span>Server-applied / 服务端已生效</span>
          <strong id="simulationSpeedApplied">-</strong>
          <span id="simulationSpeedDraftStatus" class="draft-status" hidden>Unsaved / 未保存</span>
        </div>
        <button class="primary" onclick="applySimulationSpeed()">Apply speed / 应用倍率</button>
      </div>
      <p class="simulation-explain">1× = nominal cycle。新倍率只作用于尚未开始的 future jobs；当前 in-flight job 保持其已抽样的完成时间。</p>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>Station Controls / 工站控制</h2>
        <span class="hint">修改后立即生效，正在加工的当前件会保持其已抽样的节拍。</span>
      </div>
      <div class="station-list" id="stationRows"></div>
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
    let stations = [];
    let currentState = null;
    const protectedInputValues = new Map();
    const dirtyInputKeys = new Set();
    const dirtyPlanKeys = new Set();
    const planControlIds = ["planMode", "durationHours", "quantityTarget", "shiftCount", "shiftHours"];

    function inputKey(input) {
      return input.dataset.station + ":" + input.dataset.field;
    }

    function controlKey(control) {
      return control.dataset && control.dataset.station ? inputKey(control) : "plan:" + control.id;
    }

    function planControls() {
      return planControlIds.map(id => document.getElementById(id)).filter(Boolean);
    }

    function isControlDirty(control) {
      const key = controlKey(control);
      return control.dataset.dirty === "true" || dirtyInputKeys.has(key) || dirtyPlanKeys.has(key);
    }

    function controlIsProtected(control) {
      return Boolean(control && (document.activeElement === control || isControlDirty(control)));
    }

    function rememberControl(control) {
      protectedInputValues.set(controlKey(control), {
        value: control.value,
        selectionStart: control.selectionStart,
        selectionEnd: control.selectionEnd,
      });
    }

    function editableControls() {
      const speedControl = document.getElementById("simulationSpeed");
      return [
        ...document.querySelectorAll("input[data-station][data-field]"),
        ...document.querySelectorAll("select[data-station][data-field]"),
        ...planControls(),
        ...(speedControl ? [speedControl] : []),
      ].filter((control, index, controls) => controls.indexOf(control) === index);
    }

    function captureProtectedInputs() {
      editableControls().forEach(control => {
        const key = controlKey(control);
        if (controlIsProtected(control)) {
          rememberControl(control);
        } else {
          protectedInputValues.delete(key);
        }
      });
    }

    function rememberInput(input) {
      rememberControl(input);
    }

    function markInputDirty(input) {
      const key = inputKey(input);
      dirtyInputKeys.add(key);
      rememberControl(input);
      input.dataset.dirty = "true";
      updateStationDraftStatus(input.dataset.station);
    }

    function clearStationDrafts(stationId) {
      ["base_cycle_s", "jitter_s", "nok_rate", "downstream_buffer_capacity"].forEach(field => {
        const key = stationId + ":" + field;
        protectedInputValues.delete(key);
        dirtyInputKeys.delete(key);
      });
      editableControls().forEach(control => {
        if (control.dataset.station === stationId && ["base_cycle_s", "jitter_s", "nok_rate", "downstream_buffer_capacity"].includes(control.dataset.field)) {
          control.dataset.dirty = "false";
        }
      });
      updateStationDraftStatus(stationId);
    }

    function inputDirtyAttribute(stationId, field) {
      return dirtyInputKeys.has(stationId + ":" + field) ? ' data-dirty="true"' : "";
    }

    function markPlanControlDirty(control) {
      const key = controlKey(control);
      dirtyPlanKeys.add(key);
      rememberControl(control);
      control.dataset.dirty = "true";
    }

    function clearPlanDrafts() {
      planControls().forEach(control => {
        const key = controlKey(control);
        protectedInputValues.delete(key);
        dirtyPlanKeys.delete(key);
        control.dataset.dirty = "false";
      });
    }

    function markSpeedDirty(control) {
      const key = controlKey(control);
      dirtyPlanKeys.add(key);
      rememberControl(control);
      control.dataset.dirty = "true";
      const status = document.getElementById("simulationSpeedDraftStatus");
      if (status) {
        status.hidden = false;
        status.textContent = "Unsaved / 未保存";
      }
    }

    function clearSpeedDraft() {
      const control = document.getElementById("simulationSpeed");
      if (!control) return;
      const key = controlKey(control);
      protectedInputValues.delete(key);
      dirtyPlanKeys.delete(key);
      control.dataset.dirty = "false";
      const status = document.getElementById("simulationSpeedDraftStatus");
      if (status) status.hidden = true;
    }

    function formatSpeed(value) {
      const number = Number(value);
      return Number.isInteger(number) ? number.toFixed(0) + "×" : number.toFixed(2) + "×";
    }

    function updateStationDraftStatus(stationId) {
      if (!stationId) return;
      const status = document.getElementById(stationId + "-draft-status");
      if (!status) return;
      const dirty = editableControls().some(control => control.dataset.station === stationId && isControlDirty(control));
      status.hidden = !dirty;
      status.textContent = dirty ? "Unsaved / 未保存" : "";
    }

    function setText(id, value) {
      const element = document.getElementById(id);
      if (element) element.textContent = String(value);
    }

    function updateEditableValue(control, fallback) {
      if (!control || controlIsProtected(control)) return;
      control.value = String(fallback);
    }

    function resultText(code) {
      if (code === 1) return "OK";
      if (code === 2) return "NOK";
      return "-";
    }

    function statusClass(station) {
      if (station.status === "WAITING_TRANSFER" || station.waiting_transfer) return "hold";
      if (station.paused) return "bad";
      if (station.current_dmc) return "run";
      if (station.payload_ready) return "hold";
      return "ok";
    }

    function statusText(station) {
      if (station.status === "WAITING_TRANSFER" || station.waiting_transfer) return "WAITING_TRANSFER";
      if (station.paused) return "PAUSED";
      if (station.current_dmc) return "RUNNING";
      if (station.payload_ready) return "READY";
      return "IDLE";
    }

    function nokOptions(station) {
      const codes = station.nok_codes || [];
      if (station.allow_force === false || !codes.length) return `<option value="">不支持强制NOK</option>`;
      return codes.map(code => `<option value="${code}">${code}</option>`).join("");
    }

    async function api(path, options = {}) {
      const res = await fetch(path, options);
      if (!res.ok) throw new Error(await res.text());
      return res.json();
    }

    async function loadState() {
      currentState = await api("/vplc/state");
      if (currentState && currentState.line && currentState.topology && currentState.stations) render(currentState);
    }

    function renderFlow(state) {
      const topology = state.topology || {};
      const stationIds = topology.station_ids || Object.keys(state.stations || {});
      const buffers = new Map((state.buffers || []).map(buffer => [`${buffer.from_station_id}->${buffer.to_station_id}`, buffer]));
      const parts = [];
      const flowSpeed = Number.isFinite(Number(state.speed_multiplier))
        ? Number(state.speed_multiplier)
        : 1 / Number(state.scale || 1);
      parts.push(`<div class="flow-runtime-badge"><span>Effective speed / 生效倍率</span><strong>${formatSpeed(flowSpeed)}</strong><small>server-applied runtime</small></div>`);
      stationIds.forEach((id, index) => {
        const station = state.stations[id] || {};
        const cycle = station.current_cycle;
        const progress = cycle ? Number(station.current_cycle.progress_percent || 0) : 0;
        parts.push(`<article class="flow-node station-node">
          <div class="flow-node-head"><span class="flow-node-title">${id}</span><span class="status ${statusClass(station)}">${statusText(station)}</span></div>
          <div class="flow-meta">
            <span>Current Unit <strong class="code">${cycle?.unit_id || "-"}</strong></span>
            <span>DMC <strong class="code">${cycle?.dmc || station.current_dmc || "-"}</strong></span>
            <span>Cycle <strong>${cycle ? `${cycle.elapsed_seconds.toFixed(1)} / ${cycle.planned_cycle_seconds.toFixed(1)} s` : "Idle"}</strong></span>
            ${station.status_reason ? `<span>Reason <strong>${station.status_reason}</strong></span>` : ""}
            <span>Applied base / jitter <strong>${Number(station.base_cycle_s || 0).toFixed(1)} / ${Number(station.jitter_s || 0).toFixed(1)} s</strong></span>
            <span>Applied NOK rate <strong>${(Number(station.nok_rate || 0) * 100).toFixed(1)}%</strong></span>
          </div>
          <div class="cycle-track" aria-label="${id} cycle progress"><div class="cycle-fill" style="width:${Math.max(0, Math.min(100, progress))}%"></div></div>
          <div class="hint">${cycle ? `${progress.toFixed(0)}% · remaining ${cycle.remaining_seconds.toFixed(1)} s` : "等待下一件"}</div>
        </article>`);
        if (index < stationIds.length - 1) {
          const next = stationIds[index + 1];
          const buffer = buffers.get(`${id}->${next}`) || { from_station_id: id, to_station_id: next, wip: state.wip?.[`${id}_to_${next}`] || 0, status: "EMPTY", waiting_unit_id: null, waiting_dmc: null };
          parts.push(`<div class="flow-arrow">→</div>`);
          const bufferStatus = buffer.status || (buffer.wip ? "WAITING" : "EMPTY");
          parts.push(`<article class="flow-node buffer">
            <div class="flow-node-head"><span class="flow-node-title">Buffer</span><span class="status ${bufferStatus === "FULL" ? "hold" : (buffer.wip ? "hold" : "ok")}">${bufferStatus}</span></div>
            <div class="flow-meta">
              <span>${buffer.from_station_id} → ${buffer.to_station_id}</span>
              <span>WIP <strong>${buffer.wip || 0} / ${buffer.capacity ?? "-"}</strong></span>
              <span>Waiting Unit <strong class="code">${buffer.waiting_unit_id || "-"}</strong></span>
              <span>DMC <strong class="code">${buffer.waiting_dmc || "-"}</strong></span>
            </div>
          </article>`);
          parts.push(`<div class="flow-arrow">→</div>`);
        }
      });
      document.getElementById("lineFlow").innerHTML = parts.join("");
    }

    function nokOptionsKey(station) {
      return (station.allow_force === false ? "disabled:" : "enabled:") + (station.nok_codes || []).join(",");
    }

    function stationRowHtml(id, station, buffer) {
      return `
        <article class="station-card" data-station-row="${id}">
          <div class="station-card-head">
            <div class="station-card-title">
              <span class="code">${id}</span>
              <span id="${id}-status" class="status ${statusClass(station)}">${statusText(station)}</span>
              <span id="${id}-draft-status" class="draft-status" hidden>Unsaved / 未保存</span>
            </div>
            <div class="station-live-meta">
              <div>Counter<strong id="${id}-counter" class="live-value">${station.cycle_counter}</strong></div>
              <div>Current DMC<strong id="${id}-current-dmc" class="live-value code">${station.current_dmc || "-"}</strong></div>
              <div>Recent DMC<strong id="${id}-last-dmc" class="live-value code">${station.last_dmc || "-"} ${resultText(station.last_result)}</strong></div>
              <div>Cycle progress<strong id="${id}-cycle-progress" class="live-value">等待下一件</strong></div>
            </div>
          </div>
          <div class="station-groups">
            <section class="control-group">
              <h3>Identity &amp; live status</h3>
              <div class="control-fields">
                <div class="readonly">Station identity: <strong class="code">${id}</strong></div>
                <div class="readonly">Status: <strong id="${id}-status-copy">${statusText(station)}</strong></div>
                <div class="readonly">Current unit: <strong id="${id}-current-unit" class="code">-</strong></div>
              </div>
            </section>
            <section class="control-group">
              <h3>Cycle simulation</h3>
              <div class="control-fields">
                <label class="field-label">Base cycle (s)
                  <input id="${id}-base" data-station="${id}" data-field="base_cycle_s"${inputDirtyAttribute(id, "base_cycle_s")} type="number" min="1" step="0.1" value="${station.base_cycle_s.toFixed(1)}" onfocus="rememberInput(this)" oninput="markInputDirty(this)">
                </label>
                <label class="field-label">Jitter (s)
                  <input id="${id}-jitter" data-station="${id}" data-field="jitter_s"${inputDirtyAttribute(id, "jitter_s")} type="number" min="0" step="0.1" value="${station.jitter_s.toFixed(1)}" onfocus="rememberInput(this)" oninput="markInputDirty(this)">
                </label>
                <label class="field-label">NOK rate (%)
                  <input id="${id}-nok" data-station="${id}" data-field="nok_rate"${inputDirtyAttribute(id, "nok_rate")} type="number" min="0" max="1" step="0.001" value="${station.nok_rate.toFixed(3)}" onfocus="rememberInput(this)" oninput="markInputDirty(this)" aria-label="NOK rate 0..1; 0.02 = 2%">
                  <span class="field-note">输入 0..1；例如 0.02 = 2%</span>
                </label>
              </div>
            </section>
            ${buffer ? `<section class="control-group">
              <h3>Downstream Buffer</h3>
              <div class="control-fields">
                <div class="readonly">To station: <strong class="code">${buffer.to_station_id}</strong></div>
                <label class="field-label">Capacity
                  <input id="${id}-buffer-capacity" data-station="${id}" data-field="downstream_buffer_capacity"${inputDirtyAttribute(id, "downstream_buffer_capacity")} type="number" min="1" max="100" step="1" value="${buffer.capacity ?? 1}" onfocus="rememberInput(this)" oninput="markInputDirty(this)">
                  <span class="field-note">WIP ${buffer.wip || 0} / ${buffer.capacity ?? 1} · 1..100</span>
                </label>
              </div>
            </section>` : ""}
            <section class="control-group">
              <h3>Forced NOK</h3>
              <div class="control-fields">
                <label class="field-label">Code
                  <select id="${id}-nok-code" data-station="${id}" data-field="force_nok_code" data-options-key="${nokOptionsKey(station)}" onchange="markInputDirty(this)" ${station.allow_force === false ? "disabled" : ""}>${nokOptions(station)}</select>
                </label>
                <label class="field-label">Count
                  <input id="${id}-nok-count" data-station="${id}" data-field="force_nok_count" type="number" min="1" max="100" step="1" value="1" title="连续强制 NOK 数量" onfocus="rememberInput(this)" oninput="markInputDirty(this)">
                </label>
                <div class="readonly">Pending: <strong id="${id}-pending-nok">${station.pending_forced_nok_count}</strong></div>
              </div>
            </section>
            <section class="control-group">
              <h3>Control</h3>
              <div class="actions">
                <button class="primary" onclick="saveStation('${id}')">Save parameter</button>
                <button id="${id}-pause-button" onclick="togglePause('${id}', ${!station.paused})">${station.paused ? "Resume" : "Pause"}</button>
                <button class="danger" id="${id}-force-button" onclick="forceNok('${id}')" ${station.allow_force === false ? "disabled" : ""}>Force NOK (${station.pending_forced_nok_count})</button>
                <button onclick="clearForcedNok('${id}')">Clear NOK</button>
              </div>
            </section>
          </div>
        </article>`;
    }

    function updateStationRow(id, station, state, buffer) {
      if (!station) return;
      const cycle = station.current_cycle;
      const progress = cycle ? Number(cycle.progress_percent || 0) : 0;
      const status = document.getElementById(id + "-status");
      if (status) {
        status.className = "status " + statusClass(station);
        status.textContent = statusText(station);
      }
      setText(id + "-status-copy", statusText(station));
      setText(id + "-counter", station.cycle_counter);
      setText(id + "-current-dmc", station.current_dmc || "-");
      setText(id + "-last-dmc", (station.last_dmc || "-") + " " + resultText(station.last_result));
      setText(id + "-current-unit", cycle?.unit_id || "-");
      const cycleProgressText = cycle ? progress.toFixed(0) + "% · " + cycle.remaining_seconds.toFixed(1) + " s remaining" : "等待下一件";
      setText(id + "-cycle-progress", station.waiting_transfer ? cycleProgressText + " · waiting transfer" : cycleProgressText);
      setText(id + "-pending-nok", station.pending_forced_nok_count || 0);

      const canEdit = state.allow_runtime_cycle_edit !== false;
      const baseInput = document.getElementById(id + "-base");
      const jitterInput = document.getElementById(id + "-jitter");
      const nokInput = document.getElementById(id + "-nok");
      [baseInput, jitterInput, nokInput].forEach(input => {
        if (input) input.disabled = !canEdit;
      });
      updateEditableValue(baseInput, station.base_cycle_s.toFixed(1));
      updateEditableValue(jitterInput, station.jitter_s.toFixed(1));
      updateEditableValue(nokInput, station.nok_rate.toFixed(3));
      const bufferInput = document.getElementById(id + "-buffer-capacity");
      updateEditableValue(bufferInput, buffer?.capacity ?? 1);

      const codeSelect = document.getElementById(id + "-nok-code");
      if (codeSelect && !controlIsProtected(codeSelect)) {
        const optionsKey = nokOptionsKey(station);
        if (codeSelect.dataset.optionsKey !== optionsKey) {
          const selected = codeSelect.value;
          codeSelect.innerHTML = nokOptions(station);
          codeSelect.dataset.optionsKey = optionsKey;
          if (selected && (station.nok_codes || []).map(String).includes(selected)) codeSelect.value = selected;
        }
      }
      if (codeSelect) codeSelect.disabled = station.allow_force === false || !(station.nok_codes || []).length;
      const forceButton = document.getElementById(id + "-force-button");
      if (forceButton) {
        forceButton.disabled = station.allow_force === false || !(station.nok_codes || []).length;
        forceButton.textContent = "Force NOK (" + (station.pending_forced_nok_count || 0) + ")";
      }
      const pauseButton = document.getElementById(id + "-pause-button");
      if (pauseButton) pauseButton.textContent = station.paused ? "Resume" : "Pause";
      updateStationDraftStatus(id);
    }

    function renderStationRows(state) {
      const rowHost = document.getElementById("stationRows");
      if (!rowHost) return;
      const downstreamBuffers = new Map((state.buffers || []).map(buffer => [buffer.from_station_id, buffer]));
      const topologyKey = stations.join("|");
      if (rowHost.dataset.topologyKey !== topologyKey) {
        rowHost.innerHTML = stations.map(id => stationRowHtml(id, state.stations[id], downstreamBuffers.get(id))).join("");
        rowHost.dataset.topologyKey = topologyKey;
      }
      stations.forEach(id => updateStationRow(id, state.stations[id], state, downstreamBuffers.get(id)));
    }

    function renderPlanMode(mode) {
      const modeFields = [
        ["continuousPlanHint", "continuous"],
        ["durationPlanField", "duration"],
        ["quantityPlanField", "quantity"],
        ["shiftsPlanField", "shifts"],
        ["shiftHoursPlanField", "shifts"],
      ];
      modeFields.forEach(([id, fieldMode]) => {
        const field = document.getElementById(id);
        if (field) field.hidden = fieldMode !== mode;
      });
      const startButton = document.getElementById("startPlanButton");
      if (startButton) startButton.textContent = mode === "continuous" ? "开始连续生产" : "开始生产";
    }

    function positiveNumber(value) {
      const number = Number(value);
      return Number.isFinite(number) && number > 0 ? number : null;
    }

    function planText(line, wipEntries) {
      const mode = String(line.plan_mode || "continuous").toLowerCase();
      let summary = mode.toUpperCase();
      if (mode === "continuous") {
        summary += line.plan_active ? " / Running until manual stop" : " / stopped";
      } else if (mode === "duration") {
        const hours = positiveNumber(line.remaining_seconds);
        summary += hours ? " / " + (hours / 3600).toFixed(1) + " h remaining" : " / stopped";
      } else if (mode === "quantity") {
        const quantity = positiveNumber(line.target_quantity);
        summary += quantity ? " / " + quantity + " pcs target" : " / stopped";
      } else if (mode === "shifts") {
        const shifts = positiveNumber(line.target_shifts);
        const shiftHours = positiveNumber(line.shift_hours);
        summary += shifts && shiftHours ? " / " + shifts + " shifts · " + shiftHours + " h/shift" : " / stopped";
      }
      const wip = wipEntries.map(item => item.label + " " + item.value).join(" / ") || "无中间 WIP";
      return summary + " / " + wip;
    }

    function renderPlan(line, wipEntries) {
      const modeControl = document.getElementById("planMode");
      const serverMode = String(line.plan_mode || "continuous").toLowerCase();
      if (modeControl && !controlIsProtected(modeControl)) modeControl.value = serverMode;
      const mode = modeControl?.value || serverMode;
      renderPlanMode(mode);
      setText("planHint", planText(line, wipEntries));
      setText("planRunningState", line.plan_active && serverMode === "continuous" ? "CONTINUOUS / Running until manual stop" : (line.plan_active ? serverMode.toUpperCase() + " / Running" : "STOPPED / " + (line.stop_reason || "manual stop")));
    }

    function render(state) {
      captureProtectedInputs();
      const line = state.line;
      const serverSpeed = Number.isFinite(Number(state.speed_multiplier))
        ? Number(state.speed_multiplier)
        : 1 / Number(state.scale || 1);
      stations = (state.topology && state.topology.station_ids) || Object.keys(state.stations || {});
      const topology = state.topology || {};
      const edges = topology.edges || [];
      const wipEntries = edges.map(edge => {
        const key = `${edge.from_station_id}_to_${edge.to_station_id}`;
        return { key, label: `${edge.from_station_id} -> ${edge.to_station_id}`, value: state.wip[key] || 0 };
      });
      document.getElementById("lineState").innerHTML = `<span class="dot ${line.running ? "" : "off"}"></span>${line.running ? "RUN" : "STOP"}`;
      document.getElementById("lineHint").textContent = line.running ? `${line.plan_mode} / 已运行 ${line.elapsed_seconds}s` : (line.stop_reason || "停止");
      document.getElementById("scale").textContent = state.scale.toFixed(2);
      document.getElementById("profileHint").textContent = `${state.profile} / ${state.allow_runtime_cycle_edit ? "允许节拍编辑" : "节拍锁定"}`;
      setText("simulationProfile", state.profile);
      setText("simulationScale", state.scale.toFixed(2) + "×");
      setText("simulationAuthority", state.speed_runtime_writable === false ? "runtime locked" : "runtime writable");
      setText("simulationSpeedApplied", formatSpeed(serverSpeed));
      const speedControl = document.getElementById("simulationSpeed");
      if (speedControl && !controlIsProtected(speedControl)) speedControl.value = String(serverSpeed);
      const speedDraftStatus = document.getElementById("simulationSpeedDraftStatus");
      if (speedDraftStatus && (!speedControl || !isControlDirty(speedControl))) speedDraftStatus.hidden = true;
      document.getElementById("serial").textContent = state.serial_no;
      const terminalCompleted = state.terminal_completed_total ?? state.completed_quantity ?? 0;
      const terminalOk = state.terminal_ok_count ?? state.completed_quantity ?? 0;
      const terminalNok = state.terminal_nok_count ?? 0;
      document.getElementById("completed").textContent = terminalCompleted;
      document.getElementById("terminalOk").textContent = terminalOk;
      document.getElementById("terminalNok").textContent = terminalNok;
      document.getElementById("serialHint").textContent = `${topology.entry_station_id || "入口站"} 投入件累计`;
      document.getElementById("completedHint").textContent = `${topology.terminal_station_id || "终点站"} 终点完成 = OK ${terminalOk} + NOK ${terminalNok}`;
      document.getElementById("wipLabel").textContent = wipEntries[0]?.label || "首段 WIP";
      document.getElementById("wip12").textContent = wipEntries[0]?.value || 0;
      document.getElementById("wipHint").textContent = wipEntries.slice(1).map(item => `${item.label}: ${item.value}`).join(" / ") || "无中间边";
      renderPlan(line, wipEntries);
      renderFlow(state);
      document.getElementById("rawJson").textContent = JSON.stringify(state, null, 2);
      document.getElementById("updatedAt").textContent = new Date().toLocaleTimeString();
      renderStationRows(state);
    }

    async function applySimulationSpeed() {
      const speedControl = document.getElementById("simulationSpeed");
      if (!speedControl) return;
      const reason = prompt("请输入本次运行倍率修改原因：");
      if (!reason) return;
      const nextState = await api("/vplc/simulation/speed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ speed_multiplier: Number(speedControl.value), reason })
      });
      clearSpeedDraft();
      currentState = nextState;
      setText("simulationSpeedApplied", formatSpeed(nextState.speed_multiplier));
      if (nextState.line && nextState.topology && nextState.stations) render(currentState);
    }

    async function saveStation(id) {
      const reason = prompt("请输入本次参数修改原因：");
      if (!reason) return;
      const payload = {
        base_cycle_s: Number(document.getElementById(`${id}-base`).value),
        jitter_s: Number(document.getElementById(`${id}-jitter`).value),
        nok_rate: Number(document.getElementById(`${id}-nok`).value),
        reason,
      };
      const capacityInput = document.getElementById(`${id}-buffer-capacity`);
      if (capacityInput) payload.downstream_buffer_capacity = Number(capacityInput.value);
      const nextState = await api(`/vplc/stations/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      clearStationDrafts(id);
      currentState = nextState;
      render(currentState);
    }

    async function togglePause(id, paused) {
      currentState = await api(`/vplc/stations/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paused, reason: paused ? "control page pause" : "control page resume" })
      });
      render(currentState);
    }

    async function forceNok(id) {
      const nokCode = Number(document.getElementById(`${id}-nok-code`).value);
      const count = Number(document.getElementById(`${id}-nok-count`).value);
      const reason = prompt("请输入强制 NOK 原因：");
      if (!reason) return;
      currentState = await api(`/vplc/stations/${id}/force-nok`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nok_code: nokCode, count, reason })
      });
      render(currentState);
    }

    async function clearForcedNok(id) {
      const reason = prompt("请输入清除强制 NOK 队列的原因：");
      if (!reason) return;
      currentState = await api(`/vplc/stations/${id}/force-nok?reason=${encodeURIComponent(reason)}`, {
        method: "DELETE"
      });
      render(currentState);
    }

    async function resetPipeline() {
      if (!confirm("确认重置 WIP 队列和全部工站 counter？")) return;
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

    function dashboardUrl() {
      const protocol = window.location.protocol === "https:" ? "https:" : "http:";
      return protocol + "//" + window.location.hostname + ":3001/";
    }
    const productBack = document.getElementById("productBack");
    if (productBack && typeof window !== "undefined") productBack.href = dashboardUrl();

    async function pollState() {
      try { await loadState(); } finally { setTimeout(pollState, 1000); }
    }
    renderPlanMode("continuous");
    pollState();
  </script>
</body>
</html>
"""
