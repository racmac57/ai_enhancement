#!/usr/bin/env python3
"""
chat_chunker.py - Standalone chat/text chunker for Claude Code skill use.

Replicates the core chunker_web pipeline (sentence-based chunking, metadata
enrichment, sidecar/transcript generation) with zero external dependencies
beyond the Python 3 standard library.

Usage:
    python3 chat_chunker.py <input_file> [output_dir]

If output_dir is omitted, outputs to KB_Shared/04_output on OneDrive.
"""

import sys
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# Configuration (mirrors chunker_web defaults)
# ---------------------------------------------------------------------------
DEFAULT_CHUNK_SIZE = 800   # max chars per chunk
DEFAULT_OVERLAP = 50       # char overlap between adjacent chunks
MIN_CHUNK_SIZE = 100       # discard chunks smaller than this
SUMMARY_MAX_CHARS = 240
MAX_KEY_TERMS = 6

STOPWORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "be", "this", "that", "from", "as",
    "was", "were", "it", "if", "not", "i", "you", "we", "they", "me", "my",
    "do", "did", "does", "has", "have", "had", "so", "can", "will", "just",
    "than", "then", "also", "no", "yes", "all", "any", "been", "its", "your",
    "our", "their", "what", "which", "who", "how", "when", "where", "there",
    "here", "about", "would", "could", "should", "into", "each", "other",
    "some", "such", "only", "more", "most", "very", "much", "well", "too",
})

TOPIC_KEYWORDS = {
    "ai": ("llm", "prompt", "embedding", "openai", "anthropic", "chatgpt",
           "rag", "claude", "model", "token", "inference", "fine-tune"),
    "code": ("function", "class", "import", "def ", "return ", "variable",
             "error", "debug", "commit", "branch", "merge", "refactor"),
    "conversation": ("user:", "assistant:", "human:", "ai:", "transcript",
                     "chat", "message", "reply", "conversation"),
    "docs": ("readme", "documentation", "guide", "tutorial", "changelog"),
    "data": ("dataset", "csv", "analysis", "query", "database", "sql",
             "table", "schema", "migration"),
    "devops": ("deploy", "ci", "cd", "pipeline", "docker", "container",
               "kubernetes", "terraform", "ansible"),
    "web": ("api", "endpoint", "request", "response", "http", "rest",
            "graphql", "frontend", "backend"),
}

TECH_KEYWORDS = {
    "python": (".py", "def ", "import ", "pandas", "numpy", "flask", "django"),
    "javascript": (".js", ".ts", "const ", "let ", "function ", "async ", "react"),
    "powershell": (".ps1", "param(", "Write-Host", "Get-ChildItem"),
    "sql": (".sql", "select ", "from ", "join ", "where "),
    "shell": (".sh", "bash", "#!/bin", "chmod", "grep", "awk"),
}


