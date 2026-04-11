# Claude Code Skills - Complete How-To Guide

All skills available in R. Carucci's Claude Code environment, organized by scope and purpose.

---

## Quick Reference

### Global Skills (available in every session)

| Skill | Invoke With | Purpose |
|-------|-------------|---------|
| **qa-skill-hardening** | `/qa-skill-hardening [target]` | Automated QA testing of skills/scripts |
| **frontend-slides** | `/frontend-slides` | HTML presentations from scratch or PPT |
| **chunk-chat** | `/chunk-chat [file]` | Chunk conversations for RAG ingestion |
| **validate-data** | `/validate-data` | Data quality checks on Excel/CSV files |
| **html-report** | `/html-report` | HPD-branded self-contained HTML reports |
| **check-paths** | `/check-paths` | Scan for path hygiene issues in scripts |
| **new-etl** | `/new-etl Project_Name` | Scaffold a new ETL pipeline |
| **frontend-design** | `/frontend-design` | Distinctive production-grade UI |
| **claude-api** | `/claude-api` | Build/debug Claude API apps |
| **simplify** | `/simplify` | Review changed code for quality |

### Project Skills (cad_rms_data_quality only)

| Skill | Invoke With | Purpose |
|-------|-------------|---------|
| **check-paths** | `/check-paths` | Path convention lint (6 rules, project-specific) |
| **consolidation-run** | `/consolidation-run [--dry-run]` | Execute CAD consolidation pipeline |
| **deploy-script** | `/deploy-script <script> [--schedule HH:MM]` | Deploy scripts to HPD2022LAWSOFT RDP |
| **handoff** | `/handoff [title]` | Generate AI handoff doc for next session |
| **pipeline-status** | `/pipeline-status [call-data\|crime-data\|all]` | Check nightly ESRI pipeline health |
| **validate-monthly** | `/validate-monthly <cad\|rms> [YYYY-MM]` | Validate monthly export before publishing |

---

## Global Skills

### 1. /qa-skill-hardening

**Location:** `~/.claude/skills/qa-skill-hardening/SKILL.md`
**Also at:** `ai_enhancement/.claude/skills/qa-skill-hardening/SKILL.md` (hardened copy)
**Type:** Multi-agent orchestrator (write-capable)

#### What It Does

Launches a multi-agent QA swarm that auto-discovers every skill and script in the current project, runs a 9-step binary test suite against each one, fixes failures, and generates a full hardening report. It is the project's self-referential quality gate.

#### How to Use

```
# Test all skills in the current project
/qa-skill-hardening

# Test a specific skill or directory
/qa-skill-hardening qa-skill-hardening
/qa-skill-hardening ./scripts/
```

#### The 9-Step Binary Test Framework

Every skill is scored PASS (1) or FAIL (0) on each test. No partial credit.

| # | Test | What It Checks |
|---|------|----------------|
| 1 | Exists and Loadable | File exists, valid YAML frontmatter, no syntax errors |
| 2 | Shared Context Access | All referenced files (CLAUDE.md, configs, schemas) are reachable |
| 3 | Path Safety | No hardcoded user paths, no `~/` assumptions |
| 4 | Data Dictionary Compliance | Correct field/column names per project schema |
| 5 | Idempotency | Safe to re-run; no duplicate side effects |
| 6 | Error Handling | Graceful failure with clear messages on bad input |
| 7 | Output Correctness | Produces expected file types and formats |
| 8 | CLAUDE.md Rule Compliance | Follows all project rules (naming, forbidden patterns) |
| 9 | Integration Safety | No conflicts with other skills or shared write targets |

#### Execution Phases

| Phase | What Happens |
|-------|--------------|
| 0 | Auto-discovers project structure, skills, configs |
| 1 | Designs test cases for every discovered skill |
| 2 | Tests read-only skills in parallel (Wave A) |
| 3 | Tests write-capable skills sequentially in isolation (Wave B) |
| 4 | Full regression re-test of everything |
| 5 | Generates scorecards and final report |
| 6 | Commits fixes locally (never pushes) |

#### Output Files

All generated under `docs/skill_memory/`:

- `<Skill_Name>_MEMORY.md` - per-skill scorecard and evidence
- `SKILL_HARDENING_MASTER.md` - global status tracker
- `REGRESSION_TESTS.md` - regression test registry
- `GIT_COMMIT_LOG.md` - commit history during hardening
- `FINAL_SKILL_HARDENING_REPORT.md` - summary with all scores

