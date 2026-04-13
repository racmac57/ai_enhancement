# Contributing — Adding New Skills

## Creating a New Skill

### 1. Create the skill directory

```bash
mkdir -p .claude/skills/my-new-skill
```

### 2. Write the SKILL.md

Create `.claude/skills/my-new-skill/SKILL.md` with required frontmatter:

```yaml
---
name: my-new-skill
description: Brief description of what it does and when to use it.
argument-hint: "[optional-args]"
---

# My New Skill

Instructions for Claude when this skill is invoked...
```

### Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Slash command name. Lowercase, hyphens only, max 64 chars. |
| `description` | Yes | What it does and when to trigger. Under 250 chars. |
| `argument-hint` | No | Shown in autocomplete (e.g., `[file] [format]`) |
| `allowed-tools` | No | Space-separated tools to pre-authorize |
| `effort` | No | `low`, `medium`, `high`, or `max` |
| `disable-model-invocation` | No | `true` to prevent auto-invocation |
| `user-invocable` | No | `false` to hide from slash menu (default: `true`) |

### 3. Use `$ARGUMENTS` for user input

```yaml
---
name: analyze
description: Analyze a target file or directory
argument-hint: "[path]"
---

Analyze `$ARGUMENTS` for code quality issues...
```

Users invoke with `/analyze src/utils` and Claude receives the path.

### 4. Add supporting files (optional)

```
.claude/skills/my-new-skill/
  SKILL.md              # Main skill file
  templates/            # Reference templates
  examples/             # Example inputs/outputs
  scripts/helper.sh     # Helper scripts
```

## Naming Rules

- Directory name: lowercase with hyphens (`qa-skill-hardening`)
- Skill file: always `SKILL.md` (uppercase)
- Helper scripts: lowercase with hyphens (`run-audit.sh`)
- No spaces, no underscores in directory names

## Checklist Before Committing

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`
- [ ] `name` field matches the directory name
- [ ] `description` is under 250 characters
- [ ] No hardcoded absolute paths — uses relative paths or `$CLAUDE_PROJECT_DIR`
- [ ] No secrets, credentials, or API keys
- [ ] Shell scripts (if any) use `set -euo pipefail`
- [ ] Scripts are idempotent (safe to re-run)
- [ ] Added an entry to `CHANGELOG.md`
- [ ] Updated the skill table in `README.md`

## Validating Your Skill

Run the QA hardening swarm against your new skill:

```
/qa-skill-hardening my-new-skill
```

This will run the 9-step binary test framework and produce a scorecard in `docs/skill_memory/my-new-skill_MEMORY.md`.

## Installing Globally

To make a skill available across all your projects:

```bash
cp -r .claude/skills/my-new-skill ~/.claude/skills/
```
