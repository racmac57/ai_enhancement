<!-- REFERENCE SNAPSHOT — do not edit directly.
     Source of truth: C:\Users\carucci_r\.claude\skills\session-handoff\SKILL.md
     Update this file by re-running /qa-skill-hardening Phase 7 or syncing manually. -->

# How-to: `/session-handoff`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `session-handoff` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\session-handoff\SKILL.md` |
| **Invoke** | `/session-handoff` |
| **Argument hint** | none |
| **Allowed tools** | text-only (skill is prose — no tools required at invoke time) |
| **Agents** | `[main_agent, general_purpose]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Generate a two-part **SESSION HANDOFF DOCUMENT** for the next Claude chat — an
`OPENING PROMPT` blockquote (identity + active domains + tech stack + verbatim
behavioral directives) followed by a `HANDOFF BODY` (status, decisions,
artifacts, critical context, open questions, next best action) — with built-in
conflict resolution, PII / credential guardrails, and strict nil-state fallbacks.

## When to use

- You're about to close a working session and want a clean primer for the next chat.
- You need a continuity package to paste as the first message of a new conversation.
- You want a structured record of decisions / artifacts / blockers before context is lost.
- Trigger phrases: `handoff`, `continuity`, `next session`, `wrap up`,
  `summarize for next chat`, `I'm done for today`, `closing out`.

## How to use

```text
/session-handoff
```

No arguments. The skill reviews the **entire current conversation** and emits a
single Markdown document with two parts, separated by a horizontal rule.

## Output / artifacts

A single Markdown document, ≤900 words for standard sessions (absolute ceiling
1,400 words for artifact-heavy sessions), with:

### Part 1 — OPENING PROMPT

Plain-Markdown heading line `## OPENING PROMPT — PASTE AS FIRST MESSAGE`
followed by a GitHub-flavored blockquote containing:

- `Role:` R. A. Carucci (#261), Principal Analyst, SSOCC, Hackensack PD, NJ
- `Active domains:` only what was actually discussed this session (or the
  literal nil string `Active domains: none mentioned this session.`)
- `Tech stack:` only what was actually referenced this session (or the literal
  nil string `Tech stack: none mentioned this session.`) — never inferred from
  CLAUDE.md
- `Audience:` (e.g. command staff, or "unknown" if not specified)
- 7 behavioral directives verbatim (output-first, no filler, mentor challenge, etc.)

### Part 2 — HANDOFF BODY

- `PROJECT / TASK` — one-line summary
- `SESSION METADATA` — **always emitted**, never omitted (Generated timestamp, Handoff version)
- `STATUS` — ✅ Completed / 🔄 In progress / ⏳ Pending
- `KEY DECISIONS` — `Decision → Reason` + `Rejected:` block (or `No rejected options this session.`)
- `ARTIFACTS` — per-item Name / Path / Purpose / Persistence (or `No artifacts this session.`)
- `CRITICAL CONTEXT` — `Category: detail` form, from a fixed vocabulary (Data source, Dependency, Constraint, Version, Dead end, Deadline)
- `OPEN QUESTIONS / BLOCKERS`
- `NEXT BEST ACTION` — **one item only**, no sub-bullets
- `ENVIRONMENT SNAPSHOT` — only if code / data / config was touched

## Gotchas

- **Conflict resolution runs first.** The skill scans for contradictory
  instructions before writing; when two versions exist it uses the **latest**
  position and flags the lingering conflict under OPEN QUESTIONS with ⚠️.
  Never silently reconciles.
- **Tech stack is evidence-only.** Do NOT infer from CLAUDE.md, repo state, or
  general knowledge unless the user pasted that material into **this** chat.
- **Badge `#261`** — appears in exactly 2 places (task header + blockquote
  Role line). Any drift is a regression.
- **PII pass.** Passwords / API keys / connection strings → `[REDACTED]`;
  case numbers / badges / subject-identifying detail → `[REVIEW BEFORE SHARING]`;
  internal hosts / IPs → `[REVIEW BEFORE SHARING]`. Flagged, not silently deleted.
- **Word ceiling.** Over the 900-word soft / 1,400-word hard ceiling? Compress
  CRITICAL CONTEXT and STATUS prose first. Never truncate ARTIFACTS or
  NEXT BEST ACTION.
- **Omit-not-empty rule.** Any HANDOFF BODY subsection with nothing to report is
  omitted — except SESSION METADATA (always emitted) and ARTIFACTS (emit nil line).
- **Trivial / empty conversation.** Say so in PROJECT / TASK in one line and
  omit all other subsections.

## Hardening

- **Scorecard:** `C:\Users\carucci_r\.claude\docs\skill_memory\session-handoff_MEMORY.md` — 9/9 PASS (2026-04-19)
- **Regression invariants:** 7 rules captured in `REGRESSION_TESTS.md` (R1–R7).
