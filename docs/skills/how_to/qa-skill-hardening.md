<!-- REFERENCE SNAPSHOT — do not edit directly.
     Source of truth: ~/.claude/skills/qa-skill-hardening/SKILL.md
     Update this file by re-running /qa-skill-hardening and completing Phase 7,
     or by manually syncing from the installed skill. -->

# How-to: `/qa-skill-hardening`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `qa-skill-hardening` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\qa-skill-hardening\SKILL.md` |
| **Invoke** | `/qa-skill-hardening [target-directory-or-skill-name]` |
| **Argument hint** | optional — defaults to auto-discover all skills in the project |
| **Allowed tools** | Bash, Read, Edit, Write, Glob, Grep, Agent, TaskCreate, TaskUpdate |
| **Effort** | `max` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Multi-agent QA swarm that auto-discovers every skill/script in the current project, runs a 9-step binary test framework (PASS=1 / FAIL=0), fixes what it can, guards against regressions, and — on 9/9 PASS — syncs documentation into the `ai_enhancement` hub.

## When to use

- Validating or hardening the full skill inventory of a project before release.
- Auditing a single skill after a behavior change (`/qa-skill-hardening <skill-name>`).
- Establishing evidence-based scorecards + regression tests for newly added skills.

## How to use

1. From the project root, invoke `/qa-skill-hardening` (auto-discover) or `/qa-skill-hardening <target>` for a single skill.
2. The skill runs through 8 phases, ending with Phase 7 documentation sync against `docs/skills/` in `ai_enhancement`.
3. On completion, review the scorecard in `docs/skill_memory/<Skill>_MEMORY.md` and the updated index / how-to files.

## Execution flow

```
PHASE 0: Auto-Discover
PHASE 1: Design Tests
PHASE 2: Wave A (Read-Only, Parallel)     — iterate until all PASS or BLOCKED
PHASE 3: Wave B (Write-Capable, Sequential, Isolated) — iterate until all PASS or BLOCKED
PHASE 4: Regression Test (full suite)     — if regression, fix and re-test
PHASE 5: Document & Report
PHASE 6: Commit (local only — do NOT push)
PHASE 7: Documentation Sync (passing skills only)
```

## Core principles

1. **Evidence-Based** — no claim without captured proof (exit codes, output, paths).
2. **Binary-Test Enforced** — PASS=1 / FAIL=0 only; never partial credit.
3. **Regression-Resistant** — a previously passing test may never drop to FAIL in the committed state.
4. **Autonomous Persistence** — run until every skill is PASS or definitively BLOCKED.
5. **Safe State Mutation** — dry-run → isolated fixture → test sandbox → live execution.

## Phase 7 documentation sync (rules that matter for the hub)

- **§7.2–7.3** — update the aggregated guide (`global_skills.md` or project `*_skills.md`) entry for the skill.
- **§7.4 — `SKILLS_INDEX.md` update**
  - Append/update the skill's row with canonical `SKILL.md` path, aggregated-guide link, and one-line description.
  - **Broken-link guard:** only emit a Markdown link in the **Per-skill how-to** column when the target `how_to/<name>.md` exists on disk after §7.5 completes. Otherwise write the literal text `_pending (Phase 7)_`. Never emit a link that would 404.
- **§7.5 — per-skill how-to file**
  - Default filename: `<skill-name>.md` (matching YAML `name:`).
  - Collision filename: `<skill-name>__<project-key>.md` (e.g. `check-paths__cad_rms.md`).
  - Body follows `docs/skills/how_to/_TEMPLATE.md`, populated from current `SKILL.md` + the §7.3 subsections.

## Output / artifacts

- `docs/skill_memory/<Skill>_MEMORY.md` — per-skill scorecard with evidence.
- Regression tests written alongside the hardened skill.
- Updated `docs/skills/SKILLS_INDEX.md`, aggregated guide, and `docs/skills/how_to/<skill>.md` for each 9/9 skill.
- Local-only commit at Phase 6 (the skill never pushes).

## Skip conditions

