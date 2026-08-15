# UNTRACKED_CORPUS_LOCAL_TOOLING_ADOPTION_REVIEW

## Terminal

`PASS / LOCAL_TOOLING_REVIEW_COMPLETE / 7_FILES_ADOPT_READY_AFTER_MINIMAL_HARDENING`

This gate reviewed the exact seven project-local tooling files previously classified as `LOCAL_TOOLING_REVIEW`. No Git stage, commit, push, tag, runtime, Docker, DB, PLC/V-PLC, SSH/network or cleanup authority was used.

## Authority and higher rules

- Owner instruction: `可以，先处理7个项目tooling文件`.
- Higher durable governance authority: `docs/thread_handoff/pm_operating_rules.md`.
- Reusable procedure: `.agents/skills/edge-mes-pm-governance/SKILL.md`; explicit invocation only and grants no authority.
- OpenAI official Codex documentation was checked for current AGENTS.md, custom-agent and config semantics.

## Official Codex compatibility findings

Current official Codex documentation confirms:

- project-scoped custom agents are standalone TOML files under `.codex/agents/`;
- each custom agent requires `name`, `description`, and `developer_instructions`;
- supported normal config keys such as `sandbox_mode` may be included in custom-agent files;
- global subagent settings use `[agents]`, including `agents.enabled`, `agents.max_concurrent_threads_per_session`, and `agents.interrupt_message`;
- `agents.max_concurrent_threads_per_session` may be omitted, in which case Codex selects its default;
- `approval_policy = "on-request"`, `approvals_reviewer = "user"`, `sandbox_mode = "workspace-write"`, `sandbox_workspace_write.network_access`, `features.multi_agent`, and `features.goals` are current supported config keys;
- parent-turn live permission/sandbox overrides may be reapplied when spawning a child, so a project-level `sandbox_mode = "read-only"` remains a default boundary rather than a substitute for PM changed-path containment checks.

## Pre-review findings

### `AGENTS.md`

Pre-review identity:

```text
bytes = 147
sha256 = 4dfeb894a2aa74fc59c5dcda23603e54ade4e3c034dedce8ddb487f1bd7e3f1e
```

The file contained only a transient `<claude-mem-context>` block saying no prior sessions were found. That is not a durable Edge MES project instruction and is unsuitable for adoption as the repository's Codex `AGENTS.md`.

Classification before hardening: `REVISE_BEFORE_ADOPT`.

### `.codex/config.toml`

Pre-review identity:

```text
bytes = 276
sha256 = f3e0c7070f820122532b8ecadac92564303c19b8fd09aff4634ad8475f649078
```

All keys are current supported Codex configuration. The only project-governance issue was:

```text
max_concurrent_threads_per_session = 24
```

The PM Rules require bounded, independently delegable subagent work; no project authority justified a fixed 24-child concurrency cap. Official Codex configuration permits leaving the key unset and using the current product default.

Classification before hardening: `REVISE_BEFORE_ADOPT`.

### `.codex/agents/shadow_diagnostic.toml`

Pre-review identity:

```text
bytes = 1560
sha256 = 7cdd245dddc73c94130a193df769c10ba934ed335bd7d4b04c0ce0cf355f62ca
```

Its developer instructions explicitly require behaviorally read-only diagnosis and forbid repository writes, but the profile used `sandbox_mode = "workspace-write"`. Current Codex custom-agent configuration supports an explicit `read-only` sandbox, so the project default should match the role.

Classification before hardening: `REVISE_BEFORE_ADOPT`.

## Exact minimal hardening performed

Exactly three tooling files changed:

1. `AGENTS.md`
   - replaced transient Claude-memory content with a concise Edge MES agent entrypoint;
   - points to PM Rules as higher authority;
   - points to the governance Skill as explicit-invocation-only procedure;
   - states that profiles/skills/chat history grant no authority;
   - preserves immutable terminals, exact allowlists, evidence-class separation and separate Git/runtime authority;
   - does not request automatic subagent delegation.

2. `.codex/config.toml`
   - removed only `max_concurrent_threads_per_session = 24`;
   - retained on-request user approval, workspace-write sandbox, network disabled, Goals enabled, multi-agent enabled, child-agent enablement and interruption messages.

