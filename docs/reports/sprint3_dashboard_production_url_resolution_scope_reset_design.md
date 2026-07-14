# Sprint 3 Dashboard Production URL Resolution Scope Reset Design

日期：2026-07-14

决策角色：ChatGPT PM

状态：PM APPROVED / EXECUTED

## 1. 背景与问题

Dashboard production URL-resolution 分支原本只需要证明：accepted-events 页面在有效配置下向正确 API origin 发出唯一请求，并在错误配置或错误响应下 fail closed。

后续 planning/review 将该目标扩展为包含 private parent、run-root object binding、manifest terminal transaction、57/76 字段冻结回读、目录 fsync telemetry 和完整 failure relation matrix 的强审计取证系统。该扩展没有直接增加 Dashboard URL 正确性的业务证明，却持续制造新的静态 blocker。

本设计终止该目标漂移，并重新冻结与 Edge MES Demo 阶段相匹配的 assurance level。

## 2. 方案裁决

### 方案 A：继续完成现有强审计框架

拒绝。它要求继续闭合 76 字段关系矩阵，存在无自然终点的静态审查，与一次本地 synthetic Dashboard URL 验证不成比例。

### 方案 B：业务证据最小化

采用。保留 URL resolver、absolute request、strict response parser 和 UI fail-closed 设计；使用 focused tests、typecheck、build 和一次受控 local synthetic runtime smoke 证明关键事实。只有可能导致 false PASS、安全清理失败或越界删除的问题才是 blocker。

### 方案 C：完全取消 runtime smoke，仅依赖单元测试

拒绝。它不能证明构建后的 Next server 在真实运行时使用配置 origin 并完成端到端 HTTP 请求。

## 3. 冻结目标

> 构建后的 accepted-events Dashboard 在 local synthetic 环境中，使用经过验证的 API origin，向精确 accepted-events endpoint 发出一次请求，接收严格 fixture 响应并安全结束；无效配置或异常响应不能产生 ready/成功结论。

## 4. 成功验收条件

以下十项必须全部成立：

1. URL query 在读取 API origin 和发起请求前完成验证；invalid query 不调用 resolver，不发请求。
2. resolver 只接受冻结的 `local`、`container`、`production` profile 与各自 canonical origin；错误配置返回统一安全消息且不泄漏原值。
3. API client 只接受 branded trusted origin，并构造 absolute `GET /api/v2/production/accepted-station-events`。
4. 请求只包含 `line_id`、`start_time`、`end_time`、`limit`、`cursor`；不重试、不 fallback、不携带 credentials、不跟随 redirect。
5. local runtime smoke 中 capture server 恰好收到一次目标请求，method、path、host 和 query 与预期完全一致。
6. capture server 返回严格 synthetic 22-key accepted fact fixture；Dashboard HTML 包含该 fixture 的可见业务 marker。
7. 错误配置、错误 response 或 incomplete response 不得产生 ready/成功页面，也不得产生第二个请求。
8. runtime smoke 只终止本轮记录的 capture PID 和 Next PID；不得按端口选择或终止未知进程。
9. runtime smoke 结束后 capture 与 Next 端口均释放；构建生成物仅在身份和路径都属于本轮时清理。
10. 报告限定为 local synthetic transport evidence，不声称 production DNS/TLS/egress、真实 API、真实 DB 或真实 production fact 已验证。

## 5. Blocker 规则

一个 finding 只有满足至少一项时才可阻断本轮 gate：

- 可能把错误 origin、endpoint、method 或 query 判为 PASS；
- 可能把缺失、不完整或 schema-invalid response 判为 ready/PASS；
- 可能在失败后继续使用 stale production truth；
- 可能遗留本轮启动的进程或监听端口并污染后续运行；
- 可能终止未知进程，或删除/覆盖不属于本轮的文件系统对象；
- 可能把 synthetic evidence 表述为真实 production fact、production deployment 或 DB-backed evidence。

以下问题默认是 recommendation：诊断字段分类、retained archive 全局唯一性、不会改变 PASS/HOLD 的 failure telemetry 关系完备性、unsupported filesystem telemetry 的进一步细分，以及不会改变最终结论的日志或字段格式差异。

## 6. 证据分层

### 6.1 终局权威证据

仅以下事实决定 PASS/HOLD：resolver result、target request count、exact method/path/query/origin、fixture bytes/schema 与 response completion、Dashboard expected marker、capture/Next owned PID cleanup、final port release、command exit status。

### 6.2 诊断证据

manifest parent fsync、目录 inode、完整 failure record、archive uniqueness、详细 quarantine 状态和其他 failure telemetry 可以记录，但不得在没有 false-PASS 或越界安全影响时扩大为本轮 blocker。

## 7. 对现有 findings 的裁决

- `DQ-RUNTIME-OPTIONC-D7`：降级为 recommendation/backlog。parent-fsync 分类不是 URL runtime success authority。
- `DQ-RUNTIME-OPTIONC-D8`：不再要求闭合完整 76 字段 relation matrix；只保留与 blocker 规则直接相关的 request/response/process/port/filesystem ownership 关系。
- `DQ-RUNTIME-OPTIONC-D9`：保持 observation；本轮 fixture 固定且很小，不开展 transport redesign。
- `DQ-RUNTIME-D2-3`、`DQ-URL-D3`：继续 carry forward，不阻断 local synthetic gate。

## 8. 执行边界

允许：治理文档更新、focused frontend tests、typecheck、build、一次 local synthetic runtime smoke、execution report 与 `docs/current_status.md` 同步。

不允许：Collector、DB、API、schema、migration、V-PLC、Docker、Grafana、deployment、production config、真实 API/DB connectivity、accepted fact contract 变化、通用取证框架重建，以及未经用户明确授权的 stage/commit/push/tag/deploy。

## 9. Gate 与停止条件

- focused tests/typecheck/build 失败：HOLD，先定位真实产品问题。
- runtime smoke 违反任一成功条件：HOLD，只修与该条件直接相关的最小问题。
- 十项全部通过：Dashboard production URL-resolution local synthetic gate `PASS WITH RECOMMENDATIONS`。
- reviewer 不得仅因新增诊断字段完备性要求重新打开本 gate；范围扩大必须由 PM 明确批准。
