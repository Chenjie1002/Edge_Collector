# Dashboard API Contract

更新时间：2026-07-05
状态：Phase-2 公共 API 合同；API consumer contract freeze planning
消费者：Next.js Dashboard、报告导出、受控第三方客户端

## 1. 原则

- API 是只读分析和追溯接口，不提供 PLC 控制命令。
- 不假设固定 WS01/WS02/WS03。
- 默认 `profile=normal`，跨 Profile 必须显式请求。
- 所有查询有界、分页、可取消。
- 每个指标返回口径版本和数据充分性。
- boot isolation、Profile isolation 和 config version 必须可审计。
- Raw payload 与普通 summary 使用不同权限。

## 2. 通用请求参数

| 参数 | 规则 |
| --- | --- |
| `line_id` | 必填；单线部署可由服务端注入明确默认值 |
| `plc_id` | 可选过滤 |
| `station_id` | 可重复或逗号分隔，最多 50 |
| `station_type` | 可选 |
| `profile` | 默认 `normal`；支持 fast/test/unknown/all |
| `start_time` / `end_time` | ISO-8601，必须有界 |
| `timezone` | 默认产线时区 |
| `cursor` | 列表分页 |
| `limit` | 默认 50，最大 500 |

默认时间窗 8 小时；同步最大 31 天。超过限制返回 `422 QUERY_WINDOW_TOO_LARGE`。

## 3. 通用响应 Envelope

```json
{
  "data": {},
  "meta": {
    "generated_at": "2026-06-19T14:00:00Z",
    "line_id": "LINE_001",
    "profile_scope": ["normal"],
    "time_window": {
      "start": "2026-06-19T00:00:00Z",
      "end": "2026-06-19T08:00:00Z",
      "timezone": "Asia/Shanghai"
    },
    "config_version": "2026.06.19.1",
    "config_hash": "sha256:...",
    "metric_version": "oee-v1",
    "data_completeness": "COMPLETE",
    "warnings": []
  },
  "page": {
    "next_cursor": null,
    "limit": 50
  }
}
```

通用响应 Envelope 是默认结构。当某个 endpoint 的专属合同明确声明 exact
response envelope 时，endpoint-specific exact envelope 优先于通用 Envelope。
通用 Envelope 继续是其他未声明专属 exact response envelope 的 endpoint 的默认合同。

`data_completeness`：

- `COMPLETE`
- `PARTIAL_MISSING_SCHEDULE`
- `PARTIAL_MISSING_STATE`
- `PARTIAL_GAP`
- `MIXED_PROFILE`
- `STALE`
- `UNKNOWN`

## 4. Line Configuration API

### `GET /api/v2/lines`

返回已发布产线摘要，不包含凭据或 PLC 密码。

### `GET /api/v2/lines/{line_id}/configuration`

返回 resolved topology：

```json
{
  "line_id": "LINE_001",
  "enabled": true,
  "plcs": [{"plc_id": "PLC_001", "station_count": 10}],
  "stations": [{
    "station_id": "WS01",
    "station_order": 10,
    "station_type": "ASSEMBLY",
    "station_enabled": true,
    "plc_id": "PLC_001"
  }],
  "buffers": []
}
```

不返回 host credentials、secret、write addresses 的敏感细节。

## 5. Production Accepted Fact Read API

本节冻结 API consumer contract，作为后续 Reliability、Data Quality 和
Verification review 的合同基础。它不声明新的 implementation 已完成，也不授权
FastAPI/API implementation、Dashboard/frontend implementation、tests、DB
execution、migration/schema、Collector/runtime/storage.py、V-PLC、Docker/deploy、
stage、commit、push、tag、rollback 或 real PLC pilot。

### `GET /api/v2/production/accepted-station-events`

用途：返回 accepted station-event business facts / production accepted fact
list/read。该 endpoint 不是 Dashboard summary、Quality summary、Pareto input、
debug/review diagnostics view 或 legacy trace/event 等价接口。

#### Endpoint-specific exact response envelope

