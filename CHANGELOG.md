# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `docs/skills/README.md` — reference hub for all skills (implementations may live anywhere).
- `docs/skills/how_to/` — per-skill reference markdown; `_TEMPLATE.md` and `hpd-exec-comms.md` seed; filled/updated by `/qa-skill-hardening` Phase 7.
- `SKILLS_INDEX.md` — expanded with `SKILL.md` paths, per-skill how-to links, and aggregated guide column; includes `hpd-exec-comms`.
- Four legacy flat-file skills converted to dir-form at `~/.claude/skills/`: `arcgis-pro/SKILL.md`, `data-validation/SKILL.md`, `etl-pipeline/SKILL.md`, `html-report/SKILL.md` (names preserved; content unchanged). Added `arcgis-pro` row to `SKILLS_INDEX.md`; corrected two name mismatches (`validate-data` → `data-validation`, `new-etl` → `etl-pipeline`) to reflect actual installed skills.

### Changed

- `docs/skills/global_skills.md` — added `/hpd-exec-comms` section.
- `~/.claude/skills/qa-skill-hardening/SKILL.md` — Phase 7 now creates `docs/skills/how_to/<skill>.md` per hardened skill.
- `CLAUDE.md` — clarified that `~/.claude/skills/` is the sole install location for skills; `ai_enhancement` repo is docs-only.

### Removed

- `ai_enhancement/.claude/skills/` — deleted. Previously held partial, drifting sync copies of `chunk-chat` and `qa-skill-hardening`. Source of truth is `~/.claude/skills/` only; the repo hub (`docs/skills/`) is documentation, not a mirror.
- Flat legacy files `~/.claude/skills/arcgis-pro.md`, `data-validation.md`, `etl-pipeline.md`, `html-report.md` — removed after migration to dir-form `SKILL.md` files above.

## [0.2.0] - 2026-04-10

### Added
- docs/CONVERSATION_ARCHIVIST_PROMPT.md: Reusable prompt for turning any AI into a
  Conversation Archivist. Enforces {Topic_Description}_{AI_Name}.md naming convention
  and KB_Shared/04_output as the default save location.

### Changed
- docs/SKILLS_HOW_TO.md: chunk-chat entry updated to reflect new default output path
  (KB_Shared/04_output) and optional ai_name third argument.
- .claude/skills/chunk-chat/SKILL.md: Synced with AI suffix naming convention, Windows
  tempfile path fix, and OneDrive default output path.

## [0.1.0] - 2026-04-10

### Added
- Initial repository setup with foundational documentation
- `qa-skill-hardening` skill — multi-agent QA swarm for skill testing and hardening
  - Auto-discovers project structure (CLAUDE.md, skills, scripts, configs)
  - 9-step binary test framework (PASS=1 / FAIL=0)
  - Parallel read-only testing (Wave A) and sequential write-capable testing (Wave B)
  - Regression protection — never commits a state where a passing test drops to FAIL
  - Generates per-skill memory files, regression tests, and final hardening reports
- `CLAUDE.md` with project rules, naming conventions, and forbidden patterns
- `README.md` with project overview, skill inventory, and installation guide
- `docs/SUMMARY.md` with condensed project summary
- `docs/ARCHITECTURE.md` with project structure and design decisions
- `docs/CONTRIBUTING.md` with guide for adding new skills
- `.claude/settings.json` with project-level Claude Code configuration

### Known Issues
- None at initial release

### Historical Bugs
- None — fresh repository
