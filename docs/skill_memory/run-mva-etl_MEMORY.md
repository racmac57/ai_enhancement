# run-mva-etl — Hardening Memory

## Metadata

| Field | Value |
|-------|--------|
| **Skill path** | `C:\Users\carucci_r\.claude\skills\run-mva-etl\SKILL.md` |
| **Scope** | GLOBAL |
| **Type** | Read-mostly workflow (orchestrates `python mva_crash_etl.py`; does not edit the script) |
| **Project** | Workbook_Redesign_2026 (not present under `00_dev` — script vendored in that repo) |
| **Run date** | 2026-04-17 |

---

## Classification

| Field | Value |
|-------|--------|
| **Dependencies** | `mva_crash_etl.py`; `Data_Ingest/CAD_RMS_Exports/*CAD*.xlsx`, `*timereport*.xlsx`; output `Data_Load/fact_mva_crashes_2026.csv`; upstream `/preflight-export`, `/clean-cad-export` |
| **Shared write targets** | `Data_Load/fact_mva_crashes_2026.csv` (ETL overwrites; skill documents recovery via git) |
| **Testability** | Full end-to-end needs Workbook_Redesign_2026 tree + real exports; static validation done in this run |

---

## Binary Scorecard (9-step)

| # | Test | Result | Notes |
|---|------|--------|--------|
| T1 | Exists & Loadable | **PASS** | `SKILL.md` present; YAML frontmatter parses (`yaml.safe_load` — exit 0). |
| T2 | Shared Context Access | **PASS** | All paths in the skill are stated relative to Workbook_Redesign_2026 root (`Data_Ingest/`, `Data_Load/`). Optional `handoff_gemini_2026_04_15.md` is cited as narrative context only. `mva_crash_etl.py` not in `00_dev` workspace — expected; skill targets another repo. |
| T3 | Path Safety | **PASS** (after fix) | **Before:** FAIL — example used `cd /home/user/Workbook_Redesign` (forbidden placeholder per `ai_enhancement/CLAUDE.md`). **After:** Removed; run from repo root only, explicit warning against `/home/user/...`. |
| T4 | Data Dictionary Compliance | **PASS** | Canonical columns and domains documented: `Date`, `Unit`, `MetricGroup`, `Metric`, `Value`; Unit and Metric enumerations match CompStat fact-table convention. |
| T5 | Idempotency / Safe Re-run | **PASS** | Skill states ETL overwrites output; validation checklist is repeatable; git recovery documented for failed validation. |
| T6 | Error Handling | **PASS** | Preflight abort if exports missing/small; post-checks mark FAIL; recommends follow-up actions (e.g. `git diff mva_crash_etl.py`). |
| T7 | Output Correctness | **PASS** | Markdown run report structure specified (sources, output path, schema, S2/S3/S4, distributions). |
| T8 | CLAUDE.md Rule Compliance | **PASS** (after fix) | `name` + `description` in frontmatter; description length **240** chars (limit 250). Path placeholder removed for `ai_enhancement` path rules. |
| T9 | Integration / Cross-Skill Safety | **PASS** | Documents upstream `/preflight-export`, `/clean-cad-export`; siblings `apply-s2-s3-s4`, `standardize-m-code`; no conflicting shared targets with other global skills. |

**Final score: 9/9 — PASS**

---

## Evidence Log

### T1 — Frontmatter parse

```text
Command: python -c "import yaml, pathlib; ..."
Output: frontmatter: OK
Exit code: 0
```

### T3 / T8 — Description length

```text
Command: python -c "len(description)"
Output: 240
```

### Workspace discovery (no bundled ETL in `00_dev`)

```text
Glob **/mva_crash_etl.py under 00_dev: 0 files
Grep mva_crash_etl in 00_dev: no matches
```

---

## Failure Analysis (resolved)

| Field | Value |
|-------|--------|
| Skill Name | run-mva-etl |
| Failed Test | T3 Path Safety; T8 CLAUDE.md Rule Compliance |
| Exact Problem | Bash example used `cd /home/user/Workbook_Redesign` |
| Evidence | SKILL.md lines under "### 3. Run the ETL" (pre-fix) |
| Root Cause | Linux placeholder inconsistent with Windows/OneDrive workflow and `ai_enhancement` rule: no hardcoded `/home/username/...` paths |
| Corrective Action | Replaced with "run from Workbook_Redesign_2026 repo root" + `python mva_crash_etl.py` only |
| New Strategy | Re-tested T1,T3,T8 via static analysis |

---

## Iteration History

| Round | Action |
|-------|--------|
| 1 | Initial 9-step audit; T3/T8 FAIL on path placeholder |
| 2 | Edited `~/.claude/skills/run-mva-etl/SKILL.md`; all tests PASS |

---

## Phase 4 Regression (this skill only)

| Check | Result |
|-------|--------|
| First-time hardening | No prior scorecard for `run-mva-etl` in this hub |
| Post-fix static re-test | All nine criteria remain PASS |

---

## Status

**PASS (9/9)** — Documentation sync: `docs/skills/how_to/run-mva-etl.md`, `SKILLS_INDEX.md`, `global_skills.md` updated in `ai_enhancement` repo.
