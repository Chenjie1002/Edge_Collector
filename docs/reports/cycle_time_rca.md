# Cycle Time Root Cause Analysis

日期：2026-06-18  
分析范围：单机 Edge MES Demo 的 V-PLC → Collector → PostgreSQL → API → Grafana  
分析方式：源码审计、运行端只读 HTTP 检查、运行数据库只读查询  
代码修改：无

## 1. Executive Conclusion

当前三工站 Dashboard 显示约 4 秒，不是 Dashboard 计算错误，也不是 Collector
计算错误。

**三工站 V-PLC 当前确实在按约 4 秒加工。**

直接原因已确认：

- 当前 V-PLC `scale=1.0`。
- WS01、WS02、WS03 当前运行时参数均为：
  - `base_cycle_s=1.0`
  - `jitter_s=0.0`
- V-PLC 的节拍公式为：

  ```text
  sampled_cycle_s = max(4.0, gaussian(base_cycle_s, jitter_s)) * scale
  ```

- 因此当前结果固定落在约 4 秒；PLC 时间使用整数秒，实际存储会表现为 4 或 5 秒。

运行数据库证据：

- 最近 30 分钟：
  - WS01 平均 `4.118s`
  - WS02 平均 `4.093s`
  - WS03 平均 `4.103s`
- WS03 实际相邻下线间隔平均 `4.410s`。
- `raw_plc_sample` 中 PLC 开始/结束时间本身相差 4–5 秒。
- `cycle_event.cycle_time_ms` 与数据库重新计算的
  `plc_end_time - plc_start_time` 完全一致。

对照证据：

- legacy Simulator 当前周期为 `46.950s`。
- API `/kpi/LINE_01/summary` 最近 24 小时平均为 `39.164s`。
- `production_snapshot` 最近 30 分钟平均为 `38.992s`。

因此目前存在两条不同节拍链路：

```text
DB100 legacy Simulator → production_snapshot → 旧总览：约 39s
DB101/102/103 V-PLC → cycle_event → 三工站 Dashboard：约 4.1s
```

## 2. Incident Timeline

运行数据库显示：

1. 2026-06-16 23:19:12，当前 V-PLC 进程启动。
2. WS01 cycle 1：`23:19:12 → 23:19:42`，30 秒。
3. WS01 cycle 2：`23:19:43 → 23:20:13`，30 秒。
4. WS01 cycle 3：`23:20:13 → 23:20:17`，4 秒。
5. WS02 cycle 1：`23:19:43 → 23:20:15`，32 秒。
6. WS02 cycle 2：`23:20:15 → 23:20:19`，4 秒。
7. WS03 第一个 cycle 从 `23:20:15` 开始，直接为 4 秒。

这说明进程启动时仍使用约 30 秒默认值，运行参数在
**2026-06-16 23:20:13 左右**被改为低值；已经开始的 cycle 保持原抽样节拍，
之后启动的 cycle 变成 4 秒。

Grafana 三工站 Dashboard 最后更新时间为 2026-06-16 14:17:37，早于异常切换，
因此 Dashboard 配置修改不是触发原因。

## 3. End-to-End Data Flow

### 3.1 V-PLC

#### 三工站事件链路

默认参数定义于 `s7_plc_sim/app/pipeline.py`：

| 工站 | 默认基准节拍 | 默认 jitter |
| --- | ---: | ---: |
| WS01 | 30.4s | 1.2s |
| WS02 | 29.8s | 1.0s |
| WS03 | 29.2s | 0.9s |

每件开始时调用：

```python
value = rng.gauss(base_cycle_s, jitter_s)
cycle_s = max(4.0, value) * scale
```

关键代码：

- `s7_plc_sim/app/pipeline.py:91-93`
- `s7_plc_sim/app/pipeline.py:129-133`
- `s7_plc_sim/app/pipeline.py:181-188`

`VPLC_CYCLE_SCALE` 默认 `1.0`，当前运行端也是 `1.0`，因此速度倍率不是本次原因。

V-PLC 在 cycle 开始和结束时分别生成 `datetime`，写入 DB101/102/103：

- `plc_start_time`
- `plc_end_time`
- `cycle_counter`
- payload/result

S7 中的开始和结束时间使用 Unix seconds，因此精度为 1 秒。

#### 运行时参数修改入口

控制接口允许直接修改：

```text
POST /vplc/stations/{station_id}
```

可修改：

- `base_cycle_s`
- `jitter_s`
- `nok_rate`
- `paused`

