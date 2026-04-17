# AI Handoff: T4 Scoring Pipeline Complete + Skills Audit

**Date:** 2026-04-16
**Author:** Claude (Opus 4.6, Claude Code)
**Session scope:** T4 Hotspot Analysis (`Acute_Crime`) + ai_enhancement skills inventory
**Status:** Scripts committed; skills audit report-only (no changes made)

---

## 1. Opening Prompts

### For Claude Code (T4 project)
> Resume T4 Hotspot Analysis at `C:\Users\carucci_r\OneDrive - City of Hackensack\10_Projects\Acute_Crime`. Read `CLAUDE.md` for full context. All 6 DV plan TODOs are closed (§23). `Scripts/t4/` package is committed (`0fcbf02`). Working tree is clean. Next actions: `/review` on Scripts/t4/, `/check-paths` to verify external dependencies, then `/plan` for Block_Final address normalization and Radio resolution logic.

### For Cursor (orchestrator)
> T4 scoring pipeline scripts are committed on `main` at `0fcbf02`. All 6 DV exclusion TODOs are Done in CLAUDE.md §23. The over-exclusion fix in `type_fallback.py` has been tested and committed. A skills audit identified 4 unhardened global skills and 3 stale flat command files needing cleanup. See `00_dev/ai_enhancement/docs/ai_handoff/HANDOFF_20260416_T4_Scoring_Pipeline_and_Skills_Audit.md` for full state.

### For Claude Code (ai_enhancement cleanup)
> Resume skills cleanup at `C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\ai_enhancement`. Read `docs/skills/SKILLS_INDEX.md`. Four global skills are indexed but have no SKILL.md on disk: `check-paths`, `frontend-design`, `claude-api`, `simplify`. Three stale flat files remain in `~/.claude/commands/` (`html-report.md`, `new-etl.md`, `validate-data.md`) — duplicates of dir-form skills. Seven how-to files are missing. See Section 5 of this handoff for the full inventory.

---

## 2. Background & Key Decisions

### T4 Hotspot Analysis — what happened this session

This session continued from a compacted conversation that had built the `Scripts/t4/` package. Work completed:

1. **Over-exclusion fix in `type_fallback.py`** — `build_dv_type_set()` was loading ALL rows from `incident_type_map.csv`, including generic entries (`assault`, `simple assault`, `harassment`, `threats`) that would cause false DV exclusions on non-DV RMS records. Fixed by adding a `_DV_KEYWORDS` regex filter that only loads rows containing `domestic`, `restraining`, `stalking`, `2c:25`, `tro`, `fro`.

2. **Edge case testing confirmed:**
   - `simple assault`, `assault`, `harassment`, `threats` -> KEEP (not excluded)
   - `Domestic Violence - 2C:25-21`, `domestic dispute`, `Service - TRO` -> EXCLUDE (DV)
   - `Stalking - 2C:12-10` (citation-suffixed) -> KEEP; bare `stalking` -> EXCLUDE

3. **CLAUDE.md §23 updated** — all 6 TODO rows marked Done with file pointers.

4. **CHANGELOG updated** — new "T4 scoring pipeline scripts" section; DV module section changed from Pending to Closed.

5. **Cursor committed everything** in `0fcbf02` (including NIBRS Tier 2 parsing fix and decay float fix from a parallel Cursor session).

### Skills audit — what was found

The operator asked for a skills inventory cross-referenced against the T4 project needs. The audit was report-only (no file changes). Findings are in Section 5 below.

---

## 3. Implementation Status

### T4 Project (`Acute_Crime`)

| Item | Status |
|------|--------|
| Branch | `main` (3 commits, working tree clean) |
| Latest commit | `0fcbf02` — type keyword filter, NIBRS Tier 2 parsing, decay float fix, plan sync |
| `Scripts/t4/__init__.py` | Committed |
| `Scripts/t4/column_norm.py` | Committed — 60-entry alias map, `standardize_case_number()` |
| `Scripts/t4/type_fallback.py` | Committed — 7 regex patterns + DV keyword filter (over-exclusion fixed) |
| `Scripts/t4/score_integration.py` | Committed — Tier 1 + Tier 2 + decay + boost + two-layer DV exclusion |
| `Scripts/t4/cad_rms_qc_preflight.py` | Committed — 10+ CAD checks, 7+ RMS checks, JSON output |
| CLAUDE.md §23 TODOs | All 6 Done |
| CHANGELOG | Current through this session |
| Untracked files | `Data/2025_10_29_to_2026_04_16_DV_roster.xlsx` (gitignored by `Data/` rule) |

### ai_enhancement

| Item | Status |
|------|--------|
| Skills hardened tonight (by operator) | data-validation, arcgis-pro, etl-pipeline, html-report, hpd-exec-comms, qa-skill-hardening |
| SKILLS_INDEX.md | Updated with SKILL.md paths and how-to links |
| Stale `ai_enhancement/.claude/skills/` | Deleted (operator confirmed) |
| GitHub | Committed and pushed to `racmac57/ai_enhancement.git` |

