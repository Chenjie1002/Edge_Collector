# P1 Production Metrics Contract

状态：`G1_CONTRACT_CANDIDATE / WRITTEN / PM_INTAKE_REQUIRED`

## 1. 目的与范围

本合同只冻结 P1 Quality + accepted-fact Trace MVP 的 production semantics。它只允许消费已接受的 station-business facts，不实现产品代码、DB migration、历史配置 registry、Genealogy、Performance、Availability、Full OEE 或 runtime/remote validation。

最小范围是：station-scoped Quality、accepted station-event timeline、受限的 `unit_id`/DMC Trace，以及明确的数据充分性状态。所有查询都必须声明 line/station/identity scope 与 bounded half-open window `[start, end)`；时间窗口不得被解释为 planned production time 或 operating time。

## 2. 唯一生产事实 authority

`production_accepted_station_event_fact` 是 P1 accepted station-business facts 的唯一 `PRODUCTION_AUTHORITY`。它的 `event_type`、result、identity、timestamps、`fact_key`、`config_hash` 与 `config_version` 均以 accepted row 为准。

- `station_result` 的 `production_result` 是 OK/NOK/`skip`/`not_applicable` 的业务结果来源。
- accepted NOK code/detail 只能来自 accepted business evidence：`nok_code`/`nok_origin` 与 `station_nok` 的 detail evidence fields；detail 必须绑定 `nok_detail_evidence_fact_key` 及对应 source identity。
- raw payload/raw hex、normalized candidate、adapter disposition/reason、decoder/collector diagnostics、ACK/read_done、legacy projection 都不是生产事实。
- 新 P1 语义禁止读取、join 或 fallback 到 `production_snapshot`、`cycle_event`、`station_event`、`production_unit`、`quality_event` 或其它 legacy source 来补事实。

## 3. Quality 语义

Quality 只统计 bounded scope/window 内 accepted `event_type='station_result'` facts。

- `good_count` = `production_result='ok'` 的 accepted result facts。
- `nok_count` = `production_result='nok'` 的 accepted result facts。
- `denominator` = accepted result facts whose result is `ok` 或 `nok`；`skip` 与 `not_applicable` 不算 good、不算 NOK，也不进入 Quality denominator，除非未来独立 authority 明确改变该口径。
- `quality_rate` 只在 `denominator > 0` 时计算为 `good_count / denominator`；空 denominator 必须是 `PARTIAL` 或 `UNAVAILABLE`，不得写成数值零或 0%。
- station-scoped accepted-result Quality 为 `SUPPORTED`；line/terminal Quality 只有在历史 config lineage 精确解析 terminal 后才可用，否则为 `PARTIAL`/`UNAVAILABLE`，不得固定使用 WS03。
- accepted NOK detail 缺失时，Quality result 仍可保留，但 detail/distribution 必须显式 `PARTIAL` 或 `UNAVAILABLE`；不得用 diagnostic reason、raw comparison 或 legacy `quality_event` 补齐。

## 4. Accepted event timeline

Timeline 只展示 accepted event facts，允许的 event types 为 `station_cycle_start`、`station_cycle_complete`、`station_result`、`station_nok`。窗口为 `[start, end)`，即 `event_ts >= start AND event_ts < end`。

确定性顺序为：`(event_ts ASC, accepted_at ASC, fact_key ASC)`。`fact_key` 是最终 tie-breaker；分页、去重与重放必须绑定同一 scope/window/order。

同一 cycle 的 grouping 或 pairing 只有在 producer-authoritative shared identity 明确存在时才允许。相邻行、counter-only、时间接近、legacy event 或字段相似度都不构成共享 identity。

## 5. unit_id、DMC 与缺站

- 非 null accepted `unit_id` 查询只使用 accepted row 的 exact equality；非 null accepted DMC 查询同样只使用 accepted row 的 exact equality，并声明 line/station/window scope。
- null/missing `unit_id` 或 DMC 不得生成 synthetic identity，不得从 serial、`cycle_event`、`production_unit`、邻近时间或其它 legacy field 填补；该行对相应 identity query 为 `PARTIAL`。
- 未观察到某 station 不等于该 station 已通过、跳过或存在于 genealogy；Trace 必须显示 `missing/unknown` station 与数据充分性状态。
- 本合同只提供 identity-scoped accepted facts，不声称 parent/child、assembly、replacement、rework 或 full Genealogy。`FULL_GENEALOGY_CLAIM = NO`。

