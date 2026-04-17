# How-to: `/frontend-slides`

## Metadata

| Field | Value |
|-------|--------|
| **Scope** | GLOBAL |
| **Skill name** | `frontend-slides` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\frontend-slides\SKILL.md` |
| **Invoke** | `/frontend-slides` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Build HTML presentations from scratch or from an existing PowerPoint.

## When to use

- Building a slide deck from an outline, rough notes, or a topic
- Converting a `.ppt` / `.pptx` file into a web-native HTML deck
- Creating a pitch deck, conference talk, or internal presentation
- When the user asks for an animation-rich or visually distinctive deck
- When the delivery target is a browser (kiosk, laptop, shared URL) rather than PowerPoint

Skip when the user wants a static document (use `html-report`) or a simple one-off email (use `hpd-exec-comms`).

## How to use

```
/frontend-slides
```

Provide one of:

- A topic, outline, or rough notes → skill runs **Phase 1 Content Discovery** and builds from scratch
- A path to a `.pptx` file → skill runs **Phase 4 PPT Conversion** (requires `python-pptx`)
- A path to an existing HTML deck → skill runs **Mode C Enhancement** with viewport-safety guardrails

The skill will ask a batched `AskUserQuestion` covering purpose, length, content readiness, and whether inline editing is required, then show 3 visual style previews before committing to an aesthetic.

## Output / artifacts

- **Primary:** a single self-contained HTML file with inline CSS/JS, no npm, no build step
- **Default location:** `14_Workspace/` or a user-specified path
- **Runtime resources bundled / referenced by the skill:**
  - `STYLE_PRESETS.md` — 12 curated visual presets (Phase 2)
  - `viewport-base.css` — mandatory responsive CSS, embedded into every deck
  - `html-template.md` — HTML architecture and JS feature reference
  - `animation-patterns.md` — CSS/JS animation snippets
- **Optional Phase 6 deliverables:** shareable Vercel URL (`scripts/deploy.sh`) or PDF export (`scripts/export-pdf.sh`)

## Gotchas

- **Visual exploration, not abstract choices** — the skill will show 3 preview slides before committing to a style. Don't try to describe the aesthetic in words up front; let the skill render options.
- **16:9 viewport is the default** — `viewport-base.css` assumes a 100vh/100dvh slide with `overflow: hidden`. Other aspect ratios (4:3, vertical, tablet) require an explicit ask.
- **Content density is enforced** — every slide must fit exactly within the viewport. If content exceeds the per-slide limits in `SKILL.md`, the skill will split slides automatically rather than shrink text or scroll.
- **Law-enforcement-sensitive decks need manual markings** — the skill is generic by default and does NOT apply FOUO, CUI, or `hpd-exec-comms` sensitivity banners. Add them manually or pair with `/hpd-exec-comms` for wording.
- **Animation richness bloats file size** — large decks with heavy `animation-delay` staggers and CSS gradients can hit several MB. Strip or simplify if delivering via email; prefer Phase 6 Vercel deploy or PDF export for sharing.
- **PPTX conversion is best-effort** — text, images, slide order, and speaker notes carry over reliably. Complex PPTX animations, SmartArt, and embedded video rarely map 1:1; expect to re-author motion in the HTML output.
- **No system fonts** — the skill uses Fontshare or Google Fonts. Offline environments (RDP with blocked CDN) will fall back to browser defaults and lose the intended typography.

## Hardening

- **Scorecard:** After `/qa-skill-hardening` Phase 7, see `~/.claude/skills/docs/skill_memory/frontend-slides_MEMORY.md` when generated.
