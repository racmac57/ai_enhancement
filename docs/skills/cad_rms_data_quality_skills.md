# HPD Data Pipeline — Skills Reference Guide

Skills are shortcuts that live inside Claude Code. Instead of remembering a long
PowerShell command or a complicated Python recipe, you type a short slash-command
(like `/check-paths` or `/esri-backfill`) and Claude does the heavy lifting for you.
Each skill is focused on one specific job — validating a file, publishing to the
dashboard, generating a handoff document — and takes only the information it needs.
Use these when you want to do a routine task the same way every time without
retyping the details, and when you want an audit trail of what was done.

---

## Quick Reference Table

| # | Skill | Say This | When To Use It | Requires RDP? |
|---|-------|----------|----------------|---------------|
| 1 | check-paths | `/check-paths` | Before a commit or release, to catch broken Windows paths in scripts/configs | No |
| 2 | validate-monthly | `/validate-monthly cad 2026-03` | When a new monthly CAD or RMS export arrives and you need a quality score before publishing | No |
| 3 | consolidation-run | `/consolidation-run` | After monthly exports pass validation, to rebuild the 2019–2026 master dataset | No |
| 4 | cad-export-fix | `/cad-export-fix <file.xlsx>` | When FileMaker gave you a manual CAD export and the column names don't match the dashboard pipeline | No |
| 5 | esri-backfill | `/esri-backfill <file.xlsx>` | When you need to push a fixed monthly CAD file into the public ArcGIS dashboard | Yes |
| 6 | esri-gap-check | `/esri-gap-check 60` | After a backfill, or whenever you suspect missing days on the dashboard | Yes (ArcGIS Pro) |
| 7 | esri-pipeline-status | `/esri-pipeline-status` | Morning-after check: did last night's dashboard publish work? | Yes |
| 8 | pipeline-status | `/pipeline-status all` | Broader morning check of all 4 nightly tasks (CAD export, NIBRS export, Call publish, Crime publish) | Yes |
| 9 | deploy-script | `/deploy-script scripts/my_script.py --schedule 02:00` | When you've written a new Python script and need to install it on the server | Yes |
| 10 | handoff | `/handoff Call-Data-Gap-Fix` | End of a work session when the next person (or AI) needs to pick up | No |

---

## Data Quality & Consolidation Skills

### 1. /check-paths — Spell-checker for Windows Paths in Code

**Location:** `.claude/skills/check-paths/SKILL.md`
**Type:** Read-only (lints Python, YAML, PowerShell)
**Tools:** Read, Grep, Glob

#### What It Does

Scans every Python file, YAML config, and PowerShell script in the project looking
for broken or inconsistent file paths — things like the wrong Windows username, a
misspelled OneDrive folder name, or an outdated reference to a moved file. Reports
a PASS/FAIL table so you know the code will actually find its data when it runs.

#### When to Use It

- Right before you commit changes to `scripts.json`, a YAML config, or any Python
  file that opens files on disk.
- After renaming or moving a folder in OneDrive.
- Before handing code off to another PC or to the RDP server.

#### How to Use

```
/check-paths
```

#### Output

A 6-rule PASS/FAIL table printed into the chat with the specific file and line of
any violation. If violations are found, Claude offers to auto-fix them — except
`RobertCarucci` references, which require human review first.

#### Gotchas

1. Read-only by default — never changes a file unless you explicitly approve.
2. `RobertCarucci` findings are never auto-fixed because they can signal a real
   junction problem.

---

### 2. /validate-monthly — Quality Score a Monthly Export

**Location:** `.claude/skills/validate-monthly/SKILL.md`
**Type:** Write-capable (writes reports)
**Tools:** Bash(python *), Read, Grep, Glob

#### What It Does

Takes a brand-new monthly CAD or RMS Excel export and runs it through roughly a
dozen quality checks — case-number format, null rates on required fields, whether
addresses are within Hackensack, duplicate rows, datetime consistency, and more.
Ends with a single 0–100 quality score and a list of specific problems so you know
whether the file is safe to publish.

#### When to Use It

