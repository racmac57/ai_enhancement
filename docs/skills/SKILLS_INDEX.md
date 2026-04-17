# Claude Skills — Master Index

**Reference hub:** [README.md](README.md) — how this directory relates to skills that live anywhere on disk.

**Scopes**

- **GLOBAL** — `C:\Users\carucci_r\.claude\skills\<skill-name>\SKILL.md` (available in every Claude Code session).
- **PROJECT** — `<repo-root>\.claude\skills\<skill-name>\SKILL.md` (only when that repo is the active project).

**Per-skill how-to** — `how_to/<skill-name>.md` is **created or updated** when `/qa-skill-hardening` finishes Phase 7 for that skill (9/9 PASS). Until then, use the **Aggregated guide** column.

---

## GLOBAL skills

| Skill | SKILL.md path | Per-skill how-to | Aggregated guide | One-line description |
|-------|---------------|------------------|------------------|----------------------|
| qa-skill-hardening | `C:\Users\carucci_r\.claude\skills\qa-skill-hardening\SKILL.md` | [how_to/qa-skill-hardening.md](how_to/qa-skill-hardening.md) | [global_skills.md](global_skills.md) | Multi-agent QA swarm that auto-discovers, tests, and hardens every skill in a project |
| frontend-slides | `C:\Users\carucci_r\.claude\skills\frontend-slides\SKILL.md` | [how_to/frontend-slides.md](how_to/frontend-slides.md) | [global_skills.md](global_skills.md) | Build HTML presentations from scratch or from an existing PowerPoint |
| chunk-chat | `C:\Users\carucci_r\.claude\skills\chunk-chat\SKILL.md` | [how_to/chunk-chat.md](how_to/chunk-chat.md) | [global_skills.md](global_skills.md) | Chunk long conversations into sized pieces for RAG ingestion |
| arcgis-pro | `C:\Users\carucci_r\.claude\skills\arcgis-pro\SKILL.md` | [how_to/arcgis-pro.md](how_to/arcgis-pro.md) | [global_skills.md](global_skills.md) | Guide arcpy scripts for ArcGIS Pro's bundled Python (no pip, scratchGDB, exec-compatible) |
| data-validation | `C:\Users\carucci_r\.claude\skills\data-validation\SKILL.md` | [how_to/data-validation.md](how_to/data-validation.md) | [global_skills.md](global_skills.md) | Run standard data quality checks on Excel or CSV datasets before deployment |
| html-report | `C:\Users\carucci_r\.claude\skills\html-report\SKILL.md` | [how_to/html-report.md](how_to/html-report.md) | [global_skills.md](global_skills.md) | Generate HPD-branded, self-contained HTML reports |
| check-paths | `C:\Users\carucci_r\.claude\skills\check-paths\SKILL.md` | [how_to/check-paths.md](how_to/check-paths.md) | [global_skills.md](global_skills.md) | Scan a project for path-hygiene issues in scripts and configs |
| etl-pipeline | `C:\Users\carucci_r\.claude\skills\etl-pipeline\SKILL.md` | [how_to/etl-pipeline.md](how_to/etl-pipeline.md) | [global_skills.md](global_skills.md) | Standard ETL workflow for CAD/RMS/Arrests/Summons pipelines under 02_ETL_Scripts |
| frontend-design | `C:\Users\carucci_r\.claude\skills\frontend-design\SKILL.md` | [how_to/frontend-design.md](how_to/frontend-design.md) | [global_skills.md](global_skills.md) | Produce distinctive, production-grade UI designs |
| claude-api | `C:\Users\carucci_r\.claude\skills\claude-api\SKILL.md` | [how_to/claude-api.md](how_to/claude-api.md) | [global_skills.md](global_skills.md) | Build and debug Claude API applications |
| simplify | `C:\Users\carucci_r\.claude\skills\simplify\SKILL.md` | [how_to/simplify.md](how_to/simplify.md) | [global_skills.md](global_skills.md) | Review changed code for quality and simplification opportunities |
| hpd-exec-comms | `C:\Users\carucci_r\.claude\skills\hpd-exec-comms\SKILL.md` | [how_to/hpd-exec-comms.md](how_to/hpd-exec-comms.md) | [global_skills.md](global_skills.md) | HPD / SSOCC executive communications — polish drafts into formal internal, command-staff, or descriptive outputs |

---

## PROJECT: cad_rms_data_quality

