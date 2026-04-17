# Skill Hardening Master Tracker

## Run Date: 2026-04-10
## Target: `~/.claude/skills/` (user-level skills)
## Scope: 6 skills (qa-skill-hardening excluded - already 9/9 PASS)

**Update 2026-04-17:** `standardize-m-code` — [standardize-m-code_MEMORY.md](standardize-m-code_MEMORY.md). **`run-mva-etl`** — [run-mva-etl_MEMORY.md](run-mva-etl_MEMORY.md). **`apply-s2-s3-s4`** — [apply-s2-s3-s4_MEMORY.md](apply-s2-s3-s4_MEMORY.md).

## Global Status Table

| Skill | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | Score | Status |
|-------|----|----|----|----|----|----|----|----|-----|-------|--------|
| arcgis-pro | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| data-validation | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| etl-pipeline | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| html-report | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| frontend-slides | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 8/9 | BLOCKED |
| chunk-chat | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| standardize-m-code | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| run-mva-etl | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |
| apply-s2-s3-s4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 9/9 | PASS |

## Test Legend

| # | Test |
|---|------|
| T1 | Exists & Loadable |
| T2 | Shared Context Access |
| T3 | Path Safety |
| T4 | Data Dictionary Compliance |
| T5 | Idempotency / Safe Re-run |
| T6 | Error Handling |
| T7 | Output Correctness |
| T8 | CLAUDE.md Rule Compliance |
| T9 | Integration / Cross-Skill Safety |

## Shared Lessons Learned

1. **Flat .md files in `~/.claude/skills/` work but lack discoverability.** Adding YAML frontmatter with `name` and `description` enables auto-invocation matching. All 4 flat files (arcgis-pro, data-validation, etl-pipeline, html-report) were missing frontmatter.

2. **Platform portability matters.** The chunk-chat skill used Unix-only paths (`/tmp/`) and commands (`rm /tmp/...`). User is on Windows. System temp directory references (`$TMPDIR`/`$TEMP`) are platform-agnostic.

3. **Script paths must be absolute or home-relative.** `python3 .claude/scripts/...` is CWD-relative and breaks when invoked from any project other than `~/.claude/`. Changed to `$HOME/.claude/scripts/...`.

4. **Third-party skills with their own git repos are BLOCKED for modification.** frontend-slides has a 311-char description (limit: 250) but modifying it would cause upstream drift. Flagged as BLOCKED.

## Cross-Skill Dependency Map

```
arcgis-pro.md       -> (standalone, no deps)
data-validation.md  -> references 09_Reference/Standards/ (contextual)
etl-pipeline.md     -> references path_config, 09_Reference/Standards/ (contextual)
html-report.md      -> references 08_Templates/Report_Styles/ (contextual)
frontend-slides/    -> self-contained with supporting files (STYLE_PRESETS.md, etc.)
chunk-chat/         -> depends on ~/.claude/scripts/chat_chunker.py (executable dep)
```

No shared write targets between skills. No circular dependencies.

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| frontend-slides description >250 chars | Low | Third-party repo; does not affect functionality. Monitor for upstream fix. |
| chunk-chat $HOME expansion on Windows | Low | `$HOME` expands correctly in Git Bash / WSL. In PowerShell, use `$env:USERPROFILE`. Claude adapts the command to the active shell. |
