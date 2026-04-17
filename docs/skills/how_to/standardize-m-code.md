# How-to: /standardize-m-code

> **Refreshed** by `/qa-skill-hardening` Phase 7 — **9/9 PASS** (2026-04-17).  
> Edit behavior in `SKILL.md` at the install path below; sync this file when the skill changes.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | standardize-m-code |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\standardize-m-code\SKILL.md` |
| **Invoke** | `/standardize-m-code` or mention the skill when editing Power Query `.m` files in Workbook_Redesign |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Wrapper around `standardize_m_code.py` in Workbook_Redesign_2026 with `--target-dir 02_Legacy_M_Code` pre-baked — avoids the script’s Windows OneDrive default; dry-run first, `--apply` only after review.

## When to use

- After editing any `.m` file under `02_Legacy_M_Code/` in the **Workbook_Redesign** repo.
- Before a bulk pass applying S2/S3/S4 patterns or `"Crime Analysis "` cleanup.
- User asks to standardize M code, fix Crime Analysis whitespace, or align with the project’s PQ refactor rules.

## How to use

1. Open a terminal with **repo root** = Workbook_Redesign (not `00_dev`).
2. Dry-run (always first):

   ```bash
   python standardize_m_code.py --target-dir 02_Legacy_M_Code
   ```

   Single file (fuzzy match):

   ```bash
   python standardize_m_code.py --target-dir 02_Legacy_M_Code --file csb_monthly.m
   ```

3. Review printed diffs; then apply only with explicit approval:

   ```bash
   python standardize_m_code.py --target-dir 02_Legacy_M_Code --apply
   ```

**Slash command in Claude Code:** `/qa-skill-hardening target=standardize-m-code` runs *this* QA harness on the skill doc; to *do* M-code work, invoke **`/standardize-m-code`** (or natural language) inside a session opened on Workbook_Redesign.

## Output / artifacts

- Stdout: unified diff text; per-file `S2`/`S3`/`S4`/`CLN` / `SKIP` lines.
- With `--apply`: updated `.m` files under `02_Legacy_M_Code/`. User should run `git diff 02_Legacy_M_Code/` after.

## Gotchas

- **Never** omit `--target-dir 02_Legacy_M_Code` — the script default may point at a legacy OneDrive path and fail on Linux or other machines.
- **Always** dry-run before `--apply`.
- Skill examples may show `cd /home/user/Workbook_Redesign`; on Windows, `cd` to your real clone path — then the same `python` lines apply.

## Hardening

- **Scorecard:** [standardize-m-code_MEMORY.md](../../skill_memory/standardize-m-code_MEMORY.md)
