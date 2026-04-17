# standardize-compstat-wb — Hardening Memory

**Scope:** GLOBAL — `C:\Users\carucci_r\.claude\skills\standardize-compstat-wb\SKILL.md`  
**Run:** 2026-04-17  
**Type:** procedural (read-only on `01_Legacy_Copies/`; writes `Docs/redesign_<unit>.md`, optional `.m` updates via `/standardize-m-code` helper; no default automated `.xlsx` writer)  
**Target argument:** `standardize-compstat-wb`

## Binary scorecard (9/9 = PASS)

| # | Test | Result | Evidence |
|---|------|--------|----------|
| T1 | Exists & Loadable | **PASS** | `Test-Path` True on `...\standardize-compstat-wb\SKILL.md`; `yaml.safe_load` on frontmatter succeeds; `name: standardize-compstat-wb`, `description` length 246 (≤ 250). |
| T2 | Shared Context Access | **PASS** | Skill references `Claude.md` at Workbook_Redesign_2026 root — verified on disk: `…\10_Projects\Monthly_Report\Workbook_Redesign_2026\Claude.md`. Relative paths (`01_Legacy_Copies/`, `Docs/wave_<letter>_inventory.md`, `02_Legacy_M_Code/`) resolve when cwd is that repo. |
| T3 | Path Safety | **PASS** | Examples use repo-relative paths only; no `~/`, no `/home/user/...`, no hardcoded user abspaths in runnable examples. |
| T4 | Data dictionary / schema | **PASS** | Canonical `Date \| Unit \| MetricGroup \| Metric \| Value` matches redesign program; aligns with `Claude.md` flat long-format rules (schema extended with MetricGroup for the estate). Community Outreach cross-check references `Docs/community_outreach_schema.md`. |
| T5 | Idempotency / safe re-run | **PASS** | Plan Markdown can be regenerated; M-code changes follow `/standardize-m-code` dry-run → `--apply`; legacy folder read-only; default forbids structural Python Excel writes. |
| T6 | Error handling | **PASS** | Skill requires wave inventory + paths before work; optional XML surgery behind explicit confirmation; Summons bypass documented for Patrol. |
| T7 | Output correctness | **PASS** | Defines deliverables: `Docs/redesign_<unit>.md`, M diff via helper, optional XML-built xlsx only on opt-in. |
| T8 | CLAUDE.md compliance | **PASS** | Matches `ai_enhancement/CLAUDE.md` (frontmatter, naming, path rules). Hard rules anchored to **`Claude.md`** at Workbook repo root (disambiguated from SCRPA / other `CLAUDE.md`). **Repository context** section added in this hardening pass. |
| T9 | Integration | **PASS** | Upstream `/inventory-wave`, siblings `/standardize-m-code`, `/apply-s2-s3-s4`, `/clean-summons-export`; shared writes confined to `Docs/` + `02_Legacy_M_Code/` under user control. |

**Status:** **PASS (9/9)**

## Iteration history

- Round 1: Added **Hard rules (Workbook_Redesign_2026)** intro pointing at repo `Claude.md`; added **Repository context** (paths relative to Workbook_Redesign_2026, not `ai_enhancement` / `00_dev` alone).

## Notes (non-scoring)

- Full end-to-end redesign (Excel GUI + PQ) is not automated by the skill file itself; validation is static + path proof + schema alignment with the live `Claude.md` in Workbook_Redesign_2026.
