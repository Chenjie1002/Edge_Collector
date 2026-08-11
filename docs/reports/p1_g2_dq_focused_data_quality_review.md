# P1-G2-DQ Focused Data Quality Review

结论：`PASS`

本报告是独立 Data Quality Thread 对同一冻结 Quality + accepted-fact Trace candidate 的只读、local/static/fake-DB review。结论仅覆盖本地源码、合同、测试与一次本地 focused pytest；不代表 live DB/API、部署、激活、`RUNTIME_LOADED`、`PRODUCTION_ACCEPTED` 或 Git 发布。

## 1. 任务与报告身份

- 报告名称：P1-G2-DQ Focused Data Quality Review
- 执行 Thread：Data Quality
- delivery mode：`REPOSITORY_DURABLE_REPORT`
- task：`docs/thread_handoff/pm_task_20260811T1302Z_p1_g2_dq_focused_data_quality_review.md`
- task：regular/non-symlink，`19838` bytes，SHA-256 `4184c0c8fb659ec8d06492062c2b8455de9ab9d369577050e687287236a1c144`
- exact report：`docs/reports/p1_g2_dq_focused_data_quality_review.md`
- report identity：本次唯一写入完成后由冻结 control-plane Python 计算并记录在 terminal manifest；本报告不再被回写。
- Current Gate：`P1-G2-DQ_FOCUSED_DATA_QUALITY`
- MVP classification：`MVP-ALIGNED`

## 2. Authority、candidate 与 ordered-read manifest

Authority source：`P1-SHADOW-PM-QUALITY-TRACE-LOCAL-MVP-V1`；本 task 授权只读 Data Quality review、项目 test runtime 的 local validation 与本 exact report。

Candidate identity binding 全部通过（regular/non-symlink、bytes、SHA-256）：

| object | bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` |
| `api/app/main.py` | 464 | `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |

Continuity identities also全部通过：Amendment `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter_amendment_001_project_test_runtime.md` = `5197` / `c8b558c75a926415041a90de5e8221e514e58cec80e48361c23480d83242c633`；Reliability task = `docs/thread_handoff/pm_task_20260811T1250Z_p1_g2_r_focused_reliability_review.md` = `18804` / `9d533bb231b7ddfa3561481a72cea7ffad233d493fa04f7d522ca48d327d3577`；Reliability report = `docs/reports/p1_g2_r_focused_reliability_review.md` = `7917` / `655bcd3ee79a7e55d93dd24a47a4abc41bcaecb756fddc8a0f6856e05fedabea`；current test-repair report = `docs/reports/p1_g2_i_trace_test_helper_identity_repair.md` = `10419` / `a7d7e3ade234444ec91bd48852db1e9b2e0e45fea37e89fa19c256be8ca2c3eb`。

Ordered reads 1–18 completed in task order：task self-identity、PM rules、current status、Charter、Bootstrap、Amendment、Ledger、G0 source boundary、trusted-consumption plan、G1 contract、G2-I syntax-repair report、G2-I test-helper report、G2-R Reliability report、Quality/Trace source、router registration、focused test、`.venv/pyvenv.cfg`、external base interpreter identity。未进行 directory-wide discovery。

## 3. Fresh root、Git 与 protected-state evidence

- physical cwd = `/Users/chenjie/Documents/MES/edge-mes-demo`
- `git rev-parse --show-toplevel` = `/Users/chenjie/Documents/MES/edge-mes-demo`
- branch = `main`
- HEAD = `dbe5706e4b01387101f2a4666e73f3c13ffeb0e9`
- origin/main = `2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35`
- `origin/main...HEAD` = `0 1`
- cached/staged names = empty
- pre-existing tracked dirty paths remain exactly：`api/app/main.py`、`docs/current_status.md`、`docs/thread_handoff/pm_operating_rules.md`
- pre-existing untracked Goal-control/candidate corpus preserved；未 cleanup、adopt、stage、commit、push 或修改
- report target entry/pre-write = absent、non-symlink
- `git diff --check` = PASS

Live Ledger records this dispatch as `TOTAL_DISPATCHED_GATES = 8` after the parent’s prior `7`; product repair gates remain `3`，control-plane recovery gates remain `1`。This child adds no repair or recovery gate.

## 4. Runtime 与 validation

Control-plane：`/opt/homebrew/opt/python@3.14/bin/python3.14`，version `3.14.6`，architecture `arm64`；resolved target regular/non-symlink，`52448` bytes，SHA-256 `b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf`。

