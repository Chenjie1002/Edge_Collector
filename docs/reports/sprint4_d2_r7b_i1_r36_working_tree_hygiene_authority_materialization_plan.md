# Sprint 4 D2-R7B-I1 R36 Working Tree Hygiene and Authority Materialization Plan

## 1. 报告身份

- 任务：D2-R7B-I1 R36 — Ignore Frontend Build Noise, Inventory Remaining Untracked Assets, and Prepare Exact Authority Commit Batches
- 执行 Thread：Architecture / Integration
- Authority：`PM-D2-R7B-I1-R36-WORKTREE-HYGIENE-AUTHORITY-MATERIALIZATION-260729-2221`
- Authority properties：`AUTHORIZED ONCE / LOCAL FILE WRITES ONLY / EXACT .gitignore EDIT / PRE_AUTHORITY LOCAL REPAIR WINDOW MAX 2 / EXECUTION LOCK REQUIRED / NOT REUSABLE`
- Report delivery：`REPOSITORY_REPORT_WITH_ARTIFACTS`

## 2. 结论

`PASS / HYGIENE_INVENTORY_READY_FOR_PM_GIT_CLOSEOUT`

- MVP classification：`MVP-ALIGNED`
- Blockers：none
- 本任务仅建立 working-tree hygiene、durable inventory 和 future exact Git authority batches。
- 本结果是 `WRITTEN`，不是 `ACCEPTED / VERIFIED / STAGED / COMMITTED / PUSHED`。

## 3. Scope 与 authority boundary

本任务只修改 `.gitignore` 并创建七个 exact R36 durable outputs。没有修改
`pm_operating_rules.md`、`current_status.md`、`roadmap.md`、四个 Batch C tracked dirty
artifacts、source、test、config、runtime 或历史文件。

明确未执行：

- network、SSH、remote read/mutation；
- Docker、Compose、DB、API、PLC、V-PLC、production validation；
- file delete、move、archive、cleanup；
- `git add`、stage、commit、push、tag、clean、stash、reset、restore；
- `.git/info/exclude`、global excludes 或 Git config 修改。

R35 只作为 accepted durable authority 重新验证；R36 没有刷新或扩大 remote/runtime/
production claims。

## 4. Fresh Git baseline

compact tracked recovery 精确通过：

```text
root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: ac33e6bae449ecdd9b77a53daaf7271f14133000
origin/main: ac33e6bae449ecdd9b77a53daaf7271f14133000
HEAD^: 66563677d3d1129fbc79c2c284b5f6d8b62f1932
ahead / behind: 0 / 0
cached: empty
git diff --check: PASS
git diff --cached --check: PASS
```

tracked dirty set 精确保持六项：

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

其中只有 `.gitignore` 属于本任务写权限；其他五项保持既有 bytes。

## 5. Frozen authority identities

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `.gitignore` before | 891 | `a302455543639fa197b725008240dc24c460505b9f09a0a4cd662bb6ba0bb442` |
| `docs/thread_handoff/pm_operating_rules.md` | 49170 | `a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5` |
| R35 report | 3002 | `133c303e6a556b4be9e2c9535a10ff3b5a9dd06bf5b6f3fca1f272d707b75ee0` |
| R35 local terminal | 52496 | `41c28d5c22e9c934c4edfeea0b07a1a84ec893b2ce9918d2bb17f2808afc7ce7` |
| R35 post terminal | 72307 | `135e66854fc032ceddc81ce6fa0cf28b51c90efd081f7f6c15e9e9299295e618` |
| R35 manifest | 973 | `51e172a2c5bc3f9671187dc560565c9423368741fd67281b57329edd2795d244` |

R35 revalidation：

```text
status: PASS
classification: ACTIVATED
STATIC_MAPPING_INITIALIZED: true
RUNTIME-LOADED: NO
PRODUCTION-ACCEPTED: NO
manifest: 6/6 OK
```

## 6. Pre-ignore machine capture

`git status --porcelain=v1 -z --untracked-files=all` 的原始 13,877 条没有打印到
terminal；只保存 canonical aggregate facts：

| Group | Count |
| --- | ---: |
| all untracked | 13877 |
| `frontend/node_modules/` | 12252 |
| `frontend/.next/` | 1277 |
| `docs/reports/` | 307 |
| `docs/thread_handoff/` | 38 |
| remaining frontend | 2 |
| remaining top-level docs | 1 |

补充 identities：

