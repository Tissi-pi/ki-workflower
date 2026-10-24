"""Prüfziele T1-T6 für die Veraltet-Erkennung (Machbarkeitsversuch, kein 2.7-Stand).

Schnittstelle, gegen die getestet wird (noch nicht umgesetzt):

    stale.py bind   <wurzel> <dateiliste> <nachweis.json>
    stale.py verify <wurzel> <nachweis.json>

- <dateiliste>: Textdatei, ein relativer Pfad je Zeile = gebundener Bestand.
- bind schreibt den Nachweis (Pfad -> SHA-256) und endet mit Exit-Code 0.
- verify endet mit Exit-Code 0 und der Ausgabe "OK", wenn der gebundene Bestand
  unverändert ist; sonst mit Exit-Code != 0 und einer der Marken
  "VERALTET", "NACHWEIS UNGÜLTIG" oder "FEHLER" (stdout oder stderr).

Jeder Negativtest führt zuerst ein erfolgreiches bind aus. Fehlt die Umsetzung,
scheitert er damit schon im Aufbau und kann nicht zufällig grün werden.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STALE = Path(__file__).resolve().parents[1] / "stale.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(STALE), *args],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )


def output(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


class StaleDetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        base = Path(self._tmp.name)
        self.root = base / "projekt"
        self.root.mkdir()
        (self.root / "a.txt").write_text("alpha\n", encoding="utf-8")
        (self.root / "b.txt").write_text("beta\n", encoding="utf-8")
        (self.root / "ausserhalb.txt").write_text("frei\n", encoding="utf-8")
        self.listing = base / "bestand.txt"
        self.listing.write_text("a.txt\nb.txt\n", encoding="utf-8")
        self.evidence = base / "nachweis.json"

    def bind(self) -> None:
        result = run("bind", str(self.root), str(self.listing), str(self.evidence))
        self.assertEqual(result.returncode, 0, output(result))
        self.assertTrue(self.evidence.exists(), "bind hat keinen Nachweis geschrieben")

    def verify(self) -> subprocess.CompletedProcess[str]:
        return run("verify", str(self.root), str(self.evidence))

    def assert_rejected(self, result: subprocess.CompletedProcess[str], marker: str) -> None:
        self.assertNotEqual(result.returncode, 0, output(result))
        self.assertIn(marker, output(result))
        self.assertNotIn("OK", result.stdout)

    def test_t1_unchanged_state_is_accepted(self) -> None:
        self.bind()
        result = self.verify()
        self.assertEqual(result.returncode, 0, output(result))
        self.assertIn("OK", result.stdout)

    def test_t2_changed_bound_file_is_stale(self) -> None:
        self.bind()
        (self.root / "a.txt").write_text("alpha geaendert\n", encoding="utf-8")
        self.assert_rejected(self.verify(), "VERALTET")

    def test_t3_added_or_removed_bound_file_is_stale(self) -> None:
        with self.subTest(fall="entfernt"):
            self.bind()
            (self.root / "b.txt").unlink()
            self.assert_rejected(self.verify(), "VERALTET")
        with self.subTest(fall="hinzugefuegt"):
            (self.root / "b.txt").write_text("beta\n", encoding="utf-8")
            self.listing.write_text("a.txt\nb.txt\nc.txt\n", encoding="utf-8")
            (self.root / "c.txt").write_text("gamma\n", encoding="utf-8")
            self.bind()
            (self.root / "c.txt").unlink()
            self.assert_rejected(self.verify(), "VERALTET")

    def test_t4_change_outside_bound_set_is_accepted(self) -> None:
        self.bind()
        (self.root / "ausserhalb.txt").write_text("frei geaendert\n", encoding="utf-8")
        (self.root / "neu.txt").write_text("neu\n", encoding="utf-8")
        result = self.verify()
        self.assertEqual(result.returncode, 0, output(result))
        self.assertIn("OK", result.stdout)

    def test_t5_damaged_or_missing_evidence_is_rejected(self) -> None:
        self.bind()
        original = self.evidence.read_bytes()
        with self.subTest(fall="kein JSON"):
            self.evidence.write_text("das ist kein json", encoding="utf-8")
            self.assert_rejected(self.verify(), "NACHWEIS UNGÜLTIG")
        with self.subTest(fall="leere Datei"):
            self.evidence.write_bytes(b"")
            self.assert_rejected(self.verify(), "NACHWEIS UNGÜLTIG")
        with self.subTest(fall="falsche Struktur"):
            self.evidence.write_text('{"unerwartet": 1}', encoding="utf-8")
            self.assert_rejected(self.verify(), "NACHWEIS UNGÜLTIG")
        with self.subTest(fall="Nachweis fehlt"):
            self.evidence.unlink()
            self.assert_rejected(self.verify(), "NACHWEIS UNGÜLTIG")
        with self.subTest(fall="Original wiederhergestellt"):
            self.evidence.write_bytes(original)
            result = self.verify()
            self.assertEqual(result.returncode, 0, output(result))

    def test_t6_internal_failure_is_never_reported_as_success(self) -> None:
        self.bind()
        with self.subTest(fall="gebundene Datei ist plötzlich ein Verzeichnis"):
            (self.root / "a.txt").unlink()
            (self.root / "a.txt").mkdir()
            result = self.verify()
            self.assertNotEqual(result.returncode, 0, output(result))
            self.assertNotIn("OK", result.stdout)
        with self.subTest(fall="Wurzelverzeichnis existiert nicht"):
            result = run("verify", str(self.root / "gibt-es-nicht"), str(self.evidence))
            self.assert_rejected(result, "FEHLER")
        with self.subTest(fall="bind mit nicht vorhandener Datei in der Liste"):
            self.listing.write_text("a.txt\nfehlt.txt\n", encoding="utf-8")
            other = self.evidence.with_name("nachweis2.json")
            result = run("bind", str(self.root), str(self.listing), str(other))
            self.assertNotEqual(result.returncode, 0, output(result))
            self.assertFalse(other.exists(), "bind darf bei Fehler keinen Nachweis hinterlassen")


if __name__ == "__main__":
    unittest.main(verbosity=2)