- Skill did not reach 9/9 → Phase 7 skipped for that skill; row stays (or is set to) `_pending (Phase 7)_`.
- Skill is `qa-skill-hardening` itself → Phase 7 normally skips to avoid recursive self-edit (this file was written manually by user request).
- How-to file unreachable (e.g. OneDrive offline) → warn and skip; do NOT fail the hardening run over a doc-sync failure.

## Gotchas

- **Never pushes.** Phase 6 commits locally only; pushing is a human decision.
- **Regression gate is absolute.** If any previously passing test now fails, the run must fix it before committing — no "known regressions".
- **Self-edit hazard.** Do not rely on `/qa-skill-hardening` to document itself; keep this snapshot manually in sync with the installed `SKILL.md`.
- **Hub paths are Windows-absolute** in the installed skill (`C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\ai_enhancement\...`). If the OneDrive root moves, update §7.4/§7.5 paths in the source `SKILL.md`.

## Hardening

- Scorecard (when run from a project with `docs/skill_memory/`): `docs/skill_memory/qa-skill-hardening_MEMORY.md` (if ever produced; normally self-skipped).

## Parallel Mode

The skill supports running multiple agents in parallel — one per skill — with a coordinator merge step at the end. This avoids write conflicts on shared files (`SKILL_HARDENING_MASTER.md`, `REGRESSION_TESTS.md`, `FINAL_SKILL_HARDENING_REPORT.md`, `SKILLS_INDEX.md`, `global_skills.md`).

### When to use

- Hardening 3+ skills at once and you want to run them concurrently across terminals / agent sessions.
- Any run where two or more agents might otherwise race on the shared tracker files.

### Invoke pattern

Activate parallel mode by passing `parallel=true` (or multiple `target=` values) to each agent. Each agent owns exactly one skill and writes only to its own per-skill `MEMORY.md` / `how_to/<skill>.md`.

```text
# Terminal 1
/qa-skill-hardening target=etl-pipeline parallel=true
# Terminal 2
/qa-skill-hardening target=arcgis-pro parallel=true
# Terminal 3
/qa-skill-hardening target=data-validation parallel=true
# After all complete — any single terminal
/qa-skill-hardening merge=true
```

### Rules in parallel mode

1. **One skill per agent.** Never assign two skills to one agent in parallel mode.
2. **Shared files are coordinator-owned.** During Phases 1–7, agents do NOT write to:
   - `docs/skill_memory/SKILL_HARDENING_MASTER.md`
   - `docs/skill_memory/REGRESSION_TESTS.md`
   - `docs/skill_memory/FINAL_SKILL_HARDENING_REPORT.md`
   - `docs/skills/SKILLS_INDEX.md`
   - `docs/skills/global_skills.md`
3. **Phase 7 SKILLS_INDEX update is deferred.** Each agent logs `"SKILLS_INDEX update deferred — parallel mode. Coordinator will merge."` instead of writing the index.
4. **Coordinator merge runs once.** After every parallel agent reports 9/9 PASS, a single designated coordinator (or the user) invokes `/qa-skill-hardening merge=true`.

### Merge mode (`merge=true`)

The coordinator reads every per-skill `*_MEMORY.md` from this session and writes the shared files in a single non-conflicting pass:

1. Read all `docs/skill_memory/*_MEMORY.md` files produced this session.
2. Append results into `SKILL_HARDENING_MASTER.md` (no overwrites).
3. Append regression tests into `REGRESSION_TESTS.md`.
4. Regenerate `FINAL_SKILL_HARDENING_REPORT.md` with combined totals.
5. Update `SKILLS_INDEX.md` — one row per skill, single write.
6. Update `docs/skills/global_skills.md` — append missing entries only.
7. Commit shared files in one commit: `qa-skill-hardening: merge parallel results — [skill1, skill2, skill3]`.
8. Report a table showing each skill's final score and merge status.

**Merge guard:** if any per-skill `MEMORY.md` is missing or shows non-PASS, the coordinator prints a warning listing the incomplete skills and asks for confirmation before a partial merge.
