# How-to: /inventory-wave

> **Auto-generated or refreshed** by `/qa-skill-hardening` Phase 7 when this skill scores **9/9 PASS**.  
> Edit the source `SKILL.md` for behavior; update this file via Phase 7 or manual sync with `docs/skills/`.

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `inventory-wave` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\inventory-wave\SKILL.md` |
| **Invoke** | `/inventory-wave` or natural language (“inventory Wave B”, “Phase 1 wave inventory”) |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Phase 1 wave inventory generator for Workbook_Redesign_2026 — given 3–4 legacy Compstat workbooks, produce `Docs/wave_<letter>_inventory.md` with sheet list, last-6-month schemas, `_mom` and aux tables, validation gaps, macro audit, and flat-schema mapping.

## When to use

- Phase 1 per-wave sessions; user supplies 3–4 workbook paths (often under `01_Legacy_Copies/`).
- User says “inventory Wave A”, “generate wave inventory”, or similar.
- Before `/standardize-compstat-wb` — downstream reads this Markdown.

## How to use

```
/inventory-wave
```

Provide:

1. **Wave letter** (A–D) — sets output filename `Docs/wave_<letter>_inventory.md`.
2. **3–4 workbook paths** — read-only opens (`openpyxl` read-only + optional pandas schema pass).
3. Optional **date cutoff** (default today) for the 6-month rolling window.

Workflow highlights from `SKILL.md`:

- **Never** expand beyond last **6** monthly sheets + `_mom` + up to **4** aux tables per scope rules.
- If `Docs/wave_<letter>_inventory.md` already exists, offer **update** vs **full regenerate** before re-reading workbooks.
- Cross-reference `02_Legacy_M_Code/<unit>/*.m` when noting Power Query coverage.
- For `.xlsm`, macro audit (Subs/Functions, structural vs safe).
- Community Outreach cluster and `patrol_monthly` Summons removal called out when applicable.

**Related:** `/standardize-compstat-wb` (downstream); `/apply-s2-s3-s4` (Phase 2 table work); `/preflight-export` is for Data_Ingest exports, not workbooks.

## Output / artifacts

- **Single Markdown file:** `Docs/wave_<letter>_inventory.md` with prescribed sections (file breakdown, cross-workbook observations, redesign order, Phase 2 checklist).
- **No writes** to legacy `.xlsx`/`.xlsm` under `01_Legacy_Copies/`.

## Gotchas

- **Active project** should be **Workbook_Redesign_2026** so `01_Legacy_Copies/`, `Docs/`, and `02_Legacy_M_Code/` resolve. If another folder is open, ask for paths — do not assume OneDrive layout.
- **Which CLAUDE.md:** hard rules in the skill refer to **Workbook_Redesign_2026/CLAUDE.md** (redesign-specific), not `ai_enhancement/CLAUDE.md` or SCRPA.
- **Placeholder paths:** do not use `/home/user/...` in examples when giving `cd` or path hints.

## Hardening

- **Scorecard:** [inventory-wave_MEMORY.md](../../skill_memory/inventory-wave_MEMORY.md)
- **Run date:** 2026-04-17
- **Result:** **9 / 9 PASS** — CLAUDE disambiguation + repository context + missing-input guard; end-to-end binary inspection not run from `00_dev`.
