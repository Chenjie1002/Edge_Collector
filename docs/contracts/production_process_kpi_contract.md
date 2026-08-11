# P1 Process KPI + OEE Data-Sufficiency Contract

状态：`WRITTEN / PARENT_INDEPENDENT_G3_INTAKE_REQUIRED`

Contract version：`P1-G3-PROCESS-KPI-1.0`

本文件是 `docs/contracts/production_metrics_contract.md` 的 additive G3 contract candidate。它只冻结 Process KPI/OEE data-sufficiency 语义与 G4 的 exact read-only DTO 边界，不改变 predecessor Quality + Trace contract，不实现 API、DB、历史配置 registry、Performance、Availability 或 Full OEE。

## 1. 目的、范围与不可继承边界

本 contract 的产品原则是：能算的必须算对；不能算的必须明确说不能算；不得为了 Dashboard 完整度制造业务真值。

本版本的 scope 是一个声明的 `line_id + station_id` 站点边界与 bounded half-open 时间窗口 `[from, to)`。`line_id` 仅用于 accepted-fact 分区与查询约束，不代表本 contract 已接受 line-level output authority。Contract 不提供未声明 station scope 的全线聚合，也不解析或固定任何 terminal，包括 `WS03`。

必须保持的 flags：

```text
production_accepted_station_event_fact = sole accepted production truth source
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
TIME_PROXIMITY_CYCLE_PAIRING = NO
ADJACENT_ROW_CYCLE_PAIRING = NO
COUNTER_ONLY_CYCLE_PAIRING = NO
CURRENT_YAML_AS_HISTORICAL_AUTHORITY = NO
FULL_OEE_NUMERIC_CLAIM = NO
```

本文件不继承 predecessor 的实现权限、parent Ledger、未来 G4 task 或任何 runtime/remote authority。写入本文件只表示 `WRITTEN`，不表示 `ACCEPTED`、`VERIFIED`、`G4_READY`、deployed、activated 或 production acceptance。

## 2. Sole production authority、lineage 与证据边界

### 2.1 Accepted fact predicate

所有 numeric output 和 accepted-result fact output 只能来自 `production_accepted_station_event_fact`。一个 station accepted-result event 必须同时满足：

1. source row 已位于该 accepted production fact relation；
2. `event_type = 'station_result'`；
3. `line_id`、`station_id` 与请求 scope 精确相等；
4. `event_ts >= from AND event_ts < to`；
5. `fact_key` 非 null，且 selected scope/window 内每个 `fact_key` 恰好对应一行；
6. `production_result` 为 accepted contract 允许值 `ok`、`nok`、`skip` 或 `not_applicable`。

`skip` 与 `not_applicable` 仍是 accepted station-result events，因此进入 `accepted_event_count`；它们不进入 predecessor Quality 的 good/NOK denominator。未知 `production_result`、缺失 `fact_key` 或违反 source identity precondition 时，相关 numeric metrics 必须 fail closed 为 `UNAVAILABLE`，不得静默过滤后继续计算。

### 2.2 Deterministic identity and duplicate/conflict behavior

`fact_key` 是 accepted row 的唯一 deterministic identity；它不是由 `unit_id`、DMC、`cycle_counter`、相邻 row 或时间接近关系推导。稳定排序沿用 predecessor accepted event semantics：

```text
(event_ts ASC, accepted_at ASC, fact_key ASC)
```

实现必须先检查 selected accepted facts 的 identity integrity，再计数：

