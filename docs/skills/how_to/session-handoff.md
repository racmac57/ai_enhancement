# How-to: /session-handoff

> **Auto-generated / refreshed** by `/qa-skill-hardening` Phase 7 when the skill scores **9/9 PASS**.
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `session-handoff` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\session-handoff\SKILL.md` |
| **Source-of-truth** | `<dotclaude-repo>\skills\session-handoff\SKILL.md` (deployed via `Deploy-ClaudeConfig.ps1`) |
| **Invoke** | `/session-handoff` (or trigger phrases: "handoff", "continuity", "next session", "wrap up", "I'm done for today", "closing out") |
| **Type** | Write-capable — renders Markdown AND archives to disk |
| **Aggregated guide** | [global_skills.md](../global_skills.md) § 13 |
| **Last hardened** | 2026-04-22 — 9/9 PASS (write-capable era) |

## One-line description

Generate a structured session handoff (OPENING PROMPT + HANDOFF BODY) and archive it to `00_dev/handoffs/<date>_<topic>_handoff_v<N>.md` so the next chat session can resume cold with zero context loss.

## When to use

- End of a productive session — capture decisions, artifacts, open blockers, and the single highest-value next action.
- User signals wrap-up: "handoff", "continuity", "wrap up", "summarize for next chat", "I'm done for today", "closing out".
- Mid-session checkpoint when context is about to be compacted or the conversation is approaching its limit.
- Whenever the user wants a paste-able primer to start fresh without re-explaining the project.

## How to use

```
/session-handoff
```

No arguments. The skill reads the entire current conversation transcript directly.

### Pre-flight (skill runs this internally before drafting)

1. **Prior handoff in this conversation?** Scan for `## OPENING PROMPT — PASTE AS FIRST MESSAGE` or a `Handoff version: N` line. If found: bump to `N+1`, populate `Supersedes:`, and cover only the delta since the prior version.
2. **Repo state?** If session touched git, capture branch / last 5 commits / `status --short` and surface under ENVIRONMENT SNAPSHOT → Git state.
3. **Date resolution.** Convert relative dates ("yesterday", "Thursday") to absolute ISO dates.

### Conflict resolution (after pre-flight)

When two contradictory instructions appear in the conversation, use the **latest** stated position. Never silently reconcile — flag lingering contradictions under OPEN QUESTIONS with ⚠️.

## Output / artifacts

**In chat:** Two-part Markdown document.

- **Part 1 — OPENING PROMPT** (blockquote): role (R. A. Carucci #261, SSOCC, Hackensack PD), active domains mentioned this session, tech stack mentioned this session, audience, **session-specific deviations** from CLAUDE.md (not the defaults — only deviations).
- **Part 2 — HANDOFF BODY**: PROJECT/TASK, SESSION METADATA (Generated, Handoff version, Supersedes for v2+), STATUS (Completed / In progress / Pending), KEY DECISIONS (with Rejected sub-section), ARTIFACTS (anti-inference: only items explicitly named in this conversation), CRITICAL CONTEXT (categorized: Data source / Dependency / Constraint / Version / Dead end / Deadline), OPEN QUESTIONS / BLOCKERS, NEXT BEST ACTION (single item), ENVIRONMENT SNAPSHOT (only if code/data/config involved).

**On disk:**

```
C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\handoffs\<YYYY_MM_DD>_<short-topic>_handoff_v<N>.md
```

Filename: `<YYYY_MM_DD>_<short-topic>_handoff_v<N>.md`. Topic is 1–4 words, lowercase, underscores. Example: `2026_04_22_cad_etl_resume_handoff_v2.md`.

After saving, the skill appends a single line below the displayed document:

```
Saved: C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\handoffs\2026_04_22_cad_etl_resume_handoff_v2.md
```

If write fails (path missing, permission denied), the skill surfaces:

```
Save failed: <reason>
```

…and the chat copy still serves as the paste source. The archival copy is never silently dropped.

## Gotchas

- **No CLAUDE.md restatement.** OPENING PROMPT must NOT restate CLAUDE.md defaults (output-first, mentor approach, no filler, no theory-first, etc.). The next session loads CLAUDE.md automatically; restating them is noise that dilutes the real signal. Capture only **session-specific deviations**.
- **Anti-inference for tech stack AND artifacts.** List ONLY items explicitly mentioned in this conversation. Do not infer from CLAUDE.md, repo structure, or general knowledge. Tech stack defaults to `Tech stack: none mentioned this session.` if none discussed.
- **Versioning.** First handoff in a conversation is `v1`. If a prior handoff appears earlier in the same conversation, bump to `v2` and cover only the **delta** since v1 — do not regenerate unchanged context (reference it in one line: "Prior context unchanged from v1").
- **Word ceiling.** `≤900 words` standard, `≤1,400` absolute. If over limit, compress CRITICAL CONTEXT and STATUS prose first. **Never** truncate ARTIFACTS or NEXT BEST ACTION.
- **Single NEXT BEST ACTION.** Exactly one item. No sub-bullets, no secondary suggestions. Multiple critical actions go under OPEN QUESTIONS / BLOCKERS.
- **Path rule.** Always write under `carucci_r` (canonical), never under the underlying laptop profile name. CLAUDE.md forbids the substring `RobertCarucci` in scripts and configs — the skill's regression test R10 asserts this.
- **PII / credential safety.** Passwords / API keys / connection strings → `[REDACTED]`. Case numbers / badge numbers / subject-identifying detail / internal hosts/IPs → `[REVIEW BEFORE SHARING]`. Flag rather than silently delete.
- **Trivial conversation.** If the conversation was empty or trivial, say so in PROJECT / TASK in one line and omit the other Part 2 sections.

## Hardening

- **Scorecard:** `<dotclaude-repo>\docs\skill_memory\session-handoff_MEMORY.md` — 9/9 PASS as of 2026-04-22.
- **Regression invariants (12):** R1 (frontmatter contract), R2 (badge `#261` pin), R3 (nil-state clauses), R4-v2 (no CLAUDE.md restatement), R5 (structural invariants), R6 (NEXT BEST ACTION single-item), R7 (CRITICAL CONTEXT category-form), R8 (Pre-flight section), R9 (Persistence section), R10 (forbidden `RobertCarucci` substring), R11 (ARTIFACTS anti-inference), R12 (SESSION METADATA defaults). See `<dotclaude-repo>\docs\skill_memory\REGRESSION_TESTS.md` for full text.
- **R4 v1 retired 2026-04-22** — the verbatim 7-directive block was removed because it duplicated CLAUDE.md.
