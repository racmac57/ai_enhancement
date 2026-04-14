# Claude Skills — Master Index

Claude Code skills come in two scopes: **GLOBAL** skills live under
`C:\Users\carucci_r\.claude\skills\` and are available in every session on this
machine; **PROJECT** skills live under a repo's `.claude\skills\` folder and are
only available when Claude Code is running from that project.

| Type | Skill | Detail File | One-Line Description |
|------|-------|-------------|----------------------|
| GLOBAL | qa-skill-hardening | [global_skills.md](global_skills.md) | Multi-agent QA swarm that auto-discovers, tests, and hardens every skill in a project |
| GLOBAL | frontend-slides | [global_skills.md](global_skills.md) | Build HTML presentations from scratch or from an existing PowerPoint |
| GLOBAL | chunk-chat | [global_skills.md](global_skills.md) | Chunk long conversations into sized pieces for RAG ingestion |
| GLOBAL | validate-data | [global_skills.md](global_skills.md) | Run data-quality checks on Excel or CSV files |
| GLOBAL | html-report | [global_skills.md](global_skills.md) | Generate HPD-branded, self-contained HTML reports |
| GLOBAL | check-paths | [global_skills.md](global_skills.md) | Scan a project for path-hygiene issues in scripts and configs |
| GLOBAL | new-etl | [global_skills.md](global_skills.md) | Scaffold a new ETL pipeline with standard folder layout |
| GLOBAL | frontend-design | [global_skills.md](global_skills.md) | Produce distinctive, production-grade UI designs |
| GLOBAL | claude-api | [global_skills.md](global_skills.md) | Build and debug Claude API applications |
| GLOBAL | simplify | [global_skills.md](global_skills.md) | Review changed code for quality and simplification opportunities |
| PROJECT: cad_rms_data_quality | check-paths | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Lint project configs and scripts against HPD-specific path rules |
| PROJECT: cad_rms_data_quality | validate-monthly | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Quality-score a monthly CAD or RMS Excel export (0–100) before publishing |
| PROJECT: cad_rms_data_quality | consolidation-run | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Build the 2019–2026 master CAD dataset (~750K records) with validation |
| PROJECT: cad_rms_data_quality | cad-export-fix | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Rename FileMaker CAD export columns to match the ArcGIS pipeline schema |
| PROJECT: cad_rms_data_quality | esri-backfill | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Push a fixed monthly CAD file into the public ArcGIS dashboard (RDP-paste) |
| PROJECT: cad_rms_data_quality | esri-gap-check | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Find missing or low-volume days on the live dashboard via ArcPy |
| PROJECT: cad_rms_data_quality | esri-pipeline-status | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Morning health check on the two nightly ArcGIS publish tasks |
| PROJECT: cad_rms_data_quality | pipeline-status | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Broader morning check covering all 4 nightly pipeline tasks |
| PROJECT: cad_rms_data_quality | deploy-script | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Generate PowerShell to deploy a Python script to the RDP server |
| PROJECT: cad_rms_data_quality | handoff | [cad_rms_data_quality_skills.md](cad_rms_data_quality_skills.md) | Write a structured AI handoff document for the next work session |
