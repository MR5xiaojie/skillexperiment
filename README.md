# SkillIF: Do Agents Follow Their Skills?

SkillIF evaluates whether agents follow the requirements in supplied skill specifications, separately from whether they complete the task. Requirements cover the deliverable, the procedure used to produce it, and the limits on agent behavior.

**96 skills · 10 domains · 2,194 constraints · 11 model and harness configurations**

## Benchmark results

The scores below reproduce the main results table in *SkillIF: Do Agents Follow Their Skills?*. All scores are percentages, rounded to one decimal place as in the paper. Rows follow the paper's configuration order.

| Model | Harness | Overall | Deliverable | Procedure | Restraint |
| --- | --- | ---: | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 53.0% | 55.3% | 47.9% | 49.7% |
| Claude Opus 5 | Claude Code | 53.1% | 53.6% | 51.9% | 55.7% |
| DeepSeek V4 Flash | Codex | 48.7% | 48.9% | 48.2% | 53.3% |
| DeepSeek V4 Flash | Claude Code | 54.7% | 56.1% | 48.4% | 54.4% |
| GLM 5.2 | Codex | 54.3% | 57.4% | 43.8% | 53.4% |
| GLM 5.2 | Claude Code | 53.3% | 56.2% | 44.6% | 54.3% |
| GPT-5.6 Luna | Codex | 48.8% | 51.6% | 39.3% | 50.4% |
| GPT-5.6 Luna | Claude Code | 49.3% | 50.9% | 42.1% | 51.8% |
| Grok 4.5 | Codex | 40.7% | 44.7% | 29.0% | 35.7% |
| Grok 4.5 | Claude Code | 42.1% | 44.5% | 34.4% | 41.7% |
| Qwen3.8-Max | Claude Code | 54.0% | 55.5% | 51.0% | 52.1% |

[Download all configuration scores as CSV](results/configuration_scores.csv)

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
| DeepSeek V4 Flash | Codex | 50.1% | 50.8% | 62.4% |
| DeepSeek V4 Flash | Claude Code | 55.9% | 62.1% | 52.5% |
| GLM 5.2 | Codex | 60.2% | 52.4% | 59.4% |
| GLM 5.2 | Claude Code | 56.8% | 58.3% | 52.7% |
| GPT-5.6 Luna | Codex | 52.0% | 50.3% | 50.9% |
| GPT-5.6 Luna | Claude Code | 51.5% | 46.2% | 48.2% |
| Grok 4.5 | Codex | 43.2% | 48.6% | 34.9% |
| Grok 4.5 | Claude Code | 42.9% | 43.3% | 41.5% |
| Qwen3.8-Max | Claude Code | 57.7% | 54.2% | 57.1% |

### Procedure

| Model | Harness | Step | Evidence | Tool |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 42.0% | 50.1% | 44.4% |
| Claude Opus 5 | Claude Code | 52.2% | 50.7% | 47.5% |
| DeepSeek V4 Flash | Codex | 49.3% | 35.7% | 43.9% |
| DeepSeek V4 Flash | Claude Code | 44.2% | 46.0% | 55.1% |
| GLM 5.2 | Codex | 42.1% | 45.5% | 44.4% |
| GLM 5.2 | Claude Code | 43.1% | 38.9% | 45.0% |
| GPT-5.6 Luna | Codex | 37.4% | 35.8% | 35.4% |
| GPT-5.6 Luna | Claude Code | 39.2% | 39.8% | 49.5% |
| Grok 4.5 | Codex | 31.0% | 20.0% | 34.3% |
| Grok 4.5 | Claude Code | 37.1% | 17.7% | 35.4% |
| Qwen3.8-Max | Claude Code | 47.7% | 48.3% | 56.6% |

### Restraint

| Model | Harness | Negative | Boundary | Termination |
| --- | --- | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.9% | 44.0% | 42.7% |
| Claude Opus 5 | Claude Code | 60.7% | 43.6% | 54.4% |
| DeepSeek V4 Flash | Codex | 60.6% | 43.5% | 48.5% |
| DeepSeek V4 Flash | Claude Code | 62.2% | 48.6% | 45.6% |
| GLM 5.2 | Codex | 58.4% | 50.1% | 42.7% |
| GLM 5.2 | Claude Code | 56.0% | 52.3% | 52.9% |
| GPT-5.6 Luna | Codex | 56.6% | 49.4% | 38.2% |
| GPT-5.6 Luna | Claude Code | 59.0% | 48.2% | 30.9% |
| Grok 4.5 | Codex | 44.1% | 19.3% | 30.9% |
| Grok 4.5 | Claude Code | 45.9% | 32.6% | 39.7% |
| Qwen3.8-Max | Claude Code | 57.4% | 49.4% | 45.6% |

</details>

## Evaluation setting

Each configuration uses the same 96 skill–task pairs, with one scored execution per pair: **1,056 executions** in total. Five models are evaluated under both Codex and Claude Code; Qwen3.8-Max is evaluated only under Claude Code.

The reported scores use the primary evaluation with DeepSeek V4 Flash as the LLM judge, from the first of three judging passes over the same execution records. Deterministic checks and LLM judgments evaluate individual requirements using execution evidence.

For each configuration, scores are calculated within each skill and then averaged across skills. Each category or subcategory includes the skills with assessed requirements of that type. **Overall is calculated from all assessed requirements; it is not the average of the three category scores.** These are adherence scores, with task success evaluated separately.

## Repository contents

- [`complex-skills/`](complex-skills/): skill packages and associated task and scoring specifications.
- [`runner_core.py`](runner_core.py) and [`runner_retrigger.py`](runner_retrigger.py): execution utilities.
- [`judge.py`](judge.py): reference judging implementation.
- [`results/configuration_scores.csv`](results/configuration_scores.csv): the 11 configurations and all 13 reported adherence scores, stored as numeric percentages on a 0–100 scale.
