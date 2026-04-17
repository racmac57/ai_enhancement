# How-to: `/html-report`

## Metadata

| Field | Value |
|-------|-------|
| **Scope** | GLOBAL |
| **Skill name** | `html-report` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\html-report\SKILL.md` |
| **Invoke** | `/html-report` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Generate HPD-branded, self-contained HTML reports.

## When to use

- Draft reports for command staff review (weekly briefings, cycle summaries, analytic findings).
- Stand-alone HTML for email distribution where the recipient cannot rely on external CSS/JS loading.
- Printable incident summaries, Clery snapshots, or ad-hoc styled documents that must render identically on any device.

Skip when the user needs a Power BI / ArcGIS dashboard, a plain-text memo (`/hpd-exec-comms`), or a press-ready document.

## How to use

1. Invoke `/html-report`.
2. Provide either source data (CSV / Excel) or narrative body content.
3. The skill prompts for (or confirms from context):
   - **Title** of the report
   - **Date** (defaults to today)
   - **Status** — one of `Draft`, `For Review`, or `Final`
   - **Body** — tables, findings, narrative, or charts to include
4. The skill loads `08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md` at runtime for colors, typography, author block, print CSS, and FOUO pattern, then emits a single HTML file.

## Output / artifacts

- **One `.html` file** with inline `<style>` — no external stylesheets, fonts, or scripts.
- Default landing area: the current project folder if one is active, otherwise `14_Workspace/`.
- Includes status banner (Draft / For Review / Final), author block, timestamp, and FOUO / sensitivity marking.
- Confirm after writing that the file contains **zero** external `href`/`src` references to CDNs.

## Gotchas

- **No external resources.** Never embed CDN fonts, stylesheets, or JS unless the user explicitly asks for a one-off. The report must render offline and in locked-down email clients.
- **Status string is controlled vocabulary.** Must be exactly `Draft`, `For Review`, or `Final` — other strings will not pick up the correct visual styling defined in the style prompt.
- **FOUO / sensitivity marking is required** on law-enforcement reports. Do not omit even for drafts; downgrade wording rather than remove the banner.
- **Template source is canonical.** The style tokens, palette (Navy `#1a2744`, Gold `#c8a84b`), and author block live in `08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md`. Read that file at runtime — do not invent alternate palettes.
- **Preserve `@media print` rules.** Command staff frequently print these; removing the print CSS breaks page breaks, header repetition, and ink-friendly contrast.
- **No em-dashes or en-dashes** anywhere in the output (title, headings, body, footer). Use a plain hyphen-minus with surrounding spaces for separators.
- **Path hygiene:** always `carucci_r` OneDrive root; never hardcode `RobertCarucci`.

## Hardening

- **Scorecard:** After `/qa-skill-hardening` Phase 7, see `~/.claude/skills/docs/skill_memory/html-report_MEMORY.md` when generated.
