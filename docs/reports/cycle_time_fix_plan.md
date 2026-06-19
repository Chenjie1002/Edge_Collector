# Cycle Time Fix Plan

日期：2026-06-18  
依据：[`cycle_time_rca.md`](cycle_time_rca.md)  
状态：只读分析与实施计划，未修改代码或运行参数

## 1. Conclusion

`base_cycle_s=1.0` 不是来自默认值、YAML 配置、场景切换、Docker 环境变量或 Grafana
查询。

现有实现中，三工站参数的实际覆盖链路只有：

```text
源码硬编码默认值
  → ThreeStationPipeline 内存状态
  → POST /vplc/stations/{station_id}
  → update_station()
  → 内存值被覆盖为 base_cycle_s=1.0、jitter_s=0.0
```

当前进程在 2026-06-16 23:19:12 启动。启动后的首批 cycle 仍为 30–32 秒，随后新
cycle 变为 4 秒，证明启动默认值正常，低值是在进程运行后通过参数修改入口写入。

可以确认：

- 修改渠道：V-PLC runtime station update API。
- 修改结果：三个工站均变成 `base_cycle_s=1.0`、`jitter_s=0.0`。
- 修改窗口：V-PLC 启动后、各工站下一件开始前；数据库能观察到的切换点约为
  2026-06-16 23:20:13。
- 最可能调用方式：
  1. V-PLC 控制页逐站点击“保存”。
  2. 自动化脚本或直接 HTTP 请求连续调用三个 station API。

无法确认：

- 具体操作者。
- 客户端 IP。
- 精确请求时间。
- 是人工页面操作还是脚本。

原因是当前 API 无认证、无 access audit、无业务变更日志，Uvicorn 又以 warning
级别启动。

## 2. Parameter Source Analysis

### 2.1 `base_cycle_s` 默认值定义位置

默认值硬编码在 `s7_plc_sim/app/pipeline.py` 的
`ThreeStationPipeline.__init__()`：

| 工站 | `base_cycle_s` |
| --- | ---: |
| WS01 | 30.4 |
| WS02 | 29.8 |
| WS03 | 29.2 |

这些值不是从 `config/` 目录读取。

### 2.2 `jitter_s` 默认值定义位置

同样硬编码在 `ThreeStationPipeline.__init__()`：

| 工站 | `jitter_s` |
| --- | ---: |
| WS01 | 1.2 |
| WS02 | 1.0 |
| WS03 | 0.9 |

当前运行值三个工站均为 `0.0`，也不是默认值。

### 2.3 配置加载流程

#### V-PLC main

`s7_plc_sim/app/main.py` 调用：

```python
mapping = load_mapping()
```

该函数默认读取 `/app/config/plc_mapping.yaml`，用途是：

- legacy DB100 DB number/size。
- DB100 字段编码和 code tables。

它不加载 DB101/102/103 的：

- `base_cycle_s`
- `jitter_s`
- `nok_rate`

随后 `main.py` 直接实例化 `ThreeStationPipeline`，工站参数由源码构造函数提供。

#### Business Simulator

`simulator/app/simulator.py` 单独读取 `/app/config/simulator.yaml`：

- `base_cycle_time_ms=30000`
- `cycle_time_jitter_ms=2500`

这是 DB100 legacy 链路，不是三工站 pipeline 的配置源。

#### Collector config

`config/app.yaml` 和 `config/mapping.yaml` 只影响采集、mapping、KPI 等，不反向修改
V-PLC 工站节拍。

### 2.4 场景切换逻辑

场景控制运行于 `simulator` 服务的 8100 端口。

场景包括：

- normal
- material shortage
- sensor fault
- changeover
- maintenance
- slow cycle
- fast run

`slow_cycle` 和 `fast_run` 只改变 Business Simulator 的
`cycle_time_multiplier`：

- slow cycle：`1.35`
- fast run：`0.93`

场景状态随后被 V-PLC 复制到 DB100。

三工站 pipeline 在 `tick()` 中明确使用：

