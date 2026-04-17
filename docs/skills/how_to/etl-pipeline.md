# How-to: /etl-pipeline

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|-------|
| **Scope** | GLOBAL |
| **Skill name** | `etl-pipeline` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\etl-pipeline\SKILL.md` |
| **Invoke** | `/etl-pipeline` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Standard ETL workflow for CAD, RMS, Arrests, and Summons pipelines under `02_ETL_Scripts` — enforces load patterns, path resolution, pre-write quality checks, and archive-first outputs.

## When to use

- Writing a new ETL script under `02_ETL_Scripts/` or modifying an existing one.
- Reading an Excel export that contains a case-number column (`ReportNumberNew`, `ComplaintNum`, `SummonsNumber`, etc.) — dtype must be forced to string.
- Need a refresher on the 6-step pipeline shape before writing code.
- Deciding whether a pipeline belongs under the ArcGIS Pro carve-out (see Gotchas).

## How to use

```
/etl-pipeline
```

Guidance-only skill — no arguments. Claude responds with the standard load pattern, pipeline shape, library list, and reference pointers.

Companion skills:

| Scenario | Use |
|----------|-----|
| Start a fresh ETL project | `/new-etl Project_Name` (scaffolds), then `/etl-pipeline` (guides the code) |
| Run quality checks on the loaded frame | `/data-validation` or `/validate-data` |
| Lint existing scripts for path hygiene | `/check-paths` |
| Script will run inside ArcGIS Pro's `arcpy` env | `/arcgis-pro` instead (no PyYAML, no pip, `scratchGDB` not `memory`) |

## Output / artifacts

None. The skill returns guidance text:

1. **Standard Load Pattern** — `pd.read_excel(path, dtype={"ReportNumberNew": str})`
2. **Pipeline Shape** —
   1. Resolve paths with `path_config.get_onedrive_root()` or project-relative paths.
   2. Load source; validate required columns against `09_Reference/Standards/`.
   3. Normalize fields (dates, categories, addresses).
   4. Run quality checks (nulls, duplicates, domain values) **before** writing.
   5. Write outputs under the project folder or `13_PROCESSED_DATA/` using `YYYY_MM_DD_` naming.
   6. Archive superseded source under `archive/` with a datestamp — never delete.
3. **Libraries** — prefer `pandas`, `openpyxl`, `pathlib`, `PyYAML` (where not ArcGIS Pro); `pyodbc` only for explicitly defined SQL sources.

## Gotchas

- **Case-number dtype is load-time only.** Once pandas has inferred int for `ReportNumberNew`, leading zeros are gone and cannot be recovered. Pass `dtype={"ReportNumberNew": str}` in the `read_excel` / `read_csv` call.
- **`path_config.py` is a convention, not a shipped module.** Global `CLAUDE.md` declares the function `get_onedrive_root()`; only a handful of projects actually ship the helper. `/new-etl` scaffolds it — if you are inside an older project that lacks the helper, either create it or fall back to project-relative paths.
- **`RobertCarucci` never appears in scripts.** The canonical Windows user is `carucci_r`. Hardcoded `RobertCarucci` paths break on this desktop.
- **Archive, do not delete.** When replacing an export, move the old file to `archive/<YYYY_MM_DD>_…` so every run remains auditable.
- **ArcGIS Pro exception.** The arcpy environment has no pip, no PyYAML, and must use `scratchGDB` rather than in-memory workspaces. Use `/arcgis-pro` for those scripts instead.
- **Skill description lists CAD/RMS/Arrests/Summons only.** NIBRS and Clery ETLs follow the same shape but are not enumerated in the frontmatter. Treat the skill as the pattern, not the exhaustive domain list.

## Hardening

- Last scorecard: `C:\Users\carucci_r\.claude\skills\docs\skill_memory\etl-pipeline_MEMORY.md`
- Run date: 2026-04-16
- Result: **9 / 9 PASS** — clean first pass, no fixes applied
