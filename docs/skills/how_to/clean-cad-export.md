# How-to: /clean-cad-export

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.  
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
| --- | --- |
| **Scope** | GLOBAL |
| **Skill name** | `clean-cad-export` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\clean-cad-export\SKILL.md` |
| **Invoke** | `/clean-cad-export [optional-export-path]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

CAD-export cleanup for Workbook_Redesign_2026 - strip newline from `ReportNumberNew`, normalize 15+ `How Reported` variants, preserve case-number dtype, and emit cleaned copy plus markdown diff.

## When to use

- `/preflight-export` reports WARN/FAIL on CAD export hygiene.
- Before `/run-mva-etl` or joins where case-number key quality matters.
- When monthly CAD export shows `How Reported` drift (casing, typos, newline artifacts).

## How to use

```text
/clean-cad-export
```

Input behavior:

- Default: latest `*CAD*.xlsx` from `Data_Ingest/CAD_RMS_Exports/`
- Optional: explicit source path supplied by user

Core transformations (in order):

1. Force `ReportNumberNew` to string dtype.
2. Strip embedded newlines and surrounding whitespace in `ReportNumberNew`.
3. Normalize `How Reported` values to canonical set (`911`, `Email`, `Radio`, `Walk-In`, `Phone`, `Self-Initiated`, `Alarm`, `Other`).
4. Trim categorical whitespace (`Incident`, `Disposition`, `Response Type`, `FullAddress2`).
5. Remove leading `" & "` in `FullAddress2`.
6. Preserve `HourMinuetsCalc` column name exactly (do not rename).

## Output / artifacts

- Cleaned workbook: `Data_Ingest/CAD_RMS_Exports/_cleaned/<original_basename>__cleaned.xlsx`
- Markdown diff report to stdout with:
  - input/output row counts
  - `ReportNumberNew` newline strip counts
  - per-variant `How Reported` normalization counts
  - categorical trim counts
  - `FullAddress2` prefix-fix counts

## Gotchas

- Never overwrite the original CAD export in place.
- Never write to `01_Legacy_Copies/`.
- Skill scope is text normalization only; S2 totals filtering and S3 dedupe are downstream concerns (`/apply-s2-s3-s4` or `mva_crash_etl.py`).

## Hardening

- **Scorecard:** [clean-cad-export_MEMORY.md](../../skill_memory/clean-cad-export_MEMORY.md)
- **Run date:** 2026-04-17
- **Result:** **9 / 9 PASS** - source `SKILL.md` required no modifications.
