# Using the reference runner

The results explorer works from the checked-in CSV and needs no model access. The execution scripts are a separate starting point for connecting your own tasks, agent CLI, and judging setup.

## What the runner expects

`runner_core.py` finds a skill when its directory contains `task/task.txt`. Put the task's other input files next to that file:

```text
complex-skills/
  your-skill/
    SKILL.md
    SCORING.yaml
    check.py
    task/
      task.txt
      input-file.md
```

The runner copies those input files into a fresh working directory. This repository includes skill definitions and checks, but does not include the task input directories used for the displayed results. Supply inputs appropriate to the skill you want to run.

## Check task discovery first

From the repository root:

```sh
python runner_retrigger.py --help
python runner_retrigger.py --model YOUR_MODEL --skills 006 --dry-run
```

The second command only lists matching tasks. It does not call a model or create a result directory. Until you add task inputs, the task count is zero. Replace `006` with the prefix of the skill you are preparing, or omit `--skills` to list all available tasks.

## Connect an execution backend

The runner supports `--exec-backend claude` and `--exec-backend codex`. The corresponding CLI must be installed and authenticated. It is found on `PATH`, or through `CLAUDE_CMD` or `CODEX_CMD`.

For an execution without automatic judging, after preparing the task and CLI:

```sh
python runner_retrigger.py --exec-backend claude --model YOUR_MODEL --skills 006 --tag local-check --no-judge
```

This command runs the configured model and may incur API charges. The runner is designed for unattended tasks and launches the agent with broad tool permissions. Use an isolated working environment and supply the decisions and materials the task needs before starting it.

The runner forces the selected skill to load and instructs the agent to continue without waiting for a person. Check that your task and skill requirements fit that interaction model. A preauthorization prompt does not perform the required analysis, file reads, or verification steps for the agent.

## Add judging

`judge.py` combines mechanical checks with model judgments. In addition to Python and PyYAML, it imports `extract_evidence` from an `evidence_extractor.py` module that is not included here. Integrate a compatible extractor before using the judging entry point; installing PyYAML alone is not sufficient.

The judge reads its connection settings from `JUDGE_API_KEY`, `JUDGE_API_BASE`, and `JUDGE_API_MODEL`. The runner also accepts `--judge-model`, `--judge-api-key`, and `--judge-api-base`.

To understand a mechanical check independently, start with a skill's `check.py`. The capture-triage check accepts a workspace, a tool log, and an agent output file, then prints JSON verdicts:

```sh
python complex-skills/006-capture-triage/check.py WORKSPACE TOOL_LOG AGENT_OUTPUT
```

These are the script's component verdicts. They are not the complete combined evaluation produced by the judge.

## Keep new runs separate from the displayed data

Running the scripts creates local execution records. It does not overwrite `results/configuration_scores.csv` or change the results explorer. Aggregate and verify a new set of results before updating that file.
