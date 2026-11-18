"""Regression checks for malformed input and the non-writing verification mode."""

import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

import build_site_data as builder


def csv_bytes(rows, header=builder.COLUMNS):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


class SiteDataTests(unittest.TestCase):
    def setUp(self):
        self.row = ["Example Model", "Example Harness", *("50.00" for _ in range(9))]

    def test_preserves_source_rows_scores_and_csv(self):
        source = builder.SOURCE.read_bytes()
        artifacts = builder.build_artifacts(source)
        data = json.loads(artifacts["scores.json"])
        expected = list(csv.DictReader(io.StringIO(source.decode("utf-8-sig"))))
        self.assertEqual(len(data["configurations"]), len(expected))
        self.assertEqual([metric["key"] for metric in data["metrics"]], list(builder.COLUMNS[2:]))
        for actual, row in zip(data["configurations"], expected):
            self.assertEqual(set(actual), set(builder.COLUMNS))
            self.assertEqual((actual["model"], actual["harness"]), (row["model"], row["harness"]))
            for key in builder.COLUMNS[2:]:
                self.assertEqual(f"{actual[key]:.2f}", row[key])
        self.assertEqual(artifacts["configuration_scores.csv"], source)

    def test_rejects_extra_missing_repeated_and_reordered_columns(self):
        for header in (
            (*builder.COLUMNS, "extra"), builder.COLUMNS[:-1],
            (*builder.COLUMNS[:-1], "content"), tuple(reversed(builder.COLUMNS)),
        ):
            with self.subTest(header=header), self.assertRaisesRegex(ValueError, "header"):
                builder.parse_scores(csv_bytes([self.row], header))

    def test_rejects_duplicates_missing_cells_and_empty_configuration_names(self):
        for rows in (
            [self.row, self.row], [self.row[:-1]], [self.row + ["10.00"]],
            [["", *self.row[1:]]], [[self.row[0], "  ", *self.row[2:]]],
            [[" Example Model", *self.row[1:]]], [],
        ):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                builder.parse_scores(csv_bytes(rows))

    def test_rejects_nonfinite_out_of_range_and_inexact_scores(self):
        for value in ("NaN", "Infinity", "-0.01", "100.01", "500.00", "50", "50.0", "50.000", "1e1", " 50.00", ""):
            row = self.row.copy()
            row[2] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "two decimal places"):
                builder.parse_scores(csv_bytes([row]))

    def test_accepts_range_endpoints(self):
        self.row[2:4] = ["0.00", "100.00"]
        row = builder.parse_scores(csv_bytes([self.row]))[0]
        self.assertEqual((row["content"], row["format"]), (0.0, 100.0))

    def test_check_does_not_create_or_repair_files(self):
        artifacts = builder.build_artifacts(csv_bytes([self.row]))
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "data"
            self.assertEqual(set(builder.synchronize(output, artifacts, check=True)), set(artifacts))
            self.assertFalse(output.exists())
            builder.synchronize(output, artifacts, check=False)
            self.assertEqual(builder.synchronize(output, artifacts, check=True), [])
            destination = output / "scores.json"
            destination.write_bytes(b"stale\n")
            original_time = destination.stat().st_mtime_ns
            self.assertEqual(builder.synchronize(output, artifacts, check=True), ["scores.json"])
            self.assertEqual(destination.read_bytes(), b"stale\n")
            self.assertEqual(destination.stat().st_mtime_ns, original_time)

    def test_check_accepts_checkout_line_endings(self):
        artifacts = builder.build_artifacts(csv_bytes([self.row]))
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for name, value in artifacts.items():
                (output / name).write_bytes(value.replace(b"\n", b"\r\n"))
            self.assertEqual(builder.synchronize(output, artifacts, check=True), [])


if __name__ == "__main__":
    unittest.main()