本 endpoint 是通用响应 Envelope 的 endpoint-specific exception。成功响应外层
exact keys 必须且只能为 `data`、`page`；二者均为 required。该 endpoint 不继承通用
Envelope 的 `meta`，`meta` 对本 endpoint 为 unsupported。

冻结的 exact response shape：

```text
outer envelope exact keys (required):
- data
- page

data exact keys (required):
- items

page exact keys (required):
- next_cursor
- limit
```

任何其他 envelope/data/page-level key 均为 unsupported。unsupported key 不得被
consumer 静默剥离、忽略、重命名或解释为兼容字段。`data.items[]` 的 exact keys
继续由下文 Response DTO allowlist 定义，不得扩大。下文示例 envelope 仍是本 endpoint
的规范性 accepted shape；本澄清匹配当前 API route，不要求 API response change。

Consumer semantics：shape 合法的 2xx response 正常解析。包含 unsupported
envelope/data/page/item key 的 2xx response 是 malformed successful response；consumer
parser 必须 fail closed，并保持 Dashboard client classification 为 `kind: "error"`。
不得将该 malformed 2xx response 映射为 `invalid-query` 或 `unavailable`。既有
pre-request validation → `invalid-query`、API 4xx → `invalid-query`、API 503 →
`unavailable` 的分类不变。

必须保留的 production-fact visibility boundary：

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.

Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.

raw_payload/raw_hex is evidence, not a production fact.

Decoded/source normalized payloads remain candidates until accepted.

Non-accepted dispositions do not write defect detail.

NOK/detail visibility must bind to accepted upstream business evidence.

Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

#### Source boundary

唯一 consumer-facing production fact source：

- `production_accepted_station_event_fact`

禁止把以下表或 surface 作为 equivalent production fact source、fallback source、
legacy compatibility source 或 join-derived field filler：

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

API consumers must not join diagnostic/raw/candidate tables to synthesize
`production_result`, NOK/detail, Quality/Pareto or Dashboard facts. Missing
accepted fact fields must remain missing, unknown or error according to the
response/error contract; they must not be filled from legacy/current/raw or
diagnostic sources.

#### Response DTO allowlist

`data.items[]` 只允许返回下表字段。每个字段必须直接绑定到
`production_accepted_station_event_fact` row field，fallback 均为 forbidden。

| Field | Source | Consumer meaning | Fallback |
| --- | --- | --- | --- |
| `line_id` | `production_accepted_station_event_fact.line_id` | line scope | forbidden |
| `plc_id` | `production_accepted_station_event_fact.plc_id` | PLC scope | forbidden |
| `station_id` | `production_accepted_station_event_fact.station_id` | station scope | forbidden |
| `station_type` | `production_accepted_station_event_fact.station_type` | station class | forbidden |
| `profile_id` | `production_accepted_station_event_fact.profile_id` | profile scope | forbidden |
| `config_hash` | `production_accepted_station_event_fact.config_hash` | historical config authority | forbidden |
| `config_version` | `production_accepted_station_event_fact.config_version` | config lineage label | forbidden |
| `event_type` | `production_accepted_station_event_fact.event_type` | accepted station-event kind | forbidden |
| `production_result` | `production_accepted_station_event_fact.production_result` | accepted result for `station_result` only | forbidden |
| `unit_id` | `production_accepted_station_event_fact.unit_id` | unit trace key when present on accepted fact row | forbidden |
| `dmc` | `production_accepted_station_event_fact.dmc` | DMC trace key when present on accepted fact row | forbidden |
| `cycle_counter` | `production_accepted_station_event_fact.cycle_counter` | source cycle counter | forbidden |
| `source_event_id` | `production_accepted_station_event_fact.source_event_id` | stable source event identity | forbidden |
| `event_ts` | `production_accepted_station_event_fact.event_ts` | source event time | forbidden |
| `accepted_at` | `production_accepted_station_event_fact.accepted_at` | accepted fact timestamp only; not collector freshness, ACK time, station freshness or read_done time | forbidden |
| `fact_key` | `production_accepted_station_event_fact.fact_key` | immutable production fact identity/reference | forbidden |
| `content_fingerprint` | `production_accepted_station_event_fact.content_fingerprint` | immutable content identity/reference | forbidden |
| `nok_code` | `production_accepted_station_event_fact.nok_code` | accepted NOK code only | forbidden |
| `nok_origin` | `production_accepted_station_event_fact.nok_origin` | accepted NOK origin only | forbidden |
| `nok_detail_code` | `production_accepted_station_event_fact.nok_detail_code` | accepted detail code only | forbidden |
| `nok_detail_source_event_id` | `production_accepted_station_event_fact.nok_detail_source_event_id` | detail source evidence identity | forbidden |
| `nok_detail_evidence_fact_key` | `production_accepted_station_event_fact.nok_detail_evidence_fact_key` | accepted upstream evidence fact reference | forbidden |

