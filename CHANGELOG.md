# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-04-10

### Added
- Initial repository setup with foundational documentation
- `qa-skill-hardening` skill — multi-agent QA swarm for skill testing and hardening
  - Auto-discovers project structure (CLAUDE.md, skills, scripts, configs)
  - 9-step binary test framework (PASS=1 / FAIL=0)
  - Parallel read-only testing (Wave A) and sequential write-capable testing (Wave B)
  - Regression protection — never commits a state where a passing test drops to FAIL
  - Generates per-skill memory files, regression tests, and final hardening reports
- `CLAUDE.md` with project rules, naming conventions, and forbidden patterns
- `README.md` with project overview, skill inventory, and installation guide
- `docs/SUMMARY.md` with condensed project summary
- `docs/ARCHITECTURE.md` with project structure and design decisions
- `docs/CONTRIBUTING.md` with guide for adding new skills
- `.claude/settings.json` with project-level Claude Code configuration

### Known Issues
- None at initial release

### Historical Bugs
- None — fresh repository