- 同一个 `fact_key` 出现两行，即使两行内容看似相同，也不得 `DISTINCT` 去重、last-write-wins 或任选一行；`accepted_event_count`、observed rate、Quality counts/rate 等受影响 numeric metric 返回 `UNAVAILABLE`，reason 为 `FACT_IDENTITY_DUPLICATE_OR_CONFLICT`，不带 `value`。
- 同一个 `fact_key` 对应不同 `content_fingerprint`、业务字段或 source identity，属于 conflict，同样 fail closed；不得用 `content_fingerprint` 选择“较新”版本。
- `fact_key` 缺失属于 `FACT_IDENTITY_MISSING`，不得用 `source_event_id`、`cycle_counter`、`unit_id`、DMC 或 row position 补 identity。
- 不同 `fact_key` 不得仅因时间相邻而合并；只有 source 已接受的 identity 才能定义一条 fact。任何无法确定是否为同一业务事实的 duplicate/conflict 都不得产生 numeric claim。

raw payload、raw hex、normalized candidate、adapter disposition/reason、decoder/collector diagnostics、ACK/read_done 和 legacy projection 不是 production fact，也不得作为 numeric source、join key、fallback 或 reason 的业务真值。Contract examples 是静态 DTO 形状示例，不是 synthetic production observation。

### 2.3 Historical config/hash lineage

config-dependent 语义必须逐行绑定 accepted fact 的 exact `(config_hash, config_version)`，并由独立 accepted historical immutable config/profile authority 解析到同一版本。当前 YAML、当前 default、simulation timing、`docs/kpi_definitions.md` 中的常数或 query window duration 均不能替代 historical binding。

窗口出现多个 `(config_hash, config_version)`、缺少该 tuple、tuple 无法解析或解析结果冲突时：

- `accepted_event_count`、accepted Quality counts、Quality rate 与 observed calendar-window event rate 仍可按 station fact authority 逐 metric 表达，因为它们不需要把多个 config 聚合成一个 ideal CT；
- terminal/order/line output、ideal CT、Performance、Availability 和 Full OEE 不得跨 mixed-config window 聚合为单一 numeric value；对应 metric 使用 `PARTIAL`、`UNAVAILABLE` 或 `UNSUPPORTED` 及稳定 reason；
- 不得选当前 YAML 或任意一个 config 作为代表，不得固定 `WS03`。

## 3. Counting unit 与 metric semantics

### 3.1 Counting-unit enum

`counting_unit` 是每个 metric 的必填字段，且只能是：

```text
event-count  = accepted station-result fact rows，按唯一 fact_key 一行一事件计数
unit-count   = unit identity 的计数；本版本没有被接受的 station-result 到 unit 的一对一 authority
unavailable  = 该 metric 不是当前可声明的 count，或所需 counting authority 不可用
```

`count(DISTINCT unit_id)`、`count(DISTINCT dmc)`、相邻 row、counter-only、legacy object count 和 fixed station count 都不能产生 `unit-count`。本版本的 `accepted_unit_count` 固定禁止 numeric output；`accepted_event_count` 不得改名为 unit count。

### 3.2 Metric decision matrix

下表是 G4 必须逐字消费的 current-v1 metric matrix。`正常状态`指 accepted-fact query 成功且 identity integrity 通过；具体的 empty/mixed/source-unavailable 行为按表后规则执行。