#### Safety Guards

- **Self-referential guard:** Can test itself but will never invoke itself recursively. Uses static analysis instead.
- **Empty discovery guard:** If no skills found, generates a minimal report and exits cleanly.
- **Never pushes to remote** - only commits locally.

---

### 2. /frontend-slides

**Location:** `~/.claude/skills/frontend-slides/SKILL.md`
**Type:** Read + Write (generates HTML files)

#### What It Does

Creates zero-dependency, animation-rich HTML presentations that run entirely in the browser. Can also convert PowerPoint (.pptx) files to styled HTML.

#### How to Use

```
# Create a new presentation
/frontend-slides

# Convert an existing PowerPoint
/frontend-slides   (then provide the .pptx path when prompted)
```

#### Workflow

1. **Content Discovery** - Claude asks about purpose, length, content readiness, and whether you want inline editing
2. **Style Discovery** - Choose from 12 curated presets or let Claude generate 3 visual previews based on mood
3. **Generation** - Produces a single self-contained HTML file with inline CSS/JS
4. **Delivery** - Opens in browser, provides navigation instructions
5. **Share/Export (optional)** - Deploy to Vercel for a live URL, or export to PDF

#### Key Rules

- Every slide fits exactly in 100vh - no scrolling, ever
- Content that overflows is split into multiple slides automatically
- All font sizes use `clamp()` for responsive scaling
- Zero external dependencies - the HTML file is self-contained

#### Style Presets Available

12 curated visual presets including: Bold Signal, Electric Studio, Dark Botanical, Creative Voltage, Neon Cyber, Split Pastel, Notebook Tabs, Paper and Ink, Swiss Modern, Vintage Editorial, Pastel Geometry, and more.

#### PPT Conversion

Requires `python-pptx` (`pip install python-pptx`). Extracts content, preserves slide order and speaker notes, then applies a chosen style preset.

---

### 3. /chunk-chat

**Location:** `~/.claude/skills/chunk-chat/SKILL.md`
**Type:** Read + Write (generates chunk files)

#### What It Does

Chunks the current conversation (or a provided file) into semantically meaningful text chunks for RAG ingestion. Replicates the chunker_web pipeline without manual export, file staging, or output copying.

#### How to Use

```
# Chunk the current conversation
/chunk-chat

# Chunk with a label
/chunk-chat incident-analysis-session

# Chunk a specific file
/chunk-chat ./logs/session.txt

# Custom chunk size
/chunk-chat --chunk-size=1200 --overlap=100
```

#### Output Structure

```
C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output\{timestamp}_{name}/
  chunk_00000.txt ... chunk_NNNNN.txt   # individual semantic chunks
  {timestamp}_{name}_transcript.md      # full readable transcript
  {timestamp}_{name}_sidecar.json       # metadata, tags, key terms
  {timestamp}_{name}.origin.json        # provenance / source hash
```

#### Naming Convention: {Topic}_{AI_Name}.md
The skill enforces a specific naming convention for the exported transcript files:
`Topic_Description_Claude.md` (or ChatGPT, Gemini, etc). This allows for consistent filtering and sorting in the knowledge base.

#### Defaults

- Chunk size: ~800 characters with 50-character overlap
- Splitting: sentence-boundary based
- Metadata enrichment: rule-based (no external API calls)
- Output location: `KB_Shared\04_output` on OneDrive (default)
- **ChromaDB**: Chunks are NOT automatically ingested. Run `backfill_knowledge_base.py` after processing.

---

### 4. /validate-data

**Location:** `~/.claude/commands/validate-data.md`
**Type:** Read-only (analysis)

#### What It Does

Runs standard data quality checks against an Excel or CSV file, with rules tuned to HPD's data domain (CAD, RMS, NIBRS).

#### How to Use

```
/validate-data
```

Then provide the file path when prompted.

#### Checks Performed

| Check | Details |
|-------|---------|
| **Basic stats** | Row count, column count, date range |
| **Completeness** | `notna()` percentage per column; flags critical fields below 99% |
| **Domain compliance** | Validates `How Reported` values against the canonical list (9-1-1, Phone, Walk-In, Self-Initiated, etc.) |
| **Duplicates** | Counts duplicate `ReportNumberNew` values; shows top 10 |
| **Format** | Verifies `ReportNumberNew` matches `YY-NNNNNN` pattern |

