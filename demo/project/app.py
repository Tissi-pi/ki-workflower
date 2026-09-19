#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from os import fsync, replace
import sys
import tempfile
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


EXPECTED_FIELDS = ["timestamp", "value", "unit"]


def load_measurements(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames != EXPECTED_FIELDS:
            raise ValueError(
                "Ungültige CSV-Struktur: erwartet "
                + ",".join(EXPECTED_FIELDS)
            )

        for line_no, row in enumerate(reader, start=2):
            timestamp = row["timestamp"]
            value_text = row["value"]
            unit = row["unit"]

            try:
                datetime.fromisoformat(timestamp)
            except ValueError as exc:
                raise ValueError(
                    f"Ungültiger Zeitstempel in Zeile {line_no}: {timestamp}"
                ) from exc

            try:
                Decimal(value_text)
            except InvalidOperation as exc:
                raise ValueError(
                    f"Ungültiger Messwert in Zeile {line_no}: {value_text}"
                ) from exc

            rows.append(
                {
                    "timestamp": timestamp,
                    "value": value_text,
                    "unit": unit,
                }
            )

    return rows


def render_text_report(rows: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{row['timestamp']} | {row['value']} {row['unit']}"
        for row in rows
    ) + "\n"


def render_json_report(rows: list[dict[str, str]]) -> str:
    payload = {
        "measurements": [
            {
                "timestamp": row["timestamp"],
                # Bewusst String: die im PoC geforderte Dezimaldarstellung
                # bleibt dadurch ohne float-Konvertierung erhalten.
                "value": row["value"],
                "unit": row["unit"],
            }
            for row in rows
        ]
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def write_text_atomic(target: Path, content: str) -> None:
    parent = target.parent
    if not parent.is_dir():
        raise OSError(f"Zielverzeichnis existiert nicht: {parent}")

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            fsync(handle.fileno())

        replace(temp_path, target)
        temp_path = None
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        source = Path(argv[1])
        mode = "text"
        target = None
    elif len(argv) == 4 and argv[2] == "--json":
        source = Path(argv[1])
        mode = "json"
        target = Path(argv[3])
    else:
        print(
            f"Aufruf: {Path(argv[0]).name} <messdaten.csv> "
            "[--json <ziel.json>]",
            file=sys.stderr,
        )
        return 2

    try:
        rows = load_measurements(source)

        if mode == "text":
            sys.stdout.write(render_text_report(rows))
        else:
            assert target is not None
            write_text_atomic(target, render_json_report(rows))
    except (OSError, ValueError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
