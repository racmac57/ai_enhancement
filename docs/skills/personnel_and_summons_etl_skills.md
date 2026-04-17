# Personnel & Summons ETL — Skills Reference Guide

Skills in this guide belong to two tightly-coupled projects:

- **Personnel** (`09_Reference/Personnel/`) — maintains the Gold Standard
  officer roster and publishes `Assignment_Master_V2.csv` that every downstream
  ETL consumes.
- **Summons ETL** (`02_ETL_Scripts/Summons/`) — consumes the Personnel CSV,
  enriches the e-ticket export, and publishes the DFR workbook and Power BI
  staging file.

Both projects were hardened together on 2026-04-14 (Personnel v1.7.0, Summons
v2.3.0) so officers who resigned mid-year no longer surface as "Unknown - XXXX"
on the dashboard and so time-bounded transitional duty (TTD) assignments apply
to the correct date range automatically.

---

## Quick Reference Table

| # | Skill | Say This | When To Use It | Writes? |
|---|-------|----------|----------------|---------|
| 1 | sync-assignment-master | `python scripts/sync_assignment_master.py` (Personnel) | After editing `Assignment_Master_GOLD.xlsx` (hiring, separation, rank/team changes, INACTIVE_REASON updates) | Yes — CSV + schema + Archive backup |
| 2 | apply-dfr-assignment-windows | Runs automatically inside `run_eticket_export.py` | When a date-bounded transitional duty or special assignment has to land on DFR rows | In-memory transform only |
| 3 | verify-summons-against-raw | `python scripts/verify_summons_against_raw.py --report-month YYYY-MM` (Summons) | After a monthly Summons ETL run, before publishing DFR / Power BI | No — read-only reconciliation |

---

## Personnel Skills

### 1. sync-assignment-master — Publish the Officer Roster

**Location:** `09_Reference/Personnel/scripts/sync_assignment_master.py`
**Type:** Write-capable (writes `Assignment_Master_V2.csv`, `Assignment_Master_SCHEMA.md`, timestamped Archive backup)
**Tools:** Bash(python *), Read

#### What It Does

Reads the Gold Standard workbook `Assignment_Master_GOLD.xlsx` (sheet
`Assignment_Master_V2`), validates every row, normalizes badge numbers, and
publishes two artifacts that the rest of the HPD data stack depends on:

- `Assignment_Master_V2.csv` — the flat file every ETL joins against.
- `Assignment_Master_SCHEMA.md` — the generated schema with current columns,
  valid values, and version history.

As of v1.7.0, validation includes three new rules around the `INACTIVE_REASON`
column so separated officers are always tagged with **why** they are inactive
(`RESIGNED`, `RETIRED`, `TERMINATED`, `DECEASED`, or `SUSPENDED`). This is what
lets the Summons ETL resolve historical ticket rows to their actual officer
instead of dropping them into `UNKNOWN - XXXX`.

#### When to Use It

- You hired, promoted, transferred, separated, or changed the team of an
  officer in `Assignment_Master_GOLD.xlsx`.
- You backfilled `INACTIVE_REASON` for legacy separated officers.
- You changed anything in `Assignment_Master_SCHEMA_TEMPLATE.md` (static
  schema content — field definitions, maintenance procedures, etc.).
- You want to cut a clean Archive backup of GOLD before a risky edit.

#### How to Use

From the Personnel root:

```
python scripts/sync_assignment_master.py
```

or on Windows:

```
run_sync.bat
```

#### Output

| Artifact | Where |
|----------|-------|
| Flat CSV | `Assignment_Master_V2.csv` (project root) |
| Generated schema | `Assignment_Master_SCHEMA.md` (project root) |
| GOLD backup | `Archive/Assignment_Master_GOLD_YYYY_MM_DD_HHMMSS.xlsx` |
| Console | Row count, valid-values summary, PASS / validation-errors list |

#### Gotchas

1. **GOLD is the sole source of truth.** Never hand-edit the CSV or the
   generated schema — they are overwritten every run. Edit GOLD (or the
   `SCHEMA_TEMPLATE.md`) instead.
2. **INACTIVE rows must have a reason.** A blank `INACTIVE_REASON` on an
   `INACTIVE` row fails validation. A reason on an `ACTIVE` row also fails.
   Allowed values are the five in `VALID_INACTIVE_REASONS`.
3. **Trailing-space column headers are tolerated.** The script strips column
   names after `read_excel` so `"INACTIVE_REASON "` with a trailing space still
   works — but fix it in GOLD anyway.
