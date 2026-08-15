# Edge MES Demo — Agent Instructions

`docs/thread_handoff/pm_operating_rules.md` is the durable governance authority for this repository. Read the current repository-backed PM task before acting, and do not infer authority from chat history, prior tasks, profiles, skills, or this file.

The project Skill `.agents/skills/edge-mes-pm-governance/SKILL.md` is a reusable procedure only when explicitly invoked by the Owner or current task. It grants no Owner approval, mutation authority, runtime authority, or production truth.

Preserve these boundaries:

- historical PASS/HOLD terminals are immutable;
- current facts must come from live repository/runtime evidence required by the task;
- exact changed-file allowlists are mandatory for mutations;
- stage, commit, push, tag, deploy, Docker lifecycle, DB writes, PLC/V-PLC actions, SSH/network access, cleanup, retry, reconnect, and successor gates require the authority stated by the current task/Owner;
- do not adopt, delete, reset, stash, clean, or rewrite unrelated dirty/untracked artifacts;
- local/static/synthetic evidence must not be promoted to remote/runtime/production claims;
- subagents inherit no authority beyond the current task and must not spawn nested subagents unless the current task explicitly changes that rule.

Use the project-scoped `.codex/agents/` profiles only for their named bounded roles. Final gate decisions remain with the parent PM/assigned core Thread.