| metric name | unit | counting_unit | sole source / required lineage | 正常状态 | reason | numeric value | empty/source unavailable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `accepted_event_count` | `events` | `event-count` | accepted `station_result` facts；`fact_key` unique | `SUPPORTED` | `ACCEPTED_FACT_QUERY_OK` | 允许，按 fact rows 计数 | 合法 empty 为 `0`；source unavailable 或 identity defect 为 `UNAVAILABLE`，无 value |
| `observed_accepted_event_rate` | `events_per_second` | `event-count` | `accepted_event_count` 与 calendar window duration | `SUPPORTED` | `CALENDAR_WINDOW_EVENT_RATE` | 允许，`accepted_event_count / duration_seconds` | 合法 empty 为 `0 / duration_seconds = 0`；绝不表示 Performance/operating time；source unavailable 无 value |
| `accepted_unit_count` | `units` | `unit-count` | 需要 accepted 一对一 unit authority；当前不存在 | `UNSUPPORTED` | `UNIT_COUNTING_AUTHORITY_NOT_ACCEPTED` | 禁止 | 不得因 empty 返回 zero；source unavailable 仍无 value |
| `quality_good_event_count` | `events` | `event-count` | predecessor Quality：accepted `station_result` 且 `production_result='ok'` | `SUPPORTED` | `QUALITY_PREDECESSOR_SEMANTICS` | 允许 | 合法 empty 为 `0`；source unavailable 无 value |
| `quality_nok_event_count` | `events` | `event-count` | predecessor Quality：accepted `station_result` 且 `production_result='nok'` | `SUPPORTED` | `QUALITY_PREDECESSOR_SEMANTICS` | 允许 | 合法 empty 为 `0`；source unavailable 无 value |
| `quality_denominator_event_count` | `events` | `event-count` | predecessor Quality：`ok` 或 `nok`；`skip`/`not_applicable` 排除 | `SUPPORTED` | `QUALITY_PREDECESSOR_SEMANTICS` | 允许 | 合法 empty 为 `0`；source unavailable 无 value |
| `quality_rate` | `ratio` | `unavailable` | predecessor Quality：`good_count / denominator` | `SUPPORTED` 或 `PARTIAL` | `QUALITY_PREDECESSOR_SEMANTICS` 或 `QUALITY_NOK_DETAIL_INCOMPLETE` | `denominator > 0` 时允许；`PARTIAL` 仅表示 NOK detail/distribution 不完整，不得声称 detail 完整 | denominator 为 0 时 `UNAVAILABLE`/`QUALITY_DENOMINATOR_EMPTY`，无 value；source unavailable 无 value |
| `station_cycle_time` | `seconds` | `unavailable` | producer-authoritative cycle-instance start/complete pairing key | `PARTIAL` | `CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING` | 禁止 | empty 不得返回 zero；source/authority unavailable 无 value |
| `ideal_cycle_time` | `seconds` | `unavailable` | exact historical `(config_hash, config_version, profile)` binding | `PARTIAL` | `HISTORICAL_CONFIG_AUTHORITY_MISSING` | 禁止 | mixed/empty 不得返回 zero；current YAML 不得替代 |
| `line_accepted_event_count` | `events` | `unavailable` | accepted line-output authority；当前未接受 | `UNSUPPORTED` | `LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED` | 禁止；station query 不得暗含 line aggregate | 不得返回 zero；source unavailable 无 value |
| `terminal_accepted_event_count` | `events` | `unavailable` | exact historical terminal lineage；当前未接受 | `UNSUPPORTED` | `HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE` | 禁止；不得固定 WS03 | 不得返回 zero；source unavailable 无 value |
| `performance` | `ratio` | `unavailable` | independently accepted ideal CT + authoritative operating/run-time denominator | `UNSUPPORTED` | `PERFORMANCE_AUTHORITIES_NOT_ACCEPTED` | 禁止；observed calendar rate 不得改名 | 不得返回 zero |
| `availability` | `ratio` | `unavailable` | planned production time + planned downtime + authoritative run/stop/unknown timeline | `UNSUPPORTED` | `AVAILABILITY_AUTHORITIES_NOT_ACCEPTED` | 禁止；query duration 不得代替 operating/planned time | 不得返回 zero |
| `full_oee` | `ratio` | `unavailable` | Quality、Performance、Availability required authorities independently accepted | `UNSUPPORTED` | `FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED` | 禁止；`A × P × Q` 不得拼接 partial/unsupported component | 不得返回 zero |

### 3.3 Quality component reuse

`quality_good_event_count`、`quality_nok_event_count`、`quality_denominator_event_count` 与 `quality_rate` 只复用 predecessor `production_metrics_contract.md` 的 accepted Quality semantics，不重新定义它：

