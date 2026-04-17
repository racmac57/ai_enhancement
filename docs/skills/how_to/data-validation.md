# How-to: `/data-validation`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `data-validation` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\data-validation\SKILL.md` |
| **Invoke** | `/data-validation` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) (section **/data-validation**) |

## One-line description

Run standard data quality checks (completeness, domain values, duplicates, case-number format, null patterns, before/after deltas) on Excel or CSV datasets before deployment to dashboards or reports.

## When to use

- After ETL processing, after normalization, before production handoff (ESRI polished layers, Power BI, monthly RMS/CAD exports).
- When replacing a previously-published file and you need a before/after delta on row counts and key metrics.
- As the QC step at §4 of any ETL pipeline produced via `/etl-pipeline`.

## How to use

1. Invoke `/data-validation`.
2. Provide a path to an `.xlsx` or `.csv` file.
3. The skill loads the file with `dtype={'ReportNumberNew': str, 'CaseNumber': str}` (mandatory — preserves `YY-NNNNNN`), then runs the six checks documented in `SKILL.md`:
   - Completeness (per column `notna()` share; flag critical fields below 99%)
   - Domain values (compare categoricals against canonical lists in `09_Reference/Standards/`)
   - Duplicates on natural keys (`ReportNumberNew`, etc.)
   - Case-number format `\d{2}-\d{6}`
   - Cross-field null patterns
   - Before/after row count + metric deltas (when replacing a file)
4. Review the PASS/FAIL summary table; act on the failing checks.

## Output / artifacts

A concise table or bullet summary written to the chat:

- One PASS/FAIL row per check
- Counts and example failing keys/row IDs
- Missing required columns are surfaced as **N/A** (not silently coerced to PASS)
- Missing or unreadable input files cause the run to **stop and report the path**

No files are written by the skill itself.

## Gotchas

- **Always force string dtype on case numbers at load time** — `pd.read_excel(path, dtype={'ReportNumberNew': str, 'CaseNumber': str})`. This is a hard CLAUDE.md rule; if you skip it, Excel strips leading zeros from `YY-NNNNNN`.
- Default critical-fields completeness threshold is **99%**. Non-critical fields are reported only; they do not fail the run unless the user opts in to stricter rules.
- Sibling artifact `~/.claude/commands/validate-data.md` covers the same domain via `/validate-data` (command-style). Functionally equivalent for routine validation; same load conventions apply.
- Canonical reference for field names and formats: `09_Reference/Standards/CAD_RMS/DataDictionary/current/schema/canonical_schema.json`.

## Hardening

- **Scorecard:** After `/qa-skill-hardening` Phase 7, see `~/.claude/skills/docs/skill_memory/data-validation_MEMORY.md` when generated.
- Status as of 2026-04-16: **9/9 PASS** (Iteration 2). Regression markers: `## Inputs & Failure Modes` header (T6) + `dtype={'ReportNumberNew': str` literal (T8) — see `REGRESSION_TESTS.md`.
