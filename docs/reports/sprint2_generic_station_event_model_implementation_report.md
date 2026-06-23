# Sprint 2 Generic Station Event Model Implementation Report

日期：2026-06-22
Git 基线：`e9abe45 Finalize Sprint 2 station event review gates`
结论：**RELIABILITY R-B4 MINIMAL REPAIR PASS；等待 focused re-review**

## 1. 实施范围

本轮只新增独立离线包与直接相关单元测试：

```text
common/station_event/
tests/test_station_event_model.py
```

未接入 Collector、API、DB、Dashboard、Grafana 或 V-PLC；未创建 migration、tag，
未 deploy，未执行 rollback drill。

## 2. 实现内容

- 五类 MVP event：
  `station_cycle_start/station_cycle_complete/station_result/station_nok/station_heartbeat`。
- frozen `StationEvent`、`ValidationDecision`、`LifecycleDerivedOutput` 与 projection
  dataclass。
- strict presence/null/unknown-field、event/result/NOK、authority、timestamp、UUIDv4、
  cycle identity 与 config lineage validation。
- normalized/raw JSON whole-tree resource validation：
  16/64 KiB、depth、key、array、node、string、number 与 forbidden content。
- canonical dict、JCS-equivalent standard-library JSON subset、fact/content/raw SHA-256
  fingerprint。
- event/fact/cycle-role/detail-slot duplicate/conflict 与 audit-only `raw_variant`。
- canonical NOK parent、primary/secondary/system-reserved detail policy 与 upstream
  business evidence boundary。
- eight-field lifecycle derivation、future-only late status、out-of-order preservation 与
  timestamp reversal diagnostic。
- production-result authority、detail-only defect projection 与 derived compatibility
  projection。

Future event names only remain in `FUTURE_RESERVED_EVENT_TYPES`; validator does not accept
or implement their production semantics.

## 3. Test evidence

```text
.venv/bin/python -m compileall common tests
PASS

.venv/bin/python -m pytest -q tests/test_station_event_model.py
119 passed

.venv/bin/python -m pytest -q tests
207 passed

.venv/bin/python -m pytest -q tests/test_line_config.py tests/test_station_event_model.py
本轮 B5-only repair 未要求重跑

git diff --check
PASS
```

仓库顶层无参数全量 `pytest` 已尝试，但被既有多服务 Python import layout 阻断：
API、Collector 与 V-PLC 测试均使用各自的顶层 `app` package，统一从 repo root collection
时出现 10 个 `ModuleNotFoundError: app`。本轮未修改这些服务或其 test bootstrap。

## 4. Contract coverage

| 合同项 | 实现状态 |
| --- | --- |
| MVP event types | PASS |
| frozen dataclass / mutation isolation | PASS |
| validator / serializer separation | PASS |
| payload/raw limits 与唯一错误码 | PASS |
| canonical identity / fingerprints | PASS |
| duplicate/conflict/raw_variant | PASS |
| NOK parent/detail/30003 policy | PASS |
| config/station/profile lineage | PASS |
| lifecycle derived output 8 fields | PASS |
| canonical result / detail-only projection | PASS |
| Collector/API/DB/Dashboard/V-PLC isolation | PASS |

## 5. Known limitations / recommendations

1. 本包是纯离线 contract implementation；historical config、decoder、payload schema 与
   state index 由调用方通过只读 snapshot/lookup 接口提供。本 Sprint 未实现 registry、
   persistence、retry、quarantine 或 runtime adapter。
2. canonical JSON 使用标准库实现并覆盖合同官方 numeric/fingerprint vectors；未来进入
   JavaScript/PostgreSQL 边界前，仍建议增加三端 exact-byte fixture。
3. 全仓多服务测试应继续按各服务既有独立工作目录/PYTHONPATH 运行；不要为本 Sprint
   修改 runtime package layout。

## 6. Scope proof

- `common/station_event/`：created。
- `tests/`：仅新增 `tests/test_station_event_model.py`。
- Collector/API/DB/Dashboard/Grafana/V-PLC：未修改。
- migration：未创建。
- tag：未创建。
- deploy：未执行。
- rollback drill：未执行。
- Phase-1 默认行为：未修改。
- commit / push：未执行。

## 7. Verification implementation HOLD repair

Verification implementation review 在
`docs/reports/sprint2_station_event_verification_matrix.md` 第 32 节记录五项 blocker。
本轮只修复这些 blocker，没有修改合同或接入 runtime：