```python
line_running = self.plan.active
```

而不是 legacy Simulator 的 `running` 或 scenario cycle multiplier。注释也明确指出
DB101/102/103 与旧 Simulator 随机停机解耦。

结论：

- 场景切换不会把三工站 `base_cycle_s` 改为 1.0。
- `fast_run=0.93` 也不可能把约 30 秒变成 4 秒。
- 当前 legacy state 为 `scenario_id=normal`，cycle time 仍约 43–47 秒。

### 2.5 API 修改入口

公共入口：

```text
POST /vplc/stations/{station_id}
```

请求模型允许：

```json
{
  "base_cycle_s": 1.0,
  "jitter_s": 0.0,
  "nok_rate": 0.0,
  "paused": false
}
```

约束：

- `base_cycle_s` 最小值为 1。
- `jitter_s` 最小值为 0。

`update_station()` 直接修改进程内的 `StationState`：

```python
station.base_cycle_s = max(1.0, value)
station.jitter_s = max(0.0, value)
```

不需要重启，不写文件，不写数据库。

### 2.6 Dashboard 控制入口

需要区分两个 “Dashboard”：

#### Grafana

Grafana CT 面板只读 PostgreSQL，不修改 V-PLC 参数。

但三工站 Grafana 中有一个外部链接：

```text
V-PLC控制台 → http://10.0.0.217:8200/vplc
```

因此用户可能从 Grafana 跳转到 V-PLC 控制页，但实际修改发生在 8200 控制页/API，
不是 Grafana query。

#### V-PLC 控制页

控制页会显示每站：

- 基准节拍
- jitter
- NOK rate

点击每一行的“保存”后，JavaScript 调用对应 station POST API。

页面没有：

- 二次确认。
- 变更原因输入。
- 用户身份。
- 修改前后差异预览。
- 正常/测试模式提示。
- 低节拍危险警告。

### 2.7 Docker 环境变量

当前 V-PLC 可读取：

| 环境变量 | 作用 |
| --- | --- |
| `S7_PORT` | Snap7 端口 |
| `S7_UPDATE_INTERVAL_MS` | 主循环更新间隔 |
| `SIMULATOR_URL` | legacy Simulator 地址 |
| `VPLC_CONTROL_PORT` | 控制 API 端口 |
| `VPLC_CYCLE_SCALE` | 三工站统一速度倍率 |
| `VPLC_ACK_DEADLINE_SECONDS` | ACK deadline |
| `VPLC_RUNTIME_STATE_PATH` | runtime identity 文件 |

当前 Compose 没有设置 `VPLC_CYCLE_SCALE`，代码默认 `1.0`；运行端也返回
`scale=1.0`。

没有环境变量可以把单站：

- `base_cycle_s` 改成 1.0。
- `jitter_s` 改成 0.0。

因此 Docker 环境变量不是本次直接来源。

### 2.8 配置文件覆盖链路

当前实际覆盖优先级不是常见的“默认值 → YAML → env → runtime”，而是：

```text
工站参数：
硬编码默认值 → runtime API 内存覆盖

统一倍率：
VPLC_CYCLE_SCALE env → 默认 1.0

legacy Simulator：
config/simulator.yaml → scenario multiplier
```

不存在：

- 工站节拍 YAML。
- 工站参数环境变量。
- 参数数据库。
- 参数持久化文件。
- API 修改后的重启恢复。

因此 API 覆盖只在当前进程生命周期有效。容器重启会恢复源码默认值。

## 3. How the Value Became `1.0`

### 3.1 Confirmed causal sequence

1. V-PLC 于 2026-06-16 23:19:12 启动。
2. `ThreeStationPipeline` 以约 30 秒的硬编码参数初始化。
3. WS01 前两个 cycle 和 WS02 第一个 cycle 已在修改前抽样，因此仍为 30–32 秒。
4. 在这些 cycle 运行期间，三个 station 的 runtime update API 收到低参数。
5. `update_station()` 将内存状态改为：

   ```text
   base_cycle_s = 1.0
   jitter_s = 0.0
   nok_rate = 0.0
   ```

