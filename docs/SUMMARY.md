# Project Summary

## ai_enhancement

**What**: A library of reusable Claude Code skills and QA automation tooling.

**Why**: Building AI-assisted skills is fast — but trusting them in production requires systematic validation. This project provides the skills themselves and the QA framework to harden them.

**How it works**:

1. **Skills** live in `.claude/skills/<name>/SKILL.md` — each is a self-contained prompt with YAML frontmatter that Claude Code loads as a slash command
2. **The QA Hardening Swarm** (`/qa-skill-hardening`) is itself a skill that can audit any other skill — it auto-discovers the project, designs binary tests, runs them, fixes failures, and produces evidence-backed reports
3. **Documentation** is generated automatically — per-skill memory files, regression test registries, and final scorecards

## Current Skill Inventory

| # | Skill | Type | Status |
|---|-------|------|--------|
| 1 | qa-skill-hardening | Read + Write (generates docs) | Active |

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
| `.claude/skills/*/SKILL.md` | Individual skill definitions |
| `docs/skill_memory/` | Generated test results and reports |
