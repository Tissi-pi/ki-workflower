from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
DATA = ROOT / "data" / "measurements.csv"
EXPECTED = ROOT / "expected" / "text_report.txt"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BaselineTests(unittest.TestCase):
    def run_app(self, source: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(APP), str(source)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_existing_text_output_is_exact(self) -> None:
        result = self.run_app(DATA)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, EXPECTED.read_text(encoding="utf-8"))

    def test_all_source_rows_are_present_and_ordered(self) -> None:
        result = self.run_app(DATA)
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith("2026-09-18T10:15:30+02:00"))
        self.assertTrue(lines[-1].startswith("2026-09-18T10:18:30+02:00"))

    def test_source_file_remains_unchanged(self) -> None:
        before = sha256(DATA)
        result = self.run_app(DATA)
        after = sha256(DATA)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, after)

    def test_invalid_decimal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.csv"
            bad.write_text(
                "timestamp,value,unit\n"
                "2026-09-18T10:15:30+02:00,not-a-number,°C\n",
                encoding="utf-8",
            )
            result = self.run_app(bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ungültiger Messwert", result.stderr)

    def test_invalid_timestamp_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.csv"
            bad.write_text(
                "timestamp,value,unit\n"
                "kein-zeitstempel,12.3400,°C\n",
                encoding="utf-8",
            )
            result = self.run_app(bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ungültiger Zeitstempel", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
