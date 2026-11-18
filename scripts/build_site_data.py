#!/usr/bin/env python3
"""Validate the score CSV and regenerate the static site's data using only Python.

Run this script from any directory. --check reports invalid or stale data without
writing files. Edit results/configuration_scores.csv, then run without --check.
"""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import io
import json
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "results" / "configuration_scores.csv"
OUTPUT_DIR = REPO_ROOT / "docs" / "data"
METRICS = (
    ("content", "Content", "Does the output include the required information?"),
    ("format", "Format", "Does it use the requested structure and presentation?"),
    ("coverage", "Coverage", "Does it address all the required items?"),
    ("step", "Step", "Were the prescribed actions carried out in the required order?"),
    ("evidence", "Evidence", "Were sources consulted and supporting evidence provided as required?"),
    ("tool", "Tool", "Were the specified tools used as required?"),
    ("negative", "Negative", "Did the agent respect explicit prohibitions?"),
    ("boundary", "Boundary", "Did it stay within the permitted scope?"),
    ("termination", "Termination", "Did it meet the specified stopping requirements?"),
)
COLUMNS = ("model", "harness", *(metric[0] for metric in METRICS))
SCORE_PATTERN = re.compile(r"(?:0|[1-9][0-9]{0,2})\.[0-9]{2}\Z")


def parse_scores(source_bytes: bytes) -> list[dict]:
    """Reject ambiguous CSV values before any public files are written."""
    reader = csv.reader(io.StringIO(source_bytes.decode("utf-8-sig")), strict=True)
    if tuple(next(reader, ())) != COLUMNS:
        raise ValueError("CSV header must be exactly: " + ",".join(COLUMNS))

    configurations = []
    seen = set()
    for row in reader:
        line = reader.line_num
        if len(row) != len(COLUMNS):
            raise ValueError(f"Line {line}: expected {len(COLUMNS)} fields, got {len(row)}")
        model, harness = row[:2]
        if any(not value.strip() or value != value.strip() for value in (model, harness)):
            raise ValueError(f"Line {line}: model and harness must be nonempty, with no outer whitespace")
        if (model, harness) in seen:
            raise ValueError(f"Line {line}: duplicate model/harness configuration")
        seen.add((model, harness))

        configuration = {"model": model, "harness": harness}
        for key, value in zip(COLUMNS[2:], row[2:]):
            if not SCORE_PATTERN.fullmatch(value) or not Decimal("0") <= Decimal(value) <= Decimal("100"):
                raise ValueError(f"Line {line}, {key}: expected a score from 0.00 to 100.00 with two decimal places")
            configuration[key] = float(value)
        configurations.append(configuration)

    if not configurations:
        raise ValueError("CSV must contain at least one configuration")
    return configurations


def build_artifacts(source_bytes: bytes) -> dict[str, bytes]:
    configurations = parse_scores(source_bytes)
    execution_rounds = {}
    if any(row["model"] == "GLM-5.3-Flash" for row in configurations):
        execution_rounds["GLM-5.3-Flash"] = 1
    data = {
        "metrics": [dict(zip(("key", "label", "description"), metric)) for metric in METRICS],
        "configurations": configurations,
        "metadata": {"execution_rounds": execution_rounds},
    }
    return {
        "scores.json": (json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8"),
        "configuration_scores.csv": source_bytes,
    }


def synchronize(output_dir: Path, artifacts: dict[str, bytes], *, check: bool) -> list[str]:
    """Return stale filenames; check mode never creates or modifies anything."""
    stale = []
    for name, expected in artifacts.items():
        destination = output_dir / name
        # Git can change checkout line endings across platforms. Content is what
        # matters for this check; builds still copy the CSV's original bytes.
        actual = destination.read_bytes() if destination.is_file() else None
        if actual is None or actual.replace(b"\r\n", b"\n") != expected.replace(b"\r\n", b"\n"):
            stale.append(name)
        if not check:
            output_dir.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(expected)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate source data and check generated files without writing")
    args = parser.parse_args(argv)
    try:
        source_bytes = SOURCE.read_bytes()
        artifacts = build_artifacts(source_bytes)
        stale = synchronize(OUTPUT_DIR, artifacts, check=args.check)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Data validation failed: {error}", file=sys.stderr)
        return 1
    if args.check and stale:
        print("Generated files are missing or stale: " + ", ".join("docs/data/" + name for name in stale), file=sys.stderr)
        print("Run: python scripts/build_site_data.py", file=sys.stderr)
        return 1
    count = len(json.loads(artifacts["scores.json"])["configurations"])
    action = "Checked" if args.check else "Built"
    print(f"{action} site data: {count} configurations, {len(METRICS)} metrics, {count * len(METRICS)} scores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
