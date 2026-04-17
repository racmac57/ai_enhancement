# How-to: `/hpd-exec-comms`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `hpd-exec-comms` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\hpd-exec-comms\SKILL.md` |
| **Invoke** | `/hpd-exec-comms` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) (section **/hpd-exec-comms (global add-on)**) |

## One-line description

HPD Executive Communications Chief: turn raw law enforcement drafts or data into polished **internal**, **command-staff**, or **descriptive/technical** writing for the Hackensack PD SSOCC — only when the audience and scope match HPD (not generic rewrite, not press releases).

## When to use

- Internal department or supervisor-facing communications.
- Executive summaries, briefings, or civilian-oversight material for command.
- Incident narratives, police reports, or other fact-based descriptive records.

## How to use

1. Invoke `/hpd-exec-comms`.
2. Provide source text or data.
3. The skill classifies intent (Executive Rewrite vs Internal Email vs Incident Narrative) using the table in `SKILL.md`.
4. If audience/format is ambiguous, clarify before drafting.

## Output / artifacts

- Polished prose per **Intent Detection** and the format sections in `SKILL.md` (signature blocks, brevity, formal tone).

## Gotchas

- **Do not** use for generic “polish this” without clear HPD/SSOCC scope.
- **Do not** use for press releases.
- Policy memos / training bulletins: confirm audience and scope first.

## Hardening

- Scorecard (when run from a project with `docs/skill_memory/`): `docs/skill_memory/hpd-exec-comms_MEMORY.md` or equivalent.
