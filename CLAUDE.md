# AI Enhancement — Claude Code Rules

## Project Identity

- **Project**: ai_enhancement
- **Purpose**: A collection of reusable Claude Code skills, automation scripts, and QA tooling
- **Repository**: hy5guy/ai_enhancement

## Critical Rules

### Path Safety
- Never use hardcoded absolute paths (e.g., `/home/username/...`)
- Use relative paths from the project root or environment variables (`$CLAUDE_PROJECT_DIR`)
- Never assume `~/` resolves to a specific user directory

### Naming Conventions
- Skill directories: lowercase with hyphens (e.g., `qa-skill-hardening`)
- Skill files: `SKILL.md` (uppercase, inside the skill directory)
- Documentation: `UPPER_SNAKE.md` for top-level docs (e.g., `CHANGELOG.md`, `CLAUDE.md`)
- Scripts: lowercase with hyphens (e.g., `run-tests.sh`)
- Branches: `claude/<description>` for Claude-generated branches

### Skill Structure
Every skill must follow this structure:
```
.claude/skills/<skill-name>/
  SKILL.md          # Required — YAML frontmatter + markdown body
  *.md              # Optional — supporting reference files
  scripts/          # Optional — helper scripts
```

### SKILL.md Frontmatter Requirements
Every `SKILL.md` must include valid YAML frontmatter with at minimum:
- `name`: lowercase, hyphens only, max 64 characters
- `description`: what it does and when to use it (under 250 characters)

### Code Quality
- All shell scripts must use `set -euo pipefail`
- All scripts must be idempotent (safe to re-run)
- No secrets, credentials, or API keys in committed files
- No `.env` files committed to the repository

### Git Practices
- Commit messages: conventional commits format (`feat:`, `fix:`, `docs:`, `chore:`)
- Never force-push to `main`
- Never commit a state where previously passing tests regress
- One logical change per commit

### Documentation
- Every new skill must be documented in the CHANGELOG
- README.md must stay current with the skill inventory
- Changes to shared infrastructure require updating ARCHITECTURE.md

### Testing
- Skills are evaluated using the 9-step binary test framework (see `/qa-skill-hardening`)
- Tests are PASS=1 or FAIL=0 — no partial credit
- Evidence must be captured for every test result

## Shared Context Files

These files provide context that skills may reference:
- `CLAUDE.md` (this file) — project rules and conventions
- `README.md` — project overview and skill inventory
- `CHANGELOG.md` — version history and known issues
- `docs/ARCHITECTURE.md` — project structure and design decisions
- `docs/SUMMARY.md` — condensed project summary

## Forbidden Patterns

- Do not create skills that modify other skills' files without explicit coordination
- Do not use `eval` or dynamic code execution in shell scripts
- Do not add dependencies without documenting them in the relevant skill's `SKILL.md`
- Do not create circular dependencies between skills
