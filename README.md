# Agent Skill Evaluation

This repository contains skill packages, execution utilities, and evaluation results for adherence to skill requirements. The evaluation covers deliverables, procedures, and limits on agent behavior.

## Benchmark results

Results for seven selected configurations are shown below. All scores are percentages, rounded to two decimal places. GLM-5.3-Flash reports the first execution round.

| Model | Harness | Overall | Deliverable | Procedure | Restraint |
| --- | --- | ---: | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 52.97% | 55.30% | 47.94% | 49.73% |
| Claude Opus 5 | Claude Code | 53.06% | 53.61% | 51.90% | 55.71% |
| GPT-5.6 Luna | Codex | 48.82% | 51.60% | 39.34% | 50.38% |
| GPT-5.6 Luna | Claude Code | 49.26% | 50.92% | 42.13% | 51.81% |
| Grok 4.5 | Codex | 40.65% | 44.69% | 28.95% | 35.72% |
| Grok 4.5 | Claude Code | 42.13% | 44.50% | 34.35% | 41.70% |
| GLM-5.3-Flash | Claude Code | 57.59% | 59.07% | 54.98% | 58.26% |

[Download the displayed configuration scores as CSV](results/configuration_scores.csv)

- **Overall:** satisfaction of all assessed skill requirements.
- **Deliverable:** required content, format, and coverage of the output.
- **Procedure:** required steps, supporting evidence, and tool use.
- **Restraint:** prohibitions, scope limits, and stopping requirements.

<details>
<summary><strong>View all nine requirement subcategories</strong></summary>

### Deliverable

| Model | Harness | Content | Format | Coverage |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.28% | 58.08% | 50.18% |
| Claude Opus 5 | Claude Code | 54.09% | 55.69% | 53.83% |
| GPT-5.6 Luna | Codex | 52.03% | 50.33% | 50.89% |
| GPT-5.6 Luna | Claude Code | 51.52% | 46.18% | 48.20% |
| Grok 4.5 | Codex | 43.20% | 48.61% | 34.86% |
| Grok 4.5 | Claude Code | 42.91% | 43.34% | 41.48% |
| GLM-5.3-Flash | Claude Code | 59.15% | 60.50% | 65.28% |

### Procedure

| Model | Harness | Step | Evidence | Tool |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 41.95% | 50.06% | 44.44% |
| Claude Opus 5 | Claude Code | 52.22% | 50.70% | 47.47% |
| GPT-5.6 Luna | Codex | 37.38% | 35.79% | 35.35% |
| GPT-5.6 Luna | Claude Code | 39.24% | 39.75% | 49.49% |
| Grok 4.5 | Codex | 31.00% | 19.96% | 34.34% |
| Grok 4.5 | Claude Code | 37.11% | 17.71% | 35.35% |
| GLM-5.3-Flash | Claude Code | 48.83% | 53.48% | 55.05% |

### Restraint

| Model | Harness | Negative | Boundary | Termination |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.86% | 43.96% | 42.65% |
| Claude Opus 5 | Claude Code | 60.65% | 43.60% | 54.41% |
| GPT-5.6 Luna | Codex | 56.57% | 49.40% | 38.24% |
| GPT-5.6 Luna | Claude Code | 59.02% | 48.19% | 30.88% |
| Grok 4.5 | Codex | 44.08% | 19.32% | 30.88% |
| Grok 4.5 | Claude Code | 45.92% | 32.61% | 39.71% |
| GLM-5.3-Flash | Claude Code | 68.95% | 48.55% | 52.94% |

</details>

## Evaluation setting

The seven displayed configurations use the same 96 skill–task pairs, with one scored execution per pair. Claude Opus 5, GPT-5.6 Luna, and Grok 4.5 are each evaluated under Codex and Claude Code. GLM-5.3-Flash is evaluated under Claude Code; its scores here use only the first of three independent execution rounds.

Deterministic checks and LLM judgments evaluate individual requirements using execution evidence. For each configuration, scores are calculated within each skill and then averaged across skills. Each category or subcategory includes the skills with assessed requirements of that type. **Overall is calculated from all assessed requirements; it is not the average of the three category scores.** These are adherence scores, with task success evaluated separately.

## Repository contents

- [`complex-skills/`](complex-skills/): skill packages and associated task and scoring specifications.
- [`runner_core.py`](runner_core.py) and [`runner_retrigger.py`](runner_retrigger.py): execution utilities.
- [`judge.py`](judge.py): reference judging implementation.
- [`results/configuration_scores.csv`](results/configuration_scores.csv): the seven displayed configurations and all 13 adherence scores, stored as numeric percentages on a 0–100 scale.
