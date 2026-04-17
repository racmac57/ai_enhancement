# How-to: /simplify

> **Pointer stub** — `/simplify` is a **built-in Claude Code skill**, not a repo SKILL.
> This file exists for discoverability and to keep SKILLS_INDEX.md link-clean.
> There is **no** `SKILL.md` on disk for this skill.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `simplify` |
| **SKILL.md path** | **Built-in Claude Code skill — no custom SKILL.md on disk.** See aggregated guide. |
| **Invoke** | `/simplify` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Review changed code for quality and simplification opportunities.

## When to use

- After a sizeable diff, before opening a PR.
- Looking for dead code, over-engineering, premature abstraction, or duplicated logic.
- Quick quality pass on changes you just made — not a deep audit of the whole codebase.

## How to use

```
/simplify
```

Run it after edits and before committing. Best paired with a PR-prep step.

## Output / artifacts

No separate files. Fixes are applied directly in the changed files.

## Gotchas

- **Runs over CHANGED code only.** Unchanged files are untouched — do not expect a full-codebase cleanup.
- Best used on modest diffs; on very large diffs, break review into chunks.
- This is **NOT** a hardened project skill; no `/qa-skill-hardening` score applies.
