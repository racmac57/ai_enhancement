# Regression Tests

## Run Date: 2026-04-10
## Scope: 6 user-level skills

## Results

No regressions detected. All previously-passing tests maintained PASS status after hardening.

## Regression Matrix

| Skill | Pre-Hardening Score | Post-Hardening Score | Delta | Regressions |
|-------|--------------------|--------------------|-------|-------------|
| arcgis-pro | 7/9 | 9/9 | +2 | 0 |
| data-validation | 7/9 | 9/9 | +2 | 0 |
| etl-pipeline | 7/9 | 9/9 | +2 | 0 |
| html-report | 7/9 | 9/9 | +2 | 0 |
| frontend-slides | 8/9 | 8/9 | 0 | 0 |
| chunk-chat | 6/9 | 9/9 | +3 | 0 |

**Total improvements: 11 tests fixed across 5 skills. Zero regressions.**

---

## apply-s2-s3-s4 (2026-04-17)

**Markers**

1. `SKILL.md` YAML: `name: apply-s2-s3-s4`, `description` length ≤ 250.
2. Transform fixture: 3-row CSV/DataFrame (totals row + duplicate PK) → 1 row after S2+S3, `Value` column present after S4 shim.

**Automated checks**

1. `python -c` with `yaml.safe_load` on `~/.claude/skills/apply-s2-s3-s4/SKILL.md` frontmatter (must not raise).
2. Pandas fixture: totals row removed, duplicate PK collapsed, `Value` column after shim — see `apply-s2-s3-s4_MEMORY.md`.

---

## Run Date: 2026-04-17
## Scope: `run-mva-etl` (single skill)

| Skill | Pre-Hardening Score | Post-Hardening Score | Delta | Regressions |
|-------|--------------------|--------------------|-------|-------------|
| run-mva-etl | n/a (first hub entry) | 9/9 | — | 0 |

**Regression guard:** Re-ran static 9-step criteria after SKILL.md path fix; all remained PASS. No other skills in this repo were modified during this run.
