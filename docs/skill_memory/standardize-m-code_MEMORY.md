# standardize-m-code — Hardening Memory

**Scope:** GLOBAL — `C:\Users\carucci_r\.claude\skills\standardize-m-code\SKILL.md`  
**Run:** 2026-04-17  
**Type:** read-only (instructional; underlying script is write-capable when user runs it)  
**Target argument:** `standardize-m-code` (from `/qa-skill-hardening target=standardize-m-code`)

## Binary scorecard (9/9 = PASS)

| # | Test | Result | Evidence |
|---|------|--------|----------|
| T1 | Exists & Loadable | **PASS** | `Test-Path` → `True` on `...\standardize-m-code\SKILL.md`; YAML frontmatter has `name:` + `description:`. |
| T2 | Shared Context Access | **PASS** | Skill documents running `python standardize_m_code.py` from **Workbook_Redesign** root with `--target-dir 02_Legacy_M_Code`. That repo is the intended context; `00_dev` has no `standardize_m_code.py` — expected for a cross-repo workflow skill. |
| T3 | Path Safety | **PASS** | Mandates `--target-dir 02_Legacy_M_Code` (relative). Hardcoded paths appear only as **quoted documentation** of upstream `DEFAULT_TARGET_DIR` failure mode, not as instructions to use those paths. |
| T4 | Data dictionary / schema | **PASS** | References M/PQ concepts (`Control #`, `ReportNumberNew`, `"Crime Analysis "` cleanup) consistent with Compstat workbook work; N/A to SCRPA CSV schema. |
| T5 | Idempotency / safe re-run | **PASS** | Requires dry-run before `--apply`; notes idempotent SKIP behavior in script. |
| T6 | Error handling | **PASS** | Documents SKIP reasons, user approval before apply, `git diff` post-check. |
| T7 | Output correctness | **PASS** | Describes unified diff / stdout expectations. |
| T8 | CLAUDE.md compliance | **PASS** | Does not contradict `00_dev` / SCRPA `claude.md` when used in the wrong repo — skill is explicitly Workbook_Redesign-scoped behavior. |
| T9 | Integration | **PASS** | Lists siblings (`/apply-s2-s3-s4`, `/standardize-compstat-wb`, `/inventory-wave`) without conflicting write targets at skill-doc layer. |

**Status:** **PASS (9/9)**

## Notes (non-scoring)

- Examples use `cd /home/user/Workbook_Redesign` (Linux). On Windows, use the actual clone path (e.g. `cd` to the repo root in PowerShell). Does not fail T3 — working directory is user-specific; relative `--target-dir` remains correct.

## Iteration history

- Round 1: all gates PASS; no edits required to `SKILL.md`.
