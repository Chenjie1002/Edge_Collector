# Dashboard API Contract

更新时间：2026-07-03
状态：Phase-2 公共 API 合同，尚未实施
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

本节冻结 future API contract，不声明当前 implementation 已完成。当前
FastAPI/API、Dashboard/frontend、DB read path、migration、Collector、V-PLC、
Docker/deploy 均未因此获得实施授权。

### `GET /api/v2/production/accepted-station-events`

用途：返回 accepted station-event facts / production accepted fact list/read。
该 endpoint 不是 Dashboard summary、Quality summary、Pareto input 或 legacy
trace/event 等价接口。

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

#### Source table

唯一 production fact source：

- `production_accepted_station_event_fact`

禁止把以下表作为等价 production fact source、fallback source、join-derived
replacement 或 legacy compatibility source：

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

#### Response DTO allowlist

`data.items[]` 只允许返回以下字段：

- `line_id`
- `plc_id`
- `station_id`
- `station_type`
- `profile_id`
- `config_hash`
- `config_version`
- `event_type`
- `production_result`
- `unit_id`
- `dmc`
- `cycle_counter`
- `source_event_id`
- `event_ts`
- `accepted_at`
- `fact_key`
- `content_fingerprint`
- `nok_code`
- `nok_origin`
- `nok_detail_code`
- `nok_detail_source_event_id`
- `nok_detail_evidence_fact_key`

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
      "config_version": "2026.07.03.1",
      "event_type": "station_result",
      "production_result": "ok",
      "unit_id": "U-001",
      "dmc": "DMC-001",
      "cycle_counter": 301,
      "source_event_id": "PLC_001:WS01:301",
      "event_ts": "2026-07-03T10:00:00Z",
      "accepted_at": "2026-07-03T10:00:01Z",
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

#### Forbidden fields and surfaces

Response DTO、cursor payload、meta/debug payload 和 implementation helper output
均不得暴露或派生以下字段/语义：

- `raw_payload`
- `raw_hex`
- adapter disposition/reason/phase
- candidate context
- normalized candidate payload
- raw/normalized comparison context
- decoder errors
- diagnostic/review/audit payloads
- `quality_pareto_input`
- `dashboard_state`
- legacy payload
- `raw_sample_id`
- `ack_status`
- `read_done`
- `collector_state`
- ambiguous result / defect / quality / pareto keys

#### Query requirements

- `start_time` / `end_time` 必须有界，且必须通过严格 ISO-8601 解析。
- 请求必须包含 `line_id`，或由服务端注入明确的单线默认 scope；不得隐式跨线读取。
- `limit` 默认 50，最大 500；无效、负数、非整数或超过上限必须 fail closed。
- `cursor` 必须严格解析、签名/结构校验或等价防篡改校验；无效 cursor 必须 fail closed。
- 分页顺序必须稳定，使用 `event_ts` / `accepted_at` 加稳定 identity，例如 `fact_key`。
- 无效时间边界、时间窗、scope、cursor 或 limit 必须返回错误，不得 fallback 到宽查询。
- `work_order` / `product` 过滤和响应字段暂不属于本合同，必须等待后续 schema/contract gate。

#### Reliability carry-forward

- endpoint implementation 必须使用 read-only transaction。
- 建议配置 `statement_timeout` 和 idle timeout。
- read path 不得执行 `INSERT` / `UPDATE` / `DELETE`。
- read path 不得发生 ACK/read_done mutation。
- read path 不得产生 Collector/PLC/runtime side effect。
- `fact_key`、`content_fingerprint`、`source_event_id` 只能作为 reference/identity，
  不是 mutation authority。

#### Data Quality carry-forward

- 所有 response fields 必须来自 `production_accepted_station_event_fact`。
- `accepted_at` 只表示 accepted fact timestamp，不表示 dashboard freshness、
  ACK time 或 collector state。
- NOK/detail fields 必须 bind to accepted upstream business evidence。
- adapter reason code、raw mismatch、decoder error 或 `quality_event` 不得派生
  NOK/detail。

#### Future verification matrix

- positive DTO allowlist assertions。
- negative forbidden field assertions。
- source non-equivalence / no legacy fallback assertions。
- bounded query and cursor validation。
- NOK/detail evidence response assertions。
- read-only / no ACK/read_done side-effect assertions。
- forbidden surface guard for migration/storage/collector/config/dashboard/V-PLC/docker/deploy。

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
