# Agent Skill Experiments

Imagine asking an agent to organize a folder: archive the files, delete nothing, and leave unrelated folders alone. The result might look tidy, but you would still want to know whether it followed all three instructions.

That is the idea behind this repository. We pair reusable skill packages with concrete tasks, then check the saved outputs and execution records against the instructions. The details include what belongs in the final answer, which steps need to happen along the way, and where the agent should stop.

## The scores

The table shows seven model and harness configurations, with a separate score for each of the nine requirement types.

| Model | Harness | Content | Format | Coverage | Step | Evidence | Tool | Negative | Boundary | Termination |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Claude Opus 5 | Codex | 56.28% | 58.08% | 50.18% | 41.95% | 50.06% | 44.44% | 56.86% | 43.96% | 42.65% |
| Claude Opus 5 | Claude Code | 54.09% | 55.69% | 53.83% | 52.22% | 50.70% | 47.47% | 60.65% | 43.60% | 54.41% |
| GPT-5.6 Luna | Codex | 52.03% | 50.33% | 50.89% | 37.38% | 35.79% | 35.35% | 56.57% | 49.40% | 38.24% |
| GPT-5.6 Luna | Claude Code | 51.52% | 46.18% | 48.20% | 39.24% | 39.75% | 49.49% | 59.02% | 48.19% | 30.88% |
| Grok 4.5 | Codex | 43.20% | 48.61% | 34.86% | 31.00% | 19.96% | 34.34% | 44.08% | 19.32% | 30.88% |
| Grok 4.5 | Claude Code | 42.91% | 43.34% | 41.48% | 37.11% | 17.71% | 35.35% | 45.92% | 32.61% | 39.71% |
| GLM-5.3-Flash | Claude Code | 59.15% | 60.50% | 65.28% | 48.83% | 53.48% | 55.05% | 68.95% | 48.55% | 52.94% |

[Get the numbers as CSV](results/configuration_scores.csv)

<details>
<summary>What does each column mean?</summary>

| Column | What we check |
| --- | --- |
| Content | Does the output include the required information? |
| Format | Does it use the requested structure and presentation? |
| Coverage | Does it address all the required items? |
| Step | Were the prescribed actions carried out in the required order? |
| Evidence | Were sources consulted and supporting evidence provided as required? |
| Tool | Were the specified tools used as required? |
| Negative | Did the agent respect explicit prohibitions? |
| Boundary | Did it stay within the permitted scope? |
| Termination | Did it meet the specified stopping requirements? |

</details>

## Behind the numbers

The displayed configurations use the same 96 skill–task pairs. Claude Opus 5, GPT-5.6 Luna, and Grok 4.5 each run under Codex and Claude Code. The GLM-5.3-Flash entry uses Claude Code and comes from the first of three independent execution rounds. Each entry in the table represents one execution per task.

For each column, we calculate the fraction of relevant requirements satisfied within each skill, then average across the skills that have those requirements. A skill without a particular requirement type does not count as a zero. Deterministic checks and LLM judgments assess the saved execution evidence; task completion is evaluated separately.

## Start with one skill

The [capture-triage skill](complex-skills/006-capture-triage/SKILL.md) is a concrete place to start. Read its instructions alongside the [scoring rules](complex-skills/006-capture-triage/SCORING.yaml) and [checks](complex-skills/006-capture-triage/check.py) to see how individual requirements are evaluated.

For the rest of the repository:

- [`complex-skills/`](complex-skills/) contains the skill definitions, supporting resources, and scoring rules.
- [`runner_core.py`](runner_core.py) and [`runner_retrigger.py`](runner_retrigger.py) handle execution and reruns.
- [`judge.py`](judge.py) contains the reference judging implementation.
- [`results/configuration_scores.csv`](results/configuration_scores.csv) holds the nine scores for every configuration shown above.
