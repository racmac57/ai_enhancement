# Skills reference hub (`docs/skills/`)

This directory is the **single documentation index** for Claude Code skills. Skill **implementations** may live anywhere:

- **GLOBAL:** `%USERPROFILE%\.claude\skills\<skill-name>\SKILL.md`
- **PROJECT:** `<repo-root>\.claude\skills\<skill-name>\SKILL.md`

This folder does **not** duplicate `SKILL.md` files; it holds the **catalog**, **aggregated guides**, and **per-skill reference** markdown created when skills are hardened. The `ai_enhancement` repo is **docs-only** — it does not host a `.claude/skills/` sync copy. The sole install location for skills is `~/.claude/skills/`.

## Files

| File / folder | Purpose |
|---------------|---------|
| [SKILLS_INDEX.md](SKILLS_INDEX.md) | Master table: scope, skill name, **path to `SKILL.md`**, link to per-skill how-to, one-line description |
| [global_skills.md](global_skills.md) | Long-form how-to for all GLOBAL skills (sections per skill) |
| [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Long-form how-to for `cad_rms_data_quality` project skills |
| [personnel_and_summons_etl_skills.md](personnel_and_summons_etl_skills.md) | Long-form how-to for Personnel / Summons ETL project skills |
| [how_to/](how_to/) | **One markdown per skill** — created or updated when `/qa-skill-hardening` reaches 9/9 (Phase 7) |

## Per-skill how-to files (`how_to/<skill-name>.md`)

After a successful hardening run, Phase 7:

1. Updates the aggregated `.md` for that scope (`global_skills.md`, etc.).
2. Updates [SKILLS_INDEX.md](SKILLS_INDEX.md) (paths + description).
3. **Creates or refreshes** `how_to/<skill-name>.md` with a stable reference (paths, invoke line, subsections aligned with the aggregated guide).

Skills that have not been hardened since this convention was added may show “pending” in the index until the next 9/9 run.

## Windows path roots (this machine)

| Scope | Typical repo / root |
|-------|---------------------|
| Global | `C:\Users\carucci_r\.claude\skills\` |
| `cad_rms_data_quality` | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality\` |
| `personnel_and_summons_etl` | Summons / Personnel repos under `02_ETL_Scripts\Summons`, `09_Reference\Personnel`, etc. — see each skill’s `how_to` file for the exact path |

## Related

- Hardening workflow: `/qa-skill-hardening` — see `C:\Users\carucci_r\.claude\skills\qa-skill-hardening\SKILL.md` (Phase 7: Documentation Sync).
- Adding a new skill: [../CONTRIBUTING.md](../CONTRIBUTING.md).
