# Project Summary

## ai_enhancement

**What**: A library of reusable Claude Code skills and QA automation tooling.

**Why**: Building AI-assisted skills is fast — but trusting them in production requires systematic validation. This project provides the skills themselves and the QA framework to harden them.

**How it works**:

1. **Skills** install to `~/.claude/skills/<name>/SKILL.md` (global) or `<repo>/.claude/skills/<name>/SKILL.md` (project) — each is a self-contained prompt with YAML frontmatter that Claude Code loads as a slash command. This repo is **docs-only** — it does not host `.claude/skills/` (removed in the 2026-04 cleanup; source of truth is `~/.claude/skills/`).
2. **The QA Hardening Swarm** (`/qa-skill-hardening`) is itself a skill that can audit any other skill — it auto-discovers the project, designs binary tests, runs them, fixes failures, and produces evidence-backed reports
3. **Documentation** is generated automatically — per-skill memory files, regression test registries, and final scorecards. Live skill memory lives in the owning repo (e.g. `.claude/docs/skill_memory/` for global skills). This repo's `docs/skill_memory/` is a historical snapshot from prior hardening runs.

## Current Skill Inventory

The live inventory lives in [`docs/skills/SKILLS_INDEX.md`](skills/SKILLS_INDEX.md). GLOBAL skills install under `~/.claude/skills/`; project skills under each project's `.claude/skills/`. As of 2026-04-19 the GLOBAL set includes: `qa-skill-hardening`, `session-handoff`, `chunk-chat`, `etl-pipeline`, `arcgis-pro`, `data-validation`, `html-report`, `check-paths`, `hpd-exec-comms`, `frontend-slides`, `frontend-design`, `claude-api`, `simplify`, plus the Workbook_Redesign_2026 project skills documented alongside. See `SKILLS_INDEX.md` for the authoritative list and paths — do not duplicate it here.

## Key Design Decisions

- **Project-agnostic**: Skills discover their environment at runtime — no hardcoded paths or project-specific templates
- **Binary testing**: Every test is PASS=1 or FAIL=0 — no partial credit, no subjective ratings
- **Regression protection**: The framework refuses to commit if a previously passing test has regressed
- **Swarm architecture**: Read-only skills are tested in parallel; write-capable skills are tested sequentially in isolation

## File Map

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Rules and conventions for Claude Code sessions |
| `README.md` | Public-facing project overview |
| `CHANGELOG.md` | Version history, known issues |
| `docs/SUMMARY.md` | This file — condensed project summary |
| `docs/ARCHITECTURE.md` | Structural design and rationale |
| `docs/CONTRIBUTING.md` | How to add and maintain skills |
| `docs/skills/SKILLS_INDEX.md` | Authoritative catalog of all skills with `SKILL.md` paths |
| `docs/skills/how_to/<name>.md` | Per-skill reference markdown (Phase 7 output of `/qa-skill-hardening`) |
| `docs/skills/global_skills.md` | Long-form how-to for every GLOBAL skill |
| `docs/skill_memory/` | Historical snapshot of hardening runs (live memory is in each owning repo) |