---

## 4. T4 Architecture Reference

### File tree (Scripts only)

```
Scripts/t4/
  __init__.py
  column_norm.py        # normalize_columns(), standardize_case_number(), COLUMN_ALIASES
  type_fallback.py      # build_dv_type_set(), is_dv_type(), flag_dv_by_type()
  score_integration.py  # TIER1_SCORES, TIER2_SCORES, recency_multiplier(),
                        # load_cad(), load_rms(), load_dv_blocklist(),
                        # apply_dv_exclusion(), compute_location_scores(),
                        # generate_data_quality_note(), run_pipeline()
  cad_rms_qc_preflight.py  # check_cad(), check_rms(), run_preflight()
```

### External dependencies (must resolve)

| Resource | Path | Last verified |
|----------|------|---------------|
| DV blocklist (PII-safe) | `{project}/Data/dv_case_numbers_for_t4.csv` | 2026-04-16 (1,536 rows) |
| DV enriched (PII — DO NOT COPY) | `{onedrive}/02_ETL_Scripts/dv_doj/processed_data/dv_final_enriched.csv` | 2025-10-29 |
| Incident type map | `{onedrive}/02_ETL_Scripts/dv_doj/docs/mappings/incident_type_map.csv` | 2026-04-16 |
| CallType_Categories | `{onedrive}/09_Reference/Classifications/CallTypes/CallType_Categories.csv` | 2026-04-16 |
| T4 Master workbook | `{onedrive}/Documents/Projects/T4_New/T4_Master_Query/T4_Master_Reporting_Template.xlsx` | 2025-05-28 |
| CAD data | `{project}/Data/cad/monthly/` and `yearly/` | 2026-04-16 |
| RMS data | `{project}/Data/rms/monthly/` and `yearly/` | 2026-04-16 |

`{onedrive}` = `C:\Users\carucci_r\OneDrive - City of Hackensack`
`{project}` = `{onedrive}\10_Projects\Acute_Crime`

---

## 5. Skills Audit Results (Report Only — No Changes Made)

### A. Global skills: installed vs. indexed

| Skill | SKILL.md on disk | SKILLS_INDEX row | Hardened tonight | Issue |
|-------|-----------------|-----------------|-----------------|-------|
| qa-skill-hardening | Yes | Yes | Yes | Clean |
| frontend-slides | Yes | Yes | No | Missing how-to |
| chunk-chat | Yes | Yes | No | Missing how-to |
| arcgis-pro | Yes | Yes | Yes | Clean |
| data-validation | Yes | Yes | Yes | Clean |
| html-report | Yes | Yes | Yes | Clean |
| etl-pipeline | Yes | Yes | Yes | Clean |
| hpd-exec-comms | Yes | Yes | Yes | Clean |
| **check-paths** | **No** | Yes | No | **Flat file at `~/.claude/commands/check-paths.md` only. Never converted to dir-form.** |
| **frontend-design** | **No** | Yes | No | **Index lists SKILL.md path that doesn't exist. Plugin/marketplace skill, not custom.** |
| **claude-api** | **No** | Yes | No | **Built-in Claude Code skill. Index lists phantom path.** |
| **simplify** | **No** | Yes | No | **Built-in Claude Code skill. Index lists phantom path.** |

### B. Stale flat command files (`~/.claude/commands/`)

| File | Disposition |
|------|-------------|
| `check-paths.md` | **Convert** to `~/.claude/skills/check-paths/SKILL.md` |
| `html-report.md` | **Delete** — dir-form `html-report/SKILL.md` already exists |
| `new-etl.md` | **Delete** — dir-form `etl-pipeline/SKILL.md` already exists (renamed) |
| `validate-data.md` | **Delete** — dir-form `data-validation/SKILL.md` already exists (renamed) |

### C. Missing how-to files (`docs/skills/how_to/`)

Have how-tos (6): qa-skill-hardening, arcgis-pro, data-validation, etl-pipeline, hpd-exec-comms, `_TEMPLATE.md`

Missing how-tos (7): **frontend-slides**, **chunk-chat**, **html-report**, **check-paths**, **frontend-design**, **claude-api**, **simplify**

### D. Recommended cleanup actions

1. Delete 3 stale flat files (`html-report.md`, `new-etl.md`, `validate-data.md` from `~/.claude/commands/`)
2. Convert `check-paths.md` flat file to `~/.claude/skills/check-paths/SKILL.md`
3. Remove or annotate phantom SKILLS_INDEX entries for `frontend-design`, `claude-api`, `simplify` (mark as "built-in, no custom SKILL.md")
4. Generate 7 missing how-to files (or run `/qa-skill-hardening` Phase 7 against each)

---

## 6. T4 Next Steps (Priority Order)