```text
raw porcelain bytes: 1046501
raw porcelain SHA-256: 286424545a431a0baf8900e39c1fdc4c9cfe4e587ab3e5c63856048463571085
sorted untracked NUL SHA-256: 3e5469c0f5f44cb642c222ef7f4744fc4d8d8f60b79db72b7f187cf94b6f5fb4
```

remaining frontend 是 `frontend/next-env.d.ts` 与
`frontend/tsconfig.tsbuildinfo`；top-level docs 是
`docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`。

## 7. Exact `.gitignore` edit

原内容和既有未提交修改全部保留，只在末尾追加一次：

```gitignore
# Frontend dependencies and build output
frontend/node_modules/
frontend/.next/
frontend/tsconfig.tsbuildinfo
```

post identity：

```text
bytes: 1002
SHA-256: b23d176a4e84628fd1afdb849fa6b8761c291664610c8cff35c60175852f133c
exact block occurrences: 1
exact block is suffix: true
```

`git check-ignore -v` 分别证明 `node_modules`、`.next`、`tsconfig.tsbuildinfo`
被 exact rules 忽略；`frontend/next-env.d.ts` return code 为 1，仍 untracked/not ignored。

以下宽泛规则均不存在：

```text
frontend/
docs/
docs/reports/
docs/thread_handoff/
frontend/next-env.d.ts
```

## 8. Post-ignore pre-output capture

```text
all untracked: 347
status entries: tracked dirty 6 / untracked 347
raw porcelain bytes: 32278
raw porcelain SHA-256: 93c94ab4033eb8d6425118672537daf35d5ddfbdcffeb3aee2a390d9abb49520
sorted untracked NUL SHA-256: 1c36f320808fd7585089cd116ee45cff9f2bc8f9736900f8212fdc21560656d7
```

可见性减少精确为：

```text
12252 node_modules
+ 1277 .next
+ 1 tsconfig.tsbuildinfo
= 13530 generated files
```

`git ls-files --ignored` 还会发现 package-internal 早已被内部规则忽略的路径，因此它只
作为 live diagnostic；visibility reduction authority 是 append 前后的 frozen Git status
captures。没有用宽泛规则凑数。

## 9. Execution Lock 与 repair window

- runner：strict UTF-8 / AST PASS；
- Git subprocess：参数数组；
- `shell=True`、shell command string、`os.system`：absent；
- bytecode：disabled；
- preliminary/locked/final runner identity：
  `40359` bytes /
  `079d21f3d463e9edd176580467e048d1ed06f67f5ac083c71452fc378ad3c7a1`；
- repair cycles：`1 / 2`；
- Execution Lock：`SEALED`；
- final inventory executions：`1 / 1`。

Repair cycle 1 是机械 harness correction：live ignored discovery 包含追加规则前已被
package-internal ignore 隐藏的 paths；修正后仍以 frozen pre/post status counts 为
visibility authority。没有改变 classification、authority seeds、batch boundaries、
allowlist 或 PASS/HOLD semantics。

Seal 后 runner、classification rules、authority seeds 与 batch boundaries 未修改。

## 10. Durable inventory

`untracked_durable_inventory.tsv` 精确列出 post-ignore 347 个 non-R36 untracked
paths；R36 自身 report/evidence 被 self-excluded，`node_modules/.next` 未展开。

TSV columns 精确为：

```text
path
bytes
sha256
file_type
symlink
classification
reason
authority_reference
```

结果：

| Classification | Rows |
| --- | ---: |
| `CURRENT_AUTHORITY_KEEP_AND_COMMIT` | 46 |
| `HISTORICAL_DOC_ARCHIVE_REVIEW` | 300 |
| `GENERATED_FILE_REVIEW` | 1 |
| `UNCLASSIFIED_BLOCKER` | 0 |

Coverage：

```text
rows: 347
unique paths: 347
sorted: true
coverage: 347/347
duplicate classifications: 0
unclassified: 0
```

`frontend/next-env.d.ts` 保持 `GENERATED_FILE_REVIEW`；R36 不决定 commit 或 ignore。

## 11. Current authority closure

Closure 只从 frozen exact seeds 和递归验证的 manifest members 建立，不按目录相似性、
文件名前缀或 `docs/reports/` 自动纳入。

```text
closure paths: 91
seed manifests verified: 9
verified manifest members: 79
all members exist/hash match: true
```

Closure 包含：

- `.gitignore` 与 `pm_operating_rules.md`；
- R31 planning report；
- R32 package/source manifests、Phase 1 authority、scope-reset accepted image
  reconciliation closure；