3. `.codex/agents/shadow_diagnostic.toml`
   - changed only `sandbox_mode = "workspace-write"` to `sandbox_mode = "read-only"`.

## Review-only profiles preserved byte-identically

The following four files were not modified:

```text
.codex/agents/shadow_data_quality.toml
sha256 = 6e3fd442ddb8498a3ffff58f52c005fcc45377cc84449509620286a79ffc07f6

.codex/agents/shadow_reliability.toml
sha256 = e9837ddb66c3167a702f44e8b73a889bc295f465b2812653624a98d3eec3154b

.codex/agents/shadow_repair_worker.toml
sha256 = 5344f00c733f1119b15e0fbbce67fded47035a547b5b6c3b872cd915eddbe670

.codex/agents/shadow_verification.toml
sha256 = 9dad12cbfd292561cddda38bef70e5c950fa6db4016f71c26e84b16ed9540de6
```

Their roles align with PM Rules:

- Data Quality / Reliability / Verification are bounded review agents and may need workspace-write only for the exact durable report authorized by the task;
- Repair Worker is the single mutation worker for an already-authorized minimal repair;
- all five profiles set nested `[agents] enabled = false`, matching the project rule that they must not spawn subagents;
- none grants stage/commit/push/tag, remote/runtime, DB/PLC/V-PLC or deployment authority by itself.

## Post-hardening identities

```text
AGENTS.md
bytes = 1448
sha256 = 97d0e3cb86a9a95ae162486f37b9d6a29e8c04199ef959aed61fbb1c06779dc1

.codex/config.toml
bytes = 236
sha256 = 5e0bb8a628a18b0ac10c0c43ae7c4d990f52ca95b5709ac55fda30dc8eebc136

.codex/agents/shadow_data_quality.toml
bytes = 1325
sha256 = 6e3fd442ddb8498a3ffff58f52c005fcc45377cc84449509620286a79ffc07f6

.codex/agents/shadow_diagnostic.toml
bytes = 1554
sha256 = c7624742eb99f76a57e03ac0c76060cddd265565b6b7360a6ae2b990ae040890

.codex/agents/shadow_reliability.toml
bytes = 1344
sha256 = e9837ddb66c3167a702f44e8b73a889bc295f465b2812653624a98d3eec3154b

.codex/agents/shadow_repair_worker.toml
bytes = 1215
sha256 = 5344f00c733f1119b15e0fbbce67fded47035a547b5b6c3b872cd915eddbe670

.codex/agents/shadow_verification.toml
bytes = 1326
sha256 = 9dad12cbfd292561cddda38bef70e5c950fa6db4016f71c26e84b16ed9540de6
```

## Validation

- Python `tomllib` parsing: `PASS` for all six TOML files.
- High-confidence credential marker scan: `0` matched files.
- `/Users/` absolute-path scan: `0` matched files.
- Four review-only agent SHA identities: unchanged from pre-review.
- Git staged files: `0`.
- Tracked dirty files: `0` because all seven tooling files remain untracked pending adoption authority.
- No product/runtime mutation occurred.

## Final classification

| File | Final classification | Rationale |
|---|---|---|
| `AGENTS.md` | `ADOPT_READY` | now a stable project governance entrypoint rather than transient memory |
| `.codex/config.toml` | `ADOPT_READY` | current supported schema; unjustified fixed concurrency removed |
| `shadow_data_quality.toml` | `ADOPT_READY` | bounded current Data Quality reviewer |
| `shadow_diagnostic.toml` | `ADOPT_READY` | behaviorally read-only role now defaults to read-only sandbox |
| `shadow_reliability.toml` | `ADOPT_READY` | bounded current Reliability reviewer |
| `shadow_repair_worker.toml` | `ADOPT_READY` | single task-bound mutation worker |
| `shadow_verification.toml` | `ADOPT_READY` | bounded independent Verification reviewer |

## Publication boundary

```text
TOOLING_REVIEW = PASS
TOOLING_FILES_ADOPT_READY = 7
TOOLING_FILES_STAGED = NO
TOOLING_FILES_COMMITTED = NO
TOOLING_FILES_PUSHED = NO
```

The next eligible gate is an exact-path local tooling adoption commit. It should stage only the seven tooling files plus the exact task/report artifacts chosen for durable governance continuity, verify the staged set, and commit once. Push remains separately authorized.