- good 是 accepted `production_result='ok'`；NOK 是 accepted `production_result='nok'`；denominator 是二者之和；
- `skip` 与 `not_applicable` 不进入 Quality denominator；
- `quality_rate` 只有 denominator 大于零才有 numeric value；空 denominator 不是 `0%`；
- 缺失 accepted NOK detail 不回填 diagnostic/raw/legacy `quality_event`。Quality rate 可以在 detail 不完整但 good/NOK counts 与 denominator 足够时带 numeric value，并且必须是 `PARTIAL`；detail/distribution 不得被误报为完整。

## 4. CT、ideal CT、Performance、Availability 与 Full OEE 边界

### 4.1 Station CT

只有同一 producer-authoritative `cycle_instance_id`（或等价的 accepted shared pairing identity）同时绑定 start 与 complete，且 duplicate/missing/conflict 规则通过，才可形成 cycle duration。当前 accepted source 没有被接受的该 authority，因此 `station_cycle_time` 为 `PARTIAL` 且 `numeric_value_allowed=false`。禁止 adjacent-row、time-proximity、nearest event、counter-only、`cycle_counter` 单独配对以及 legacy `cycle_event.cycle_time_ms` fallback。

### 4.2 Ideal CT

ideal CT 必须绑定每个 accepted fact 的 historical exact `config_hash + config_version + profile`，并由 immutable historical authority 解析。当前 YAML 只能是 current auxiliary evidence，不是历史 authority；解析不到、mixed-config 或 profile 冲突时不出 numeric value。当前版本不实现 historical config registry，也不把任何 current YAML/default 值写进 response。

### 4.3 Performance

`Performance` 不是 `observed_accepted_event_rate` 的别名。只有同一 scope/window 内 independently accepted 的 historical ideal CT 与 producer-authoritative operating/run-time denominator 同时存在，才可能支持 Performance；缺任一项即 `UNSUPPORTED` 或更保守状态。自然 query-window duration 只能用于 observed calendar-window rate，不能成为 OEE denominator。

### 4.4 Availability

Availability 需要 planned production time、planned downtime 以及可解释 unknown 的 authoritative machine run/stop timeline。API window、Collector health、ACK/read_done、snapshot、raw sample、adapter diagnostics 与 current YAML 都不是替代 authority。缺任一项即 `UNSUPPORTED` 或更保守状态。

### 4.5 Full OEE

本版本固定 `FULL_OEE_NUMERIC_CLAIM = NO`。除非未来有独立 accepted authority 重新冻结 required components，并由新的 explicit owner task 变更本 contract，否则 `full_oee` 必须 `UNSUPPORTED`、无 value；不得把 Quality 的可用数值与不具备 authority 的 A/P 相乘。

## 5. Status、reason 与 source aggregation

### 5.1 Status enum

状态在 metric level 与 response top level 都使用以下枚举：

- `SUPPORTED`：声明的 scope/window 下，required authority、lineage、identity 与 counting 语义齐全；numeric value 或事实输出可被声明。
- `PARTIAL`：accepted facts 或 component 可展示/部分计算，但存在 lineage、pairing、detail、completeness 或 denominator 缺口；除本 contract 明确允许的 `quality_rate` 情形外，不得带 numeric value，更不得声称完整 metric。
- `UNAVAILABLE`：本次请求的 required source/query/authority resolution 或 source identity integrity 当前不可用；必须 fail closed，不带 numeric value。空 accepted window 的 event count/rate 是例外的合法 `SUPPORTED` zero，不属于 source unavailable。
- `UNSUPPORTED`：本版本没有建立该 metric 所需 authority，不能声称已支持；不得用 fallback、zero 或另一个 metric 变成 numeric result。

### 5.2 Metric DTO numeric rule

每个 metric 必须包含 `name`、`unit`、`counting_unit`、`status`、`reason`、`source` 与 `numeric_value_allowed`。只有 `numeric_value_allowed=true` 时才出现 numeric `value`；`value` 不得以 null、字符串、zero fallback 或隐式缺省形式代表失败结果。

允许带 value 的组合只有：

