# Contributing

Small, specific changes are welcome: a clearer explanation, a broken link fixed, or a score that can be traced to its execution records.

## Work on the viewer

The viewer lives in `docs/` and uses plain HTML, CSS, and JavaScript. Serve it from the repository root:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory docs
```

Open `http://localhost:8000`. Check both a desktop-sized window and a narrow mobile layout. Search, harness filtering, sorting, metric selection, and CSV download should remain usable with a keyboard.

## Change results

`results/configuration_scores.csv` is the source of truth. Each row represents one model and harness configuration, followed by nine requirement scores:

```text
model,harness,content,format,coverage,step,evidence,tool,negative,boundary,termination
```

Use numeric percentages from 0 to 100, with two decimal places. Each model and harness pair must be unique. Calculate the values from the underlying results before rounding; adding a zero to a previously rounded number does not recover its precision.

Include enough context in your pull request to explain where a result came from: the model, harness, task set, execution round, scoring procedure, and aggregation. The current GLM-5.3-Flash row uses its first execution round.

After editing the CSV, regenerate the copies used by the site:

```sh
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python -m unittest discover -s scripts -p 'test_*.py'
```

Update the README table as well. Review the generated diff to make sure the same values appear in the table, JSON, and downloadable CSV.

## Change a skill or check

Keep the skill's instructions, scoring rules, and mechanical checks consistent with one another. Describe the concrete behavior your change affects, and include a small example when it helps explain the difference.

Changes to reference code or skill packages do not automatically update the displayed scores. Explain whether a change would require a fresh execution or a new judgment of existing records.

## Report an issue

For a display problem, include the page size and the steps that produced it. For a result question, name the model, harness, and score column. A focused report makes it much easier to investigate.
