# How-to: /standardize-compstat-wb

> **Refreshed** by `/qa-skill-hardening` Phase 7 (9/9 PASS).  
> Edit behavior in the source `SKILL.md`; keep this file in sync after changes.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | standardize-compstat-wb |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\standardize-compstat-wb\SKILL.md` |
| **Invoke** | `/standardize-compstat-wb` (name the legacy workbook + wave inventory context) |
| **Aggregated guide** | [global_skills.md](../global_skills.md) § 11d |

## One-line description

Phase 3 showpiece — redesign one legacy Compstat workbook from sheet-per-month + `_mom` pivot into macro-free `.xlsx` on canonical `Date|Unit|MetricGroup|Metric|Value` schema. Wires `pReportMonth`, rewrites M code (S2/S3/S4), audits macros. Per-workbook.

## When to use

- Phase 2/3 per-workbook redesign after `/inventory-wave` has documented the workbook.
- User names a legacy workbook in `01_Legacy_Copies/` (e.g. “standardize patrol_monthly”).
- You need a full redesign plan: metric catalog, flat preview, validation rules, M-code strategy, macro audit, human Excel checklist.

## How to use

1. Open the **Workbook_Redesign_2026** repo as the active project (or obtain explicit paths from the user).
2. Load `Docs/wave_<letter>_inventory.md` for that workbook.
3. Follow `SKILL.md` steps: catalog metrics, flat-table preview (read-only pandas), Community Outreach schema check, validation rules, Patrol Summons bypass if applicable, M rewrite via `python standardize_m_code.py --target-dir 02_Legacy_M_Code --file <unit>.m` (dry-run, then `--apply`), macro audit for `.xlsm`.
4. Emit `Docs/redesign_<unit>.md` with the full plan.

Do **not** use Python to write workbook structure by default (`openpyxl.save` / `to_excel` for structure). Optional XML zip surgery only if the user explicitly opts in and confirms.

## Output / artifacts

- `Docs/redesign_<unit>.md` — redesign plan (catalog, preview, validation, M summary, macro disposition, Excel checklist).
- Updated `.m` under `02_Legacy_M_Code/<unit>/` when the user runs the standardize helper with `--apply`.
- Optional new `.xlsx` via XML assembly only when explicitly requested.

## Gotchas

- Paths (`01_Legacy_Copies/`, `Docs/`, `02_Legacy_M_Code/`) are relative to **Workbook_Redesign_2026** — not `ai_enhancement` or SCRPA.
- Product rules live in **`Claude.md`** at the Workbook repo root (read-only on `01_Legacy_Copies/`, macro-free `.xlsx`, `pReportMonth`, no hardcoded month columns).
- For Patrol, Summons is out of scope in the redesigned workbook (DAX join to `summons_slim_for_powerbi.csv`).

## Hardening

- **Scorecard:** [standardize-compstat-wb_MEMORY.md](../../skill_memory/standardize-compstat-wb_MEMORY.md)