最低允许 `base_cycle_s=1`。控制页“保存”按钮会直接调用此接口。

关键代码：

- `s7_plc_sim/app/control_api.py:12-16`
- `s7_plc_sim/app/control_api.py:47-53`
- `s7_plc_sim/app/control_api.py:325-335`
- `s7_plc_sim/app/pipeline.py:412-422`

当前接口没有认证、操作审计或参数变更日志。

#### DB100 legacy 链路

另有独立的 Business Simulator：

- 配置基准值：`config/simulator.yaml:4`，`30000ms`
- 抖动：`2500ms`
- 生成公式：`simulator/app/simulator.py:220-224`

该值写入 DB100 `DBD20`，与三工站 pipeline 的 `base_cycle_s` 无关。

### 3.2 Collector

#### legacy Collector

旧采集链路从 DB100 `DBD20` 直接读取 `cycle_time_ms`，写入
`production_snapshot.cycle_time_ms`。

它不重新计算节拍，只复制 Simulator 当前提供的周期设定值。

#### event Collector

三工站 Collector：

1. 读取 DB101/102/103。
2. 将 Unix seconds 解码为 ISO datetime。
3. 使用以下公式计算：

   ```text
   cycle_time_ms = int((plc_end_time - plc_start_time).total_seconds() * 1000)
   ```

4. 写入 `cycle_event`，并同步派生到 `station_event`。

关键代码：

- `collector/app/plc/decoder.py:45-49`
- `collector/app/services/event_collector.py:81-88`
- `collector/app/services/storage.py:329-332`
- `collector/app/services/storage.py:791-796`

Collector 的轮询间隔、数据库写入时间或 ACK 延迟不参与该公式。

### 3.3 Database

#### `production_snapshot`

保存 legacy 快照：

- `ts`
- `cycle_counter`
- `good_count`
- `ng_count`
- `total_count`
- `cycle_time_ms`
- 运行、报警和停机字段

`cycle_time_ms` 是 DB100 Simulator 提供的当前/下一周期设定值，不是由两次产出时间
差计算出的整线下线节拍。

Schema：`db/init/001_schema.sql:10-26`

#### `raw_plc_sample`

保存：

- 原始 S7 bytes：`raw_hex`
- 解码结果：`decoded_json`
- `sample_time`

可用来核对 PLC 原始 `plc_start_time`、`plc_end_time` 和 counter。

Schema：`db/init/003_event_schema.sql:1-16`

#### `cycle_event`

保存：

- `plc_start_time`
- `plc_end_time`
- `edge_read_time`
- `edge_write_time`
- `cycle_time_ms`
- `station_id`
- `cycle_counter`
- `plc_boot_id`
- payload、result、ACK 等

Schema：`db/init/003_event_schema.sql:18-52`

#### `station_event`

复制 cycle 的：

- `plc_start_time`
- `plc_end_time`
- `cycle_time_ms`

Schema：`db/init/004_unit_trace_schema.sql:49-73`

### 3.4 API

#### `/kpi/LINE_01/summary`

返回最近 24 小时 legacy 指标：

- `output_24h`
- `good_24h`
- `ng_24h`
- `quality_rate`
- `avg_cycle_time_ms`

数据源是 `production_snapshot`，不是 `cycle_event`。

关键代码：`api/app/routes/kpi.py:146-183`

本次只读结果：

```json
{
  "output_24h": 989,
  "good_24h": 962,
  "ng_24h": 27,
  "quality_rate": "97.27",
  "avg_cycle_time_ms": "39164.24"
}
```

#### `/trace/api`

返回单件三工站事件，包括：

- `plc_start_time`
- `plc_end_time`
- `cycle_time_ms`
- result、ACK、payload

追溯页面仅把 `cycle_time_ms / 1000` 显示为秒。

关键代码：

- `api/app/routes/trace.py:85-106`
- `api/app/routes/trace.py:461-465`

#### API 与 Grafana 的关系

当前两个 Grafana CT 面板都不经过 API。Grafana 直接连接 PostgreSQL。

### 3.5 Dashboard

#### Edge MES 单线生产总览

数据源：`production_snapshot`

平均 CT：

```sql
SELECT round(avg(p.cycle_time_ms)::numeric / 1000.0, 2)
FROM production_snapshot p
WHERE ...
  AND p.running = TRUE;
```

趋势：

```sql
SELECT p.ts, round(p.cycle_time_ms::numeric / 1000.0, 2)
FROM production_snapshot p
WHERE ...
  AND p.running = TRUE;
```