6. 已运行的 cycle 不受影响。
7. 之后启动的 cycle 调用：

   ```text
   max(4.0, gaussian(1.0, 0.0)) * 1.0 = 4.0s
   ```

8. V-PLC 把 4 秒开始/结束时间写入 DB101/102/103。
9. Collector、Database 和 Dashboard 正确传递和显示 4 秒。

### 3.2 Source attribution boundary

V-PLC 控制页每次只保存一个工站。因此三个工站均变为相同值意味着至少存在：

- 三次页面保存请求；或
- 三次脚本/API 请求。

由于没有请求审计，只能把来源定位到 API channel，不能定位到人。

## 4. Repair Objectives

修复必须同时满足：

1. 正常 Demo 默认约 30 秒。
2. 不改变 legacy 场景控制功能。
3. 测试仍可快速运行。
4. 正常节拍参数和仿真加速参数不再混用。
5. 每个生效参数都能回答：
   - 来自哪里。
   - 谁改的。
   - 何时改的。
   - 改前改后是什么。
   - 当前是否偏离正常基线。

## 5. Recommended Repair Design

### 5.1 Separate process parameters from simulation speed

推荐定义两类不同概念：

#### Process parameters

- WS01 `base_cycle_s=30.4`, `jitter_s=1.2`
- WS02 `base_cycle_s=29.8`, `jitter_s=1.0`
- WS03 `base_cycle_s=29.2`, `jitter_s=0.9`

这些值代表真实设计节拍，不应用于测试加速。

#### Simulation speed

使用单独的：

```text
VPLC_PROFILE=normal|fast|test
VPLC_CYCLE_SCALE
```

建议：

| Profile | 默认 scale | 用途 |
| --- | ---: | --- |
| `normal` | 1.0 | 现场演示和生产口径 |
| `fast` | 0.1 或明确配置 | 人工快速演示 |
| `test` | 测试自行注入，如 0.05 | 自动化测试 |

测试继续使用现有构造参数：

```python
ThreeStationPipeline(scale=0.05)
```

因此不影响现有快速单元测试。

### 5.2 Create a controlled station parameter source

建议新增独立配置，例如：

```text
config/vplc.yaml
```

内容分层：

```yaml
profile: normal
stations:
  WS01:
    base_cycle_s: 30.4
    jitter_s: 1.2
    nok_rate: 0.02
  WS02:
    base_cycle_s: 29.8
    jitter_s: 1.0
    nok_rate: 0.015
  WS03:
    base_cycle_s: 29.2
    jitter_s: 0.9
    nok_rate: 0.01
profiles:
  normal:
    cycle_scale: 1.0
    allow_runtime_cycle_edit: false
  fast:
    cycle_scale: 0.1
    allow_runtime_cycle_edit: true
  test:
    cycle_scale: 0.05
    allow_runtime_cycle_edit: true
```

建议优先级：

```text
built-in safe defaults
  → vplc.yaml
  → validated profile/env override
  → authorized runtime override
```

每层都必须保留 source metadata。

### 5.3 Normal-mode guardrails

在 `normal` profile：

- `base_cycle_s` 建议限制在经 contract 确认的安全范围，例如 20–60 秒。
- `jitter_s` 建议限制在 0–10 秒。
- 低于安全范围的修改：
  - 默认拒绝；或
  - 要求显式 `simulation_override=true`、变更原因和授权身份。
- scale 偏离 1.0 时启动失败或产生高优先级告警。

不要删除快速仿真能力；应把它放入显式 `fast/test` profile。

### 5.4 Preserve scenario control

现有 8100 legacy 场景继续保持原行为：

- 停机。
- 报警。
- 慢节拍。
- fast run。

第一版修复不要把 legacy scenario multiplier 自动套到三工站 station base 参数上，
否则会引入新的跨链路耦合。

若后续希望场景同时影响三工站，应单独冻结 scenario contract，并定义：

