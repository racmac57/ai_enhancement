# How-to: /run-mva-etl

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.  
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `run-mva-etl` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\run-mva-etl\SKILL.md` |
| **Invoke** | `/run-mva-etl` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Wrap `mva_crash_etl.py` in Workbook_Redesign_2026 with preflight + post-checks — schema validation, row-count delta vs prior, S2/S3/S4 proof, unit/metric distribution sanity. Emits a Markdown run report. Use for the monthly MVA crash refresh.

## When to use

- Monthly MVA crash refresh or Power BI fact table update.
- User asks to run the MVA ETL, refresh crashes, or regenerate `fact_mva_crashes`.
- After CAD + timereport exports have passed `/preflight-export`.

## How to use

```
/run-mva-etl
```

Workflow (see `SKILL.md` for full checklists):

1. Optionally capture prior state from `Data_Load/fact_mva_crashes_2026.csv` (counts, max date, distributions).
2. Lightweight preflight: ensure `Data_Ingest/CAD_RMS_Exports/` has a `*CAD*.xlsx` and `*timereport*.xlsx`, each **> 10 KB**.
3. From the **Workbook_Redesign_2026** repository root:

```bash
python mva_crash_etl.py
```

4. Post-validate the output CSV (canonical schema, dtypes, S2/S3/S4, deltas, date coverage, unit WARN thresholds).
5. Emit the Markdown run report template from the skill.

**Related:** `/preflight-export`, `/clean-cad-export`; `/standardize-m-code` and `/apply-s2-s3-s4` for other Workbook_Redesign units.

## Output / artifacts

- **Data:** `Data_Load/fact_mva_crashes_2026.csv` (overwritten by the ETL).
- **Human-facing:** A Markdown **run report** (sources, row counts, schema PASS/FAIL, S2/S3/S4 proof, unit/metric distributions, overall PASS/FAIL).

The skill does not modify `mva_crash_etl.py`; it orchestrates validation around the existing script.

## Gotchas

- **Active project must be Workbook_Redesign_2026** so `Data_Ingest/` and `Data_Load/` resolve. Do not use placeholder paths like `/home/user/...`.
- **Overwrite risk:** The script replaces the fact CSV; if post-checks fail, recover from git (`git checkout HEAD~1 -- Data_Load/fact_mva_crashes_2026.csv` if needed — see Hard rules in `SKILL.md`).
- **Negative row delta** or **Other/Admin** spike: follow the skill’s FAIL/WARN thresholds and investigation hints.

## Hardening

- **Scorecard:** [run-mva-etl_MEMORY.md](../../skill_memory/run-mva-etl_MEMORY.md)
- **Run date:** 2026-04-17
- **Result:** **9 / 9 PASS** — path placeholder removed from `SKILL.md`; end-to-end ETL execution is validated in the Workbook_Redesign_2026 repo, not in `00_dev`.
