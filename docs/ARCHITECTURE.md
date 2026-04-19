# Architecture

## Overview

ai_enhancement is the **documentation hub** for a skill library hosted elsewhere plus a self-referential QA system. Skill implementations live under `~/.claude/skills/` (global) or each project's `.claude/skills/` (project-scoped). This repo does not host `.claude/skills/` — that tree was removed in the 2026-04 cleanup to prevent drifting sync copies. The QA hardening skill validates all other skills (and itself) against their real install locations.

## Directory Layout

```
ai_enhancement/
│
├── CLAUDE.md                    # Source of truth for project rules
├── README.md                    # Entry point for humans
├── CHANGELOG.md                 # Chronological change log
│
└── docs/
    ├── SUMMARY.md               # Condensed project context
    ├── ARCHITECTURE.md          # This file
    ├── CONTRIBUTING.md          # How to add skills
    ├── skills/                  # Documentation catalog (see below)
    │   ├── SKILLS_INDEX.md      # Authoritative skill catalog
    │   ├── global_skills.md     # Long-form how-to for GLOBAL skills
    │   ├── <project>_skills.md  # One per project-scoped skill set
    │   └── how_to/<name>.md     # Per-skill reference (Phase 7 output)
    └── skill_memory/            # Historical hardening snapshots
        ├── *_MEMORY.md          # Per-skill test scorecards
        ├── REGRESSION_TESTS.md  # Cross-run regression registry
        ├── GIT_COMMIT_LOG.md    # Hardening commit history
        └── SKILL_HARDENING_MASTER.md

# Skill install locations (not in this repo):
# - GLOBAL:  C:\Users\carucci_r\.claude\skills\<name>\SKILL.md
# - PROJECT: <repo-root>\.claude\skills\<name>\SKILL.md
```

## Skill Anatomy

A skill is a directory under the install location (global `~/.claude/skills/` or project `<repo>/.claude/skills/`) containing at minimum a `SKILL.md` file:

```yaml
---
name: my-skill                # Slash command name (/my-skill)
description: What it does     # Used for auto-invocation matching
argument-hint: "[target]"     # Shown in autocomplete
allowed-tools: Bash Read      # Pre-authorized tools
effort: max                   # Reasoning depth
---

# Skill Title

Instructions for Claude when this skill is invoked...
```

### Skill Lifecycle

```
Author writes SKILL.md
       |
Install to ~/.claude/skills/ (global) or .claude/skills/ (project)
       |
Invoke with /skill-name [args]
       |
Claude loads frontmatter + body as system context
       |
Skill executes using allowed tools
       |
/qa-skill-hardening validates the skill (9-step binary test)
```

## QA Hardening Architecture

The `/qa-skill-hardening` skill operates as a multi-agent swarm:

```
Orchestrator Agent
  |
  ├── Discovery Agent      — Phase 0: finds all skills, configs, rules
  ├── Test Design Agent    — Phase 1: creates 9-step test per skill
  ├── Wave A Agents        — Phase 2: parallel read-only skill testing
  ├── Wave B Agent         — Phase 3: sequential write-capable testing
  ├── Regression Agent     — Phase 4: full suite re-run
  ├── Documentation Agent  — Phase 5: generates reports
  └── Git Agent            — Phase 6: commits only on improvement
```

### Agent Isolation Model

| Agent Type | Parallelism | File Access | Isolation |
|------------|-------------|-------------|-----------|
| Discovery | Single | Read-only | None needed |
| Wave A (read-only) | Parallel | Read-only | None needed |
| Wave B (write) | Sequential | Read + Write | Git worktree |
| Regression | Single | Read-only | None needed |
| Git | Single | Read + Write | Main worktree only |

### Test Framework: 9-Step Binary Tests

| # | Test | Category |
|---|------|----------|
| 1 | Exists & Loadable | Structural |
| 2 | Shared Context Access | Dependency |
| 3 | Path Safety | Security |
| 4 | Data Dictionary Compliance | Correctness |
| 5 | Idempotency / Safe Re-run | Reliability |
| 6 | Error Handling | Robustness |
| 7 | Output Correctness | Correctness |
| 8 | CLAUDE.md Rule Compliance | Governance |
| 9 | Integration / Cross-Skill Safety | Safety |

## Design Principles

1. **Self-contained skills**: Each skill carries everything it needs in its directory
2. **Runtime discovery**: No hardcoded project assumptions — skills discover their environment
3. **Evidence over claims**: Every test result must have captured proof
4. **Regression as a gate**: The system refuses to commit if quality drops
5. **Additive growth**: New skills are added without modifying existing ones