4. **Badge normalization is mandatory.** `BADGE_NUMBER` is cleaned of any
   `.0` float suffix and exported as an integer string; `PADDED_BADGE_NUMBER`
   is exactly 4 digits with leading zeros. Do not remove either step.
5. **Path-agnostic.** `BASE_DIR` is derived from the script's own location, so
   the same code runs on the desktop (`carucci_r`) and the laptop
   (`RobertCarucci`) without edits.

---

## Summons ETL Skills

### 2. apply-dfr-assignment-windows — Date-Bounded Assignment Overrides

**Location:** `02_ETL_Scripts/Summons/summons_etl_enhanced.py` — method
`_apply_dfr_assignment_windows` on `SummonsETLProcessor`
**Type:** In-memory transform (pure function, no disk writes)
**Tools:** pandas; depends on `scripts/summons_etl_normalize.py`

#### What It Does

For the small set of officers whose assignment changes mid-month (e.g., an
officer on a brief SSOCC detail, or a Lieutenant moving to Temporary
Transitional Duty after an injury), the baseline `ASSIGNMENT_OVERRIDES` lookup
is not enough — it has no date dimension and would stamp every historical
ticket with the new assignment.

`_apply_dfr_assignment_windows` fixes this by reading the module-level
`DFR_ASSIGNMENTS` list (badge + assignment + `date_start` + `date_end` +
reason), running each window through `normalize_date_windows` so multi-month
ranges split into one row per calendar month, then merging onto the enriched
summons frame on `(PADDED_BADGE_NUMBER, VIOLATION_DATE)`. Rows whose date
falls inside a window get the window's assignment; rows outside the window are
untouched.

Current `DFR_ASSIGNMENTS` entries:

| Badge | Officer | Assignment | Window | Reason |
|-------|---------|------------|--------|--------|
| 2025 | Ramirez | SSOCC | 2026-03-01 → 2026-03-04 | MARCH_WINDOW |
| 0115 | Lt. Dominguez | TTD | 2026-04-06 → open-ended (2099-12-31) | TRANSITIONAL_DUTY |

#### When to Use It

- Rarely invoked directly — it runs automatically inside
  `create_unified_summons_dataset` during every `run_eticket_export.py` run.
- You only touch it when you need to **add** a new date-bounded assignment.
  Add a dict to the `DFR_ASSIGNMENTS` list at the top of
  `summons_etl_enhanced.py` and re-run the ETL. (A planned `/add-ttd-window`
  skill will automate this edit.)

#### How to Use

```python
# Inside summons_etl_enhanced.py, at module top:
DFR_ASSIGNMENTS = [
    {"badge": "2025", "assignment": "SSOCC",
     "date_start": "2026-03-01", "date_end": "2026-03-04",
     "reason": "MARCH_WINDOW"},
    {"badge": "0115", "assignment": "TTD",
     "date_start": "2026-04-06", "date_end": None,
     "reason": "TRANSITIONAL_DUTY"},
]
```

Then:

```
python run_eticket_export.py
```

and the helper fires inside the enrichment step.

#### Output

- A new column `WG2` populated with the window's assignment for every
  matching row.
- A console log of how many ticket rows each window affected
  (e.g., `Applied DFR window for 2025 (SSOCC) -> 73 ticket(s)`).
- Rows whose badge is absent from `DFR_ASSIGNMENTS` or whose date falls
  outside all windows are untouched.

#### Gotchas

1. **Open-ended windows are allowed.** `date_end = None` is interpreted as a
   `FAR_FUTURE` sentinel (`2099-12-31`), which the helper then clips to the
   data's actual max date.
2. **End-of-data edge case.** If a window's `date_start` is *beyond* the
   data's max date (e.g., Dominguez TTD starting 2026-04-06 in a pipeline
   whose data only runs through 2026-04-01), the window is silently dropped
   rather than raising. Fine — those tickets don't exist yet. Will reapply
   next run when new data lands.
3. **Composition with `ASSIGNMENT_OVERRIDES`.** Windows win on date overlap,
   but the baseline `ASSIGNMENT_OVERRIDES` still runs first. The two layers
   compose — if you need FIRE LANES conditional logic for a badge *and* a
   date-bounded override, both apply in order.
4. **Unicode-safe logs.** Log lines use `->` instead of `→` because the
   Windows `cp1252` console cannot encode the arrow character.
5. **One calendar month per split row.** `normalize_date_windows` uses
   `pd.offsets.MonthEnd(0)` so a 3-month range becomes three rows — this
   makes downstream month-based reporting correct without extra joins.

---

### 3. verify-summons-against-raw — Monthly Reconciliation CLI

