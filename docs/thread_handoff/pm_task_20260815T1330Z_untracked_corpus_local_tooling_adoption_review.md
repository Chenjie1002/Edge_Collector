# UNTRACKED_CORPUS_LOCAL_TOOLING_ADOPTION_REVIEW

## Authority

Owner instruction: `可以，先处理7个项目tooling文件`.

This task is limited to the seven previously classified project-local tooling files:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/shadow_data_quality.toml`
- `.codex/agents/shadow_diagnostic.toml`
- `.codex/agents/shadow_reliability.toml`
- `.codex/agents/shadow_repair_worker.toml`
- `.codex/agents/shadow_verification.toml`

PM Rules remain the higher durable authority. This task grants no runtime, DB, PLC/V-PLC, Docker, network, Git stage/commit/push/tag, cleanup, or deployment authority.

## Objective

Review the seven files as project-level Codex tooling and make only the minimum local hardening needed before later adoption into `main`.

## Accepted review inputs

- `docs/thread_handoff/pm_operating_rules.md`
- `.agents/skills/edge-mes-pm-governance/SKILL.md`
- current OpenAI Codex official documentation for AGENTS.md, custom agents, and config keys
- live contents and identities of the seven tooling files

## Review criteria

1. project-scoped and reusable rather than machine/session-specific;
2. no embedded secrets or personal absolute paths;
3. no authority expansion relative to PM Rules;
4. custom-agent roles remain bounded and non-nesting;
5. sandbox defaults match each role's actual mutation needs;
6. project config avoids unjustified broad concurrency or hidden remote/network authority;
7. AGENTS.md is a durable project instruction entrypoint, not transient memory.

## Exact mutation allowlist

Only these three files may be changed in this gate if the review requires hardening:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/shadow_diagnostic.toml`

The other four agent profiles are review-only and must remain byte-identical unless this task terminalizes HOLD before any broader change.

## Required minimal hardening

- replace transient Claude-memory content in `AGENTS.md` with a concise Edge MES governance entrypoint that points to PM Rules and the explicit-invocation governance Skill and grants no authority;
- remove the project-local hard cap `agents.max_concurrent_threads_per_session = 24`, leaving Codex to use its current default while PM Rules govern actual bounded delegation;
- change `shadow_diagnostic` to `sandbox_mode = "read-only"` because its own contract forbids repository writes;
- preserve all other current tooling semantics.

## Validation

- parse all six TOML files with Python `tomllib`;
- verify the four review-only agent files retain their pre-gate SHA-256 identities;
- scan all seven files for high-confidence credential markers and machine-local absolute paths;
- verify Git tracked state remains clean and no file outside this exact tooling/task/report scope is modified;
- write one durable report under `docs/reports/`.

## Git publication

`STAGE / COMMIT / PUSH = NOT AUTHORIZED` in this task. A later Owner gate may authorize exact-path adoption after review.

## Terminal

PASS only if the seven files are classified and the exact three-file hardening is validated with no scope drift. Otherwise HOLD at the first decisive violation.