- R33 report/manifest closure；
- R34、R34-R1、R34-R2 report/manifest closure；
- R35 report/manifest closure；
- manifest 直接绑定的 committed package source paths。

所有未被该 exact closure 证明的历史 reports/evidence/handoffs 进入人工 archive/keep
review，不被猜测为 current authority。

## 12. Exact authority materialization batches

| Batch | Path count | Purpose |
| --- | ---: | --- |
| A | 2 | `.gitignore` + `pm_operating_rules.md` governance/ignore |
| B | 89 | exact current activation authority closure（A 两项除外） |
| C | 4 | pre-existing tracked dirty reconciliation |
| D | 300 | historical documentation/execution/review evidence |
| E | 1 | generated/local review（`frontend/next-env.d.ts`） |

Batch C 精确四项，未自动并入 A/B：

```text
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
```

Batch properties：

```text
A-E disjoint: true
overlap: 0
inventory covered exactly once: 347/347
SAFE_TO_DELETE claims: 0
```

D 只使用 `ARCHIVE_REVIEW_REQUIRED / KEEP_REVIEW_REQUIRED` 语义；E 使用
`KEEP_REVIEW_REQUIRED`。每个 batch 的 `stage_authority_required`、
`commit_authority_required`、`push_authority_required` 均为 `true`，表示未来必须另获
授权，不是本任务已授予。

## 13. Artifact identities before report/terminal manifest closeout

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `run_inventory.py` | 40359 | `079d21f3d463e9edd176580467e048d1ed06f67f5ac083c71452fc378ad3c7a1` |
| `untracked_durable_inventory.tsv` | 132983 | `32959bde73c53076d4908f392c6b3f3f785f5413274018da862a8794c64ca9f9` |
| `generated_noise_summary.json` | 4571 | `18c257937e98bb70e00e6c23dd1bbea7ebc4955c0f79445bd5f53b2f3841c10f` |
| `authority_materialization_plan.json` | 122377 | `4d73092bb058ff2643ce9092327846ec41e2c12b10468e86ff6739cb514f8705` |

Final report、terminal 和 self-excluded six-entry manifest identities 由 manifest 与最终
窗口报告给出。

## 14. Allowlist 与 forbidden-action audit

Exact allowed paths：

```text
.gitignore
docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/run_inventory.py
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/inventory_terminal.json
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/untracked_durable_inventory.tsv
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/generated_noise_summary.json
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/manifest.sha256
```

Counters：

```text
allowlist violations: 0
network/remote/Docker/DB/API/PLC: 0
Git mutations: 0
delete: 0
move: 0
cleanup/archive: 0
```

## 15. Blockers 与 recommendations

Blockers：none。

Recommendations：

1. ChatGPT PM 必须从 repository exact paths 读取本报告与 artifacts，先完成 durable
   intake；不能把 Chat summary 当成 authority。
2. 未来 Git closeout 必须按 A–E 独立评估并重新授权 exact paths；不得 broad-stage。
3. Batch D/E 只能人工 review；本任务没有 `SAFE_TO_DELETE` 结论。
4. `frontend/next-env.d.ts` 的 keep/ignore 决定留给独立 PM review。

## 16. MVP 路径一致性

- approved MVP deliverable：把已经支持 package-closed Collector activation 的 current
  authority chain materialize 为可审查的 exact commit batches，同时隔离 frontend
  generated noise 和历史证据。
- minimum invariant：不丢失 current authority、不把历史/生成文件猜成可删除、不把
  local hygiene PASS 写成 runtime/production PASS。
- 新产品能力、threat model、runtime topology、audit/forensics subsystem：none。
- task inflation：no；本任务只形成一次性 inventory/plan，不替代产品验证。
- classification：`MVP-ALIGNED`。

## 17. Next gate 与 stop point

唯一 next gate：

```text
R36 report and artifacts WRITTEN
→ ChatGPT PM durable intake only
```

本报告不授予或继承 stage、commit、push、tag、delete、move、archive、cleanup、remote、
runtime-loaded、production validation、status 或 roadmap authority。完成 durable report
和 manifest 后立即停止。

## 18. Thread 输出 / 上下文评估

- 本次输出长度：长；完整事实已持久化，Chat 只返回 concise manifest。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：R36 authority 已使用一次并 terminalize；下一步只能由 ChatGPT PM 做 durable
  intake，后续任何 Git 或 cleanup decision 都需要新 authority。