# ---------------------------------------------------------------------------
# Sentence splitting (no NLTK required)
# ---------------------------------------------------------------------------
# Abbreviations that should NOT trigger a sentence break
_ABBREVS = re.compile(
    r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|Inc|Ltd|Corp|approx|dept|est|vol"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    r"|e\.g|i\.e|fig|eq)\.$",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    """Split text into sentences using regex heuristics."""
    # Normalize whitespace but preserve newlines for structure
    text = re.sub(r"[ \t]+", " ", text)

    # Split on sentence-ending punctuation followed by whitespace and uppercase
    # or on double-newlines (paragraph breaks)
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z\"])|(?:\n\s*\n)", text)

    sentences = []
    buffer = ""
    for fragment in raw:
        if not fragment or not fragment.strip():
            if buffer:
                sentences.append(buffer.strip())
                buffer = ""
            continue
        candidate = (buffer + " " + fragment).strip() if buffer else fragment.strip()
        # Check if the last period is actually an abbreviation
        if _ABBREVS.search(candidate):
            buffer = candidate
        else:
            sentences.append(candidate)
            buffer = ""
    if buffer:
        sentences.append(buffer.strip())

    return [s for s in sentences if s]


# ---------------------------------------------------------------------------
# Chunking engine
# ---------------------------------------------------------------------------
def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    min_chunk: int = MIN_CHUNK_SIZE,
) -> list[str]:
    """Split text into overlapping chunks along sentence boundaries."""
    sentences = split_sentences(text)
    if not sentences:
        return [text.strip()] if text.strip() else []

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        slen = len(sentence)

        # If adding this sentence exceeds the limit and we have content, flush
        if current_len + slen + 1 > chunk_size and current:
            chunk_body = " ".join(current)
            if len(chunk_body) >= min_chunk:
                chunks.append(chunk_body)

            # Build overlap: walk backward keeping sentences until we hit overlap chars
            overlap_sents: list[str] = []
            overlap_len = 0
            for s in reversed(current):
                if overlap_len + len(s) > overlap:
                    break
                overlap_sents.insert(0, s)
                overlap_len += len(s) + 1

            current = overlap_sents + [sentence]
            current_len = sum(len(s) for s in current) + len(current) - 1
        else:
            current.append(sentence)
            current_len += slen + 1

    # Flush remaining
    if current:
        chunk_body = " ".join(current)
        if len(chunk_body) >= min_chunk:
            chunks.append(chunk_body)
        elif chunks:
            # Merge short tail into last chunk
            chunks[-1] += " " + chunk_body

    return chunks


# ---------------------------------------------------------------------------
# Metadata enrichment (lightweight, rule-based)
# ---------------------------------------------------------------------------
def extract_key_terms(text: str, max_terms: int = MAX_KEY_TERMS) -> list[str]:
    """Return the most frequent non-stopword terms."""
    words = re.findall(r"\b[a-z][a-z0-9_]{2,}\b", text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [term for term, _ in Counter(filtered).most_common(max_terms)]


def detect_tags(text: str) -> list[str]:
    """Detect topic tags via keyword matching."""
    low = text.lower()
    tags = [tag for tag, kws in TOPIC_KEYWORDS.items() if any(kw in low for kw in kws)]
    for tech, kws in TECH_KEYWORDS.items():
        if any(kw.lower() in low for kw in kws):
            tags.append(f"tech:{tech}")
    return sorted(set(tags))


def generate_summary(text: str, max_chars: int = SUMMARY_MAX_CHARS) -> str:
    """Heuristic summary: first N chars of cleaned text."""
    clean = " ".join(text.split())
    if len(clean) <= max_chars:
        return clean
    # Try to break at a word boundary
    trunc = clean[:max_chars]
    last_space = trunc.rfind(" ")
    if last_space > max_chars * 0.6:
        trunc = trunc[:last_space]
    return trunc + "..."


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------
def process(input_path: str, output_dir: str | None = None) -> dict:
    """
    Main processing pipeline. Reads input, chunks, generates all artifacts.

    Returns a summary dict printed as JSON to stdout.
    """
    src = Path(input_path)
    text = src.read_text(encoding="utf-8", errors="replace")

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # Sanitize basename: remove spaces, limit length
    basename = re.sub(r"[^\w\-.]", "_", src.stem)[:60]

    if output_dir is None:
        out_root = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output")
    else:
        out_root = Path(output_dir)

    folder = out_root / f"{timestamp}_{basename}"
    folder.mkdir(parents=True, exist_ok=True)

    # -- Chunk ---------------------------------------------------------------
    chunks = chunk_text(text)

    # -- Write chunk files ---------------------------------------------------
    chunk_records: list[dict] = []
    for i, chunk in enumerate(chunks):
        cfile = folder / f"chunk_{i:05d}.txt"
        cfile.write_text(chunk, encoding="utf-8")

        chunk_id = f"{timestamp}:{basename}:{i:05d}"
        chunk_records.append({
            "chunk_id": chunk_id,
            "chunk_index": i,
            "file": cfile.name,
            "tags": detect_tags(chunk),
            "key_terms": extract_key_terms(chunk),
            "summary": generate_summary(chunk),
            "char_length": len(chunk),
            "byte_length": len(chunk.encode("utf-8")),
        })

    # -- Transcript ----------------------------------------------------------
    transcript_path = folder / f"{timestamp}_{basename}_transcript.md"
    lines = [
        f"# Transcript: {basename}",
        f"**Processed:** {datetime.now().isoformat()}",
        f"**Source:** {src.name}",
        f"**Chunks:** {len(chunks)}",
        f"**Total characters:** {len(text):,}",
        "",
        "---",
        "",
    ]
    for i, chunk in enumerate(chunks):
        lines.append(f"## Chunk {i}")
        lines.append("")
        lines.append(chunk)
        lines.append("")
    transcript_path.write_text("\n".join(lines), encoding="utf-8")

    # -- Sidecar JSON --------------------------------------------------------
    all_tags = detect_tags(text)
    all_terms = extract_key_terms(text)
    file_summary = generate_summary(text)
    content_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

    sidecar = {
        "file": src.name,
        "processed_at": datetime.now().isoformat(),
        "department": "conversation",
        "type": "chat_log",
        "output_folder": str(folder),
        "transcript": transcript_path.name,
        "chunks": chunk_records,
        "metadata_enrichment": {
            "enabled": True,
            "tags": all_tags,
            "key_terms": all_terms,
            "summary": file_summary,
        },
        "source_hash": content_hash,
        "total_chars": len(text),
        "total_chunks": len(chunks),
    }
    sidecar_path = folder / f"{timestamp}_{basename}_sidecar.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")

    # -- Origin manifest -----------------------------------------------------
    origin = {
        "original_full_path": str(src.resolve()),
        "timestamp_created": datetime.now().isoformat(),
        "file_size_bytes": src.stat().st_size,
        "sha256_hash": content_hash,
        "department": "conversation",
    }
    origin_path = folder / f"{timestamp}_{basename}.origin.json"
    origin_path.write_text(json.dumps(origin, indent=2), encoding="utf-8")

    # -- Summary -------------------------------------------------------------
    result = {
        "status": "success",
        "output_folder": str(folder),
        "chunks_created": len(chunks),
        "total_chars": len(text),
        "transcript": str(transcript_path),
        "sidecar": str(sidecar_path),
        "origin": str(origin_path),
        "tags": all_tags,
        "key_terms": all_terms,
    }
    print(json.dumps(result, indent=2))
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: chat_chunker.py <input_file> [output_dir]\n"
            "\n"
            "  input_file  Path to the text/chat file to chunk\n"
            "  output_dir  Where to write output (default: KB_Shared/04_output)",
            file=sys.stderr,
        )
        sys.exit(1)

    in_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    process(in_file, out_dir)