#### Critical Fields Monitored

`ReportNumberNew`, `Incident`, `Time of Call`, `FullAddress2`, `PDZone`, `How Reported`, `Disposition`

#### Important

`ReportNumberNew` is always loaded as string dtype to preserve the `YY-NNNNNN` format (Excel strips leading zeros).

---

### 5. /html-report

**Location:** `~/.claude/commands/html-report.md` and `~/.claude/skills/html-report.md`
**Type:** Write (generates HTML file)

#### What It Does

Generates a self-contained, HPD-branded HTML report suitable for monthly reports, Clery reports, analysis summaries, or ad-hoc styled documents.

#### How to Use

```
/html-report
```

Claude will ask for: report title, date, status (Draft / For Review / Final), and body content or data.

#### Design Rules

- **Self-contained**: No external CSS, JS, or fonts unless explicitly requested
- **HPD palette**: Navy `#1a2744`, Gold `#c8a84b`, success `#2e7d32`, error `#b71c1c`
- **Required elements**: Author block, status badge, FOUO/sensitivity language, `@media print` rules
- **No em-dashes or en-dashes** anywhere - use plain hyphens only
- **Style source**: `08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md`

#### Output

Single `.html` file with inline `<style>`. Default output location is the current project or `14_Workspace/`.

---

### 6. /check-paths (global)

**Location:** `~/.claude/commands/check-paths.md`
**Type:** Read-only (analysis)

#### What It Does

Scans all source files in the current project for common path hygiene issues specific to the HPD workspace.

#### How to Use

```
/check-paths
```

Runs automatically against the current working directory.

#### Issues Detected

| Issue | What It Flags |
|-------|---------------|
| **RobertCarucci** | Non-comment lines using `RobertCarucci` instead of `carucci_r` |
| **Deprecated dictionary refs** | Paths pointing at removed `unified_data_dictionary` locations |
| **Hardcoded absolute paths** | `C:\Users\...` or `D:\` paths that bypass `path_config` |
| **PowerBI_Date typo** | References to `PowerBI_Date` (should be `PowerBI_Data`) |
| **Stale artifacts** | References to retired paths like `PD_BCI_01` outside archive/docs |

#### File Types Scanned

`.py`, `.yaml`, `.yml`, `.json`, `.bat`, `.ps1`, `.cmd`

---

### 7. /new-etl

**Location:** `~/.claude/commands/new-etl.md`
**Type:** Write (scaffolds files)

#### What It Does

Scaffolds a new ETL pipeline project with the correct directory structure, imports, and configuration stubs.

#### How to Use

```
/new-etl Traffic_Stops
```

#### What Gets Created

```
02_ETL_Scripts/Traffic_Stops/
  traffic_stops_etl.py    # Main script with pathlib, pandas, path_config
  config.yaml             # Input/output paths, sheet_name, delimiters
  README.md               # Purpose, inputs, outputs, how to run
  .gitignore              # __pycache__/, *.pyc, data/, output/