## 6. 历史 config lineage、terminal、order 与 line output

dynamic terminal、station order、line-level output 与 line-level Quality 都是 conditional auxiliary semantics。只有 accepted fact 的 exact `config_hash` + `config_version` 能解析到对应 historical immutable config 时，才可读取 terminal、route/order、profile 或 line semantics。

- current `config/lines/demo_3_station.yaml` 仅是当前 conditional auxiliary evidence，不是历史事实 authority。
- 不得把 current YAML 的 terminal、order、cycle profile 或当前值套用于 lineage 不匹配的 accepted facts。
- fixed `WS03` production authority 禁止；WS03 只能是被 exact historical lineage 解析出的 terminal result。
- lineage 缺失、混合或不匹配时，terminal/order/line output 必须为 `PARTIAL` 或 `UNAVAILABLE`，不得产生 numeric line claim；accepted facts 本身仍可展示。
- output counting unit（event-count 或 unit-count）必须显式声明；缺失 unit identity 时不得把 event-count 冒充 unit-count。

## 7. Station cycle time 与 ideal CT

station cycle time 需要 producer-authoritative start/complete pairing key，并且该 key 的 duplicate/missing/conflict 规则必须 fail closed。当前 accepted fact surface 未证明此 key，因此 `STATION_CYCLE_TIME = PARTIAL`。

禁止使用 adjacent-row pairing、counter-only pairing、`cycle_counter` 单独配对、time-proximity、nearest event 或 legacy `cycle_event.cycle_time_ms` fallback。

ideal cycle time 只有在 accepted fact 的 exact historical `config_hash`/`config_version` 与 exact profile binding 可解析时才可使用；当前 YAML、`docs/kpi_definitions.md` 的 30s、simulation timing 或 current default 都不能替代历史 binding。因此 `IDEAL_CT = PARTIAL`。

## 8. Performance、Availability 与 Full OEE

- `Performance = UNSUPPORTED`：需要 historical ideal CT 与同 scope/window 的 producer-authoritative operating/runtime denominator；自然窗口 elapsed time 不是该 denominator。
- `Availability = UNSUPPORTED`：需要 planned production time、planned downtime 与 authoritative machine-state run/stop timeline；API window、Collector health、ACK 或 snapshot 不是替代来源。
- `Full OEE = UNSUPPORTED`：当 A/P 任一 unsupported 时，不得输出 `A × P × Q` numeric claim。可以展示组件状态，但不得把 partial component 拼成完整百分比。

## 9. 数据充分性状态

状态含义固定如下：

- `SUPPORTED`：在声明的 scope/window/identity 下，authority、字段与确定性语义齐全，可形成该语义的生产数值或事实。
- `PARTIAL`：accepted facts 可展示或部分计算，但 identity、lineage、pairing、completeness 或 denominator 尚不充分；不得隐藏缺口或升级为完整 claim。
- `UNAVAILABLE`：本次声明 scope/window 的 required source 或 lineage 当前不可用，不能形成 numeric result；必须返回明确不可用状态。
- `UNSUPPORTED`：当前 Goal 未建立所需 source/authority，不能声称该语义已支持；不得用 fallback 变成 numeric result。

`SUPPORTED` 不会升级 G0 已接受的 `PARTIAL/UNSUPPORTED`：station-scoped Quality 与 accepted event timeline 可 `SUPPORTED`；`unit_id`/DMC Trace、historical terminal/order、throughput、station CT、ideal CT 保持 `PARTIAL`；Performance、Availability、Full OEE 保持 `UNSUPPORTED`。

## 10. 固定禁止项与 Gate flags

```text
PRODUCTION_FACT_SOURCE = production_accepted_station_event_fact
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
TIME_PROXIMITY_TRACE_FILL = NO
SYNTHETIC_IDENTITY_FILL = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
FULL_GENEALOGY_CLAIM = NO
FULL_OEE_NUMERIC_CLAIM = NO
DB_MIGRATION = 0
```

本合同是 docs-only semantic freeze。它不接受、自行验证或授权 G2、Reliability、Data Quality rereview、Verification、DB/API runtime、Collector、config mutation、Frontend、V-PLC、remote、production 或 Git action；`PARENT_PM_INTAKE_REQUIRED = YES`。

