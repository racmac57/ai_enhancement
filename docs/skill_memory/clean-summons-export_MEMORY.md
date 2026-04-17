# clean-summons-export — Hardening Memory

## Metadata

| Field | Value |
|-------|--------|
| **Skill path** | `C:\Users\carucci_r\.claude\skills\clean-summons-export\SKILL.md` |
| **Scope** | GLOBAL |
| **Type** | Read-only transformation spec (guidance with concrete pandas patterns) |
| **Project** | Workbook_Redesign_2026 (input/output paths are project-relative) |
| **Run date** | 2026-04-17 |

---

## Classification

| Field | Value |
|-------|--------|
| **Dependencies** | `pandas`; `Data_Ingest/CAD_RMS_Exports/*eticket*.csv`; output `Data_Load/summons_slim_for_powerbi.csv`; upstream `/preflight-export`; sibling `/clean-cad-export`, `/clean-arrest-export` |
| **Shared write targets** | `Data_Load/summons_slim_for_powerbi.csv` (overwrite-idempotent monthly slim extract) |
| **Testability** | Full E2E requires Workbook_Redesign_2026 data files; this run executed static/rule validation in `00_dev` |

---

## Binary Scorecard (9-step)

| # | Test | Result | Notes |
|---|------|--------|--------|
| T1 | Exists & Loadable | **PASS** | `SKILL.md` exists; YAML frontmatter parsed successfully. |
| T2 | Shared Context Access | **PASS** | Referenced paths are project-relative and coherent for Workbook_Redesign_2026 (`Data_Ingest/`, `Data_Load/`). |
| T3 | Path Safety | **PASS** | No hardcoded `/home/...` or `~/...`; paths are relative and portable per `ai_enhancement/CLAUDE.md`. |
| T4 | Data Dictionary Compliance | **PASS** | Core schema columns are explicitly mapped (`Date`, `MonthKey`, `CaseTypeCode`, `Metric`, `OfficerBadge`, `OffenseCode`, `OffenseDescription`, `PleadingAmount`, `Value`). |
| T5 | Idempotency / Safe Re-run | **PASS** | Output is explicit overwrite (`summons_slim_for_powerbi.csv`) and documented as idempotent monthly refresh. |
| T6 | Error Handling | **PASS** | Parse strategy uses `on_bad_lines="warn"` and date coercion; malformed rows are logged rather than causing opaque failure. |
| T7 | Output Correctness | **PASS** | Slim output contract and field typing are fully specified, including drop-null-date behavior and DAX join semantics via `MonthKey`. |
| T8 | CLAUDE.md Rule Compliance | **PASS** | Frontmatter present (`name`, `description`); description length 238 (<=250); no forbidden path patterns. |
| T9 | Integration / Cross-Skill Safety | **PASS** | Upstream/downstream chain is explicit and non-conflicting; no cross-skill write collisions beyond intended slim output artifact. |

**Final score: 9/9 — PASS**

---

## Evidence Log

### T1 / T8 — Frontmatter and description length

```text
Command: python -c "yaml.safe_load(frontmatter); len(description)"
Output:
  frontmatter: OK
  name: clean-summons-export
  description_len: 238
Exit code: 0
```

### T3 — Path safety markers

```text
Command: python -c "scan SKILL.md for '/home/' and '~/...'"
Output:
  contains_home_placeholder: False
  contains_tilde_path: False
Exit code: 0
```

### T4 / T7 — Schema markers and output contract

```text
rg matches in SKILL.md:
- MonthKey join to ___DimMonth[MonthKey]
- CaseTypeCode derived from Case Type Code
- PleadingAmount numeric coercion from Pleading Amount
- Output file Data_Load/summons_slim_for_powerbi.csv
```

---

## Iteration History

| Round | Action |
|-------|--------|
| 1 | Initial 9-step audit completed; all tests PASS; no SKILL.md code changes required. |

---

## Phase 4 Regression (this skill only)

| Check | Result |
|-------|--------|
| First-time hardening | No prior scorecard for `clean-summons-export` in this hub |
| Post-audit re-check | All nine criteria remain PASS |

---

## Status

**PASS (9/9)** — Documentation sync completed: `docs/skills/how_to/clean-summons-export.md`, `docs/skills/SKILLS_INDEX.md`, and `docs/skills/global_skills.md` updated.