- 场景影响 base 还是 scale。
- 场景结束如何恢复。
- 与人工 runtime override 的优先级。

### 5.5 Operational recovery sequence

实施代码改造前，可按运维步骤恢复当前运行值，但本次未执行：

```bash
curl -X POST http://10.0.0.217:8200/vplc/stations/WS01 \
  -H 'Content-Type: application/json' \
  -d '{"base_cycle_s":30.4,"jitter_s":1.2,"nok_rate":0.02}'

curl -X POST http://10.0.0.217:8200/vplc/stations/WS02 \
  -H 'Content-Type: application/json' \
  -d '{"base_cycle_s":29.8,"jitter_s":1.0,"nok_rate":0.015}'

curl -X POST http://10.0.0.217:8200/vplc/stations/WS03 \
  -H 'Content-Type: application/json' \
  -d '{"base_cycle_s":29.2,"jitter_s":0.9,"nok_rate":0.01}'
```

恢复后只影响新启动的 cycle；已经加工中的 cycle 保持其已抽样时长。

## 6. Fail-Safe and Audit Design

### 6.1 Configuration audit

启动时生成一份 resolved configuration：

```json
{
  "profile": "normal",
  "scale": 1.0,
  "stations": {
    "WS01": {
      "base_cycle_s": 30.4,
      "jitter_s": 1.2,
      "source": "config/vplc.yaml"
    }
  },
  "config_hash": "...",
  "loaded_at": "...",
  "process_boot_id": "..."
}
```

审计项：

- 配置文件路径。
- profile。
- 环境变量覆盖。
- 每个字段最终值及 source。
- 配置 hash。
- 容器/image version。

### 6.2 Parameter change log

建议增加追加写、不可覆盖的参数变更记录。

最小字段：

| 字段 | 说明 |
| --- | --- |
| `change_id` | UUID |
| `changed_at` | 修改时间 |
| `plc_boot_id` | V-PLC 运行实例 |
| `station_id` | 工站 |
| `parameter_name` | 参数名 |
| `old_value` | 修改前 |
| `new_value` | 修改后 |
| `source` | UI / API / startup / scenario / test |
| `actor` | 用户或 service identity |
| `client_ip` | 请求来源 |
| `request_id` | 请求追踪 |
| `reason` | 修改原因 |
| `profile` | normal / fast / test |
| `accepted` | 是否生效 |
| `rejection_reason` | 拒绝原因 |

建议落 PostgreSQL 表：

```text
vplc_parameter_change_log
```

任何涉及该新表和 API 字段的实施，必须先更新 `docs/contracts/`。

### 6.3 Parameter snapshots

建议两类快照：

#### Startup snapshot

每次 V-PLC 启动记录：

- 全部默认值。
- 配置文件值。
- env override。
- 最终 resolved values。
- config hash。
- profile。

#### Runtime snapshot

在以下事件后记录完整参数集：

- 任一参数修改成功。
- 场景开始/结束。
- profile 切换。
- reset。
- 定时心跳，例如每 5 分钟。

建议表：

```text
vplc_parameter_snapshot
```

快照应记录整个三工站状态，便于回答“某一时刻实际生效的参数是什么”。

### 6.4 Startup parameter checks

启动检查建议分级：

#### Fatal

normal profile 下：

- base 小于安全下限。
- scale 不等于 1.0 且未显式允许。
- 配置缺失或类型错误。
- 三站配置不完整。

#### Warning

- jitter 为 0。
- 三站 base 完全相同且与设计基线偏差过大。
- `config/app.yaml` 理论节拍与 V-PLC 基线不一致。
- 当前值相对基线偏差超过阈值。

启动日志必须打印完整参数，而不是只打印 `scale`。

### 6.5 Dashboard parameter display

建议新增只读工程面板：

#### Current V-PLC Parameters

显示：

- profile。
- scale。
- 每站 base/jitter/NOK rate。
- 参数 source。
- 最后修改时间。
- actor。
- 是否偏离正常基线。

#### Parameter Changes

显示最近变更：