关键位置：

- `edge_mes_overview.json:156`
- `edge_mes_overview.json:287`

#### Edge MES 三工站追溯与采集监控

数据源：`cycle_event`

平均 CT：

```sql
SELECT round(avg(cycle_time_ms) / 1000.0, 2)
FROM cycle_event
WHERE $__timeFilter(plc_end_time)
  AND station_id IN (...)
  AND cycle_time_ms IS NOT NULL;
```

趋势按时间 bucket 和工站计算 `avg(cycle_time_ms) / 1000.0`。

关键位置：

- `edge_mes_station_traceability.json:203`
- `edge_mes_station_traceability.json:411`
- `edge_mes_station_traceability.json:670`

这些 SQL 没有把 30 秒错误缩放为 4 秒。

## 4. Suspicious Modules

| 模块 | 判断 | 依据 |
| --- | --- | --- |
| V-PLC runtime station parameters | 根因所在 | 当前三站均为 `base=1.0, jitter=0.0` |
| V-PLC control API / page | 最可能触发入口 | 可无认证修改参数，且无审计 |
| V-PLC cycle formula | 放大了低参数的表现 | 最低值钳制为 4 秒，因此 1 秒配置显示为 4 秒 |
| Collector | 基本排除 | 计算值与 PLC 原始开始/结束时间一致 |
| Database | 排除数据损坏 | raw、cycle timestamps 和 `cycle_time_ms` 相互一致 |
| 三工站 Dashboard | 排除 | SQL 只做平均和毫秒转秒 |
| legacy Dashboard / API | 口径分叉风险 | 显示约 39 秒，但它读取另一条链路 |
| `config/app.yaml` ideal cycle | 配置债务 | 仍为 `1200ms`，但当前 CT 面板未使用，非本次原因 |

## 5. Possible Causes Ranked

### 1. V-PLC 控制页面或 API 将三站运行时参数改为 1 秒（极高，直接原因确认）

证据：

- 当前运行状态明确返回三个工站 `base_cycle_s=1.0`、`jitter_s=0.0`。
- 进程启动后前两个 cycle 为 30–32 秒。
- 从约 23:20:13 开始，新 cycle 立即变为 4 秒。
- 修改接口的最小允许值正是 1 秒。
- 当前参数组合与控制页面可提交的数据完全一致。

无法确认的是具体操作者或调用方，因为当前没有 audit log。

### 2. 某个自动化脚本、浏览器会话或直接 HTTP 调用调用了同一接口（高）

控制 API 暴露在 `8200`，没有认证。即使没有人工“修改 PLC 配置”，任何能访问该
地址的客户端都可以修改运行时参数。

异常在进程启动约 1 分钟后出现，更符合运行时 POST，而不是静态配置或镜像默认值。

### 3. 当前看到的是三工站事件 Dashboard，而此前认知来自 legacy 总览（中）

两个 Dashboard 的“CT”名称相近，但数据源不同：

- legacy：约 39 秒。
- 三工站：约 4.1 秒。

该问题会造成认知混淆，但不能解释 `cycle_event` 和 PLC 时间为何真实为 4 秒。

### 4. V-PLC 镜像或部署版本与仓库源码不一致（低）

运行端仍显示旧版 `require_ack=false`，说明树莓派尚未部署当前工作树的可靠性修改。
但数据库证明该进程启动后的最初 cycle 是约 30 秒，因此即使镜像较旧，它的启动默认值
仍是约 30 秒。版本差异不是 4 秒切换的主要解释。

### 5. `VPLC_CYCLE_SCALE` 被改小（已排除）

当前运行端 `scale=1.0`。如果倍率是约 0.13，确实可能把 30 秒缩短到约 4 秒，但现有
运行状态不支持该假设。

### 6. Collector 计算或单位转换错误（已排除）

`cycle_time_ms` 与 `plc_end_time - plc_start_time` 一致。Collector 只把秒差乘 1000。

### 7. Dashboard SQL 或单位配置错误（已排除）

SQL 只执行 `avg(cycle_time_ms) / 1000.0`，Grafana unit 为秒。在线 Dashboard 的 query
与仓库一致，且 Dashboard 更新时间早于异常。

### 8. 历史窗口、异常值或三站平均导致 4 秒（已排除）

最近数据逐条均为 4–5 秒，最近 30 分钟三个工站也都约 4.1 秒，不是少量历史值拉低平均。

### 9. Unix seconds 精度（次要影响，不是根因）