Project test runtime preconditions全部通过：`.venv/pyvenv.cfg version=3.13.3`；runtime Python `3.13.3`；architecture `arm64`；resolved base `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`，regular/non-symlink，`119328` bytes，SHA-256 `f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`；pytest `9.1.1`；fastapi `0.115.6`；psycopg `3.2.3`。

Compile/import smoke（in-memory，未启动 server、未连接 DB/API）：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api ./.venv/bin/python -B -c 'compile quality_trace.py; compile test_quality_trace_api.py; import app.main'
result = G2_DQ_IMPORT_COMPILE_SMOKE=PASS
```

Focused pytest 严格启动 1 次：

```text
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=api ./.venv/bin/python -m pytest -q api/tests/test_quality_trace_api.py
result = 16 passed in 0.19s
```

## 5. Data Quality review findings

### 5.1 Accepted-fact authority 与 lineage

PASS。Quality SQL 只读 `production_accepted_station_event_fact`，绑定 `line_id`、`station_id` 与半开窗口 `[start,end)`；Trace SQL 只读同一 accepted-fact 表，绑定 `line_id`、选定 exact identity、窗口与 limit（`api/app/routes/quality_trace.py:133-183`）。未发现 raw/normalized candidate、adapter/decoder diagnostic、ACK/read_done、`production_snapshot`、`cycle_event`、`station_event`、`production_unit` 或 `quality_event` fallback/join。

PASS。Trace 只报告实际返回的 `observed_station_ids`，固定返回 `missing_station_status=UNKNOWN` 与 `route_data_sufficiency=PARTIAL`，空结果为 `UNAVAILABLE`；没有 current YAML、固定 WS03、route fabrication、time-nearest fill、genealogy/parent-child/rework inference（`quality_trace.py:294-303`）。历史 config lineage 未被静默声称已解析。

### 5.2 Quality denominator、NOK 与 empty semantics

PASS。SQL 限定 `event_type='station_result'`；实现只将 `production_result='ok'` 计 good、`'nok'` 计 NOK，denominator 为二者之和，因而 `skip`/`not_applicable` 不入 denominator；空 denominator 返回 `quality_rate=null` 与 `data_sufficiency=UNAVAILABLE`，不制造 0%（`quality_trace.py:133-142,222-257`）。NOK distribution 来自 accepted row 的 `nok_code`，未使用 diagnostic reason；缺失 NOK code 时保留 counts/rate 但标记 `PARTIAL`。

测试 fake-DB evidence 覆盖 OK/NOK/skip、empty denominator、accepted-fact-only SQL 与 forbidden source 检查（`api/tests/test_quality_trace_api.py:219-270`）。该 evidence 是 local synthetic/fake-DB evidence，不是 production DB observation。

### 5.3 Trace identity、deterministic projection 与 no leakage

PASS。`unit_id`/DMC 先 trim，blank/missing/both/neither 在 DB query 前 fail closed；动态 SQL identifier 仅从固定 `unit_id`/`dmc` 分支选择，查询使用 exact equality 和 `IS NOT NULL`，没有 serial、cycle、时间接近或 legacy identity 合成（`quality_trace.py:261-292`）。

PASS。Trace chronology 使用 accepted row 的 `ORDER BY event_ts ASC, accepted_at ASC, fact_key ASC`，limit 受 `1..500` bounded contract 约束（`quality_trace.py:153-183`）。DTO 由显式 `DTO_FIELDS` 逐字段投影，时间字段只做 UTC 表示转换；focused tests 验证 field allowlist、stable order、forbidden surfaces/sources 与 no-DB rejection（`quality_trace.py:14-37,110-115`；`test_quality_trace_api.py:274-360`）。响应未泄露 raw payload/raw_hex、diagnostic reason、ACK/read_done、legacy payload 或内部异常文本。

### 5.4 Scope、failure boundary 与 MVP sufficiency

PASS。请求参数、line/station/identity、UTC timestamp、half-open window 与 limit 均 fail closed；读事务为 `BEGIN READ ONLY`，设置 statement/idle timeout，异常 rollback，source failure 为明确 503，未触发 ACK/read_done 或写入。focused tests 覆盖这些边界（`test_quality_trace_api.py:363-411`）。

PASS。当前实现只声称 station-scoped Quality 与受限 accepted-fact Trace；没有 numeric Performance、Availability、station CT、ideal CT 或 Full OEE claim。`PARTIAL`/`UNKNOWN`/`UNAVAILABLE` 保持与 G0/G1 contract 一致，未扩大 MVP 或引入 DB migration。

## 6. 结论、blockers、recommendations 与 next gate

- Blockers = `0`
- Recommendations = `0`
- MVP path = `MVP-ALIGNED`
- 结论 = `PASS`
- 唯一 next gate：Parent Shadow Mainline PM independent intake；Data Quality PASS 不自动接受后续 Gate。Parent 若独立 intake 本报告与同一 candidate identities 后，可另行发布一个 exact `P1-G2-V` focused Verification task。

Recommendations classification：none；未把未来 source、历史 config registry、Full Genealogy、OEE、retention、audit/forensic framework 或 live deployment evidence 引入当前 Gate。

## 7. State distinctions 与 action audit

本报告的 `WRITTEN` 只表示 exact durable report 已写入；`REVIEWED` 表示本 Thread 已完成 local/static/fake-DB review；`PARENT_PM_INTAKE_REQUIRED=YES`。本 Thread 不宣称 `ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`RUNTIME_LOADED` 或 `PRODUCTION_ACCEPTED`。

