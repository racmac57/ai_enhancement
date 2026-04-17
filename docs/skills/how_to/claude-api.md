# How-to: /claude-api

> **Pointer stub** — `/claude-api` is a **built-in Claude Code skill**, not a repo SKILL.
> This file exists for discoverability and to keep SKILLS_INDEX.md link-clean.
> There is **no** `SKILL.md` on disk for this skill.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `claude-api` |
| **SKILL.md path** | **Built-in Claude Code skill — no custom SKILL.md on disk.** See [Anthropic Claude API docs](https://docs.anthropic.com/en/api/overview) and the aggregated guide. |
| **Invoke** | `/claude-api` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Build and debug Claude API applications.

## When to use

- Adding or tuning **prompt caching** in an Anthropic SDK codebase.
- Migrating existing Claude API code between model versions (e.g. 4.5 → 4.6, 4.6 → 4.7).
- Using Anthropic SDK features — tool use, batch, files, citations, thinking, memory, managed agents.
- Debugging why cache hits are low or why a model change broke behavior.

## How to use

```
/claude-api
```

Or let it auto-trigger when code imports `anthropic` / `@anthropic-ai/sdk` and you start editing.

## Output / artifacts

No separate files. Edits go directly into the SDK code you're working on.

## Gotchas

- **Triggers only in an Anthropic SDK codebase.** Skip entirely for OpenAI or other-provider SDKs — filename patterns like `*-openai.py` / `*-generic.py` are left alone.
- Provider-neutral / general-ML code should not invoke this skill.
- Official reference: https://docs.anthropic.com/en/api/overview
- This is **NOT** a hardened project skill; no `/qa-skill-hardening` score applies.
