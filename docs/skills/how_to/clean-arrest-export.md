# How-to: /clean-arrest-export

> Auto-generated or refreshed by `/qa-skill-hardening` Phase 7 when this skill scores 9/9 PASS.  
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `clean-arrest-export` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\clean-arrest-export\SKILL.md` |
| **Invoke** | `/clean-arrest-export [optional-input-path]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

LawSoft arrest-export cleanup for Workbook_Redesign_2026, including S2 totals filtering, whitespace normalization, reviewer casing normalization, Race/UCR splits, ATS header/footer handling, and artifact-column cleanup.

## When to use

- `/preflight-export` flagged an arrest export.
- User asks to clean or normalize LawSoft/ATS arrest data.
- Before Workbook_Redesign inventory/redesign phases that rely on grouped arrest metrics.

## How to use

```text
/clean-arrest-export
```

- Default input is latest `*LawSoft*Arrest*.xlsx` under `Data_Ingest/CAD_RMS_Exports/`.
- ATS variant (`*ATS*.xlsx`) uses 4-row header skip and footer trim.
- Optional explicit file path is supported.

## Output / artifacts

- Cleaned workbook at `Data_Ingest/CAD_RMS_Exports/_cleaned/<original_basename>__cleaned.xlsx`.
- Markdown cleanup report to stdout (row deltas, normalization counts, dropped columns, PII warning for `SS#Calc`).

## Gotchas

- Never overwrite the source export in place.
- Never write to `01_Legacy_Copies/`.
- Keep case-number fields as strings on load (`ReportNumberNew`).
- Do not print raw `SS#Calc` values in chat/log output.
- Stop with a clear error if required columns are missing or ATS header/footer parsing fails.

## Hardening

- **Scorecard:** `docs/skill_memory/clean-arrest-export_MEMORY.md` in the `ai_enhancement` documentation hub.