1. historical config snapshot 在 stateful validation 中重新执行完整
   station/PLC/type/profile lineage；missing station 返回 `CONFIG_NOT_FOUND`，
   station/profile mismatch 返回 `EVENT_LINEAGE_INVALID`。
2. `30003/system_reserved` parent 不再在 `result=skip` 后提前返回；必须同时匹配
   line/PLC/station/boot/cycle/counter/unit/DMC。跨 station/cycle 与 future parent
   返回 `PARENT_EVENT_INVALID`；合法 same-cycle skip parent 仍保持 non-production
   isolated，不进入 ordinary defect/Pareto。
3. secondary detail 必须有 accepted primary，且 code 不得与 primary 或已有 secondary
   重复；重复返回 `DETAIL_CODE_DUPLICATE`。
4. `validated_nok_detail` evidence 必须继续解析 cited detail 的 accepted canonical
   `station_result(result=nok)` parent，并校验 direct predecessor 与 unit/DMC subject
   lineage；missing parent 返回
   `UPSTREAM_EVIDENCE_NOT_FOUND`，OK/non-accepted/mismatched parent 返回
   `UPSTREAM_EVIDENCE_INVALID`。
5. raw JSON 使用类别级 fail-closed 规则拒绝 image/WebP/PDF/octet-stream data URI、
   binary MIME、普通 key 下 decode 后为 WebP/PDF/高比例不可打印字节的 base64、
   binary/blob/file/pdf/attachment/content-type key hint，以及超过 4 KiB 后呈现高重复率
   的单行/多行 log-like string，统一返回 `RAW_CONTENT_FORBIDDEN`。正常短文本、DMC、
   station note 与合理长度非重复文本保持 accepted。明显 forbidden binary/data URI/
   base64 在超过 raw string limit 时仍优先 `RAW_CONTENT_FORBIDDEN`；无法归类为
   forbidden content 的普通超长文本保留既有资源错误码。

新增 focused tests 覆盖 valid/missing/mismatch lineage、reserved parent isolation、
primary/secondary code 去重、validated detail canonical parent、raw binary/image/log
bypass，以及对应合法正例。

## 8. Repair verification evidence

```text
.venv/bin/python -m compileall common tests
PASS

.venv/bin/python -m pytest -q tests/test_station_event_model.py
119 passed

.venv/bin/python -m pytest -q tests
207 passed

git diff --check
PASS
```

## 9. B5-only repair（2026-06-22）

Verification focused re-review 已确认 B1～B4 CLOSED，仅 B5 STILL OPEN。本轮没有修改
B1～B4、合同语义或任何 runtime/integration 路径，只补强公共 raw validation helper
与 B5 regression tests：

- WebP data URI 与普通 key WebP base64：reject。
- 普通 key PDF / generic binary base64：reject。
- `pdf/binary/blob/file` encoded payload 与 binary MIME hint：reject。
- 约 7 KiB 单行重复 token / repeated character：reject。
- normal JSON short strings、DMC、station note、ordinary message 与合理非重复文本：
  accept。

该轮 B5 repair 通过本地 tests 后进入 Verification B5-only focused re-review，并形成
下方第 10 节的 final repair 输入。ChatGPT PM 明确授权前仍不得 commit/push 或进入
integration。

## 10. B5 final repair（2026-06-22）

Verification B5-only re-review 已关闭 WebP、PDF/generic binary 与 ordinary-key binary
base64，只留下 B5-R1/R2。本轮只修复这两项：

- 使用 bounded zlib compression signal 检测 4～16 KiB 单行文本中的边界无关周期性
  重复；不再只依赖固定 32-character chunk。约 7 KiB 的非 32-byte 对齐周期片段与
  structured log fragment 均返回 `RAW_CONTENT_FORBIDDEN`。
- 对超过 raw string limit 的值，先执行有界 prefix/category scan：data URI、PDF、
  WebP、既有 image header 与高多样性 generic binary base64 可在最多 4096 encoded
  characters 的 sample 内分类，返回 `RAW_CONTENT_FORBIDDEN`；不完整 decode 巨大
  字符串。
- 单一重复字符等低多样性普通超长文本不会仅因“看起来像 base64 alphabet”被误判，
  继续返回 `RAW_STRING_BYTES_LIMIT`。短 note/message、DMC、`text/plain` 与合理
  非重复长文本继续 accepted。

该轮未修改 B1～B4、合同、event types 或 runtime/integration 路径；随后
Verification B5-final re-review 已 PASS。未获 ChatGPT PM 明确授权前仍不得
commit/push。

## 11. Reliability R-B2 / R-B4 focused repair（2026-06-22）

