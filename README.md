# Agent Skill Evaluation

This repository contains skill packages, execution utilities, and evaluation results for adherence to skill requirements. The evaluation covers deliverables, procedures, and limits on agent behavior.

## Benchmark results

Results for six selected configurations are shown below. All scores are percentages, reported to one decimal place.

| Model | Harness | Overall | Deliverable | Procedure | Restraint |
| --- | --- | ---: | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 53.0% | 55.3% | 47.9% | 49.7% |
| Claude Opus 5 | Claude Code | 53.1% | 53.6% | 51.9% | 55.7% |
| GPT-5.6 Luna | Codex | 48.8% | 51.6% | 39.3% | 50.4% |
| GPT-5.6 Luna | Claude Code | 49.3% | 50.9% | 42.1% | 51.8% |
| Grok 4.5 | Codex | 40.7% | 44.7% | 29.0% | 35.7% |
| Grok 4.5 | Claude Code | 42.1% | 44.5% | 34.4% | 41.7% |

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
| Claude Opus 5 | Codex | 56.3% | 58.1% | 50.2% |
| Claude Opus 5 | Claude Code | 54.1% | 55.7% | 53.8% |
| GPT-5.6 Luna | Codex | 52.0% | 50.3% | 50.9% |
| GPT-5.6 Luna | Claude Code | 51.5% | 46.2% | 48.2% |
| Grok 4.5 | Codex | 43.2% | 48.6% | 34.9% |
| Grok 4.5 | Claude Code | 42.9% | 43.3% | 41.5% |

### Procedure

| Model | Harness | Step | Evidence | Tool |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 42.0% | 50.1% | 44.4% |
| Claude Opus 5 | Claude Code | 52.2% | 50.7% | 47.5% |
| GPT-5.6 Luna | Codex | 37.4% | 35.8% | 35.4% |
| GPT-5.6 Luna | Claude Code | 39.2% | 39.8% | 49.5% |
| Grok 4.5 | Codex | 31.0% | 20.0% | 34.3% |
| Grok 4.5 | Claude Code | 37.1% | 17.7% | 35.4% |

### Restraint

| Model | Harness | Negative | Boundary | Termination |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.9% | 44.0% | 42.7% |
| Claude Opus 5 | Claude Code | 60.7% | 43.6% | 54.4% |
| GPT-5.6 Luna | Codex | 56.6% | 49.4% | 38.2% |
| GPT-5.6 Luna | Claude Code | 59.0% | 48.2% | 30.9% |
| Grok 4.5 | Codex | 44.1% | 19.3% | 30.9% |
| Grok 4.5 | Claude Code | 45.9% | 32.6% | 39.7% |

</details>

## Evaluation setting

The six displayed configurations use the same 96 skill–task pairs, with one scored execution per pair. Claude Opus 5, GPT-5.6 Luna, and Grok 4.5 are each evaluated under Codex and Claude Code.

Deterministic checks and LLM judgments evaluate individual requirements using execution evidence. For each configuration, scores are calculated within each skill and then averaged across skills. Each category or subcategory includes the skills with assessed requirements of that type. **Overall is calculated from all assessed requirements; it is not the average of the three category scores.** These are adherence scores, with task success evaluated separately.

## Repository contents

- [`complex-skills/`](complex-skills/): skill packages and associated task and scoring specifications.
- [`runner_core.py`](runner_core.py) and [`runner_retrigger.py`](runner_retrigger.py): execution utilities.
- [`judge.py`](judge.py): reference judging implementation.
- [`results/configuration_scores.csv`](results/configuration_scores.csv): the six displayed configurations and all 13 adherence scores, stored as numeric percentages on a 0–100 scale.