PLC 时间只有秒级精度，因此真实约 4.1 秒会存成 4 或 5 秒。它解释了离散值，但不能把
真实 30 秒变成 4 秒。

## 6. Verification Plan

### 6.1 Code to Inspect

1. `s7_plc_sim/app/pipeline.py`
   - 默认工站参数。
   - `next_cycle_time()` 公式。
   - `update_station()` 的运行时修改。
2. `s7_plc_sim/app/control_api.py`
   - `POST /vplc/stations/{station_id}`。
   - 页面保存时发送的 payload。
   - 是否存在认证和审计。
3. `s7_plc_sim/app/main.py`
   - `VPLC_CYCLE_SCALE`。
   - 进程启动日志与参数输出。
4. `collector/app/plc/decoder.py`
   - Unix seconds 解码。
5. `collector/app/services/storage.py`
   - `_cycle_time_ms()`。
6. `api/app/routes/kpi.py`
   - legacy KPI 来源。
7. `api/app/routes/trace.py`
   - event CT 返回与显示。
8. 两个 Grafana dashboard JSON
   - 明确查询的是 `production_snapshot` 还是 `cycle_event`。

### 6.2 Runtime State to Check

```bash
curl -s http://10.0.0.217:8200/vplc/state | jq '{
  scale,
  started_at: .line.started_at,
  stations: .stations
    | with_entries(.value |= {
        base_cycle_s,
        jitter_s,
        cycle_counter,
        current_dmc,
        last_end_time
      })
}'
```

预期异常证据：三个工站 `base_cycle_s=1.0`、`jitter_s=0.0`。

同时检查 legacy：

```bash
curl -s http://10.0.0.217:8100/state | jq '{
  cycle_time_ms,
  running,
  scenario_id,
  scenario_name
}'
```

### 6.3 Database Tables and Queries

#### A. 最近 cycle 原始时间与 Collector 结果

```sql
SELECT
  station_id,
  cycle_counter,
  plc_start_time,
  plc_end_time,
  cycle_time_ms,
  extract(epoch FROM (plc_end_time - plc_start_time)) AS recomputed_s
FROM cycle_event
ORDER BY plc_end_time DESC, id DESC
LIMIT 30;
```

若 `recomputed_s` 也是 4 秒，则 Collector 没有计算偏差。

#### B. 各站平均、最小、最大

```sql
SELECT
  station_id,
  count(*) AS rows,
  round(avg(cycle_time_ms) / 1000.0, 3) AS avg_cycle_s,
  min(cycle_time_ms) / 1000.0 AS min_cycle_s,
  max(cycle_time_ms) / 1000.0 AS max_cycle_s
FROM cycle_event
WHERE plc_end_time >= now() - interval '30 minutes'
GROUP BY station_id
ORDER BY station_id;
```

#### C. 实际 WS03 下线间隔

```sql
WITH x AS (
  SELECT
    plc_end_time,
    lag(plc_end_time) OVER (ORDER BY plc_end_time) AS previous_end
  FROM cycle_event
  WHERE station_id = 'WS03'
    AND plc_end_time >= now() - interval '30 minutes'
)
SELECT
  round(avg(extract(epoch FROM (plc_end_time - previous_end))), 3)
FROM x
WHERE previous_end IS NOT NULL;
```

这一步区分“单站加工时长”和“整线真实下线节奏”。

#### D. raw sample

```sql
SELECT
  station_id,
  sample_time,
  decoded_json ->> 'plc_start_time' AS plc_start_time,
  decoded_json ->> 'plc_end_time' AS plc_end_time,
  decoded_json ->> 'cycle_counter' AS cycle_counter
FROM raw_plc_sample
ORDER BY sample_time DESC
LIMIT 30;
```

#### E. legacy 对照

```sql
SELECT
  round(avg(cycle_time_ms) / 1000.0, 3) AS avg_cycle_s,
  min(cycle_time_ms) / 1000.0 AS min_cycle_s,
  max(cycle_time_ms) / 1000.0 AS max_cycle_s
FROM production_snapshot
WHERE ts >= now() - interval '30 minutes'
  AND running = TRUE;
```

#### F. 异常切换时间

```sql
SELECT
  station_id,
  cycle_counter,
  plc_start_time,
  plc_end_time,
  cycle_time_ms / 1000.0 AS cycle_s
FROM cycle_event
WHERE plc_end_time BETWEEN
      '2026-06-16 23:19:00+08' AND '2026-06-16 23:21:00+08'
ORDER BY plc_end_time, id;
```

