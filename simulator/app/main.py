import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .models import CustomFaultRequest, MachineState, ScenarioRequest, ScenarioSummary
from .simulator import ProductionSimulator

app = FastAPI(title="Edge MES Simulator")
simulator = ProductionSimulator()


@app.on_event("startup")
async def start_loop() -> None:
    async def loop() -> None:
        while True:
            simulator.tick()
            await asyncio.sleep(1)

    asyncio.create_task(loop())


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/state", response_model=MachineState)
def state() -> dict:
    return simulator.state()


@app.get("/scenarios", response_model=list[ScenarioSummary])
def scenarios() -> list[dict]:
    return simulator.scenarios()


@app.post("/scenario/{scenario_id}", response_model=MachineState)
def set_scenario(scenario_id: str, request: ScenarioRequest | None = None) -> dict:
    try:
        return simulator.set_scenario(
            scenario_id,
            duration_seconds=request.duration_seconds if request else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/reset-counts", response_model=MachineState)
def reset_counts() -> dict:
    return simulator.reset_counts()


@app.post("/custom-fault", response_model=MachineState)
def custom_fault(request: CustomFaultRequest) -> dict:
    try:
        return simulator.trigger_custom_fault(
            name=request.name,
            fault_code=request.fault_code,
            duration_seconds=request.duration_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/trigger/alarm")
def trigger_alarm(code: int = 1001, duration_seconds: int = 60) -> dict:
    return simulator.trigger_alarm(code, duration_seconds)


@app.post("/trigger/stop")
def trigger_stop(code: int = 2, duration_seconds: int = 60) -> dict:
    return simulator.trigger_stop(code, duration_seconds)


@app.post("/clear")
def clear() -> dict:
    return simulator.clear()


@app.get("/", response_class=HTMLResponse)
@app.get("/control", response_class=HTMLResponse)
def control_page() -> str:
    return CONTROL_PAGE_HTML


CONTROL_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Edge MES Scenario Control</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --surface: #ffffff;
      --line: #d9dee7;
      --text: #17202f;
      --muted: #667085;
      --accent: #1967d2;
      --danger: #b42318;
      --ok: #067647;
      --warn: #b54708;
      font-family: "Inter", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--text); font-size: 14px; }
    header { background: var(--surface); border-bottom: 1px solid var(--line); padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
    h1 { margin: 0; font-size: 20px; line-height: 1.2; letter-spacing: 0; }
    main { width: min(1180px, calc(100vw - 32px)); margin: 20px auto 32px; display: grid; gap: 16px; }
    .status-strip { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
    .metric, .panel { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }
    .metric { padding: 14px 16px; min-height: 104px; }
    .metric .label { color: var(--muted); font-size: 12px; margin-bottom: 10px; }
    .metric .value { font-size: 22px; font-weight: 700; line-height: 1.1; white-space: nowrap; }
    .metric .hint { margin-top: 8px; color: var(--muted); font-size: 12px; line-height: 1.4; }
    .panel { padding: 18px; }
    .panel-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; }
    h2 { margin: 0; font-size: 16px; letter-spacing: 0; }
    .toolbar, .form-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    label.inline { display: inline-flex; align-items: center; gap: 6px; color: var(--muted); font-size: 12px; }
    input, select { height: 36px; border: 1px solid var(--line); border-radius: 6px; padding: 0 10px; font: inherit; background: #fff; }
    input.short { width: 104px; }
    input.medium { width: 180px; }
    select { width: 160px; }
    button { height: 36px; border: 1px solid var(--line); border-radius: 6px; padding: 0 12px; background: #fff; color: var(--text); font: inherit; cursor: pointer; }
    button.icon { width: 36px; padding: 0; font-size: 20px; line-height: 1; }
    button:hover { border-color: #9aa4b2; background: #f9fafb; }
    button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
    button.danger { border-color: #fecdca; color: var(--danger); }
    .scenario-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
    .scenario { border: 1px solid var(--line); border-radius: 8px; padding: 14px; background: #fff; text-align: left; height: auto; min-height: 124px; display: grid; align-content: start; gap: 8px; }
    .scenario.active { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
    .scenario strong { font-size: 15px; }
    .scenario span, .help { color: var(--muted); line-height: 1.45; }
    .help { margin: 0 0 14px; font-size: 13px; }
    .badge { display: inline-flex; align-items: center; width: fit-content; min-height: 26px; border-radius: 999px; padding: 0 10px; font-size: 12px; font-weight: 700; background: #eef4ff; color: #1849a9; }
    .badge.ok { background: #ecfdf3; color: var(--ok); }
    .badge.warn { background: #fffaeb; color: var(--warn); }
    .badge.danger { background: #fef3f2; color: var(--danger); }
    .progress-track { height: 10px; margin-top: 10px; background: #edf1f7; border-radius: 999px; overflow: hidden; }
    .progress-bar { height: 100%; width: 0%; background: linear-gradient(90deg, #1967d2, #7c3aed); border-radius: inherit; transition: width 0.35s linear; }
    .custom-fault { display: none; margin-top: 14px; padding: 14px; border: 1px dashed #a9b4c2; border-radius: 8px; background: #fbfcfe; }
    .custom-fault.open { display: grid; gap: 10px; }
    pre { margin: 0; padding: 14px; background: #111827; color: #e5e7eb; border-radius: 8px; overflow: auto; min-height: 170px; font-size: 12px; line-height: 1.55; }
    @media (max-width: 900px) { header { align-items: flex-start; flex-direction: column; } .status-strip, .scenario-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (max-width: 620px) { main { width: min(100vw - 20px, 1180px); } .status-strip, .scenario-grid { grid-template-columns: 1fr; } .panel-head { align-items: flex-start; flex-direction: column; } .toolbar, .form-row { width: 100%; } input, select, button { flex: 1 1 auto; } }
  </style>
</head>
<body>
  <header>
    <h1>Edge MES 场景控制台</h1>
    <div class="toolbar">
      <a href="/state" target="_blank"><button>State JSON</button></a>
      <a id="grafanaLink" href="#" target="_blank"><button>Grafana</button></a>
    </div>
  </header>
  <main>
    <section class="status-strip">
      <div class="metric"><div class="label">当前场景</div><div class="value" id="scenarioName">-</div><div class="hint" id="remaining">-</div></div>
      <div class="metric"><div class="label">设备状态</div><div class="value" id="running">-</div><div class="hint" id="alarmStop">-</div></div>
      <div class="metric"><div class="label">总产量</div><div class="value" id="total">-</div><div class="hint" id="goodNg">-</div></div>
      <div class="metric"><div class="label">当前节拍</div><div class="value" id="cycle">-</div><div class="hint" id="cycleHint">-</div><div class="progress-track"><div class="progress-bar" id="cycleProgress"></div></div></div>
      <div class="metric"><div class="label">产品/班次</div><div class="value" id="product">-</div><div class="hint" id="shift">-</div></div>
    </section>
    <section class="panel">
      <div class="panel-head">
        <h2>手动触发工况</h2>
        <div class="toolbar">
          <label class="inline">持续秒数 <input id="duration" class="short" type="number" min="1" step="1" value="180"></label>
          <button class="primary" onclick="applyScenario('normal')">恢复正常</button>
          <button class="icon" title="新增自定义故障" onclick="toggleCustomFault()">+</button>
          <button class="danger" onclick="resetCounts()">清零产量</button>
        </div>
      </div>
      <p class="help">持续秒数用于手动工况的持续时间；点击“恢复正常”时，同一个数值表示暂停随机故障的稳定运行时间，避免刚恢复又被随机停机打断。</p>
      <div class="scenario-grid" id="scenarioGrid"></div>
      <div class="custom-fault" id="customFault">
        <div class="form-row">
          <label class="inline">故障名称 <input id="customFaultName" class="medium" value="自定义故障"></label>
          <label class="inline">故障类别
            <select id="customFaultType" onchange="syncFaultCodeRange()">
              <option value="equipment">设备故障 1001-1099</option>
              <option value="non_equipment">非设备故障 1100-1199</option>
            </select>
          </label>
          <label class="inline">故障代码 <input id="customFaultCode" class="short" type="number" min="1001" max="1099" value="1001"></label>
          <label class="inline">停机秒数 <input id="customFaultDuration" class="short" type="number" min="1" value="180"></label>
          <button class="primary" onclick="submitCustomFault()">触发故障</button>
        </div>
        <div class="help">设备故障代码范围：1001-1099；非设备故障代码范围：1100-1199。触发后设备进入报警停机，倒计时结束自动恢复。</div>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head"><h2>实时状态 JSON</h2><span class="badge" id="pollState">polling</span></div>
      <pre id="rawState">{}</pre>
    </section>
  </main>
  <script>
    let currentState = {};
    let scenarios = [];
    document.getElementById("grafanaLink").href = `${window.location.protocol}//${window.location.hostname}:3000/d/edge-mes-overview`;

    function fmtSeconds(seconds, scenarioId) {
      if (!seconds) return "无倒计时";
      const m = Math.floor(seconds / 60);
      const s = seconds % 60;
      const label = scenarioId === "normal" ? "随机故障暂停" : "自动恢复";
      return `${label}：${m}分${String(s).padStart(2, "0")}秒`;
    }

    function statusBadge(state) {
      if (state.alarm_active) return ["报警", "danger"];
      if (state.stop_reason_code) return ["停机", "warn"];
      if (state.running) return ["运行", "ok"];
      return ["等待", "warn"];
    }

    async function fetchJson(url, options) {
      const res = await fetch(url, options);
      if (!res.ok) throw new Error(await res.text());
      return res.json();
    }

    async function loadScenarios() {
      scenarios = await fetchJson("/scenarios");
      const grid = document.getElementById("scenarioGrid");
      grid.innerHTML = scenarios.filter(s => s.id !== "normal").map(s => `
        <button class="scenario" id="scenario-${s.id}" onclick="applyScenario('${s.id}')">
          <strong>${s.name}</strong><span>${s.description}</span><span>默认 ${s.default_duration_seconds}s</span>
        </button>`).join("");
    }

    async function applyScenario(id) {
      const durationInput = Number(document.getElementById("duration").value || 0);
      const body = { duration_seconds: durationInput || undefined };
      currentState = await fetchJson(`/scenario/${id}`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
      });
      renderState(currentState);
    }

    async function resetCounts() {
      currentState = await fetchJson("/reset-counts", { method: "POST" });
      renderState(currentState);
    }

    function toggleCustomFault() {
      document.getElementById("customFault").classList.toggle("open");
    }

    function syncFaultCodeRange() {
      const type = document.getElementById("customFaultType").value;
      const code = document.getElementById("customFaultCode");
      if (type === "equipment") { code.min = 1001; code.max = 1099; code.value = Math.min(Math.max(Number(code.value) || 1001, 1001), 1099); }
      else { code.min = 1100; code.max = 1199; code.value = Math.min(Math.max(Number(code.value) || 1100, 1100), 1199); }
    }

    async function submitCustomFault() {
      syncFaultCodeRange();
      const payload = {
        name: document.getElementById("customFaultName").value || "自定义故障",
        fault_code: Number(document.getElementById("customFaultCode").value),
        duration_seconds: Number(document.getElementById("customFaultDuration").value || 180),
      };
      currentState = await fetchJson("/custom-fault", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
      });
      renderState(currentState);
    }

    function renderState(state) {
      const [label, klass] = statusBadge(state);
      document.getElementById("scenarioName").textContent = state.scenario_name || "-";
      document.getElementById("remaining").textContent = fmtSeconds(state.scenario_remaining_seconds, state.scenario_id);
      document.getElementById("running").innerHTML = `<span class="badge ${klass}">${label}</span>`;
      document.getElementById("alarmStop").textContent = `报警 ${state.alarm_code || 0} / 停机 ${state.stop_reason_code || 0}`;
      document.getElementById("total").textContent = state.total_count;
      document.getElementById("goodNg").textContent = `OK ${state.good_count} / NG ${state.ng_count}`;
      document.getElementById("cycle").textContent = `${(state.cycle_time_ms / 1000).toFixed(1)}s`;
      document.getElementById("cycleHint").textContent = `本周期 ${(state.cycle_elapsed_ms / 1000).toFixed(1)}s / 进度 ${state.cycle_progress_percent.toFixed(1)}%`;
      document.getElementById("cycleProgress").style.width = `${state.cycle_progress_percent}%`;
      document.getElementById("product").textContent = state.product_type;
      document.getElementById("shift").textContent = state.shift_id;
      document.getElementById("rawState").textContent = JSON.stringify(state, null, 2);
      document.querySelectorAll(".scenario").forEach(el => el.classList.remove("active"));
      const active = document.getElementById(`scenario-${state.scenario_id}`);
      if (active) active.classList.add("active");
    }

    async function poll() {
      try {
        currentState = await fetchJson("/state");
        renderState(currentState);
        document.getElementById("pollState").textContent = "polling";
        document.getElementById("pollState").className = "badge ok";
      } catch (err) {
        document.getElementById("pollState").textContent = "offline";
        document.getElementById("pollState").className = "badge danger";
      }
    }

    loadScenarios().then(poll);
    setInterval(poll, 1000);
  </script>
</body>
</html>
"""
