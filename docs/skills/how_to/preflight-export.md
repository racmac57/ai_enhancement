# How-to: /preflight-export

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.  
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `preflight-export` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\preflight-export\SKILL.md` |
| **Invoke** | `/preflight-export [optional file path or glob]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Validate raw CAD/RMS/arrest/summons exports in `Data_Ingest/CAD_RMS_Exports` before ETL to catch corrupt files and schema drift at the boundary.

## When to use

- Before running `mva_crash_etl.py` or `/run-mva-etl`.
- Before any `/clean-*-export` workflow.
- After receiving a fresh monthly CAD/RMS/arrest/e-ticket/ATS drop.

## How to use

```text
/preflight-export
```

Optional: provide an explicit path or glob when validating a specific file instead of default discovery.

## Output / artifacts

- Emits a Markdown report to stdout with per-file PASS/WARN/FAIL checks.
- Reports include size/openability/header contract/delimiter/gotcha scans and row-count sanity drift.
- No files are created or modified.

## Gotchas

- Read-only rule is strict: do not rename/move/modify exports and never write into `01_Legacy_Copies/`.
- E-Ticket delimiter must be `;` (sniff for drift).
- ATS header starts on row 5 (`skiprows=4`).
- Preserve case-number columns as strings (`ReportNumberNew`, `Control #`) to prevent zero-loss.
- If the known RMS null-byte corruption pattern appears, mark FAIL and stop; do not attempt repair.

## Hardening

- **Scorecard:** `docs/skill_memory/preflight-export_MEMORY.md` (this repo hardening run, 2026-04-17).
