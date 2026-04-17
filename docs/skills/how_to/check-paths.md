# How-to: /check-paths

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|-------|
| **Scope** | GLOBAL |
| **Skill name** | `check-paths` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\check-paths\SKILL.md` |
| **Invoke** | `/check-paths` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Scan the current project's source files for path hygiene issues.

## When to use

- Before committing changes that touch scripts, configs, or pipeline YAML.
- After a mass rename (e.g., profile directory change, folder reorganization).
- When auditing a project for HPD path-convention compliance (canonical
  `carucci_r` root, `PowerBI_Data` not `PowerBI_Date`, no deprecated
  `unified_data_dictionary` references, no stale `PD_BCI_01`).
- When onboarding an older project into the current standards.

## How to use

```
/check-paths
```

No arguments. The skill scans recursively from the current working directory
across `.py`, `.yaml`, `.yml`, `.json`, `.bat`, `.ps1`, and `.cmd` files.

## Output / artifacts

No file output. Claude returns a grouped report of issues:

- One section per issue type (1 through 5).
- Each hit as `path:line  <excerpt>`.
- A summary with per-category counts and total.
- A short recommended-fix line per category.

## Gotchas

The five rules enforced (do not invent new categories):

1. **`RobertCarucci` → `carucci_r`.** The real Windows profile on this
   desktop is `carucci_r`; `RobertCarucci` only belongs in git history or
   archived docs.
2. **Deprecated `unified_data_dictionary`.** Canonical location is
   `09_Reference/Standards/`.
3. **Hardcoded `C:\Users\...` or `D:\` paths.** Prefer
   `path_config.get_onedrive_root()` or project-relative paths. Allow when
   clearly documented as intentional.
4. **`PowerBI_Date` → `PowerBI_Data`.** Known typo; must not re-enter scripts.
5. **Stale `PD_BCI_01`** outside archive/docs folders.

Additional notes:

- `scripts.json` legitimately uses `carucci_r` — not a false positive.
- `archive/`, `_Archived/`, `docs/history/` etc. may contain deprecated
  references legitimately; report them as informational, not as errors.
- JSON files may not surface accurate line numbers in every reader —
  best-effort is acceptable.
- This is the **GLOBAL** variant. A project-scoped variant also exists at
  `02_ETL_Scripts/cad_rms_data_quality/.claude/skills/check-paths/SKILL.md`
  (see [check-paths__cad_rms.md](check-paths__cad_rms.md)). The project
  variant may extend the rule set with domain-specific checks; when both
  are registered, the project skill takes precedence for cad_rms work.

## Hardening

- Last scorecard: `docs/skill_memory/check-paths_MEMORY.md` (populated by
  `/qa-skill-hardening` Phase 7 once the skill is scored).