```text
SUPPORTED metric + authority/query/integrity sufficient
quality_rate with PARTIAL + denominator > 0 + only NOK detail/distribution incomplete
```

所有 `UNAVAILABLE`、`UNSUPPORTED`、`PARTIAL`（不属于上述 quality exception）的 metric 都不出现 `value`。

### 5.3 Top-level aggregation

合法请求且 accepted-fact query 成功时：

1. 所有 metric 都 `SUPPORTED` 时 top-level `status=SUPPORTED`；
2. 至少一个 metric 为 `SUPPORTED` 或明确允许 numeric 的 `PARTIAL`，且存在其他 `PARTIAL`/`UNSUPPORTED`/metric-level `UNAVAILABLE` 时，top-level `status=PARTIAL`；
3. 没有可用 metric，且至少一个 required source/query/identity integrity 为 unavailable 时，top-level `status=UNAVAILABLE`；
4. 所有 metric 都 `UNSUPPORTED` 且没有 source failure 时，top-level `status=UNSUPPORTED`。

当前 fixed metric set 因 P/A/OEE 与 line/terminal 未被接受，正常 station response 通常是 top-level `PARTIAL`；这不使 available accepted-event counts 变成 unavailable，也不使 unsupported metric 变成 numeric。

### 5.4 Stable reason taxonomy

`reason.code` 是 machine-readable stable code；`reason.detail` 只能解释该 code，不得改变 authority。G3 v1 至少冻结以下 codes：

```text
ACCEPTED_FACT_QUERY_OK
CALENDAR_WINDOW_EVENT_RATE
EMPTY_ACCEPTED_WINDOW
QUALITY_PREDECESSOR_SEMANTICS
QUALITY_NOK_DETAIL_INCOMPLETE
QUALITY_DENOMINATOR_EMPTY
UNIT_COUNTING_AUTHORITY_NOT_ACCEPTED
FACT_IDENTITY_MISSING
FACT_IDENTITY_DUPLICATE_OR_CONFLICT
CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING
HISTORICAL_CONFIG_AUTHORITY_MISSING
MIXED_HISTORICAL_CONFIG_WINDOW
LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED
HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE
PERFORMANCE_AUTHORITIES_NOT_ACCEPTED
AVAILABILITY_AUTHORITIES_NOT_ACCEPTED
FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED
ACCEPTED_FACT_SOURCE_UNAVAILABLE
ACCEPTED_FACT_QUERY_FAILED
AUTHORITY_RESOLUTION_FAILED
INVALID_REQUEST
METHOD_NOT_ALLOWED
BODY_NOT_ALLOWED
```

## 6. Empty、mixed-config、duplicate/conflict 与 source-unavailable

### 6.1 Valid empty window

当 window 合法、accepted-fact query 成功、identity integrity 通过且返回零 `station_result` facts 时，`accepted_event_count=0`、`observed_accepted_event_rate=0/duration_seconds`、三个 Quality count 为 numeric zero；Quality rate 为 `UNAVAILABLE` + `QUALITY_DENOMINATOR_EMPTY`，不带 value；`accepted_unit_count`、CT、ideal CT、line/terminal、P/A/OEE 仍按其 authority matrix 为 `UNSUPPORTED`/`PARTIAL`，绝不 zero fallback。空 window 与 source unavailable 必须由 HTTP/DTO status 明确分离。

### 6.2 Mixed-config window

response 的 `source.config_window_state` 必须为 `SINGLE_RESOLVED`、`MIXED` 或 `UNRESOLVED`。`MIXED` 表示 selected accepted rows 跨多个 historical config/hash tuples；它不阻挡 station event count、Quality 或 calendar rate，但阻挡任何需要单一 config/profile/terminal/ideal CT 的 numeric claim。对应 metric 的 reason 必须是 `MIXED_HISTORICAL_CONFIG_WINDOW` 或更具体的 accepted code，不得任取一个 config 合并。

### 6.3 Duplicate/conflict window