- 时间。
- 工站。
- old → new。
- actor/source。
- reason。

#### Guardrail status

显示：

- 正常 / 警告 / 危险。
- 设计 CT 与当前 expected CT。
- 当前实际 CT。
- WS03 下线间隔。

Grafana 应保持只读。参数修改仍通过受控管理接口完成，不建议在 Grafana query 中直接
写数据库或 PLC。

### 6.6 API safety

参数修改 API 建议要求：

- 身份认证。
- 角色授权。
- `reason` 必填。
- `If-Match` 或当前版本号，防止覆盖其他人的修改。
- 返回 old/new/resolved expected cycle。
- normal profile 的危险值需要明确 override 权限。
- 每个请求生成 request ID 并写日志。

控制页建议增加：

- normal / fast 模式醒目标识。
- 保存前差异确认。
- 危险值红色警告。
- “恢复设计默认值”按钮。
- “仅加速仿真”入口，修改 scale/profile，不修改 base。

## 7. Proposed Implementation Phases

### Phase 0: Contract first

在修改协议、数据库结构或公共 API 前，先新增或更新：

```text
docs/contracts/vplc_runtime_parameters.md
```

冻结：

- 参数真源与优先级。
- normal/fast/test profile。
- 安全范围。
- runtime update API。
- audit fields。
- snapshot semantics。

### Phase 1: Restore and separate profiles

1. 将约 30 秒 station defaults 放入受控配置。
2. 增加 normal/fast/test profile。
3. 保留测试构造函数 scale 注入。
4. normal profile 禁止用低 base 模拟加速。
5. 增加启动 resolved-config 日志。

### Phase 2: Audit and snapshots

1. 新增 parameter change log。
2. 新增 startup/runtime snapshots。
3. API 捕获 actor、IP、reason 和 request ID。
4. 增加参数查询 API。

### Phase 3: Dashboard visibility

1. 展示当前 resolved parameters。
2. 展示最近变更。
3. 展示基线偏差和 expected cycle。
4. 明确区分 legacy CT、station processing CT 和 WS03 interarrival。

### Phase 4: Verification

验证矩阵：

| 场景 | 预期 |
| --- | --- |
| normal 启动 | 三站约 30 秒、scale=1 |
| fast profile | 快速运行但 base 仍保留设计值 |
| test `scale=0.05` | 单元测试快速完成 |
| normal 修改 base=1 | 拒绝并记录 rejected audit |
| authorized fast override | 允许并记录 actor/reason |
| 容器重启 | 从受控配置恢复，不继承匿名内存值 |
| 场景 slow/fast | legacy 场景行为保持 |
| 参数修改 | Dashboard 数秒内显示新值和操作者 |

## 8. Impact Assessment

计划中的后续实施可能影响：

- 新 V-PLC 参数 contract。
- V-PLC 配置加载。
- station update 公共 API。
- PostgreSQL schema/migration。
- Grafana 工程面板。
- Docker profile/environment。

因此实施顺序必须为：

```text
更新 docs/contracts/
  → 修改代码、配置和 migration
  → 在 docs/reports/ 记录兼容性、影响范围和验证结果
```

## 9. Final Answers

1. 默认 `base_cycle_s` 和 `jitter_s` 都定义在
   `ThreeStationPipeline.__init__()`，默认约 30 秒。
2. 三工站节拍当前不从 YAML 加载。
3. legacy 场景切换不修改三工站参数。
4. Docker 环境只可能通过 `VPLC_CYCLE_SCALE` 统一缩放；当前 scale 为 1.0。
5. Grafana 只提供跳转到 V-PLC 控制台的链接，不直接修改参数。
6. 唯一能解释运行中从约 30 秒变为 `1.0/0.0` 的现有代码路径是
   `POST /vplc/stations/{station_id}`。
7. 具体操作者无法从现有系统恢复，因为参数修改没有认证、日志或快照。
8. 修复应保留约 30 秒 process parameters，把快速仿真移到显式 fast/test
   profile 或 scale。
