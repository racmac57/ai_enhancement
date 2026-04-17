# How-to: /arcgis-pro

> **Auto-generated** by `/qa-skill-hardening` Phase 7 after this skill scored **9/9 PASS** on 2026-04-16.
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|-------|
| **Scope** | GLOBAL |
| **Skill name** | `arcgis-pro` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\arcgis-pro\SKILL.md` |
| **Invoke** | `/arcgis-pro` (or auto-triggers when writing arcpy scripts) |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Guides writing Python scripts for ArcGIS Pro's bundled arcpy environment, enforcing constraints like no pip, scratchGDB usage, and exec-compatible patterns.

## When to use

- Writing or modifying Python scripts that run inside ArcGIS Pro's bundled Python (arcpy)
- Clery, SCRPA, CAD dashboard scripts that execute in the Pro Python window or as scheduled Pro-env tasks on the RDP server
- Any geoprocessing workflow that should NOT rely on pip-installed packages

Skip when the script is a pandas/openpyxl ETL without arcpy — use `etl-pipeline` instead.

## How to use

```
/arcgis-pro
```

Typical session: describe the geoprocessing task, paste existing script, or ask Claude to scaffold a new arcpy script. The skill enforces Pro-compatible patterns automatically.

## Output / artifacts

No files produced directly. The skill shapes the code Claude writes into other files — arcpy scripts compatible with:

- `exec(open(r"path\to\script.py").read())` from the Pro Python window
- Command-line / Task Scheduler invocation via the ArcGIS Pro Python interpreter (`C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`)

## Gotchas

- **No `pip install`** in the Pro default env. If the user documents a cloned env, note it explicitly.
- **No PyYAML**, no package-style `__init__.py` unless the project already uses them in Pro.
- **scratchGDB**, not `in_memory`, for intermediate data in long workflows. Clear scratchGDB contents between runs for idempotency.
- **`sys.argv` under `exec()` is NOT populated** — only works for command-line / Task Scheduler invocation. For Pro Python window exec, set module-level variables in the Pro window before `exec()`.
- **`print()` vs `arcpy.AddMessage`:** inside geoprocessing tools, use `arcpy.AddMessage/AddWarning/AddError`; `print()` only surfaces in the Python window.
- **Error handling:** wrap arcpy calls with `try/except arcpy.ExecuteError` and surface `arcpy.GetMessages(2)` for full tool diagnostics. Exit non-zero (`sys.exit(1)`) on failure so Task Scheduler's LastTaskResult reflects it.
- **Paths:** respect `carucci_r` OneDrive root; use `path_config.get_onedrive_root()` when the script also writes file outputs. Never hardcode `RobertCarucci`.
- **Project-specific imports** (local geocoding helpers, etc.) live under `10_Projects/*/CLAUDE.md` — consult that before inventing new paths.

## Hardening

- **Scorecard:** `~/.claude/skills/docs/skill_memory/arcgis-pro_MEMORY.md` — **9/9 PASS** on 2026-04-16 (Iteration 2 after T6 Error Handling fix); future runs refresh the same path.