source query 成功不等于 numeric integrity 成功。检测到 missing/duplicate/conflicting `fact_key` 时，受影响 station count/rate/Quality metrics 必须 `UNAVAILABLE` 且无 value；不得以 zero、distinct、first/last、row order 或 legacy source 继续。unsupported metrics 仍保持 `UNSUPPORTED`，不能用该 status 掩盖 base-source identity defect。

### 6.4 Source unavailable

accepted fact DB/query failure、base source unavailable 或 required authority resolution failure 必须 fail closed：

- base accepted-fact query failure：HTTP `503`，top-level `status=UNAVAILABLE`，reason code 为 `ACCEPTED_FACT_SOURCE_UNAVAILABLE` 或 `ACCEPTED_FACT_QUERY_FAILED`，不得返回 HTTP 200 空结果；
- optional config/terminal/cycle authority resolution failure：HTTP `200` 的 metric-level `UNAVAILABLE`（或更保守 `PARTIAL`），reason 为 `AUTHORITY_RESOLUTION_FAILED`，不带 value；它不能伪装成 source success numeric；
- 任一 source-unavailable response 不得使用 legacy KPI/Trace、snapshot、cycle_event、station_event、production_unit、quality_event、raw sample、adapter diagnostic 或 zero fallback。

## 7. Exact G4 read-only endpoint

### 7.1 Request contract

唯一 endpoint：

```text
GET /api/v2/process-metrics
```

Required query parameters（每个恰好一次）：

```text
line_id=<non-empty text>
station_id=<non-empty text>
from=<RFC3339 timestamp with UTC offset or Z>
to=<RFC3339 timestamp with UTC offset or Z>
```

Validation：

- parseable timezone-aware RFC3339/UTC values，canonical response format 为 UTC `Z`；
- `from` inclusive、`to` exclusive，必须 `from < to`；
- maximum window 为 `31 days`（`duration_seconds <= 2678400`）；超过上限、naive timestamp、invalid timestamp、空 scope 或 `from >= to` 均 invalid；
- request body 必须为空；不得使用 POST、PUT、PATCH、DELETE；
- unknown/duplicate query parameter、`terminal_id`、`group_by`、`aggregate`、`metric`、`limit`、`scope=line`/`scope=terminal` 等均禁止；本 endpoint 不提供 line/terminal aggregation 或 caller-selected metric semantics；
- `line_id` 是 station fact partition filter，不是 line-level output authority；`station_id` 是 minimum production scope boundary；terminal 不能通过别名或固定值隐式解析。

invalid request 返回 HTTP `422`，method 不允许返回 HTTP `405`；两者都不能执行 accepted-fact query，也不能产生 numeric value。base source/query failure 返回 HTTP `503`。合法 empty/mixed/partial/unsupported metric response 使用 HTTP `200`，因为 DTO 会明确表示其 metric-level sufficiency；这不表示所有 metrics supported。

### 7.2 Success response DTO

HTTP `200` body 的 exact top-level shape：

```jsonc
{
  "contract_version": "P1-G3-PROCESS-KPI-1.0",
  "scope": {
    "line_id": "<request-line-id>",
    "station_id": "<request-station-id>",
    "aggregation": "station"
  },
  "window": {
    "from": "<canonical-utc-from>",
    "to": "<canonical-utc-to>",
    "interval": "[from,to)",
    "duration_seconds": "<positive-number>"
  },
  "status": "<SUPPORTED|PARTIAL|UNAVAILABLE|UNSUPPORTED>",
  "reason": {
    "code": "<stable-reason-code>",
    "detail": "<non-authoritative explanation>"
  },
  "source": {
    "authority": "production_accepted_station_event_fact",
    "identity": "fact_key",
    "config_window_state": "<SINGLE_RESOLVED|MIXED|UNRESOLVED>",
    "fallback": "none"
  },
  "metrics": [
    {
      "name": "<metric-name-from-fixed-matrix>",
      "unit": "<metric-unit>",
      "counting_unit": "<event-count|unit-count|unavailable>",
      "status": "<SUPPORTED|PARTIAL|UNAVAILABLE|UNSUPPORTED>",
      "reason": {
        "code": "<stable-reason-code>",
        "detail": "<non-authoritative explanation>"
      },
      "source": {
        "authority": "<accepted-authority-or-not-accepted>",
        "lineage": "<fact_key-or-required-unresolved-lineage>",
        "fallback": "none"
      },
      "numeric_value_allowed": "<true|false>",
      "value": "<number-only-when-numeric_value_allowed-is-true>"
    }
  ]
}
```