- The 1st of every month, as soon as the previous month's CAD/RMS export arrives.
- Before running `/consolidation-run` (don't consolidate a broken export).
- When someone says "the dashboard looks weird" and you want to prove whether the
  source data was bad.

#### How to Use

```
/validate-monthly cad 2026-03
/validate-monthly rms 2026-03
/validate-monthly cad
```

(Leave off the month to default to the most recent file.)

#### Output

| Artifact | Where |
|----------|-------|
| Summary in chat | score, record count, duplicate rate, top action items, PUBLISH / REVIEW / DO NOT PUBLISH verdict |
| HTML summary | `monthly_validation/reports/<date>/summary.html` |
| Action items | `monthly_validation/reports/<date>/action_items.xlsx` |
| Metrics JSON | `monthly_validation/reports/<date>/metrics.json` |

#### Gotchas

1. The Excel sources live under `05_EXPORTS\_CAD\monthly\` and `05_EXPORTS\_RMS\monthly\`.
   On a machine without OneDrive, Claude emits the command for you to run on a PC
   that has access.
2. A score below 80 is a hard "do not publish" — investigate the action items.
3. Validates CAD against the canonical schema in `09_Reference/Standards/CAD_RMS/`;
   update the schema first if a new field appears in the export.

---

### 3. /consolidation-run — Build the Master 2019–2026 Dataset

**Location:** `.claude/skills/consolidation-run/SKILL.md`
**Type:** Write-capable (writes CSV + reports)
**Tools:** Bash(python *), Bash(pip *), Read, Grep, Glob

#### What It Does

Loads every yearly CAD file (2019 through 2025) plus each monthly file for 2026,
merges them, deduplicates, applies normalization rules, and produces one big
validated CSV of roughly 750,000 records that the ArcGIS dashboard and Power BI
reports are built on top of. Writes a run report so you can see what changed since
last time.

#### When to Use It

- After a new monthly export passes `/validate-monthly`.
- When a yearly file has been updated (rare — usually only for historical backfills).
- When the Power BI / ArcGIS team reports "my data cuts off at month X."

#### How to Use

```
/consolidation-run
/consolidation-run --dry-run
```

Use `--dry-run` to preview sources, record counts, and disk paths without running
the 2–3 minute job.

#### Output

A status block in the chat (success/fail, total records, quality score, duplicate
rate, runtime, per-year record counts, and the delta vs. the previous run). The
CSV and per-run reports land in `consolidation/output/` and `consolidation/reports/`.

#### Gotchas

1. **Always runs with `--full`.** Incremental mode is deprecated; it caused data loss
   in 2026-Q1.
2. Needs Excel sources from `05_EXPORTS\_CAD\` — must run on the Windows PC or the
   RDP server. Claude will emit the exact command if you're on another machine.
3. Expect 700,000–800,000 records total. Numbers outside that band usually mean a
   source file didn't load — check the sources list in the report.

---

## ESRI Dashboard Pipeline Skills

### 4. /cad-export-fix — Repair a FileMaker CAD Export's Column Names

**Location:** `.claude/skills/cad-export-fix/SKILL.md`
**Type:** Write-capable (writes `_FIXED.xlsx` alongside input)
**Tools:** Read, Bash(python *), Write

#### What It Does

When someone hands you a manual CAD export from FileMaker, the column names are
usually slightly wrong (`HourMinuetsCalc` instead of `Hour_Calc`, underscores
instead of spaces, missing lat/lon columns). This skill fixes all of those
automatically and saves a new copy of the file that the ArcGIS dashboard pipeline
can actually accept.

#### When to Use It

- Anytime someone does a manual re-pull of a CAD month from FileMaker (e.g. for a
  backfill or to patch a bad day).
- Before running `/esri-backfill` — the backfill pipeline expects the fixed
  21-column schema.

#### How to Use

```
/cad-export-fix "C:\Users\carucci_r\OneDrive - City of Hackensack\Desktop\2026_04_CAD.xlsx"
```

#### Output

A new file saved alongside the original with `_FIXED` added to the name (e.g.
`2026_04_CAD_FIXED.xlsx`). Claude prints the before/after column list, the row
count, and any extra columns that were dropped.

#### Gotchas

1. The original file is never overwritten — always use the `_FIXED.xlsx` for the
   next step.
2. `latitude` and `longitude` are added as blank — correct. The ArcGIS model
   geocodes the address later via the NJ State Plane Composite locator.
3. If the file is missing a required column entirely (not just misnamed), the skill
   exits with a clear error — it will not silently invent data.

---

### 5. /esri-backfill — Push a Monthly CAD File into the Public Dashboard

**Location:** `.claude/skills/esri-backfill/SKILL.md`
**Type:** Read-only (emits PowerShell text to paste on RDP)
**Tools:** Read, Grep, Glob

#### What It Does

Generates a complete PowerShell block that, when pasted on the RDP server, will:
back up the live CAD export, stage your monthly file in its place, kick off the
`Publish Call Data_2026_NEW` scheduled task, wait for it to finish, report success
or failure, and then restore the live export so tomorrow's nightly run isn't
disturbed. Also emits a follow-up ArcPy snippet to verify the new records actually
landed on the dashboard.

#### When to Use It

- After `/cad-export-fix` produces a clean `_FIXED.xlsx`, to publish a missing or
  corrected month.
- When backfilling a historical gap (e.g. the 2026-04-07 → 2026-04-13 outage).

#### How to Use

```
/esri-backfill 2026_04_CAD_FIXED.xlsx
/esri-backfill "\\tsclient\C\Users\carucci_r\OneDrive - City of Hackensack\Desktop\2026_04_CAD_FIXED.xlsx" "April 2026"
```

#### Workflow (what the generated PowerShell does on the server)

| Step | Action |
|------|--------|
| 1 | Back up the current live `ESRI_CADExport.xlsx` |
| 2 | Stage the supplied monthly file into the live path |
| 3 | Start scheduled task `Publish Call Data_2026_NEW` |
| 4 | Poll until the task leaves `Running` |
| 5 | Report `LastTaskResult` + read tail of the log |
| 6 | Restore the live FileMaker export |

#### Output

Two copy-and-paste code blocks in the chat:

1. A PowerShell block to paste on the RDP server (runs the backfill end-to-end).
2. An ArcPy block to paste in ArcGIS Pro's Python window to confirm records landed.

#### Gotchas

1. **RDP required.** Runs on `HPD2022LAWSOFT` where the scheduled task, staging
   folders, and live FileMaker export live.
2. If your file is on your desktop, use the `\\tsclient\C\Users\carucci_r\...`
   prefix so the RDP session can see it.
3. Restore runs at the end even if the task fails, to protect the normal nightly
   run.
4. `LastTaskResult = 0` means success. Anything else → open the log under
   `C:\Users\administrator.HPD\AppData\Local\ESRI\ArcGISPro\Geoprocessing\ScheduledTools\Logs\`.

---

### 6. /esri-gap-check — Find Missing Days on the Public Dashboard

**Location:** `.claude/skills/esri-gap-check/SKILL.md`
**Type:** Read-only (emits ArcPy text to paste in ArcGIS Pro)
**Tools:** Read

#### What It Does

Generates an ArcPy script that asks the live ArcGIS Online dashboard "how many
calls did you receive on each day over the last N days?" and prints any days with
zero calls (gaps) or suspiciously low counts (partial publishes). Confirms a
backfill actually worked or catches silent publish failures.

#### When to Use It

- Immediately after `/esri-backfill` (to confirm the month landed).
- When a supervisor asks "did yesterday's calls make it onto the dashboard?"
- Monthly, as a quick health check on the last 60 days.

#### How to Use

```
/esri-gap-check
/esri-gap-check 60
/esri-gap-check --from 2026-02-01 --to 2026-04-13
```

(No argument → 60-day lookback.)

#### Output

An ArcPy code block to paste into the ArcGIS Pro Python window. When run it prints:

| Section | What It Shows |
|---------|---------------|
| Date window | From / to dates used |
| Total records | Count in the window |
| Zero-call days | Days with no records (gaps) |
| Low-volume days | Days with <50 records (partial publishes) |
| Last 7 days | Trailing-week snapshot |

#### Gotchas

1. **Requires ArcGIS Pro**, signed in to the HPD AGOL organization. Paste into
   Pro's Python window, not PowerShell.
2. Hackensack's normal volume is ~190–265 calls per day. Anything under 50 is
   almost always a partial publish, not a quiet day.
3. Read-only — it queries the dashboard and prints numbers. Never changes anything.

---

### 7. /esri-pipeline-status — Morning Health Check on the Two Publish Tasks

**Location:** `.claude/skills/esri-pipeline-status/SKILL.md`
**Type:** Read-only (emits PowerShell text to paste on RDP)
**Tools:** Read

#### What It Does

Generates a short PowerShell block that, when pasted on the RDP server, tells you
in one table: when each of the two nightly dashboard publishes last ran, whether
it succeeded, what log status code it reported, and an approximate record count.
"Did the dashboard actually update last night?"

#### When to Use It

- First thing in the morning, before the Chief asks.
- When a dashboard widget looks stale and you want to know if last night's run
  succeeded.
- After fixing a license or credential issue, to confirm the next run went clean.

#### How to Use

```
/esri-pipeline-status
```

#### Output

A PowerShell block that prints one row per publish task (`Publish Call Data_2026_NEW`,
`Publish Crime Data_2026`) with `LastRunTime`, `LastTaskResult`, `LogStatus`,
record count, and log file name.

**Log status codes:**

| Code | Meaning |
|------|---------|
| 4 | Success |
| 5 | License / sign-in failure (most common) |
| 0 | Unknown / incomplete |

#### Gotchas

1. **RDP required** — reads local logs under `C:\Users\administrator.HPD\AppData\Local\ESRI\...`.
2. `LogStatus = 5` almost always means the scheduled-task account isn't signed in
   to AGOL inside ArcGIS Pro. Sign in once manually and the next nightly run will
   succeed.
3. Record count is best-effort regex scraping. Sanity check, not official total.

---

### 8. /pipeline-status — Broader Morning Check of All 4 Nightly Tasks

**Location:** `.claude/skills/pipeline-status/SKILL.md`
**Type:** Read-only (emits PowerShell text to paste on RDP)
**Tools:** Read, Grep

#### What It Does

Similar in spirit to `/esri-pipeline-status`, but covers the full nightly chain:
the two FileMaker export tasks (CAD at 12:30 AM, NIBRS at 1:00 AM) plus the two
ArcGIS publish tasks (Call Data at 1:00 AM, Crime Data at 1:30 AM). Also checks
that the Excel input files are fresh and reads the ArcGIS XML logs for detailed
status.

#### When to Use It

- When something is visibly wrong and you want the full story (did the FileMaker
  export even write a file? Did the publish task just fail to run?).
- After a server reboot or a password change on `HPD\administrator`.
- As a weekly audit — paste it Monday morning and glance through.

#### How to Use

```
/pipeline-status all
/pipeline-status call-data
/pipeline-status crime-data
```

#### The 4 Nightly Tasks

| Task | When | Role |
|------|------|------|
| `LawSoftESRICADExport` | 12:30 AM | FileMaker → CAD Excel |
| `LawSoftESRINIBRSExport` | 1:00 AM | FileMaker → NIBRS Excel |
| `Publish Call Data_2026_NEW` | 1:00 AM | Excel → AGOL Call layer |
| `Publish Crime Data_2026` | 1:30 AM | Excel → AGOL Crime layer |

#### Output

PowerShell that prints last-run-time and result for each of 4 tasks, file size /
timestamp for both FileMaker export Excel files, and the most recent log files
for each pipeline. Claude will interpret the output when you paste it back.

#### Gotchas

1. **RDP required.**
2. Use `/esri-pipeline-status` if you just want the publish-task summary.
3. If an input file is older than 26 hours or is 0 bytes, the FileMaker export
   failed — fix that before worrying about the publish task.

---

### 9. /deploy-script — Install a New Python Script on the Server

**Location:** `.claude/skills/deploy-script/SKILL.md`
**Type:** Read-only (emits PowerShell text to paste on RDP)
**Tools:** Read, Grep, Glob

#### What It Does

Generates the PowerShell commands you need to copy a new or updated Python script
to the RDP server, test it with the correct Python interpreter, and (optionally)
register it as a scheduled task that runs automatically every night. Handles the
ArcPy vs. standard-Python distinction and the "run as HPD\administrator with
highest privileges" requirement.

#### When to Use It

- After writing a new monitoring/cleanup script that should live on the server.
- When replacing an older version of a script that's already scheduled.
- When adding a new nightly job to the automation chain.

#### How to Use

```
/deploy-script scripts/monitor_dashboard_health.py
/deploy-script scripts/monitor_dashboard_health.py --schedule 02:00
```

(Add `--schedule HH:MM` only if you want a Task Scheduler entry created.)

#### Output

PowerShell commands covering:

| Step | Purpose |
|------|---------|
| Copy | Script → `C:\HPD ESRI\04_Scripts\` |
| Verify | Hash compare + file-exists check |
| Test run | Capture stdout/stderr to a log |
| Register | Task Scheduler entry under `HPD\administrator`, RunLevel Highest (if `--schedule`) |

#### Gotchas

1. **RDP required.** The scheduled task runs on the server, not your desktop.
2. Scripts that use `arcpy` must run under the ArcGIS Python interpreter — Claude
   picks the right one automatically by reading your script's imports.
3. The scheduled task must run as `HPD\administrator` with RunLevel Highest;
   SYSTEM can't access ArcGIS licenses.
4. Never use `pythonw.exe` — it hides errors and has caused at least one silent
   pipeline failure.

---

### 10. /handoff — Write the "Here's What's Next" Document

**Location:** `.claude/skills/handoff/SKILL.md`
**Type:** Write-capable (writes to `docs/ai_handoff/`)
**Tools:** Bash(git log *), Read, Grep, Glob

#### What It Does

Generates a structured markdown document that summarizes what was done in the
current work session, what remains to be done, and exactly how the next person
(or AI session) should pick up. Includes copy-paste opening prompts for both
Cursor and Claude Code so the next session starts with full context.

#### When to Use It

- End of day, before you stop working on a multi-day project.
- Before handing a ticket off to a colleague.
- When you're about to start a fresh AI session and want the new one to know what
  the last one accomplished.

#### How to Use

```
/handoff Call-Data-Gap-Fix
/handoff Year-End-Clery-Prep
```

(The argument becomes part of the filename.)

#### Output

A new markdown file saved under
`docs/ai_handoff/HANDOFF_YYYYMMDD_<your-title>.md` containing:

| Section | Purpose |
|---------|---------|
| Background | What the project is and what's been done |
| Implementation plan | Step-by-step for the next session |
| Architecture reference | Tables the next session will need on-hand |
| If It Fails | Diagnosis tree for 2–3 likely failure modes |
| Opening prompts | Paste-ready blocks for Cursor and Claude Code |

#### Gotchas

1. Filenames are date-stamped. Running `/handoff` twice in the same day with the
   same title overwrites the first (intentional — keep iterating until happy).
2. The opening-prompt sections must be fully self-contained — the next AI starts
   with zero context, so no "as we discussed" references.
3. The "If It Fails" section is required — it forces you to think about likely
   failure modes before walking away.

---

## Skill Locations Summary

| Skill | Path | Type |
|-------|------|------|
| check-paths | `.claude/skills/check-paths/SKILL.md` | Read-only |
| validate-monthly | `.claude/skills/validate-monthly/SKILL.md` | Write-capable |
| consolidation-run | `.claude/skills/consolidation-run/SKILL.md` | Write-capable |
| cad-export-fix | `.claude/skills/cad-export-fix/SKILL.md` | Write-capable |
| esri-backfill | `.claude/skills/esri-backfill/SKILL.md` | Read-only |
| esri-gap-check | `.claude/skills/esri-gap-check/SKILL.md` | Read-only |
| esri-pipeline-status | `.claude/skills/esri-pipeline-status/SKILL.md` | Read-only |
| pipeline-status | `.claude/skills/pipeline-status/SKILL.md` | Read-only |
| deploy-script | `.claude/skills/deploy-script/SKILL.md` | Read-only |
| handoff | `.claude/skills/handoff/SKILL.md` | Write-capable |

---

## Tips

1. **Read-only skills are safe to run anytime.** They either print a report or
   emit a code block for you to paste elsewhere. They never modify project files.
2. **RDP-required skills emit, they don't execute.** Claude generates the
   PowerShell or ArcPy block in the chat; you copy it to the RDP server and run
   it there. That keeps a clean audit trail of what was pasted.
3. **Chain validations before publishing.** The safe order is always
   `/validate-monthly` → `/consolidation-run` → (if dashboard work)
   `/cad-export-fix` → `/esri-backfill` → `/esri-gap-check`.
4. **Use `/handoff` generously.** It costs nothing to write one, and the next AI
   session (or colleague) starts with full context instead of guessing.
5. **When in doubt, start with `/pipeline-status all`.** It's the widest-angle
   diagnostic and will tell you whether the problem is the FileMaker export, the
   publish task, or something downstream.
