# Sprint 4 D2-R7B-W0-SR-A19-C1 V2 Helper/Test Implementation

## Conclusion

结论：PASS WITH RECOMMENDATIONS。

本轮已在 Codex Local checkout 完成 A19-C1 V2 helper/test implementation。V2 focused suite 完整通过，锁后 stability run1 与 run2 均保持 36/36 GREEN；helper、test、legacy helper/test、process-capture adapter 及 adapter test 的冻结身份均未漂移。当前交付边界仍是 PM read-only intake，未进入 A19 execution、real Prepare/Execute、retained mutation、Git 或 runtime gate。

## Scope

本报告只覆盖 relaunch authority 授权的三个 repository-relative outputs：

- docs/thread_handoff/pm_tools/w0_s1_fresh_sibling_candidate_execution_v2.py
- docs/thread_handoff/pm_tools/test_w0_s1_fresh_sibling_candidate_execution_v2.py
- docs/reports/sprint4_d2_r7b_w0_sr_a19_c1_live_git_baseline_compatibility_repair_implementation.md

执行环境是 /Users/chenjie/Documents/MES/edge-mes-demo 的本地 Codex checkout。未连接、获取或等待 Devspace、MCP workspaceId 或其他外部 coding-workspace binding。未授权并且未执行 A19 execution task/report/evidence、real Prepare/Execute、retained mutation、Git stage/commit/push/tag、deployment、runtime 或 production activation。

## Accepted planning authority

- relaunch task：docs/thread_handoff/pm_task_20260807T0302Z_d2_r7b_w0_sr_a19_c1_v2_helper_test_implementation_relaunch_codex_local.md；regular / non-symlink；17230 bytes；SHA-256 92aa3671f56a885aa2b74e9b1161619b013e46370aac46e5887b717442fdde4d。
- parent V2 implementation/TDD specification：docs/thread_handoff/pm_task_20260807T0100Z_d2_r7b_w0_sr_a19_c1_v2_helper_test_implementation.md；regular / non-symlink；35758 bytes；SHA-256 b50f39caf05e6491f2ba9eb34c1a3207199930c435f313e5c3ec8c1095d1c003。
- C2 planning authority：docs/reports/sprint4_d2_r7b_w0_sr_a19_c2_live_git_baseline_compatibility_repair_planning_publication_correction.md；读取结论为 PM ACCEPTED / PASS WITH RECOMMENDATIONS / LOCAL_HELPER_COMPATIBILITY_REPAIR_PLANNING_ONLY。
- 当前 PM Rules：docs/thread_handoff/pm_operating_rules.md；69697 bytes；SHA-256 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f。

此前 CODING_WORKSPACE_BINDING_UNAVAILABLE 已由 ChatGPT PM 判定为 PM REJECTED / CROSS_ENVIRONMENT_TOOL_BINDING_ASSUMPTION，因此没有继承为当前 implementation HOLD。历史 UNAUTHORIZED_WRITE_OUTSIDE_EXACT_ALLOWLIST 仍作为 historical truth 保留；其唯一 stray 已清理，历史原路径在本轮入口、首次写入审计、锁和最终审计中均保持 absent。

## Root cause addressed

旧 V1 helper 的 Git contract 依赖固定或历史基线形状，不能把 task-role 声明的 Git baseline 与调用者提供的实际 Git state 作为两个独立对象进行 exact validation。这会把历史快照漂移、固定 dirty-path 清单、head/origin 漂移和 caller 自授权混入 acceptance。

V2 将 git_baseline 纳入 execution-task role，并在 role authority/self-identity 通过后分别验证 task role baseline 与 caller actual git_state，再要求两者 canonical equality。V2 不查询、写入或推断真实 execution；它只为后续 fresh authority 调用提供 claim-neutral 的 contract gate。

## Files created and frozen identities

- docs/thread_handoff/pm_tools/w0_s1_fresh_sibling_candidate_execution_v2.py：regular / non-symlink；63896 bytes；SHA-256 0c87cef2302f963eda70a84f4e07e1871692f426127a6be70e70ef21b593bab3。
- docs/thread_handoff/pm_tools/test_w0_s1_fresh_sibling_candidate_execution_v2.py：regular / non-symlink；40442 bytes；SHA-256 a8f6879e1fb0041558472d7148d94e1c50170554fc160a5219ccda8eb576caeb；包含 36 个 focused test methods。
- docs/reports/sprint4_d2_r7b_w0_sr_a19_c1_live_git_baseline_compatibility_repair_implementation.md：入口 absent；在两次 stability run 完成后按 single implementation-report write 规则写入一次；其 postimage identity 由最终审计记录。

## V2 execution-task role schema