#### Item required-key and null semantics

`data.items[]` 的每个元素必须是 JSON object，其 own JSON key 集合必须与上表
Response DTO allowlist 完全相等。上表全部 22 个字段均为 required key：

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

required key presence != non-null value。required 仅表示该 key 必须存在；不改变
任何现有业务字段的 nullable 规则。允许业务值为空的字段仍必须以完整 key 和显式
JSON `null` 返回；不得以省略 key 表示空值、unknown 或 not applicable。missing key
与 explicit `null` 不等价。

缺失任意一个 required item key 的 2xx response 是 malformed successful response。
consumer parser 必须 fail closed：不得使用 `?? null`、默认值、兼容映射或任何其他
normalization 将 missing field 变为合法 item；不得从其他 table、endpoint、cache、
diagnostic、legacy、raw 或 current source 补齐。该 malformed 2xx 必须保持 Dashboard
client classification 为 `kind: "error"`，不得映射为空 `items`、`invalid-query` 或
`unavailable`。

allowlist 外的任意 item key 同样为 unsupported；unknown key 与 missing required key
均使整个 response 失败。parser 不得返回 partial item 或 partial envelope，也不得从
unsupported container 中 salvage accepted-looking field。

当前 API route 的 `_format_row()` 已按 `DTO_FIELDS` 对每个 item 建立完整 22-key
object，数据库 nullable value / Python `None` 通过完整 key 加 JSON `null` 表示。该
合同澄清不要求 API producer、query、cursor、pagination 或 status 修改；不改变
production authority、DTO field list、NOK/detail、config lineage、identity 或
`accepted_at` 语义，也不授权 frontend implementation。

示例 envelope：

```json
{
  "data": {
    "items": [{
      "line_id": "LINE_001",
      "plc_id": "PLC_001",
      "station_id": "WS01",
      "station_type": "ASSEMBLY",
      "profile_id": "normal",
      "config_hash": "sha256:...",
      "config_version": "2026.07.05.1",
      "event_type": "station_result",
      "production_result": "ok",
      "unit_id": "U-001",
      "dmc": "DMC-001",
      "cycle_counter": 301,
      "source_event_id": "PLC_001:WS01:301",
      "event_ts": "2026-07-05T10:00:00Z",
      "accepted_at": "2026-07-05T10:00:01Z",
      "fact_key": "sha256:...",
      "content_fingerprint": "sha256:...",
      "nok_code": null,
      "nok_origin": null,
      "nok_detail_code": null,
      "nok_detail_source_event_id": null,
      "nok_detail_evidence_fact_key": null
    }]
  },
  "page": {
    "next_cursor": null,
    "limit": 50
  }
}
```

#### Forbidden DTO / source leakage

Response DTO、cursor payload、meta/debug payload、Dashboard production consumer
payload 和 implementation helper output 均不得暴露、派生或使用以下字段/语义：

- raw payload, `raw_payload`, `raw_hex`, `raw_sample_id` or raw bytes;
- decoded/source normalized candidate payloads before accepted decision;
- adapter disposition, reason, phase or candidate context;
- raw/normalized comparison context;
- decoder errors;
- diagnostic/review/audit payloads;
- `ack_status`, `read_done`, `collector_state`;
- `quality_pareto_input`, `dashboard_state`;
- ambiguous production-looking keys: bare `result`, `defect`, `quality`,
  `pareto`;
- any legacy/current table join that fills missing accepted fact fields;
- any synthetic field that makes non-accepted dispositions visible as
  production facts.

