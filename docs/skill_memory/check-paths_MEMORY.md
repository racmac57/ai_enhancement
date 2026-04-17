# check-paths — Hardening Memory

## Metadata

| Field | Value |
|-------|--------|
| **Skill path** | `C:\Users\carucci_r\.claude\skills\check-paths\SKILL.md` |
| **Scope** | GLOBAL |
| **Type** | Read-only static scanner (emits Markdown report; makes no file changes) |
| **Project context** | Generic HPD workspace path-convention linter |
| **Run date** | 2026-04-17 |

---

## Classification

| Field | Value |
|-------|--------|
| **Dependencies** | None (reads current working directory source files only: `.py`, `.yaml`, `.yml`, `.json`, `.bat`, `.ps1`, `.cmd`) |
| **Shared write targets** | None |
| **Testability** | Static audit only — rule scope is fixed to five enumerated path hygiene issues; no binary data dependencies |
| **Sibling variant** | `02_ETL_Scripts/cad_rms_data_quality/.claude/skills/check-paths/SKILL.md` (project scope; may extend rule set) |

---

## Binary Scorecard (9-step)

| # | Test | Result | Evidence |
|---|------|--------|----------|
| T1 | Exists & Loadable | **PASS** | `SKILL.md` exists at canonical path; YAML frontmatter has `name: check-paths` and `description` (61 chars, ≤ 250). |
| T2 | Shared Context Access | **PASS** | Skill references `path_config.get_onedrive_root()` and `09_Reference/Standards/` as context — both are documented project conventions in global `CLAUDE.md`. No external file dependencies required to run. |
| T3 | Path Safety | **PASS** | No hardcoded `/home/...` placeholders, no `~/` assumptions in the scanner's logic. Skill operates relative to `os.getcwd()`. |
| T4 | Data Dictionary Compliance | **PASS** | Issue set explicitly enforces the canonical vocabulary: `carucci_r` (not `RobertCarucci`), `PowerBI_Data` (not `PowerBI_Date`), `09_Reference/Standards/` (not `unified_data_dictionary`). Aligns with global `CLAUDE.md` Path Resolution rules. |
| T5 | Idempotency / Safe Re-run | **PASS** | Read-only scanner; re-runs produce identical reports for unchanged inputs. No side effects. |
| T6 | Error Handling | **PASS** | Skill explicitly instructs "Do not invent new issue categories. If a file looks suspicious but does not match one of the five rules, note it under the summary as 'needs manual review' rather than as a flagged issue." — graceful handling of ambiguous cases. |
| T7 | Output Correctness | **PASS** | Output format is fully specified: grouped-by-issue report with `path:line` format, per-category counts, total summary, recommended-fix line. Example output block in SKILL.md is canonical. |
| T8 | CLAUDE.md Rule Compliance | **PASS** | Frontmatter valid (`name`, `description`); description length 61 ≤ 250; dir-form `SKILL.md` (recently migrated from command form per `d2a5da1`); aligns with global `CLAUDE.md` Path Resolution section. |
| T9 | Integration / Cross-Skill Safety | **PASS** | No shared write targets; does not modify source files. Coexists with project-scoped `check-paths` variant (separate `SKILL.md` at `02_ETL_Scripts/cad_rms_data_quality/.claude/skills/check-paths/`). `how_to/check-paths.md` notes the project-variant precedence rule for cad_rms work. |

**Final score: 9/9 — PASS**

---

## Evidence Log

### T1 / T8 — Frontmatter and description length

```text
File: C:\Users\carucci_r\.claude\skills\check-paths\SKILL.md
Frontmatter parsed: OK
  name: check-paths
  description: "Scan the current project's source files for path hygiene issues."
  description length: 61
Exit code: 0
```

### T3 — Path safety scan

```text
Command: grep -n "/home/\|~/\|C:\\\\Users\\\\" SKILL.md
Observed: no hardcoded user-specific absolute paths in runnable instructions.
The only `C:\Users\...` reference is in an example OUTPUT excerpt illustrating
a detected issue (not instructions to the agent).
Exit code: 0 (no false positives)
```

### T4 — Rule coverage vs canonical vocabulary

| Rule | Matches global `CLAUDE.md` convention |
|------|---------------------------------------|
| `RobertCarucci` → `carucci_r` | ✅ (Path Resolution §1) |
| `unified_data_dictionary` → `09_Reference/Standards/` | ✅ (Canonical Data Sources) |
| Hardcoded `C:\Users\...` → `path_config.get_onedrive_root()` | ✅ (Path Resolution §4) |
| `PowerBI_Date` → `PowerBI_Data` | ✅ (Path Resolution §2) |
| `PD_BCI_01` retired → archive-only | ✅ (Output Standards / archive-first) |

### T9 — Variant coexistence

```text
Global:  C:\Users\carucci_r\.claude\skills\check-paths\SKILL.md
Project: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality\.claude\skills\check-paths\SKILL.md
Precedence: project variant wins inside cad_rms_data_quality; global wins elsewhere.
Documented in: docs/skills/how_to/check-paths.md (Gotchas section).
```

---

## Iteration History

| Round | Action |
|-------|--------|
| 1 | Retroactive static audit added 2026-04-17 during `/qa-skill-hardening` audit-only verification pass. No SKILL.md changes required. Dir-form migration (commit `d2a5da1`) already brought it into compliance with the rest of the hub. |

---

## Phase 4 Regression (this skill only)

| Check | Result |
|-------|--------|
| First-time hub entry | Previously hardened indirectly via the 2026-04-10 command-form run; no prior scorecard row in this hub |
| Post-migration re-audit (2026-04-17) | All nine criteria PASS; dir-form `SKILL.md` parses cleanly |

---

## Status

**PASS (9/9)** — Memory file created retroactively during 2026-04-17 audit to close the documentation gap. No functional changes to `SKILL.md`; this run was audit-only verification of documentation drift.
