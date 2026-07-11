# Sprint 3 Dashboard frontend typecheck/build validation planning gate report

Date: 2026-07-11

报告名称：
Sprint 3 Dashboard frontend typecheck/build validation planning gate report

任务名称：
Freeze an exact, non-runtime validation lane for the current Dashboard baseline using package-local TypeScript typecheck and Next.js production build commands, with strict workspace-drift detection and generated-artifact cleanup

执行 Thread：
Architecture / Integration

风险等级：
Level 1 — planning-only, frontend validation boundary

结论：PASS WITH RECOMMENDATIONS

本 gate 只完成现状审计、风险识别与未来命令执行范围冻结。它不授权运行 `npm run typecheck`、`npm run build`、tests、browser/manual smoke、API/DB/Postgres、Docker、server/runtime、Collector、V-PLC、real PLC、stage、commit、push、deploy、tag 或 rollback，也不授权修改任何 frontend production/test/config/package 文件。

## 1. Baseline and recovery

本 gate 第一动作执行了 read-only Git recovery。

```text
branch:
main

HEAD:
51c9e9eb0743d0451fb578d56ff8b4016d9e6565
51c9e9e Sync Dashboard stale-data regression status

origin/main:
51c9e9eb0743d0451fb578d56ff8b4016d9e6565

cached diff:
empty

tracked working-tree diff:
M .gitignore
```

Live baseline 与 PM 授权时状态一致。当前 working tree 只有已知 external artifacts：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/
```

本 planning report 创建后，它是本 gate 唯一新增的项目文件，保持 untracked、未 stage。

## 2. Required context reviewed

已读取并遵守：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`