#### Query / filter / sort / page contract

- Required scope: request must include `line_id`, or the service must inject an
  explicit single-line default. Implicit cross-line reads are forbidden.
- Required time range: `start_time` and `end_time` must be present, bounded and
  parsed as strict timezone-aware ISO-8601.
- Maximum time window: 31 days unless a later contract changes the limit.
- Pagination: `limit` default 50, max 500.
- Invalid `limit`, invalid filter, invalid time, missing/unbounded window or
  over-large window must fail closed with 4xx, not fallback to a wider query.
- Cursor must be tamper-resistant, schema/version checked and bound to line,
  time range, accepted-fact filters, limit, direction and ordering tuple.
- Invalid, mismatched, stale-version or cross-scope cursor must fail closed with
  4xx.
- Stable order: `event_ts ASC`, `accepted_at ASC`, `fact_key ASC`.
- Eligible future filters must be sourced only from accepted fact table fields:
  `station_id`, `station_type`, `event_type`, `production_result`,
  `config_hash`, `unit_id`, `dmc`, `cycle_counter`, `source_event_id`,
  `fact_key`, `content_fingerprint`, `nok_code`, `nok_origin`,
  `nok_detail_code`, `nok_detail_source_event_id` and
  `nok_detail_evidence_fact_key`.
- Excluded until a later schema/contract authority gate: `work_order`,
  `product`, raw evidence filters, diagnostic reason filters,
  candidate-state filters and legacy/current table fields.

#### Reliability contract requirements

Future implementation must satisfy these requirements before review:

- use read-only DB transaction or equivalent read-only query semantics;
- set and document statement timeout plus idle/read timeout expectation;
- protect bounded queries and large-query behavior through required scope, time
  range, limit, cursor binding and max window checks;
- define DB unavailable, missing table, missing schema or missing authority
  behavior as explicit error, empty or unknown response;
- explicitly prohibit fallback to legacy/raw/current/diagnostic sources for DB
  unavailable, missing table, missing schema or missing authority cases;
- never execute `INSERT`, `UPDATE`, `DELETE` or write-side helper calls;
- perform no ACK/read_done mutation;
- perform no Collector, PLC, V-PLC, runtime, storage or Dashboard side effect;
- treat `fact_key`, `content_fingerprint` and `source_event_id` as
  reference/identity only, not mutation authority.

#### Dashboard consumer field matrix

Dashboard production surfaces must consume accepted fact API fields only unless
a future debug/review gate explicitly authorizes a separate diagnostic surface.

| Page / component | Allowed accepted fact fields | Forbidden fields/sources | Empty/error/unknown state |
| --- | --- | --- | --- |
| Line overview | aggregated `event_type`, `production_result`, `event_ts`, `accepted_at`, `line_id`, `plc_id`, `station_id`, `station_type`, `profile_id`, `config_hash`, counts from accepted facts | raw/diagnostic/candidate fields, legacy/current summaries, `quality_pareto_input`, `dashboard_state`, OEE denominator synthesis | OEE, schedule or runtime denominator gaps must display incomplete/unknown/null with reason; must not fabricate missing denominator values or fill zero as truth |
| Station status | `station_id`, `station_type`, latest accepted `event_ts`, latest accepted `production_result`, `config_hash`, `config_version`, `profile_id`, `accepted_at` as accepted fact timestamp | `accepted_at` as collector freshness/ACK/station freshness/read_done time, `collector_state`, `ack_status`, `read_done`, raw/debug fields | No accepted fact means unknown/no accepted event; DB/schema/source errors show error or unknown, not stale collector health |
| Accepted result trend | `event_ts`, `accepted_at`, `station_id`, `station_type`, `profile_id`, `config_hash`, `event_type`, `production_result`, accepted fact counts | fallback to `quality_event`, `production_snapshot`, `production_events`, `station_event`, raw/candidate/diagnostic sources | Empty bucket means no accepted facts in bounded scope; incomplete data is partial/unknown, not fabricated trend |
| NOK/detail visibility | `production_result`, `nok_code`, `nok_origin`, `nok_detail_code`, `nok_detail_source_event_id`, `nok_detail_evidence_fact_key`, `fact_key`, `source_event_id` | adapter reason code, raw mismatch, decoder error, non-accepted disposition, `quality_pareto_input`, bare `defect`/`quality`/`pareto` keys | Missing NOK/detail accepted evidence means absent/unknown detail; must not synthesize detail from diagnostics |
| Traceability drilldown | `unit_id`, `dmc`, `cycle_counter`, `source_event_id`, `event_ts`, `accepted_at`, `fact_key`, `content_fingerprint`, line/PLC/station/profile/config fields | raw bytes, raw hex, candidate payload, diagnostic context, legacy event filler, `work_order`, `product` until later authority gate | Missing unit/DMC fields remain missing; trace gaps show unknown/partial with reason, not legacy-fill |