```

#### Built-In Rules

- Uses `get_onedrive_root()` from shared `path_config` for path resolution
- Forces `dtype={'ReportNumberNew': str}` when applicable
- Never uses `RobertCarucci` - always `carucci_r` or `path_config`

---

### 8. /frontend-design

**Location:** Plugin (`claude-plugins-official/frontend-design`)
**Type:** Write (generates UI code)

#### What It Does

Creates distinctive, production-grade frontend interfaces - web components, pages, or applications with exceptional visual design that avoids generic "AI slop" aesthetics.

#### How to Use

```
/frontend-design
```

Then describe what you want built.

#### Design Approach

Before writing code, Claude commits to a bold aesthetic direction:
- Chooses an extreme tone (brutally minimal, maximalist, retro-futuristic, art deco, etc.)
- Picks distinctive fonts (never Inter, Roboto, or Arial)
- Creates cohesive color palettes with dominant colors and sharp accents
- Adds purposeful motion, texture, and spatial composition

#### Output

Working code in HTML/CSS/JS, React, Vue, or whatever framework fits the project. Every output should feel custom-crafted with a clear aesthetic point-of-view.

---

### 9. /claude-api

**Type:** Built-in skill

#### What It Does

Helps build, debug, and optimize applications that use the Claude API or Anthropic SDK. Includes prompt caching best practices.

#### When It Activates

- Code imports `anthropic` or `@anthropic-ai/sdk`
- You ask about the Claude API, Anthropic SDKs, or Managed Agents
- Invoked directly with `/claude-api`

---

### 10. /simplify

**Type:** Built-in skill

#### What It Does

Reviews changed code for reuse opportunities, quality issues, and efficiency problems, then fixes any issues found.

#### How to Use

```
/simplify
```

Best used after making changes to code, before committing.

---

### Built-In Utility Skills

These are part of Claude Code itself and don't have separate SKILL.md files:

| Skill | Purpose |
|-------|---------|
| `/update-config` | Configure Claude Code settings.json (hooks, permissions) |
| `/keybindings-help` | Customize keyboard shortcuts in `~/.claude/keybindings.json` |
| `/loop` | Run a skill or prompt on a recurring interval |
| `/schedule` | Create cron-scheduled remote agents |

---

## Project Skills: cad_rms_data_quality

These 6 skills are only available when working inside the `02_ETL_Scripts/cad_rms_data_quality/` project. They live at `.claude/skills/` within that repo.

### 11. /check-paths (project)

**Location:** `cad_rms_data_quality/.claude/skills/check-paths/SKILL.md`
**Type:** Read-only (lint)
**Tools:** `Bash(git *)`, `Read`, `Grep`, `Glob`

#### What It Does

Project-specific version of the global `/check-paths`. Lints all config and Python files for 6 path convention rules specific to the cad_rms_data_quality repo.

#### How to Use

```
/check-paths
```

When invoked from within the cad_rms_data_quality project, the project-level skill takes precedence over the global one.

#### Rules Enforced

| # | Rule | What It Catches |
|---|------|-----------------|
| 1 | No `RobertCarucci` | Scripts/configs must use `carucci_r` (junction exists but code references the canonical name) |
| 2 | `PowerBI_Data` canonical | Flags misspellings like `PowerBi_Data`, `powerbi_data` |
| 3 | OneDrive full suffix | Paths must use `OneDrive - City of Hackensack`, not bare `OneDrive` |
| 4 | `${standards_root}` in schemas | `config/schemas.yaml` must use the variable, not hardcoded Standards paths |
| 5 | Config path consistency | All paths in `consolidation_sources.yaml` / `rms_sources.yaml` are consistent |
| 6 | No hardcoded normalization dicts | Since v1.7.0, mappings load from `Standards/CAD_RMS/mappings/*.json` - no inline dicts |

#### Output Format

Results table with PASS/FAIL per rule, followed by violations with file:line details. Offers auto-fix for most rules except Rule 1 (junction status must be verified manually first).

---

### 12. /consolidation-run

**Location:** `cad_rms_data_quality/.claude/skills/consolidation-run/SKILL.md`
**Type:** Write-capable (runs Python pipeline)
**Tools:** `Bash(python *)`, `Bash(pip *)`, `Read`, `Grep`, `Glob`

#### What It Does

Executes `consolidate_cad_2019_2026.py --full` - the main CAD data consolidation pipeline. Merges yearly and monthly CAD export files into a single consolidated dataset, validates record counts, and reports quality metrics.

#### How to Use

```
# Preview without running
/consolidation-run --dry-run

# Full consolidation
/consolidation-run
```

#### Pre-Flight Checks (run automatically)

1. Reads `config/consolidation_sources.yaml` to verify sources and expected counts
2. Confirms mode is `full` (incremental is deprecated - causes data loss)
3. Verifies output directories exist
4. Checks Python dependencies (pandas, yaml, openpyxl, numpy)

#### Post-Run Validation

| Metric | Threshold |
|--------|-----------|
| Total records | 700,000 - 800,000 |
| Quality score | >= 95 |
| Duplicate rate | <= 1% |

Also checks for record count drops vs. previous run, missing months, and duplicate spikes from overlapping date ranges.

#### Important

- **Always use `--full`**. Incremental mode is deprecated.
- The script reads Excel files from `05_EXPORTS\_CAD\` - must run on the Windows machine or RDP server.
- Uses parallel loading (8 workers) and chunked reading for files >50MB.

---

### 13. /deploy-script

**Location:** `cad_rms_data_quality/.claude/skills/deploy-script/SKILL.md`
**Type:** Read-only (generates commands, does not execute on server)
**Tools:** `Read`, `Grep`, `Glob`

#### What It Does

Reads a local Python script, determines its dependencies and purpose, then generates the exact PowerShell commands to deploy it to the HPD2022LAWSOFT RDP server. Optionally generates Task Scheduler entries.

#### How to Use

```
# Deploy a script (generates copy commands)
/deploy-script scripts/monitor_dashboard_health.py

# Deploy with a scheduled task at 1:30 AM
/deploy-script scripts/monitor_dashboard_health.py --schedule 01:30
```

#### What It Generates

1. **Copy commands** - `Copy-Item` from OneDrive to the correct server directory
2. **Verification** - `Test-Path` and file info checks
3. **Test run** - Full command with the correct Python interpreter and log capture
4. **Scheduled task** (if `--schedule` provided) - `Register-ScheduledTask` with trigger, credentials, and verification

#### Server Directory Logic

| Script Type | Target Directory |
|-------------|-----------------|
| ArcGIS/ESRI scripts | `C:\HPD ESRI\04_Scripts\` |
| Pipeline automation | `C:\ESRIExport\Scripts\` |
| Utilities/monitoring | `C:\HPD ESRI\04_Scripts\` |

#### Python Interpreter Selection

| Script Uses | Interpreter |
|-------------|-------------|
| `arcpy` | `C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe` |
| `pandas` only | Same ArcGIS Python (has pandas) |
| Standard lib | System `python.exe` |

#### Critical Notes

- Always use `python.exe`, never `pythonw.exe` (hides errors - caused a prior pipeline failure)
- Run as `HPD\administrator` with RunLevel Highest (SYSTEM can't access ArcGIS licenses)
- Do not modify `task.py` files auto-generated by ArcGIS Pro

---

### 14. /handoff

**Location:** `cad_rms_data_quality/.claude/skills/handoff/SKILL.md`
**Type:** Write (generates markdown)
**Tools:** `Bash(git log *)`, `Read`, `Grep`, `Glob`

#### What It Does

Generates a structured AI handoff document for the next work session. Creates a self-contained briefing that another Claude Code instance or Cursor session can consume cold to continue the work.

#### How to Use

```
# Generate a handoff (Claude asks for details)
/handoff

# With a title
/handoff esri-pipeline-fix
```

#### Output

Creates `docs/ai_handoff/HANDOFF_YYYYMMDD_<title>.md` with:

- **Opening prompts** for both Cursor and Claude Code (copy-paste ready)
- **Background** - what was done, key decisions
- **Implementation plan** - exact commands and steps
- **Architecture reference** - paths, URLs, service details
- **If It Fails** section (mandatory) - 2-3 failure modes with diagnosis steps
- **Next steps** - verification and follow-up

#### What Makes a Good Handoff

- Opening prompts are self-contained - the next AI has zero context
- Includes exact PowerShell/Python commands, not vague instructions
- Server paths use Windows backslashes
- Expected output is shown for verification commands

---

### 15. /pipeline-status

**Location:** `cad_rms_data_quality/.claude/skills/pipeline-status/SKILL.md`
**Type:** Read-only (generates PowerShell commands)
**Tools:** `Read`, `Grep`

#### What It Does

Generates PowerShell commands to check the health of the 4 nightly ESRI pipelines on HPD2022LAWSOFT. Used for morning-after verification.

#### How to Use

```
# Check all pipelines
/pipeline-status

# Check specific pipeline
/pipeline-status call-data
/pipeline-status crime-data
```

#### Pipelines Monitored

| Pipeline | Task Name | Runs At |
|----------|-----------|---------|
| Call Data | `Publish Call Data_2026_NEW` | 1:00 AM |
| Crime Data | `Publish Crime Data_2026` | 1:30 AM |
| CAD Export | `LawSoftESRICADExport` | 12:30 AM |
| NIBRS Export | `LawSoftESRINIBRSExport` | 1:00 AM |

#### Generated Commands Check

1. `Get-ScheduledTaskInfo` for all 4 tasks (LastResult, LastRun, NextRun)
2. Input file freshness (ESRI_CADExport.xlsx, ESRI_NIBRSExport.xlsx)
3. ArcGIS XML logs (Call Data)
4. Crime Data text logs

#### Interpreting Results

| LastTaskResult | Meaning |
|----------------|---------|
| `0` | Success |
| `1` | Python script error - read log for traceback |
| `2147942401` | Access denied - wrong user |
| `2147943645` | Service unavailable - check AGOL/VPN |
| `2147946720` | Timeout - check for GDB locks |

#### Common Failure Modes

1. Password expired for `HPD\administrator`
2. AGOL token expired - sign in to ArcGIS Pro interactively
3. GDB locked - check for `.wr.lock` files
4. Input file 0 bytes - FileMaker export failed
5. Input file stale (>26 hours) - FileMaker Server may be down

---

### 16. /validate-monthly

**Location:** `cad_rms_data_quality/.claude/skills/validate-monthly/SKILL.md`
**Type:** Write-capable (runs validation pipeline)
**Tools:** `Bash(python *)`, `Bash(pip *)`, `Read`, `Grep`, `Glob`

#### What It Does

Runs the full validation suite against a monthly CAD or RMS export file. Parses quality scores, checks field completeness, runs domain validators, and produces a publish/no-publish recommendation.

#### How to Use

```
# Validate March 2026 CAD export
/validate-monthly cad 2026-03

# Validate most recent RMS export
/validate-monthly rms

# Thorough check with drift detection
/validate-monthly cad 2026-03   (then ask for drift detection)
```

#### Input File Paths

- **CAD:** `05_EXPORTS\_CAD\monthly\{YYYY}\{YYYY}_{MM}_CAD.xlsx`
- **RMS:** `05_EXPORTS\_RMS\monthly\{YYYY}\{YYYY}_{MM}_RMS.xlsx`

#### Quality Thresholds

| Metric | Pass | Warning | Fail |
|--------|------|---------|------|
| Quality score | >= 95 | 80-94 | < 80 |
| Duplicate rate | <= 1% | - | > 1% |
| NULL required fields | <= 5% | - | > 5% |
| Record count (CAD) | 2,000-5,000/month | - | Outside range |

#### Validators

| Validator | Checks |
|-----------|--------|
| `CaseNumberValidator` | Pattern `^\d{2}-\d{6}([A-Z])?$`, uniqueness |
| `HowReportedValidator` | Domain values, normalization |
| `DispositionValidator` | Required, concatenated value splitting |
| `IncidentValidator` | Non-null, matches known call types |
| `DateTimeValidator` | Parseable dates, chronological order |
| `DurationValidator` | Response time calculations, exclusion rules |
| `GeographyValidator` | Lat/lon populated, within Hackensack bounds |
| `OfficerValidator` | Personnel field validation |
| `DerivedFieldValidator` | Computed fields match source data |

#### Output

- `monthly_validation/reports/<run_dir>/metrics.json`
- `monthly_validation/reports/<run_dir>/validation_summary.html`
- `monthly_validation/reports/<run_dir>/action_items.xlsx`

Final recommendation: **PUBLISH** / **REVIEW BEFORE PUBLISHING** / **DO NOT PUBLISH**

---

## Skill Locations Summary

| Location | Scope | Contents |
|----------|-------|----------|
| `~/.claude/skills/` | Global (all projects) | frontend-slides, chunk-chat, qa-skill-hardening, html-report |
| `~/.claude/commands/` | Global (all projects) | validate-data, html-report, check-paths, new-etl |
| `~/.claude/plugins/` | Global (marketplace) | frontend-design |
| `ai_enhancement/.claude/skills/` | ai_enhancement only | qa-skill-hardening (hardened copy) |
| `cad_rms_data_quality/.claude/skills/` | cad_rms_data_quality only | check-paths, consolidation-run, deploy-script, handoff, pipeline-status, validate-monthly |

**Skills** (`SKILL.md` with YAML frontmatter) support `allowed-tools`, `effort`, `argument-hint`, and `disable-model-invocation`.

**Commands** (`~/.claude/commands/*.md`) are simpler markdown files without frontmatter.

---

## Tips

- **Run `/qa-skill-hardening` against any project** to validate all its skills and scripts before deploying
- **Use `/check-paths` regularly** after editing ETL scripts to catch path hygiene regressions
- **Force `ReportNumberNew` to string** on every Excel load - this is enforced by `/validate-data` and should be in every ETL script
- **HTML reports must be self-contained** - no external dependencies unless explicitly requested
- **Skill names use lowercase-with-hyphens**, skill files are always `SKILL.md` (uppercase)
- **`/consolidation-run --dry-run` first** before running a full consolidation to catch config issues
- **`/pipeline-status` is for generating commands** - paste them into the RDP session, then paste results back for diagnosis
- **`/handoff` before ending any session** to preserve context for the next AI
