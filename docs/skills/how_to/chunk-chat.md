# How-to: /chunk-chat

> Manual snapshot reflecting the installed `SKILL.md` (chunk-chat 2.0).
> Edit the source `SKILL.md` for behavior; refresh this file via `/qa-skill-hardening` Phase 7 or manual sync.

## Metadata

| Field | Value |
|-------|-------|
| **Scope** | GLOBAL |
| **Skill name** | `chunk-chat` |
| **SKILL.md path** | `C:\Users\carucci_r\.claude\skills\chunk-chat\SKILL.md` |
| **Invoke** | `/chunk-chat [file-path-or-topic-label] [--chunk-size=N] [--overlap=N]` |
| **Aggregated guide** | [global_skills.md](../global_skills.md) |

## One-line description

Chunk long conversations into sized pieces for RAG ingestion.

## When to use

- Saving the current session for RAG ingestion into the Enterprise Chunker knowledge base.
- Preparing a conversation or chat-log file for semantic search (ChromaDB-backed).
- Splitting a long transcript into sentence-boundary chunks without invoking the `02_data/` watcher.

## How to use

```
/chunk-chat                                   # chunk the current conversation
/chunk-chat CAD_Backfill_Triage               # same, with a Title_Case topic label
/chunk-chat ./logs/session.txt                # chunk an existing file
/chunk-chat ./logs/session.txt --chunk-size=1200 --overlap=80
```

If no file path is supplied, the skill reconstructs the conversation from its context window, writes it to the real Windows temp directory (resolved via `python -c "import tempfile; print(tempfile.gettempdir())"` — **not** `/tmp/`), invokes the chunker, and cleans up the temp file.

## Output / artifacts

Per-run folder under `C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output\{timestamp}_{Topic_Description}_Claude\`:

- `chunk_00000.txt ... chunk_NNNNN.txt` — sentence-boundary semantic chunks (~800 chars, 50-char overlap by default).
- `{timestamp}_{name}_transcript.md` — full readable transcript.
- `{timestamp}_{name}_sidecar.json` — per-chunk metadata (tags, key terms, summary, `source_type`, `language`, `enrichment_version`).
- `{timestamp}_{name}.origin.json` — provenance and source hash.

Override the destination by passing an explicit output dir as the second positional argument to `chat_chunker.py`. The chunker is stdlib-only; enrichment (tags, key terms, summary) is rule-based and runs inline.

## Gotchas

- **PII.** CAD/RMS transcripts routinely contain case numbers (`YY-NNNNNN`), badge numbers, victim/officer names, and addresses. `04_output` is OneDrive-scoped and safe; **do not** upload chunked folders to third-party services without sanitization or the Conversation Archivist PII pass.
- **Not auto-ingested.** Chunks land in `KB_Shared\04_output\` but the ChromaDB watcher only monitors `02_data\`. Run `C:\_chunker\backfill_knowledge_base.py --path <output-folder>` (or the manual process tool) to push a new folder into the knowledge base.
- **Windows `python`, not `python3`.** The SKILL.md and underlying `chat_chunker.py` are invoked with `python` and the full script path (`C:\Users\carucci_r\.claude\scripts\chat_chunker.py`) — `python3` is not registered on this profile and `$HOME` expansion is unreliable under Git Bash.
- **Chunk size vs. overlap.** Smaller chunks improve retrieval precision but inflate vector-store size. Defaults (`~800` / `50`) match `chunker_web` and the Enterprise Chunker watcher — only override via `--chunk-size=` / `--overlap=` if you have a concrete reason.
- **Deterministic IDs.** Chunk filenames are indexed (`chunk_00000` ...) inside a folder keyed by topic + timestamp, so re-running on the same conversation creates a **new** folder rather than overwriting; downstream vector stores will treat a re-run as new chunks. Do incremental updates by chunking only new transcript deltas.
- **Topic label.** If `$ARGUMENTS` is a topic rather than a path, use 4–8 Title_Case words per the AI Suffix Naming Convention; the skill always appends `_Claude`.
- **Context compression.** If earlier turns were summarized out of context, the skill stamps a `[Note]: Earlier portions of this conversation were summarized...` header on the temp file — treat those chunks as lossy and do not rely on them for verbatim recall.
- **Chunking strategy.** Despite the 2.0 framing, the implementation is **sentence-boundary splitting** at a fixed char budget with overlap — not embedding-based semantic clustering. Plan retrieval strategy accordingly.

## Hardening

- Last hardened during the 2026-04-10 dual-session blitz (`HANDOFF_20260410_Skill_Hardening_Final.md`) — Windows temp-dir fix, `python3`→`python`, sidecar schema aligned with Enterprise Chunker (`source_type`, `language`, `enrichment_version`). Re-run `/qa-skill-hardening chunk-chat` to refresh the scorecard.