`value` 是 optional：`numeric_value_allowed=false` 时该 key 必须完全省略，而不是 `null`。`metrics` 必须覆盖第 3.2 节 fixed metric set；不得借由省略 unsupported metric 让 top-level 看起来 complete。`source.fallback` 固定为 `none`；任何 legacy/fixed-station/current-YAML substitution 都是 contract violation。

### 7.3 Error DTOs

Invalid request（HTTP `422`，body 不执行 query）：

```jsonc
{
  "contract_version": "P1-G3-PROCESS-KPI-1.0",
  "error": {
    "code": "INVALID_REQUEST",
    "detail": "<invalid parameter, duplicate parameter, forbidden scope or body>"
  },
  "numeric_value": "absent"
}
```

Base source unavailable（HTTP `503`，不得伪装为合法 empty）：

```jsonc
{
  "contract_version": "P1-G3-PROCESS-KPI-1.0",
  "scope": {
    "line_id": "<request-line-id>",
    "station_id": "<request-station-id>",
    "aggregation": "station"
  },
  "window": {
    "from": "<canonical-utc-from>",
    "to": "<canonical-utc-to>",
    "interval": "[from,to)",
    "duration_seconds": "<positive-number>"
  },
  "status": "UNAVAILABLE",
  "reason": {
    "code": "ACCEPTED_FACT_SOURCE_UNAVAILABLE",
    "detail": "<source/query failure>"
  },
  "source": {
    "authority": "production_accepted_station_event_fact",
    "identity": "fact_key",
    "config_window_state": "UNRESOLVED",
    "fallback": "none"
  },
  "metrics": []
}
```

`metrics=[]` 在这个 envelope 中只表示 503 source failure，不能与 HTTP 200 valid empty response 混淆；error body 不含任何 numeric `value`。

### 7.4 Contract-only case examples

以下是 DTO 形状示例，不是数据库观察、synthetic production evidence 或 acceptance evidence；`<...>` 仅是非字面占位符。

Supported accepted-event count（非 empty 的 numeric value 必须由 source-derived integer 替换）：

```jsonc
{
  "name": "accepted_event_count",
  "unit": "events",
  "counting_unit": "event-count",
  "status": "SUPPORTED",
  "reason": {"code": "ACCEPTED_FACT_QUERY_OK", "detail": "<source-derived>"},
  "source": {"authority": "production_accepted_station_event_fact", "lineage": "fact_key", "fallback": "none"},
  "numeric_value_allowed": true,
  "value": <source_derived_integer>
}
```

Valid empty window（`0` 是 contract rule，不是 production observation）：