ROLE_SCHEMA 为 D2-R7B-W0-SR-A19-C1-S1-EXECUTION-TASK-AUTHORITY-V2。role 的 exact 17 fields 为：schema、task_role、attempt_id、execution_authority_id、execution_report_path、evidence_root、helper、test、retained_parent、retained_base、retained_child、retained_history_child、max_child_mkdir_attempts、claim_authority、materialization_claim_established、w0_accepted、git_baseline。

git_baseline 的 exact 9 fields 为：branch、head、origin_main、ahead、behind、tracked_unstaged、cached_diff、diff_check、cached_diff_check。helper/test nested identity 继续使用 path、bytes、sha256、type、symlink 五字段；role parse 仍要求 canonical single-line JSON、固定 marker order、exact schema、authority binding、PM_INTAKE_ONLY、materialization_claim_established=false、w0_accepted=false 和 max_child_mkdir_attempts=1。

## Live Git validation implementation

V2 的 validate_git_state 对 object shape、exact keys、strict scalar types、bool/int distinction、list item types、relative safe path components、duplicate、排序、lowercase 40-hex head/origin、main branch、ahead/behind 为 0、cached_diff 为空以及两个 diff checks 为 PASS 进行验证，并返回 defensive copies。

_validate_git 的数据流是：

- validate task role git_baseline；
- 独立 validate caller git_state；
- 对两个验证后的 objects 做 exact equality；
- 不相等时 terminal rejection，错误为 live Git drift。

parse_execution_task_role 先完成 role/authority/self-identity validation，随后才进入 Git validation。synthetic_git_state 已不再提供默认基线，而是明确拒绝，要求测试和调用者显式提供 Git fixture。源代码没有 real-mode historical HEAD、固定 dirty list 或 V1 fallback。

本轮 repository pre-lock live audit 记录为：cwd 与 Git top-level 均为 /Users/chenjie/Documents/MES/edge-mes-demo；branch main；HEAD 与 origin/main 均为 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35；ahead/behind 0/0；tracked dirty 仅为 docs/current_status.md 与 docs/thread_handoff/pm_operating_rules.md；cached diff 为空；diff_check 与 cached_diff_check 均为 PASS。该快照仅用于本轮本地审计，不构成 execution evidence 或 production claim。

## TDD evidence

入口检查确认三个 implementation outputs 均为 regular / non-symlink absent，历史 parent same-suffix stray 也为 absent。首次 repository mutation 先写入 exact V2 test target，使用显式绝对 source/destination 的本地 copy primitive；立即审计确认只有该 allowlisted V2 test path 新增，tracked dirty 未变，cached index 仍为空，stray 仍 absent。

TDD 顺序和结果如下：

- missing-helper RED：V2 test 先于 helper implementation 运行，exit 1，精确失败为 V2 helper missing。
- V1-seeded contract RED：将 legacy helper 复制到 exact V2 helper target 后运行 28-test inherited suite，exit 1，2 failures、19 errors，核心失败为 V2 git_baseline/schema 不存在。
- V2-contract RED：先加入 tests 29–36，再以未实现 V2 contract 的 helper 运行完整 suite，36 tests，4 failures、22 errors；新增 Git shape、drift、unsafe path、role order/self-authorization、source scan 和 continuity contracts 均参与 RED。
- minimal implementation：加入 exact V2 role/Git validation 和 equality gate；保持 downstream evidence、retained、publication 与 claim-neutral behavior 不扩张。
- complete focused-suite GREEN：36 tests，failures 0，errors 0，skips 0。
- 静态边界由 test_02 的 stdlib-only/standalone AST contract 与 test_35 的 source scan 覆盖；test_36 覆盖 legacy/adapter identity 和 downstream contract preservation。

repair ledger 使用 2/2 个 mechanical correction slots，均未产生额外 repository output：第 1 次修正了 primitive smoke 自检中的 digest literal 表达式；第 2 次修正了首次写入审计中 macOS NUL awk target-count parser，改用 exact Git pathspec audit。锁后未修改 helper/test。

## Focused-suite stability

锁后执行同一 exact command 两次：

env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/opt/python@3.14/bin/python3.14 -B docs/thread_handoff/pm_tools/test_w0_s1_fresh_sibling_candidate_execution_v2.py -v

- stability run1：Ran 36 tests in 0.227s；OK；failures/errors/skips 均为 0。
- stability run2：Ran 36 tests in 0.230s；OK；failures/errors/skips 均为 0。

两次运行前后 V2 helper identity 均为 63896 bytes / 0c87cef2302f963eda70a84f4e07e1871692f426127a6be70e70ef21b593bab3，V2 test identity 均为 40442 bytes / a8f6879e1fb0041558472d7148d94e1c50170554fc160a5219ccda8eb576caeb；report 在两次 stability run 后写入前仍为 absent，且无 __pycache__ 留存。

## Legacy and adapter non-regression

以下 protected continuity identities 在实现、锁和两次 stability run 后保持不变：

