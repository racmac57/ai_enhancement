# inventory-wave — Skill Hardening Memory

## Classification

| Field | Value |
|-------|--------|
| **Path** | `C:\Users\carucci_r\.claude\skills\inventory-wave\SKILL.md` |
| **Type** | `write-capable` (orchestrates creation of `Docs/wave_<letter>_inventory.md`; read-only on legacy workbooks) |
| **Project** | Workbook_Redesign_2026 (tree not under `00_dev`; skill paths are repo-relative) |
| **Dependencies** | Workbook `.xlsx`/`.xlsm` under `01_Legacy_Copies/`; optional `02_Legacy_M_Code/<unit>/*.m` cross-reference; **Workbook_Redesign_2026/CLAUDE.md** for redesign rules |
| **Shared write targets** | `Docs/wave_<letter>_inventory.md` (one file per wave; coordinate with user on overwrite) |
| **Testability** | Full 6-month + macro audit needs real binaries; this run: static analysis + YAML + rule compliance |

## 9-Step Binary Scorecard

| # | Test | Result | Evidence |
|---|------|--------|----------|
| T1 | Exists & Loadable | **PASS** | `SKILL.md` present; `python -c` `yaml.safe_load` on frontmatter — exit 0; keys `name`, `description`; `desc_len` 246 (≤250 per `ai_enhancement/CLAUDE.md`) |
| T2 | Shared Context Access | **PASS** (after fix) | **Before:** "CLAUDE.md" ambiguous (SCRPA vs redesign). **After:** "Repository context" + "Workbook_Redesign_2026/CLAUDE.md" for hard rules; documents `$CLAUDE_PROJECT_DIR` for correct repo |
| T3 | Path Safety | **PASS** | Examples use `load_workbook(path,...)`, `pd.read_excel(path,...)` — no `/home/user/...`; paths `01_Legacy_Copies/`, `Docs/`, `02_Legacy_M_Code/` are relative to Workbook root |
| T4 | Data Dictionary Compliance | **PASS** | Canonical mapping table uses `Date`, `Unit`, `MetricGroup`, `Metric`, `Value`; Community Outreach cluster + Patrol Summons removal align with referenced redesign doc |
| T5 | Idempotency / Safe Re-run | **PASS** | Skill says check `Docs/wave_<letter>_inventory.md` first; offer update vs regenerate; does not mandate blindly overwriting |
| T6 | Error Handling | **PASS** (after fix) | **After:** explicit "If any required input is missing, stop and ask" + coexistence with existing inventory file |
| T7 | Output Correctness | **PASS** | Single Markdown deliverable with prescribed sections (header, file breakdown, cross-workbook observations, Phase 2 checklist) |
| T8 | CLAUDE.md Rule Compliance | **PASS** (after fix) | **ai_enhancement:** frontmatter + description length. **Redesign:** hard rules attributed to correct `CLAUDE.md`; no contradiction with path-safety rules in `ai_enhancement/CLAUDE.md` when skill is used in wrong repo — mitigated by repository context |
| T9 | Integration / Cross-Skill Safety | **PASS** | Read-only on `01_Legacy_Copies/`; downstream `/standardize-compstat-wb`; sibling `/apply-s2-s3-s4`; no conflicting shared writes with other global skills |

**Final score: 9/9 — PASS**

## Iteration History

1. Initial static review: T2/T8 at risk due to undifferentiated "CLAUDE.md".
2. **Fix:** Renamed section to **Workbook_Redesign_2026/CLAUDE.md**; added **Repository context** (paths relative to Workbook repo, ask if not open project); strengthened inputs for T6.

## Failure Analysis

None — no FAIL states remained after corrective edits.

## Regression re-check (Phase 4)

Post-fix: re-ran YAML validation and manual criterion check; all nine remain PASS. No other skills modified in `SKILL.md` for this run.
