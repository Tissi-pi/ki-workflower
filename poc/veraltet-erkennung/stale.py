#!/usr/bin/env python3
"""Veraltet-Erkennung (Machbarkeitsversuch, kein 2.7-Stand).

    stale.py bind   <wurzel> <dateiliste> <nachweis.json>
    stale.py verify <wurzel> <nachweis.json>

bind bindet einen Nachweis an die SHA-256-Summen der in <dateiliste> genannten
Dateien. verify meldet "OK" nur, wenn genau dieser Bestand unverändert ist.
Exit-Codes: 0 = in Ordnung, 1 = abgelehnt (VERALTET / NACHWEIS UNGÜLTIG /
FEHLER), 2 = falscher Aufruf.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from os import fsync, replace
from pathlib import Path, PurePosixPath

HASH_PATTERN = re.compile(r"[0-9a-f]{64}")


class Rejected(Exception):
    """Abgelehnt; text beginnt mit der Marke (VERALTET, NACHWEIS UNGÜLTIG, FEHLER)."""


def safe_relative(name: str) -> str:
    # Nur relative Pfade ohne ".." – der Nachweis darf nicht aus der Wurzel zeigen.
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(name)
    return path.as_posix()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text_atomic(target: Path, content: str) -> None:
    # Wie in der Demo: temporäre Datei im Zielverzeichnis, dann atomar ersetzen.
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=target.parent,
            prefix=f".{target.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            fsync(handle.fileno())
        replace(temp_path, target)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def bind(root: Path, listing: Path, evidence: Path) -> None:
    if not root.is_dir():
        raise Rejected(f"FEHLER: Wurzelverzeichnis existiert nicht: {root}")
    try:
        names = [line.strip() for line in listing.read_text(encoding="utf-8").splitlines()]
    except (OSError, UnicodeDecodeError) as exc:
        raise Rejected(f"FEHLER: Dateiliste nicht lesbar: {exc}") from exc

    files: dict[str, str] = {}
    for name in filter(None, names):
        try:
            rel = safe_relative(name)
        except ValueError:
            raise Rejected(f"FEHLER: Ungültiger Pfad in der Dateiliste: {name}") from None
        path = root / rel
        if path.is_symlink() or not path.is_file():
            raise Rejected(f"FEHLER: Keine reguläre Datei: {rel}")
        try:
            files[rel] = file_sha256(path)
        except OSError as exc:
            raise Rejected(f"FEHLER: {rel} nicht lesbar: {exc}") from exc
    if not files:
        raise Rejected("FEHLER: Die Dateiliste enthält keine Einträge")

    # Erst nach erfolgreicher Berechnung schreiben: bei Fehler bleibt kein Nachweis zurück.
    payload = json.dumps({"files": files}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        write_text_atomic(evidence, payload)
    except OSError as exc:
        raise Rejected(f"FEHLER: Nachweis nicht schreibbar: {exc}") from exc


def load_evidence(evidence: Path) -> dict[str, str]:
    try:
        data = json.loads(evidence.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise Rejected(f"NACHWEIS UNGÜLTIG: nicht lesbar oder kein JSON ({exc})") from exc
    files = data.get("files") if isinstance(data, dict) else None
    if not isinstance(files, dict) or not files:
        raise Rejected("NACHWEIS UNGÜLTIG: Struktur entspricht nicht dem Format")
    for name, digest in files.items():
        try:
            safe_relative(name)
        except ValueError:
            raise Rejected(f"NACHWEIS UNGÜLTIG: unzulässiger Pfad {name!r}") from None
        if not isinstance(digest, str) or not HASH_PATTERN.fullmatch(digest):
            raise Rejected(f"NACHWEIS UNGÜLTIG: keine gültige Prüfsumme für {name}")
    return files


def verify(root: Path, evidence: Path) -> None:
    if not root.is_dir():
        raise Rejected(f"FEHLER: Wurzelverzeichnis existiert nicht: {root}")
    bound = load_evidence(evidence)

    changed: list[str] = []
    for name, expected in sorted(bound.items()):
        path = root / name
        if path.is_symlink() or not path.is_file():
            changed.append(f"{name} (fehlt oder ist keine reguläre Datei)")
            continue
        try:
            actual = file_sha256(path)
        except OSError as exc:
            raise Rejected(f"FEHLER: {name} nicht lesbar: {exc}") from exc
        if actual != expected:
            changed.append(f"{name} (Inhalt geändert)")
    if changed:
        raise Rejected("VERALTET: " + "; ".join(changed))


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 5 and argv[1] == "bind":
            bind(Path(argv[2]), Path(argv[3]), Path(argv[4]))
            print("OK: Nachweis gebunden")
        elif len(argv) == 4 and argv[1] == "verify":
            verify(Path(argv[2]), Path(argv[3]))
            print("OK")
        else:
            print(
                f"Aufruf: {Path(argv[0]).name} bind <wurzel> <dateiliste> <nachweis.json>\n"
                f"        {Path(argv[0]).name} verify <wurzel> <nachweis.json>",
                file=sys.stderr,
            )
            return 2
    except Rejected as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