`accepted_at` must not be displayed as collector freshness, ACK time, station
freshness or read_done time on any Dashboard component.

#### Optional debug/review diagnostics view

Debug/review diagnostics view is explicitly deferred. It must be:

- a separate Level 2 gate;
- separate from production Dashboard surfaces;
- scoped to diagnostic/audit/review namespaces;
- reviewed with leakage-negative assertions before implementation;
- unable to become OEE, traceability main fact, NOK/detail authority,
  Quality/Pareto input, Dashboard production state or ACK/read_done authority.

This contract freeze does not authorize debug/review diagnostics
implementation.

#### Future review checklist

Reliability review must cover:

- read-only transaction or read-only query semantics;
- statement timeout and idle/read timeout;
- bounded queries and large-query protection;
- no ACK/read_done mutation and no Collector/PLC/V-PLC/runtime side effect;
- DB unavailable, missing table, missing schema and missing authority behavior.

Data Quality review must cover:

- field authority for every DTO field;
- NOK/detail evidence binding to accepted upstream business evidence;
- forbidden fallback from legacy/raw/current/diagnostic sources;
- diagnostic/raw/candidate leakage into production facts, OEE, traceability,
  Quality/Pareto and Dashboard surfaces.

Verification review must cover:

- DTO allowlist and forbidden field/source negative matrix;
- invalid filter, invalid cursor, invalid limit, invalid time and unbounded
  window cases;
- stable ordering and cursor binding to line/time/filter/limit/direction/order;
- Dashboard component field matrix and empty/error/unknown state matrix;
- no side-effect and excluded-surface audit for API implementation, Dashboard,
  Collector/runtime/storage.py, migration/schema, config, Docker/deploy, DB
  execution, stage, commit and push.

## 6. Dashboard Summary API

### `GET /api/v2/dashboard/summary`

返回：

- line status。
- OEE/A/P/Q。
- actual/target/delta。
- quality rate。
- active station / total station。
- Top loss。
- stale/gap/collector warning。

完整 OEE 数据不足时，OEE 为 `null`，并返回 partial reason，不能填 0。

## 7. OEE API

### `GET /api/v2/oee/summary`

支持 `group_by=line|station`。

### `GET /api/v2/oee/trend`

支持 `bucket=5m|15m|1h|shift|day`，最多 1000 点。

核心字段：

```json
{
  "scope_id": "WS01",
  "availability": 0.92,
  "performance": 0.88,
  "quality": 0.99,
  "oee": 0.8015,
  "good_count": 1200,
  "total_count": 1212,
  "planned_production_seconds": 28800,
  "run_seconds": 26496,
  "ideal_cycle_time_seconds": 20.0
}
```

## 8. Quality API

### `GET /api/v2/quality/summary`

返回 good/NOK/SKIPPED、FPY/pass rate、NOK rate。

### `GET /api/v2/quality/trend`

按 bucket 和 station/group 生成趋势。

### `GET /api/v2/quality/pareto`

返回 code、name、count、percentage、cumulative_percentage；支持 `top_n`，其余合并为
`OTHER`。

### `GET /api/v2/quality/stations`

工站质量排名，包含分母，禁止仅按 NOK 数排序而忽略产量。

## 9. Trace API

### `GET /api/v2/trace/search`

支持：

- `q`：UID/DMC/label/reject。
- `cycle_counter` + `station_id`。
- `nok_code`。
- station/time window。

