# How-to: /clean-summons-export

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `clean-summons-export` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\clean-summons-export\SKILL.md` |
| **Invoke** | `/clean-summons-export [optional-input-path]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

E-Ticket summons cleanup for Workbook_Redesign_2026 with semicolon parsing, whitespace cleanup, date normalization, dual-use slash-column splitting, and slim output for Power BI DAX joins.

## When to use

- Monthly summons export lands in `Data_Ingest/CAD_RMS_Exports/`.
- `/preflight-export` identified an E-Ticket CSV needing cleanup.
- You need to refresh `Data_Load/summons_slim_for_powerbi.csv` for model refresh.

## How to use

```text
/clean-summons-export
```

Optional explicit source:

```text
/clean-summons-export Data_Ingest/CAD_RMS_Exports/2026_03_eticket_export.csv
```

## Output / artifacts

- Overwrites `Data_Load/summons_slim_for_powerbi.csv` (idempotent monthly target).
- Emits a cleanup report summarizing:
  - input vs output rows
  - malformed-row warnings
  - whitespace strips
  - dropped empty columns
  - parking vs moving counts

## Gotchas

- Source delimiter is `;`, not `,`.
- `Charge Time` is HHMM-like text and must be normalized (`0310` -> `03:10`).
- Slash columns are context-dependent on `Case Type Code` and must be split.
- Keep PII columns out of outputs/logs (`Defendant Last Name`, `License Plate Number`, address fields).
- Never write to `01_Legacy_Copies/`, and never recreate a Summons worksheet in the Patrol workbook.

## Hardening

- **Scorecard:** `docs/skill_memory/clean-summons-export_MEMORY.md` (9/9 PASS on 2026-04-17).