| # | Action | Tool/Skill | Rationale |
|---|--------|-----------|-----------|
| 1 | `/review` on `Scripts/t4/` | `/review` | Scoring weights, DV exclusion, and PII boundaries are high-stakes. Never peer-reviewed. |
| 2 | `/check-paths` on Acute_Crime | `/check-paths` | Verify 12+ external dependency paths in CLAUDE.md §3 still resolve. One broken path silently breaks the pipeline. |
| 3 | `/data-validation` on CAD/RMS inputs | `/data-validation` | Complement `cad_rms_qc_preflight.py` with HPD-domain validators (field-level compliance, badge format). |
| 4 | `/plan` for Block_Final + Radio resolution | `/plan` | Two biggest functional gaps before E2E scoring is meaningful. Block_Final affects every scoring, classification, and displacement calc. |
| 5 | E2E dry run of `score_integration.py` | Manual | `python -m Scripts.t4.score_integration --cycle-id T4_TEST --cad-pull-start 2026-01-01 --cad-pull-end 2026-03-28 --rms-pull-start 2026-01-01 --rms-pull-end 2026-04-11 --analysis-date 2026-04-16` |

### Pending — Core Pipeline (not started)

- Address normalization (`Block_Final`) — `score_integration.py` uses raw address as proxy
- `HowReported = Radio` resolution — scored by default with DQ flag; full linkage check (§6.3) not implemented
- Cycle alignment from T4 Master workbook not wired in
- ArcGIS Pro/Online publishing workflow
- Power BI CSV export generation
- Displacement analysis automation
- Effectiveness feedback loop automation

---

## 7. Open Decisions

| Decision | Owner | Context |
|----------|-------|---------|
| Cycle ID generation method | R. A. Carucci | Calendar file vs. Section 0 manual entry. See `Docs/t4_cycle_id_strategy.md`. |
| `check-paths` skill conversion | R. A. Carucci | Flat file still active in `~/.claude/commands/`. Convert to dir-form or leave? |
| Built-in skill index entries | R. A. Carucci | Remove `frontend-design`, `claude-api`, `simplify` from SKILLS_INDEX or annotate as built-in? |

---

## 8. Known Risks

- **DV roster lag:** Blocklist covers through 2026-04-16. Any T4 window past that date needs a roster refresh per `Docs/dv_blocklist_refresh_governance.md`.
- **Over-exclusion (mitigated):** `build_dv_type_set()` now filters to DV keywords only. Bare `stalking` still excluded by exact match — appropriate for DV context but monitor for edge cases.
- **Flat+dir skill collision:** `~/.claude/commands/html-report.md` and `~/.claude/skills/html-report/SKILL.md` both exist. Claude Code may load both, producing unpredictable behavior. Delete the flat file.
- **Missing Data/ dirs:** `Data/cad/` and `Data/rms/` are gitignored. `score_integration.py` validates paths and exits early if missing, but a fresh clone will have no data.
- **PII:** Never copy `dv_final_enriched.csv` into `Acute_Crime/`. Use only `Data/dv_case_numbers_for_t4.csv` (3 columns, PII-safe).

---

## 9. How to Resume

### T4 project
1. `cd "C:\Users\carucci_r\OneDrive - City of Hackensack\10_Projects\Acute_Crime"` — `git status` should show clean working tree
2. Read `CLAUDE.md` (full agent context, §1-25)
3. Verify `Data/dv_case_numbers_for_t4.csv` exists (1,536 rows, through 2026-04-16)
4. Run `/review` on `Scripts/t4/` before any further development
5. Run `/check-paths` to validate external dependency paths
6. Next build phase: `/plan` for Block_Final normalization + Radio resolution

### ai_enhancement cleanup
1. `cd "C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\ai_enhancement"` — read `docs/skills/SKILLS_INDEX.md`
2. Delete stale flat files: `~/.claude/commands/html-report.md`, `new-etl.md`, `validate-data.md`
3. Convert `~/.claude/commands/check-paths.md` to `~/.claude/skills/check-paths/SKILL.md`
4. Decide on phantom index entries for built-in skills
5. Generate missing how-to files or run `/qa-skill-hardening` Phase 7

---

## 10. Session Artifacts

| File | Location | Purpose |
|------|----------|---------|
| This handoff | `{onedrive}/00_dev/ai_enhancement/docs/ai_handoff/HANDOFF_20260416_T4_Scoring_Pipeline_and_Skills_Audit.md` | Cross-project handoff |
| Prior T4 handoff | `{project}/Docs/handoffs/handoff_20260416_2115.md` | Superseded by this file (that handoff was written before over-exclusion fix and commit `0fcbf02`) |
| Prior skills handoff | `{onedrive}/00_dev/ai_enhancement/docs/ai_handoff/HANDOFF_20260410_Skill_Hardening_Final.md` | Still valid for chunk-chat 2.0 and Windows hardening context |