### `GET /api/v2/trace/units/{unit_pk}`

返回 unit summary 和动态 timeline：

```json
{
  "unit_pk": "uuid",
  "unit_id": "U-...",
  "final_result": "NOK",
  "events": [{
    "event_id": "uuid",
    "station_id": "WS04",
    "station_order": 40,
    "station_type": "TEST",
    "result": "NOK",
    "process_status": "PROCESSED",
    "plc_boot_id": "uuid",
    "cycle_counter": 301,
    "event_time": "..."
  }]
}
```

### `GET /api/v2/trace/by-cycle`

请求至少包含：

```text
line_id + plc_id + station_id + cycle_counter
```

强烈建议带 `plc_boot_id`。未带时响应必须返回选中的 current boot 和选择依据。禁止跨 boot
匹配相同 counter。

### `GET /api/v2/trace/by-station`

按 station/time/result 分页返回事件。

### `GET /api/v2/trace/by-nok-code`

返回 quality event 和关联 unit/cycle。

## 10. Station Event API

### `GET /api/v2/stations`

返回动态 station list 和最后采集状态。

### `GET /api/v2/stations/{station_id}/events`

支持 result/process status/time/profile 过滤。

### `GET /api/v2/stations/{station_id}/metrics`

返回 throughput、CT p50/p95/p99、NOK rate、freshness 和 collector latency。

## 11. Raw Payload Drilldown

### `GET /api/v2/events/{event_id}/payload`

返回：

- decoded payload。
- schema id/version。
- raw sample reference。
- field validation warnings。
- config hash。

默认不返回原始 bytes；`include_raw=true` 需要工程权限，并限制响应大小。敏感字段根据
payload schema 的 classification 进行掩码。

## 12. Genealogy API 预留

### `GET /api/v2/units/{unit_pk}/genealogy`

仅返回有明确来源事件的关系。支持 parent/child 两个方向和最大深度，默认 3、最大 10。
禁止无限递归。

## 13. Hold / Rework API 预留

只读：

- `GET /api/v2/holds`
- `GET /api/v2/rework`

Phase-2 不提供 `POST /hold`、`POST /release` 或 PLC 控制接口。若未来需要操作员工作流，
必须建立独立安全合同，且不等同于直接控制设备。

## 14. 错误合同

```json
{
  "error": {
    "code": "QUERY_WINDOW_TOO_LARGE",
    "message": "Requested window exceeds 31 days",
    "details": {},
    "request_id": "..."
  }
}
```

稳定 code：

- `INVALID_FILTER`
- `QUERY_WINDOW_TOO_LARGE`
- `INVALID_CURSOR`
- `LINE_NOT_FOUND`
- `STATION_NOT_FOUND`
- `BOOT_REQUIRED`
- `AMBIGUOUS_CYCLE`
- `PAYLOAD_NOT_AVAILABLE`
- `METRIC_DATA_INCOMPLETE`
- `RATE_LIMITED`

## 15. 性能与保护

- summary p95 < 1 秒。
- Trace detail p95 < 2 秒。
- 列表默认 50、最大 500。
- 单次趋势最大 1000 点。
- SQL statement timeout。
- 每个 endpoint 定义允许的 sort/filter。
- 导出、大窗口和高基数查询走异步任务。
- 响应支持 ETag/config hash；缓存键必须包含 line/profile/time/filter/metric version。

## 16. 兼容策略

- 现有 `/trace/api`、`/trace/api/by-cycle` 在迁移期保留。
- `/api/v2` 为动态模型合同，不在旧响应里硬塞不兼容结构。
- 兼容 adapter 必须保留 Phase-1 counter/route_step 语义。
- 删除旧 endpoint 前需要 usage audit、deprecation header 和独立 release note。

## 17. 验收条件

- 3/10/20 工站响应不改变 schema。
- by-cycle 不跨 boot。
- normal 默认不混入 fast/test/unknown。
- OEE 数据不足返回 null + reason。
- 所有列表分页且时间窗有界。
- Raw payload 访问可审计、可限制、可掩码。
- API 无 PLC 控制动作。