```text
REPORT_WRITES = 1
PRODUCT_SOURCE_MUTATIONS = 0
TEST_SOURCE_MUTATIONS = 0
CONTRACT_MUTATIONS = 0
MAIN_PY_MUTATIONS = 0
AMENDMENT_MUTATIONS = 0
LEDGER_MUTATIONS_BY_CHILD = 0
VENV_MUTATIONS = 0
PACKAGE_OR_PIP_MUTATIONS = 0
NETWORK = 0
DB_API_LIVE_RUNTIME = 0
DOCKER_COMPOSE = 0
SSH_REMOTE = 0
PLC_VPLC = 0
PRODUCTION_STIMULUS = 0
GIT_STAGE_COMMIT_PUSH_TAG = 0
NESTED_SUB_AGENTS = 0
PRODUCT_REPAIR_GATE_DELTA = +0
CONTROL_PLANE_RECOVERY_GATE_DELTA = +0
TOTAL_DISPATCHED_GATE_DELTA = +1
```

Explicit boundary block：

```text
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
TIME_PROXIMITY_TRACE_FILL = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
FULL_GENEALOGY_CLAIM = NO
FULL_OEE_NUMERIC_CLAIM = NO
DB_MIGRATION = 0
```

Required terminal block：

```text
G2_DQ_TASK_SELF_IDENTITY_PASS = YES
G2_DQ_CANDIDATE_IDENTITIES_PRESERVED = YES
G2_DQ_G1_CONTRACT_IDENTITY_PRESERVED = YES
G2_DQ_AMENDMENT_IDENTITY_PRESERVED = YES
G2_DQ_PREDECESSOR_RELIABILITY_IDENTITY_PRESERVED = YES
G2_DQ_PROJECT_TEST_RUNTIME = PASS
G2_DQ_IMPORT_COMPILE_SMOKE = PASS
G2_DQ_FOCUSED_PYTEST_STARTS = 1
G2_DQ_FOCUSED_TEST = PASS
G2_DQ_BLOCKERS = 0
G2_DQ_RECOMMENDATIONS = 0
G2_DQ_PRODUCT_SOURCE_MUTATIONS = 0
G2_DQ_TEST_SOURCE_MUTATIONS = 0
G2_DQ_CONTRACT_MAIN_AMENDMENT_LEDGER_MUTATIONS = 0
G2_DQ_VENV_PACKAGE_NETWORK_DB_DOCKER_REMOTE_PLC_ACTIONS = 0
G2_DQ_GIT_MUTATIONS = 0
G2_DQ_P1_G3_EXECUTION = 0
G2_DQ_CHILD_TERMINAL = PASS / P1_G2_DQ_FOCUSED_DATA_QUALITY_REVIEW_COMPLETE
PARENT_PM_INTAKE_REQUIRED = YES
```

Thread output/context assessment：本 Thread 使用 `no / none` sub-agent scope，实际 nested sub-agents = 0；只产生本 exact report。该结果是对 exact candidate 的独立 local/static/fake-DB Data Quality evidence，不继承 Reliability acceptance，也不向 parent、Verification、G3、Git、DB、remote、runtime 或 production actions 传递隐含 authority。