```jsonc
{
  "status": "PARTIAL",
  "reason": {"code": "EMPTY_ACCEPTED_WINDOW", "detail": "<query succeeded; no accepted facts>"},
  "metrics": [
    {"name": "accepted_event_count", "unit": "events", "counting_unit": "event-count", "status": "SUPPORTED", "reason": {"code": "EMPTY_ACCEPTED_WINDOW", "detail": "<contract example>"}, "source": {"authority": "production_accepted_station_event_fact", "lineage": "fact_key", "fallback": "none"}, "numeric_value_allowed": true, "value": 0},
    {"name": "observed_accepted_event_rate", "unit": "events_per_second", "counting_unit": "event-count", "status": "SUPPORTED", "reason": {"code": "EMPTY_ACCEPTED_WINDOW", "detail": "<contract example>"}, "source": {"authority": "production_accepted_station_event_fact", "lineage": "fact_key+calendar_window", "fallback": "none"}, "numeric_value_allowed": true, "value": 0},
    {"name": "quality_rate", "unit": "ratio", "counting_unit": "unavailable", "status": "UNAVAILABLE", "reason": {"code": "QUALITY_DENOMINATOR_EMPTY", "detail": "<no ok/nok denominator>"}, "source": {"authority": "production_accepted_station_event_fact", "lineage": "fact_key", "fallback": "none"}, "numeric_value_allowed": false},
    {"name": "full_oee", "unit": "ratio", "counting_unit": "unavailable", "status": "UNSUPPORTED", "reason": {"code": "FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED", "detail": "<no zero fallback>"}, "source": {"authority": "not-accepted", "lineage": "required A/P authority unresolved", "fallback": "none"}, "numeric_value_allowed": false}
  ]
}
```

Unsupported OEE component（no numeric claim）：

```jsonc
{"name": "performance", "unit": "ratio", "counting_unit": "unavailable", "status": "UNSUPPORTED", "reason": {"code": "PERFORMANCE_AUTHORITIES_NOT_ACCEPTED", "detail": "<ideal CT and operating-time authority absent>"}, "source": {"authority": "not-accepted", "lineage": "historical ideal CT + authoritative operating/run-time", "fallback": "none"}, "numeric_value_allowed": false}
```

Mixed-config window（station count may remain numeric；config-dependent metric must not aggregate）：

```jsonc
{"source": {"authority": "production_accepted_station_event_fact", "identity": "fact_key", "config_window_state": "MIXED", "fallback": "none"}, "metrics": [{"name": "accepted_event_count", "status": "SUPPORTED", "reason": {"code": "ACCEPTED_FACT_QUERY_OK", "detail": "<config-independent count>"}, "numeric_value_allowed": true, "value": <source_derived_integer>}, {"name": "ideal_cycle_time", "status": "PARTIAL", "reason": {"code": "MIXED_HISTORICAL_CONFIG_WINDOW", "detail": "<no single ideal CT>"}, "numeric_value_allowed": false}]}
```

Source unavailable 必须使用上面的 HTTP `503` error DTO，不能把 `metrics=[]` 作为 HTTP `200` empty response，也不能返回任何 zero/value。

## 8. G4 implementation boundary and validation obligations

G4 later task 只能实现本 contract 的 exact endpoint/DTO，且必须保持：

- read-only `GET`；不注册或改变 predecessor `/api/v2/production/quality`、`/api/v2/production/trace` 的 meaning；
- 只读取 `production_accepted_station_event_fact`，不 join/fallback 任何 predecessor 禁止源；
- 先做 `fact_key` identity integrity，再做 count/Quality/rate；冲突不 dedupe；
- 不实现 historical config registry、P/A/full OEE numeric、line/terminal resolution 或 cycle pairing；这些是当前 sufficiency boundary，不是 G4 convenience feature；
- 把 `observed_accepted_event_rate` 保留为 calendar-window/event rate，不能命名为 `Performance`、`operating_rate`、`operating_time` 或 OEE denominator；
- 不把本文件、示例、静态检查或 local no-DB evidence 表述为 API runtime、DB-backed、remote、deployed、activated 或 production acceptance。

本 contract 与 predecessor 的边界：predecessor 继续拥有已接受 Quality + Trace semantics；本文件只增加 Process KPI/OEE metric names、sufficiency/status/reason、scope/window 与 bounded endpoint DTO。任何需要改变 predecessor authority、字段 meaning、Quality denominator 或 status meaning 的需求必须停止并返回 `HOLD / PREDECESSOR_ACCEPTED_CONTRACT_CHANGE_REQUIRES_OWNER_REVIEW`。
