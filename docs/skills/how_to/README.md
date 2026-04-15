# Per-skill how-to files

Each file named `<skill-name>.md` (or `<skill-name>__<project-key>.md` when the same name exists in global and project scope) holds a **stable reference** for that skill: paths, invoke line, when/how, gotchas.

## When these files appear

- **Created or refreshed** by `/qa-skill-hardening` **Phase 7** after a skill scores **9/9 PASS**, for that skill.
- Until then, the master index shows `_pending (Phase 7)_` for that row instead of a dead link; use the **aggregated** guide (`global_skills.md`, `cad_rms_data_quality_skills.md`, etc.) from [SKILLS_INDEX.md](../SKILLS_INDEX.md).
- Phase 7 §7.4 must only write a link in `SKILLS_INDEX.md` when the target `how_to/<name>.md` exists on disk after §7.5; otherwise it writes the literal text `_pending (Phase 7)_`.

## Template

See [_TEMPLATE.md](_TEMPLATE.md).