Verification B1～B5 已全部 CLOSED。Reliability focused implementation review 仅留下
R-B2/R-B4，本轮只修复这两个 blocker：

- R-B2：`_parent_matches()` 的统一 identity relation 增加 `config_hash`，因此同
  station/cycle 但跨 config 的 accepted skip parent 不能支持 `30003`，稳定返回
  `PARENT_EVENT_INVALID`。合法 same-config skip parent 仍 accepted，但 projection
  保持 non-production isolated，不进入 ordinary defect 或 Pareto。
- R-B4：`validated_nok_detail` 解析 accepted canonical parent 后复用同一个
  `_parent_matches()`，同时校验 parent 为 authoritative PLC/V-PLC
  `station_result(result=nok)`、parent/detail config 一致、source/actor authority
  一致，以及 primary code/origin 或 secondary origin relation。任一 mismatch 返回
  `UPSTREAM_EVIDENCE_INVALID`。
- duplicate/conflict/rejected parent、detail self-result、direct predecessor 和
  unit/DMC 既有 fail-closed 行为保持不变。

未修改 R-B3 duplicate detail-set、B5 raw validation、合同、event types 或任何
runtime/integration 路径。下一步仅需 Reliability focused re-review；Verification 只需
对 R-B2/R-B4 relation 做定向 sanity re-review，不重开 B1/B5。

## 12. Reliability R-B4 canonical role minimal repair（2026-06-22）

Reliability focused re-review 已关闭 R-B2、R-B3 与 B5，仅发现 canonical parent role
旁路。本轮只在共享 `_parent_matches()` 增加一个明确约束：

```text
parent.correlation.event_role == production_result
```

因此，即使 parent 同时满足 `event_type=station_result`、`result=nok`、accepted、
authority/config/code-origin relation，只要 role 为 `cycle_complete`、`diagnostic`、
`compatibility`、`None` 或缺失，`validated_nok_detail` 都 fail closed，返回
`UPSTREAM_EVIDENCE_INVALID`，且不产生 production outcome、ordinary defect 或 Pareto
projection。合法 `production_result` parent 继续 accepted。

R-B2 config isolation 语义未改变；共享 matcher 的合法 skip parent fixture 与跨 config
negative fixture 均通过。R-B3 duplicate detail-set 和 B5 raw validation 未修改。
下一步必须先交 Reliability focused re-review；通过后再做 Verification targeted
relation sanity check 与 Data Quality focused review。

## 13. Data Quality DQ-F1～DQ-F3 minimal implementation repair（2026-06-23）

Data Quality focused implementation review 当前为 HOLD。本轮只修复 DQ-F1、DQ-F2、
DQ-F3，没有修改合同、duplicate/conflict/raw_variant 裁决或任何 runtime/integration
路径：

1. `_parent_matches()` 在既有 line/PLC/station/boot/cycle/unit/DMC/config relation
   基础上增加 `profile_id` 与 `station_type` exact comparison。任一 mismatch 均
   `PARENT_EVENT_INVALID`。
2. `validated_nok_detail` cited detail 必须满足
   `correlation.event_role=nok_detail`，并通过 ordinary `station_nok` stateless
   canonical validation；compatibility、diagnostic、wrong role、missing role、
   non-accepted record、wrong parent relation 均 fail closed 为
   `UPSTREAM_EVIDENCE_INVALID` 或既有 missing/unavailable 语义。
3. 只要 historical snapshot 下的 event 携带 `raw_payload`，snapshot 必须提供 callable
   `decode_raw_payload`。decoder 缺失或抛出异常返回 `RAW_PARSE_ERROR`；raw-only 或
   decoded canonical JSON 与 normalized payload 不一致返回
   `RAW_NORMALIZED_MISMATCH`。rejected event 不产生 authoritative outcome、defect
   detail、compatibility/Pareto projection 或 projection eligibility。
4. 既有 raw_variant fixture 改为提供 normalized payload 与 exact historical decoder；
   不再依赖 raw-only fail-open。相同 canonical content、不同 raw fingerprint 仍保持
   `duplicate + raw_variant`。

新增/补强 tests 覆盖 parent profile/station type mismatch、cited detail
compatibility/diagnostic/cycle-complete/missing role、missing decoder、raw-only、decoder
exception、raw/normalized mismatch 与 rejected projection isolation。

本 Thread 只完成 Architecture implementation repair。Data Quality report 未修改；
下一步必须执行 Data Quality targeted re-review 与 Verification DQ-F1～F3 targeted
sanity check。两者通过且 PM 明确授权前，仍不得 commit/push。