**Repo root:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality`

| Skill | SKILL.md path | Per-skill how-to | Aggregated guide | One-line description |
|-------|---------------|------------------|------------------|----------------------|
| check-paths | `...\cad_rms_data_quality\.claude\skills\check-paths\SKILL.md` | [how_to/check-paths__cad_rms.md](how_to/check-paths__cad_rms.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Lint project configs and scripts against HPD-specific path rules (project variant; not the global `/check-paths`) |
| validate-monthly | `...\cad_rms_data_quality\.claude\skills\validate-monthly\SKILL.md` | [how_to/validate-monthly.md](how_to/validate-monthly.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Quality-score a monthly CAD or RMS Excel export (0–100) before publishing |
| consolidation-run | `...\cad_rms_data_quality\.claude\skills\consolidation-run\SKILL.md` | [how_to/consolidation-run.md](how_to/consolidation-run.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Build the 2019–2026 master CAD dataset (~750K records) with validation |
| cad-export-fix | `...\cad_rms_data_quality\.claude\skills\cad-export-fix\SKILL.md` | [how_to/cad-export-fix.md](how_to/cad-export-fix.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Rename FileMaker CAD export columns to match the ArcGIS pipeline schema |
| esri-backfill | `...\cad_rms_data_quality\.claude\skills\esri-backfill\SKILL.md` | [how_to/esri-backfill.md](how_to/esri-backfill.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Push a fixed monthly CAD file into the public ArcGIS dashboard (RDP-paste) |
| esri-gap-check | `...\cad_rms_data_quality\.claude\skills\esri-gap-check\SKILL.md` | [how_to/esri-gap-check.md](how_to/esri-gap-check.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Find missing or low-volume days on the live dashboard via ArcPy |
| esri-pipeline-status | `...\cad_rms_data_quality\.claude\skills\esri-pipeline-status\SKILL.md` | [how_to/esri-pipeline-status.md](how_to/esri-pipeline-status.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Morning health check on the two nightly ArcGIS publish tasks |
| pipeline-status | `...\cad_rms_data_quality\.claude\skills\pipeline-status\SKILL.md` | [how_to/pipeline-status.md](how_to/pipeline-status.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Broader morning check covering all 4 nightly pipeline tasks |
| deploy-script | `...\cad_rms_data_quality\.claude\skills\deploy-script\SKILL.md` | [how_to/deploy-script.md](how_to/deploy-script.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Generate PowerShell to deploy a Python script to the RDP server |
| handoff | `...\cad_rms_data_quality\.claude\skills\handoff\SKILL.md` | [how_to/handoff__cad_rms.md](how_to/handoff__cad_rms.md) | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Write a structured AI handoff document for the next work session |

---

## PROJECT: personnel_and_summons_etl

**Personnel root:** `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Personnel`  
**Summons root:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Summons`

| Skill | SKILL.md path | Per-skill how-to | Aggregated guide | One-line description |
|-------|---------------|------------------|------------------|----------------------|
| sync-assignment-master | `...\Personnel\.claude\skills\sync-assignment-master\SKILL.md` | [how_to/sync-assignment-master.md](how_to/sync-assignment-master.md) | [personnel_and_summons_etl_skills.md](personnel_and_summons_etl_skills.md) | Sync Assignment_Master_GOLD.xlsx → CSV + schema with INACTIVE_REASON validation |
| apply-dfr-assignment-windows | `...\Summons\.claude\skills\apply-dfr-assignment-windows\SKILL.md` | [how_to/apply-dfr-assignment-windows.md](how_to/apply-dfr-assignment-windows.md) | [personnel_and_summons_etl_skills.md](personnel_and_summons_etl_skills.md) | Apply date-bounded DFR overrides to enriched summons rows |
| verify-summons-against-raw | `...\Summons\.claude\skills\verify-summons-against-raw\SKILL.md` | [how_to/verify-summons-against-raw.md](how_to/verify-summons-against-raw.md) | [personnel_and_summons_etl_skills.md](personnel_and_summons_etl_skills.md) | Reconcile staged Summons output against raw e-ticket export for a report month |

---

## PROJECT: SCRPA (project-local, not hardened via ai_enhancement hub)

**Repo root:** `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA`

SCRPA skills are flat `.md` files (legacy format) scoped to the SCRPA reporting pipeline. They are **not** global and are **not** mirrored in `~/.claude/skills/`. Listed here for discoverability only.

| Skill | SKILL path | Per-skill how-to | Aggregated guide | One-line description |
|-------|------------|------------------|------------------|----------------------|
| check_html_template_sync | `...\16_Reports\SCRPA\.claude\skills\check_html_template_sync.md` | _n/a (project-local)_ | _n/a_ | Verify SCRPA HTML template output matches the canonical style block (SCRPA only) |

Other SCRPA-local skills exist under the same folder (`check_cycle_calendar`, `check_lag_logic`, `generate_cycle_report`, etc.) — open that directory for the full set.

---

### Notes

- **`...`** in project tables means the repo root shown in each section header.
- **Name collisions** (e.g. `check-paths` global vs `cad_rms`): different `SKILL.md` paths; per-skill how-to files use a suffix where needed (`check-paths__cad_rms.md`).
- **Per-skill how-to** links point to files that Phase 7 will create on the next 9/9 hardening sync; until then, open the **Aggregated guide** for full detail.