**Location:** `02_ETL_Scripts/Summons/scripts/verify_summons_against_raw.py`
**Type:** Read-only verification (no writes)
**Tools:** Bash(python *), Read

#### What It Does

After a Summons ETL run you need to know, quickly and honestly, whether the
staged Power BI output actually represents the raw e-ticket export — without
eyeballing 4000+ rows. This CLI loads three datasets for one report month and
reports:

- `summons_powerbi_latest.xlsx` — staged output the ETL just wrote.
- `05_EXPORTS/_Summons/E_Ticket/{YYYY}/month/{YYYY}_{MM}_eticket_export.csv`
  (or its `_FIXED.csv` twin) — the raw export the ETL read.
- `Assignment_Master_V2.csv` — the Personnel roster.

For a given `--report-month`, it counts raw vs staged rows, distinct badges,
remaining `UNKNOWN - XXXX` tags, and badges that were successfully resolved
from the INACTIVE lookup. It samples 10 such resolutions with
`PADDED_BADGE_NUMBER`, `OFFICER_DISPLAY_NAME`, and `INACTIVE_REASON` so you
can spot-check the retention path.

The script exits non-zero if any INACTIVE officer present in the raw file is
still `UNKNOWN` in staging — that's a regression.

#### When to Use It

- Immediately after every `run_eticket_export.py` for the most-recent full
  month.
- Before refreshing the Power BI DFR dashboard.
- Any time the DFR team asks "are these numbers real?" — you can produce a
  receipt in under ten seconds.

#### How to Use

From the Summons root:

```
python scripts/verify_summons_against_raw.py --report-month 2026-03
```

#### Output

Console block with:

- Raw row count vs staged row count (with delta).
- Distinct-badge count raw vs staged.
- Remaining `UNKNOWN` count (target: 0).
- Resolved-from-INACTIVE count, plus a 10-row sample with badge + display
  name + INACTIVE_REASON.
- Exit code `0` on success, non-zero if any INACTIVE officer is still
  unresolved.

Example line from the 2026-03 run: `4148/4160 rows, 64/64 badges, 0 UNKNOWN`.

#### Gotchas

1. **Pure reader — no locking.** Safe to run while the ETL is writing; it
   opens the most recent staging file at invocation time.
2. **`_FIXED.csv` fallback.** `raw_path()` tries the canonical
   `_eticket_export.csv` first, then the `_FIXED.csv` twin. A stale
   `_FIXED.csv` from a prior rehab can silently mask the canonical file —
   make sure your staging flow keeps only one per month.
3. **Report-month format is strict.** Pass `YYYY-MM` (e.g. `2026-03`). Any
   other format raises a clear argparse error.
4. **Does not write anywhere.** Never modifies GOLD, CSV, SCHEMA, or staging
   files — respects Personnel Rule 2 (no manual edits to generated files).

---

## Cross-Skill Workflow

A clean monthly cadence:

1. HR tells you an officer resigned → open
   `Assignment_Master_GOLD.xlsx`, flip `STATUS` to `INACTIVE`, fill
   `INACTIVE_REASON`.
2. `python scripts/sync_assignment_master.py` — republishes the CSV and
   schema, drops a timestamped GOLD backup.
3. If HR also tells you someone is on TTD, add a row to `DFR_ASSIGNMENTS` in
   `summons_etl_enhanced.py`.
4. `python run_eticket_export.py` — the Summons ETL consumes the new CSV,
   resolves historical ticket rows via the INACTIVE lookup, applies any
   date-bounded windows, and writes `summons_powerbi_latest.xlsx` + the DFR
   workbook.
5. `python scripts/verify_summons_against_raw.py --report-month YYYY-MM` —
   you get a one-screen receipt. Exit 0 means publish.

---

## Version & Hardening History

- **Personnel v1.7.0 (2026-04-14)** — Added `INACTIVE_REASON` column, valid-
  values set, three validation rules, schema generator extension, defensive
  trailing-space strip.
- **Summons v2.3.0 (2026-04-14)** — Added historical badge resolution via
  INACTIVE lookup, `Violation Type` + `Fine Amount` as first-class DFR
  columns, `DFR_ASSIGNMENTS` windowed override system,
  `normalize_date_windows` helper, `verify_summons_against_raw.py` CLI.
- **Hardening run (2026-04-14)** — All three skills passed 9/9 on the
  9-step binary test framework. Regression guards added for unrelated-badge
  preservation and outside-window date preservation.
  See `09_Reference/Personnel/docs/skill_memory/FINAL_SKILL_HARDENING_REPORT.md`.
