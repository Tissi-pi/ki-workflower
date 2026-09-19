from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
DATA = ROOT / "data" / "measurements.csv"
EXPECTED_JSON = ROOT / "expected" / "json_report.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_app_module():
    spec = importlib.util.spec_from_file_location("demo_app", APP)
    if spec is None or spec.loader is None:
        raise RuntimeError("app.py konnte nicht geladen werden")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class JsonExportTests(unittest.TestCase):
    def run_json_export(
        self,
        source: Path,
        target: Path,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(APP), str(source), "--json", str(target)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def test_json_output_matches_reference_byte_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            result = self.run_json_export(DATA, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), EXPECTED_JSON.read_bytes())

    def test_json_is_valid_complete_and_ordered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            result = self.run_json_export(DATA, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(target.read_text(encoding="utf-8"))

        rows = payload["measurements"]
        self.assertEqual(len(rows), 4)
        self.assertEqual(
            [r["timestamp"] for r in rows],
            [
                "2026-09-18T10:15:30+02:00",
                "2026-09-18T10:16:30+02:00",
                "2026-09-18T10:17:30+02:00",
                "2026-09-18T10:18:30+02:00",
            ],
        )

    def test_decimal_representation_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            result = self.run_json_export(DATA, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(target.read_text(encoding="utf-8"))["measurements"]

        self.assertEqual(
            [r["value"] for r in rows],
            [
                "12.3400",
                "0.1",
                "123456.789012",
                "0.100000000000000005",
            ],
        )

    def test_timestamp_and_offset_text_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            result = self.run_json_export(DATA, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(target.read_text(encoding="utf-8"))["measurements"]

        for row in rows:
            self.assertRegex(row["timestamp"], r"\+02:00$")

    def test_source_file_remains_unchanged_during_json_export(self) -> None:
        before = sha256(DATA)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            result = self.run_json_export(DATA, target)
        after = sha256(DATA)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, after)

    def test_invalid_record_json_export_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bad = tmp_path / "bad.csv"
            target = tmp_path / "report.json"
            bad.write_text(
                "timestamp,value,unit\n"
                "2026-09-18T10:15:30+02:00,not-a-number,°C\n",
                encoding="utf-8",
            )

            result = self.run_json_export(bad, target)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Ungültiger Messwert", result.stderr)
            self.assertFalse(target.exists())

    def test_failed_atomic_replace_is_not_reported_as_success(self) -> None:
        module = load_app_module()

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.json"
            original = b"ORIGINAL\n"
            target.write_bytes(original)

            stderr = io.StringIO()
            with mock.patch.object(
                module,
                "replace",
                side_effect=OSError("simulierter atomarer Austauschfehler"),
            ):
                with contextlib.redirect_stderr(stderr):
                    rc = module.main(
                        [
                            str(APP),
                            str(DATA),
                            "--json",
                            str(target),
                        ]
                    )

            self.assertNotEqual(rc, 0)
            self.assertEqual(target.read_bytes(), original)
            self.assertIn("simulierter atomarer Austauschfehler", stderr.getvalue())
            leftovers = list(Path(tmp).glob(".report.json.*.tmp"))
            self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