### 6.4 Logs to Inspect

在树莓派检查：

```bash
docker logs --since "2026-06-16T23:18:00+08:00" \
  --until "2026-06-16T23:22:00+08:00" edge-mes-s7-plc-sim

docker logs --since "2026-06-16T23:18:00+08:00" \
  --until "2026-06-16T23:22:00+08:00" edge-mes-collector
```

重点查：

- V-PLC 容器启动时间与 `scale`。
- WS01/02/03 counter 增长速度。
- 是否存在 HTTP access log：
  - `POST /vplc/stations/WS01`
  - `POST /vplc/stations/WS02`
  - `POST /vplc/stations/WS03`

限制：

- 当前 Uvicorn 以 `log_level="warning"` 启动。
- 参数更新函数没有业务日志。
- 没有 `operation_audit_log`。

因此现有日志很可能只能确认进程启动和 counter 速度，不能确认操作者。

### 6.5 Dashboard Queries to Inspect

在 Grafana Panel → Inspect → Query 中核对：

1. `Edge MES 单线生产总览 / 平均CT`
   - 表：`production_snapshot`
   - 预期约 39 秒。
2. `Edge MES 三工站追溯与采集监控 / 平均CT(三站)`
   - 表：`cycle_event`
   - 当前约 4.1 秒。
3. `三工站Cycle Time趋势`
   - 检查 station variable 当前选择。
   - 分别只选 WS01、WS02、WS03，三个站都应约 4.1 秒。
4. `最近产品追溯记录`
   - 逐条确认 `cycle_time_s` 为 4 或 5。

## 7. Recommended Fixes

以下仅为建议，本次未执行。

### 7.1 Immediate Operational Recovery

在保留当前状态证据后，将运行时参数恢复为：

| 工站 | base_cycle_s | jitter_s |
| --- | ---: | ---: |
| WS01 | 30.4 | 1.2 |
| WS02 | 29.8 | 1.0 |
| WS03 | 29.2 | 0.9 |

恢复后验证：

1. `/vplc/state` 返回目标参数。
2. 新启动的 cycle 恢复到约 29–32 秒。
3. `raw_plc_sample` 开始/结束时间恢复。
4. `cycle_event.cycle_time_ms` 恢复。
5. 三工站 Dashboard 随时间窗口更新恢复约 30 秒。

不要通过修改 Dashboard SQL 来“显示 30 秒”，那会掩盖真实 V-PLC 状态。

### 7.2 Permanent Engineering Fixes

1. 为 V-PLC 参数修改增加认证或限制到可信管理网段。
2. 参数修改必须记录：
   - 时间
   - 工站
   - old/new value
   - 调用来源或用户
   - request ID
3. 将节拍参数的真源明确为受控配置，不依赖不可追踪的进程内状态。
4. 启动时记录全部 station 参数，而不只记录 scale。
5. 每次 `update_station()` 后写业务日志。
6. 对异常范围增加 guardrail，例如 Demo 正常模式下 `base_cycle_s < 20` 时告警或拒绝。
7. Dashboard 明确区分：
   - `Legacy Simulator 当前周期设定值`
   - `工站加工时长`
   - `WS03 实际下线间隔`
8. 增加 V-PLC 当前参数面板和最近参数变更记录。
9. 清理 `config/app.yaml` 中仍为 `1200ms` 的旧 `ideal_cycle_time_ms`，避免后续 KPI
   使用时产生第三套口径。

若上述措施涉及协议、数据库结构或公共接口，实施时必须遵守：

```text
先更新 docs/contracts/ → 再修改代码/migration → 最后在 docs/reports/ 记录影响范围
```

## 8. Final Answer to the Three Possibilities

| 假设 | 结论 |
| --- | --- |
| 实际生产节拍变成 4 秒 | **是。三工站 V-PLC 实际加工与 WS03 下线均约 4–4.4 秒。** |
| Dashboard 计算错误 | **否。三工站 Dashboard 正确展示 `cycle_event`。** |
| Collector 数据错误 | **否。Collector 结果与 raw PLC 开始/结束时间一致。** |

最终根因：

> 三工站 V-PLC 的运行时 `base_cycle_s` 被改为 1 秒、`jitter_s` 被改为 0；V-PLC
> 公式将最小周期钳制为 4 秒，因此生成了真实的 4 秒 PLC cycle。该参数修改发生在
> 2026-06-16 23:20:13 左右，最可能通过未认证且无审计的 V-PLC 控制页面/API 完成。
