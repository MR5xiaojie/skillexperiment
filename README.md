# Agent Skill Evaluation

This repository contains skill packages, execution utilities, and evaluation results for adherence to skill requirements. The evaluation covers deliverables, procedures, and limits on agent behavior.

## Benchmark results

Nine subcategory scores for seven selected configurations are shown below. All scores are percentages, rounded to two decimal places. GLM-5.3-Flash reports the first execution round.

| Model | Harness | Content | Format | Coverage | Step | Evidence | Tool | Negative | Boundary | Termination |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.28% | 58.08% | 50.18% | 41.95% | 50.06% | 44.44% | 56.86% | 43.96% | 42.65% |
| Claude Opus 5 | Claude Code | 54.09% | 55.69% | 53.83% | 52.22% | 50.70% | 47.47% | 60.65% | 43.60% | 54.41% |
| GPT-5.6 Luna | Codex | 52.03% | 50.33% | 50.89% | 37.38% | 35.79% | 35.35% | 56.57% | 49.40% | 38.24% |
| GPT-5.6 Luna | Claude Code | 51.52% | 46.18% | 48.20% | 39.24% | 39.75% | 49.49% | 59.02% | 48.19% | 30.88% |
| Grok 4.5 | Codex | 43.20% | 48.61% | 34.86% | 31.00% | 19.96% | 34.34% | 44.08% | 19.32% | 30.88% |
| Grok 4.5 | Claude Code | 42.91% | 43.34% | 41.48% | 37.11% | 17.71% | 35.35% | 45.92% | 32.61% | 39.71% |
| GLM-5.3-Flash | Claude Code | 59.15% | 60.50% | 65.28% | 48.83% | 53.48% | 55.05% | 68.95% | 48.55% | 52.94% |

[Download the displayed configuration scores as CSV](results/configuration_scores.csv)

## Evaluation setting

The seven displayed configurations use the same 96 skill–task pairs, with one scored execution per pair. Claude Opus 5, GPT-5.6 Luna, and Grok 4.5 are each evaluated under Codex and Claude Code. GLM-5.3-Flash is evaluated under Claude Code; its scores here use only the first of three independent execution rounds.

Deterministic checks and LLM judgments evaluate individual requirements using execution evidence. For each configuration, scores are calculated within each skill and then averaged across skills. Each subcategory includes the skills with assessed requirements of that type. These are adherence scores, with task success evaluated separately.

## Repository contents

- [`complex-skills/`](complex-skills/): skill packages and associated task and scoring specifications.
- [`runner_core.py`](runner_core.py) and [`runner_retrigger.py`](runner_retrigger.py): execution utilities.
- [`judge.py`](judge.py): reference judging implementation.
- [`results/configuration_scores.csv`](results/configuration_scores.csv): the seven displayed configurations and nine subcategory scores, stored as numeric percentages on a 0–100 scale.
