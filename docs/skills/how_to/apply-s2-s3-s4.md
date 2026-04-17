# How-to: `/apply-s2-s3-s4`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `apply-s2-s3-s4` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\apply-s2-s3-s4\SKILL.md` |
| **Invoke** | `/apply-s2-s3-s4` (provide inputs in chat) |
| **Aggregated guide** | [global_skills.md](../global_skills.md) (section **/apply-s2-s3-s4**) |

## One-line description

Generic S2/S3/S4 applier for Workbook_Redesign_2026 — given a raw flat table + primary-key column, emit refactored DataFrame (S2 totals dropped, S3 deduped, S4 Value=1 shim) + equivalent Power Query M snippet. Use for any non-MVA unit in Phase 2.

## When to use

- Phase 2 workbook redesign for any unit that still uses a flat extract (not MVA crashes).
- User asks to apply S2/S3/S4, prep for unpivot, or generate M-code stubs for a new flat source.
- You need the same ordering as `mva_crash_etl.py` without copying that script.

## How to use

1. Confirm the **Workbook_Redesign_2026** tree (or the user’s path) is available — `mva_crash_etl.py` / `standardize_m_code.py` are **not** in `ai_enhancement`.
2. Invoke `/apply-s2-s3-s4` and supply:
   - Path to `.csv` or `.xlsx`, **or** a DataFrame already in scope
   - Primary-key column (string); for composite keys, pass a list of columns for `drop_duplicates`
   - Totals row substring (default `"Total"`) — if metrics could false-positive, narrow the label or column scope per `SKILL.md`
   - Value behavior: `shim` (default `Value=1`) or `existing` to coerce an existing `Value` column
3. Optionally save to `<original_dir>/_refactored/<basename>__s2s3s4.csv`.
4. Paste the emitted **M snippet** into the redesigned `.m` file and substitute `<TableName>` / `<PK_COL>` (and align S2 row logic if subtotals are not in the PK field).

## Output / artifacts

- In-memory `pandas` DataFrame after **S2 → S3 → S4** (order fixed).
- Markdown report: rows dropped per step, optional save path.
- Power Query M block for Excel — equivalent structure, may differ from Python on which columns detect “totals” (see Gotchas).

## Gotchas

- **Never** modify `01_Legacy_Copies/` in place — read-only.
- **Performance:** very wide tables with >1M rows: row-wise S2 can be slow; warn before running.
- **M vs Python:** sample M filters totals using the PK column; Python `_is_totals_row` defaults to scanning all string columns — document any intentional gap when pasting M.
- **Repository context:** see `Repository context` and `Failure modes` in `SKILL.md` for missing files, missing PK, and totals over-match.

## Hardening

- **Scorecard:** `docs/skill_memory/apply-s2-s3-s4_MEMORY.md`
- Status as of 2026-04-17: **9/9 PASS**