- legacy helper：docs/thread_handoff/pm_tools/w0_s1_fresh_sibling_candidate_execution.py；62068 bytes；SHA-256 12698a6624cd01dac2d74926f65de7e10f87296791d61c925a75239c200f71e9。
- legacy test：docs/thread_handoff/pm_tools/test_w0_s1_fresh_sibling_candidate_execution.py；26856 bytes；SHA-256 ba43d540a928e07d0bf2a65df71b71ca2ee1a565e4bf7eb62f28a8fb52f7af93。
- process-capture adapter：docs/thread_handoff/pm_tools/w0_process_capture_adapter.py；6939 bytes；SHA-256 bbe65273bc08dbb7e82726018d2fac916523334d51895921ffa331ae3a469f5c。
- adapter test：docs/thread_handoff/pm_tools/test_w0_process_capture_adapter.py；19546 bytes；SHA-256 eee077c8c91636c52c83f9221172f2a8d10c7a0b716638855c7c7c11a80ea7ae。

V2 test_36 证明这些 continuity identities、six-path topology、state/claim behavior 和 downstream contracts 未因 V2 Git baseline repair 改写。

## Implementation lock

A19_C1_V2_IMPLEMENTATION_LOCK 在最终锁门控中确认，时间为 2026-08-07T12:19:11+0800。锁门控确认 cwd/top-level exact、V2 helper/test regular identity exact、36 tests、report absent、cached index empty、V2 paths 为 exact untracked allowlist entries、历史 parent same-suffix stray absent、无 __pycache__。之后仅执行 stability run1/run2 和本报告 single write；未修改 helper/test。

## Changed-path audit

本报告写入前的 Git audit 为：V2 helper 与 V2 test 各自仅以 exact untracked path 出现；本报告 path absent；cached index bytes 为 0；tracked dirty 仍仅为既有 docs/current_status.md 与 docs/thread_handoff/pm_operating_rules.md。其它既存 dirty/untracked corpus 不属于本轮 mutation。

本报告写入后的 final audit 必须保持以下集合边界：本轮新增且 allowlisted 的三个 exact paths 仅为 V2 helper、V2 test、implementation report；不得出现其它本轮新增 path。Git stage、commit、push、tag 均为 0。历史 parent same-suffix helper/test/report、A19 future execution report/evidence root/retained child 和 Python cache 均保持 absent。

## Claim boundary

本轮最终状态是 LOCAL_V2_HELPER_TEST_IMPLEMENTATION / IMPLEMENTATION_DRAFT / TESTED / IDENTITY_FROZEN / PM INTAKE PENDING。它不表示 EXECUTION_FACTS_CONFIRMED、MATERIALIZED、PM ACCEPTED、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

没有 Prepare、Execute、retained object、A19 report/evidence、container/image、deployment、runtime、production activation 或 remote-workspace binding claim。后续任何 execution authority 必须由新的 fresh PM authority 明确提供并重新绑定 live Git facts。

## Blockers and recommendations

implementation 本身无 blocker。一次只读锁检查曾使用环境中不存在的固定 /usr/bin/rg 路径，随后改用已验证可用的 rg 命令名复核通过；该诊断错误没有 repository mutation。最终检查曾发现一个 empty、untracked、非 Git 记录的 docs/thread_handoff/pm_tools/__pycache__ directory；确认为空后按 exact path 移除，最终 audit 为 absent，未改变任何 allowlisted file bytes。

建议 PM 只按 read-only intake 接收本报告、V2 helper/test identities、TDD RED/GREEN、两次 stability GREEN、legacy/adapter continuity 和 final changed-path audit；不把本报告升级为 execution、materialization、runtime 或 production acceptance。

## Next gate

下一步仅为 ChatGPT PM read-only intake：重新读取本报告和两个 V2 implementation outputs，核对 relaunch/parent authority identities、V2 17-field role、9-field Git state、36-test GREEN、run1/run2 stability、protected continuity identities、exact allowlist 和 final postimage audit。PM 若接受，可另行决定是否发布全新的 A19 execution authority；本线程不执行该 authority。

## MVP alignment

本实现为 MVP-ALIGNED：它只修复 stale/historical Git baseline 导致的 false HOLD 风险，并增加 task-declared baseline 与 caller actual state 的 exact independent validation；同时拒绝 caller self-authorization 和 unsafe Git path arrays。没有新增产品能力、部署能力或生产状态。

## Thread output / context assessment

本线程输出是本地 helper/test implementation 与一份 durable implementation report，停止点为 ChatGPT PM read-only intake。未使用 subagent，未建立 Devspace/MCP workspace binding，未扩大 repository read/write allowlist。所有 execution、retained mutation、Git publication、deployment、runtime 和 production claims 均明确保留给后续独立 authority。