本 gate 还只读审计了：

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/next.config.ts`
- tracked `.gitignore` at `HEAD`
- frontend package/config Git history
- current frontend top-level generated-artifact state

## 3. Scope

### In scope

- 确认当前 `frontend/package.json` 中 typecheck/build 的唯一权威命令；
- 确认当前 package、lockfile、TypeScript、Next.js 配置及 authoring-time Node/npm 环境；
- 审计历史 `npm run build` 配置漂移风险；
- 冻结 typecheck 与 build 的执行顺序、命令 allowlist、前后快照、通过条件、生成物清理范围和 stop conditions；
- 给出未来 Verification execution gate 的精确权限边界和报告要求。

### Explicitly out of scope

- 不运行 `npm run typecheck`；
- 不运行 `npm run build`；
- 不运行 `npm test`、focused tests 或 full frontend suite；
- 不运行 `npm ci`、`npm install`、`npm update`、`npm audit fix`；
- 不修改 `frontend/package.json`、lockfile、`tsconfig.json`、`next.config.ts`、source 或 tests；
- 不创建或修改 browser test、Playwright、server、API mock 或 runtime configuration；
- 不启动 frontend dev/prod server；
- 不进行 browser/manual smoke；
- 不连接 API、Postgres、Docker、V-PLC 或 real PLC；
- 不修改 durable status docs；
- 不 stage、commit 或 push。

## 4. Current frontend validation authority

### 4.1 Package-local scripts

`frontend/package.json` 当前冻结：

```json
{
  "scripts": {
    "test": "vitest run --environment jsdom",
    "typecheck": "tsc --noEmit",
    "build": "next build"
  }
}
```

本 gate 的未来执行只允许：

```text
npm run typecheck
npm run build
```

不得改写为直接调用其他 TypeScript/Next CLI 参数，不得增加 `--force`、`--no-lint`、环境变量、experimental flag 或其他脚本。

### 4.2 Dependency/config baseline

当前 package authority：

```text
Next.js: 16.2.10
React: 19.2.7
React DOM: 19.2.7
TypeScript: 6.0.3
package-lock lockfileVersion: 3
```

Authoring-time local command environment：

```text
Node: v22.23.0
npm: 11.17.0
```

Future execution Thread 必须重新记录 live Node/npm 版本。版本差异本身不是自动 blocker，但若命令失败、产生配置漂移或与 lockfile/package engine 不兼容，必须报告实际证据，不得通过安装或升级依赖自行修复。

`frontend/package.json`、`frontend/package-lock.json`、`frontend/tsconfig.json` 与 `frontend/next.config.ts` 自 `896c2d1 Add accepted-events Dashboard frontend` 后没有后续提交修改。

### 4.3 Existing dependency environment

`frontend/node_modules/` 已存在，是早先授权 `npm ci` 产生的 local dependency artifact。当前 package/config 没有后续 commit 变化，因此未来第一条 typecheck/build validation lane 推荐复用现有环境，不重复运行 `npm ci`。

如果未来执行发现：

- `node_modules/` 缺失；
- dependency resolution 错误；
- package tree 与 lockfile 不一致导致命令不可运行；

则该 execution gate 必须报告 `HOLD`，由 PM 决定是否单独打开 dependency environment preparation gate。不得在 typecheck/build gate 内自动运行 `npm ci` 或修复 package state。

## 5. Historical risk findings

### 5.1 Prior build mutated tracked TypeScript configuration

历史 Dashboard implementation Verification review 曾因以下问题返回 HOLD：

```text
npm run build mutated frontend/tsconfig.json by adding "incremental": true
```

该问题后来通过 Architecture repair 和 Verification re-review 关闭。当前 tracked `frontend/tsconfig.json` 已包含：

```json
"incremental": true
```

因此当前 build 不应再次需要同一修改。但历史证据说明，未来验证不能只看命令 exit code；必须同时证明 tracked frontend 工作区没有被 Next.js/TypeScript 自动改写。

### 5.2 Generated artifacts are not covered by tracked .gitignore

当前 tracked `.gitignore` 没有忽略以下候选生成物：

```text
frontend/.next/
frontend/tsconfig.tsbuildinfo
frontend/next-env.d.ts
frontend/out/
frontend/coverage/
```

在 planning 时，上述路径均不存在。未来命令可能短暂生成：

- `npm run typecheck`：可能生成 `frontend/tsconfig.tsbuildinfo`，因为 `incremental: true`；
- `npm run build`：预期生成 `frontend/.next/`，并可能生成 `frontend/next-env.d.ts` 和 `frontend/tsconfig.tsbuildinfo`。

这些生成物不是 implementation changes，也不能进入 Git commit。未来 execution gate 必须先记录、再仅按精确路径清理，并证明清理后 frontend 状态恢复到 preflight 状态。

### 5.3 Current TypeScript include depends on generated Next types

`frontend/tsconfig.json` 包含：

```text
.next/types/**/*.ts
.next/dev/types/**/*.ts
```

当前 `.next/` 不存在。`tsc --noEmit` 必须在该状态下仍能正确通过；不得把预先运行 build 当作 typecheck 的隐藏前置条件。未来顺序必须是 typecheck first、build second。

## 6. Approaches considered

### Approach A — in-place sequential validation with strict snapshots and exact generated-artifact cleanup

在当前 main checkout 中：

1. 记录 preflight；
2. 运行 package-local typecheck；
3. 审计 tracked drift 与生成物；
4. 精确清理 typecheck 生成物；
5. 再运行 package-local build；
6. 审计 tracked drift 与生成物；
7. 精确清理 build 生成物；
8. 证明最终 frontend 状态与 preflight 一致。

Advantages：

- 使用真实当前 checkout 和现有 dependency environment；
- 命令与用户后续实际开发环境一致；
- 最小范围、无需 npm install/network；
- 能直接捕获 Next.js 对 tracked config 的自动修改；
- 容易执行 exact command/cleanup audit。

Risks：

- build/typecheck 会在本地生成未跟踪产物；
- 若 tracked config 自动变化，working tree 会进入 HOLD 状态并等待 PM 处理；
- cleanup 必须严格按精确路径，不得 broad clean。

### Approach B — rerun `npm ci` before typecheck/build

Advantages：

- 重建 dependency environment；
- 提高 lockfile-based reproducibility。

Disadvantages：

- 超出本 gate 的 typecheck/build 核心目标；
- 修改整个 `frontend/node_modules/`；
- 可能需要 network/cache，并引入 install warnings/failures；
- package/config 自 `896c2d1` 后未变化，没有证据要求重新安装；
- dependency repair 与 compile/build validation 被混在一个 gate。

### Approach C — isolated temporary worktree/copy with separate dependency install

Advantages：

- 不污染当前 checkout；
- 可作为 future CI-like lane。

Disadvantages：

- 需要额外 worktree、dependency installation 或 node_modules sharing policy；
- 验证环境与当前实际 checkout 不完全相同；
- 对两个 package-local命令而言成本过高；
- 增加 cleanup 和 provenance 风险。

### Decision

**Approach A is selected and recommended.**

当前目标是验证现有 baseline，而不是重建开发环境或设计 CI。未来 Verification Thread 应在当前 checkout 执行两个命令，但把每一步的 tracked drift 与 generated artifacts 作为一等验证对象。

## 7. Future execution gate classification

Recommended future gate：

```text
Level 1 — Dashboard frontend typecheck/build validation execution
Owner: Verification
```

该 gate 是 commands-only validation。默认 implementation allowlist 为空：

```text
changed source/config/test files:
none expected
```

唯一允许的 filesystem mutation 是命令短暂生成并随后精确清理的已知 generated artifacts。

### Read-only reference files

```text
frontend/package.json
frontend/package-lock.json
frontend/tsconfig.json
frontend/next.config.ts
frontend/src/**
docs/reports/sprint3_dashboard_frontend_typecheck_build_validation_plan.md
```

`frontend/src/**` 仅用于 compiler/build 读取，不授权修改。

## 8. Future exact command sequence

Future Verification Thread 必须从项目根目录开始。

### 8.1 Read-only preflight

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
git log -1 --format='%H %s'
git rev-parse origin/main
git diff --name-only
git diff --cached --name-only
node --version
npm --version

git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
```

Expected preflight at authorization time：

```text
HEAD == origin/main == 51c9e9eb0743d0451fb578d56ff8b4016d9e6565
cached diff empty
frontend status excluding node_modules empty
no generated-artifact candidates present
```

A later docs-only commit may move live HEAD. The future PM prompt must supply the then-current expected baseline. The execution Thread must use that live PM-authorized value rather than blindly requiring `51c9e9e`.

### 8.2 Typecheck lane

Run exactly：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend
npm run typecheck
```

Expected command semantics：

```text
tsc --noEmit
exit code 0
```

Immediately after typecheck：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git diff --name-only -- frontend
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
```

Typecheck PASS conditions：

- `npm run typecheck` exit code 0；
- no tracked frontend diff；
- no unexpected untracked frontend file；
- only `frontend/tsconfig.tsbuildinfo` may appear as an allowed transient artifact；
- no `.next/`、`next-env.d.ts`、`out/`、`dist/` 或 `coverage/` from typecheck；
- cached diff remains empty。

After evidence capture, if and only if it was absent in preflight and generated by typecheck, exact cleanup is allowed：

```bash
rm -f /Users/chenjie/Documents/MES/edge-mes-demo/frontend/tsconfig.tsbuildinfo
```

Then verify：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
```

If typecheck fails or tracked drift exists, stop. Do not run build.

### 8.3 Build lane

Only after the typecheck lane and its cleanup verification pass, run exactly：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend
npm run build
```

Expected command semantics：

```text
next build
exit code 0
production build completes
```

Immediately after build：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git diff --name-only -- frontend
git diff -- frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/next.config.ts
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
```

Build PASS conditions：

- `npm run build` exit code 0；
- no tracked frontend diff；
- `frontend/package.json` unchanged；
- `frontend/package-lock.json` unchanged；
- `frontend/tsconfig.json` unchanged；
- `frontend/next.config.ts` unchanged；
- no unexpected untracked frontend file；
- allowed transient artifacts are limited to:
  - `frontend/.next/`
  - `frontend/next-env.d.ts`
  - `frontend/tsconfig.tsbuildinfo`
- no `frontend/out/`、`frontend/dist/` 或 `frontend/coverage/` unless the current package/config is separately changed by a future authorized gate；
- cached diff remains empty。

After evidence capture, only paths absent in preflight and generated by build may be cleaned：

```bash
rm -rf /Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next
rm -f /Users/chenjie/Documents/MES/edge-mes-demo/frontend/next-env.d.ts
rm -f /Users/chenjie/Documents/MES/edge-mes-demo/frontend/tsconfig.tsbuildinfo
```

Forbidden cleanup commands：

```text
git clean -fd
git clean -fdx
rm -rf frontend
rm -rf frontend/node_modules
broad find -delete
```

### 8.4 Final restoration audit

After exact cleanup：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
git diff --name-only
git diff --cached --name-only
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
```

Final PASS requires：

- no new tracked or untracked frontend artifact except pre-existing `frontend/node_modules/`；
- project-level tracked diff remains only the pre-existing external `.gitignore`；
- cached diff empty；
- external dirty artifacts unchanged；
- no stage/commit/push。

## 9. Acceptance matrix

| Case | Required evidence | PASS condition |
| --- | --- | --- |
| baseline | live HEAD/origin and preflight status | match PM-authorized baseline; cached empty |
| dependency authority | package/lock/scripts read-only | no install or package mutation |
| typecheck command | complete command output and exit code | `tsc --noEmit`, exit 0 |
| typecheck drift | immediate Git/generated-artifact snapshot | no tracked drift; only optional tsbuildinfo |
| typecheck cleanup | exact path cleanup and recheck | frontend clean excluding node_modules |
| build command | complete command output and exit code | `next build`, exit 0 |
| tracked config safety | package/lock/tsconfig/next config diff | all unchanged |
| build artifacts | immediate generated-artifact inventory | only `.next`, next-env, tsbuildinfo |
| build cleanup | exact path cleanup and final snapshot | generated artifacts absent |
| Git safety | final status/cached | no new project diff; cached empty |
| scope | command log | no tests/browser/API/DB/Docker/runtime/Git writes |

## 10. Stop conditions and HOLD rules

Future Verification Thread must stop and report `HOLD` when any of the following occurs：

- live baseline conflicts with PM authorization；
- cached diff is non-empty before execution；
- frontend has pre-existing tracked/untracked state other than `node_modules/`；
- `npm run typecheck` exits non-zero；
- typecheck modifies any tracked frontend file；
- typecheck generates anything beyond optional `tsconfig.tsbuildinfo`；
- exact typecheck cleanup fails；
- `npm run build` exits non-zero；
- build modifies `package.json`、lockfile、`tsconfig.json`、`next.config.ts` or any source/test file；
- build requires accepting an automatic config rewrite；
- build generates unexpected paths outside `.next/`、`next-env.d.ts`、`tsconfig.tsbuildinfo`；
- cleanup requires broad delete or Git restore/reset；
- `npm ci`、install、package/config repair、source repair or test modification becomes necessary；
- external dirty artifacts change；
- any staging occurs。

If a command fails due to source/config/type errors：

- do not edit production/test/config files；
- do not rerun with relaxed flags；
- do not suppress diagnostics；
- return `HOLD` with concise failing output and implicated exact files；
- PM must open a separate repair planning gate。

If build mutates a tracked file：

- capture exact diff；
- do not automatically `git restore`、reset or overwrite the file；
- report `HOLD` and wait for PM repair authorization。

Allowed transient generated artifacts may still be cleaned by the exact commands in section 8 after failure evidence is captured, provided no tracked file is touched.

## 11. Explicit exclusions

The future execution gate excludes：

```text
.gitignore
frontend/node_modules/
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Also excluded：

- source/test/config/package changes；
- full/focused frontend tests；
- browser/manual smoke；
- frontend server start；
- API tests；
- DB-backed tests；
- Postgres/SSH tunnel；
- Docker/docker compose；
- Collector/V-PLC/real PLC；
- docs/status sync；
- stage/commit/push/tag/deploy/rollback。

Forbidden Git commands remain：

```text
git add .
git add -A
git add docs/
git clean -fd
git clean -fdx
git reset --hard
git restore .
```

## 12. Future Verification report requirements

The execution Thread must return the PM Rules window report format and include：

```text
报告名称：
Sprint 3 Dashboard frontend typecheck/build validation execution report

任务名称：
Execute package-local frontend typecheck and production build with strict workspace-drift validation

执行 Thread：
Verification

结论：
PASS / PASS WITH RECOMMENDATIONS / HOLD

Scope:
- reviewed files:
- commands run:
- changed files:
- generated artifacts observed:
- cleanup performed:
- explicitly not touched:

Evidence:
- live baseline:
- node/npm:
- typecheck:
- post-typecheck drift:
- build:
- post-build drift:
- final frontend status:
- final cached diff:

Blockers:
- none / exact blocker

Recommendations:
- none / non-blocking items

Next gate:
- eligible for:
- PM approval required before:

Thread 输出 / 上下文评估:
- 本次输出长度：短 / 中 / 长
- 当前 Thread 是否建议继续：yes / no
- 下一轮是否建议新开 Thread：yes / no
- 理由：
```

A `PASS WITH RECOMMENDATIONS` is acceptable only when both commands pass and workspace restoration is exact. A failed command, tracked drift, unexpected artifact or incomplete cleanup is a blocker and must be `HOLD`。

## 13. Blockers

None for this planning gate.

The current package-local scripts are explicit, package/config history is stable since `896c2d1`, and the prior `tsconfig.json` mutation has already been incorporated into tracked configuration. The main planning concern is generated-artifact and config-drift control during future execution。

## 14. Recommendations

1. Open a new Verification Thread for the exact commands-only execution gate described above。
2. Reuse the current `node_modules/` environment; do not bundle `npm ci` into this gate。
3. Run typecheck first and stop before build on any failure or tracked drift。
4. Treat build success plus any tracked config mutation as `HOLD`, not PASS。
5. Keep browser/manual smoke as the next separate gate after typecheck/build closes。
6. After execution and review PASS, perform a separate docs/status sync; no implementation commit should exist because no source/config changes are expected。

## 15. Next gate

Eligible for：

```text
Level 1 — Dashboard frontend typecheck/build validation execution
Executing Thread: Verification
Commands:
cd frontend && npm run typecheck
cd frontend && npm run build
plus exact pre/post audits and generated-artifact cleanup from this plan
```

Not automatically authorized：

- command execution；
- `npm ci` or dependency repair；
- source/config/package/test repair；
- full tests；
- browser/manual smoke；
- API/DB validation；
- docs/status sync；
- stage/commit/push；
- deploy/tag/rollback。

PM must separately authorize the Verification execution gate。

## 16. Thread output / context assessment

Thread 输出 / 上下文评估：

- 本次输出长度：中
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：planning 已冻结 commands、artifact cleanup 和 HOLD 规则；execution 应由新的 Verification Thread 独立完成，避免 Architecture planning 权限被误扩展为命令执行或修复权限。
