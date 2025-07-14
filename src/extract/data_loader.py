import csv
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def load_csv(filepath: Path) -> list[dict]:
    if not filepath.exists():
        raise FileNotFoundError(f"no existe: {filepath}")
    rows = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    log.info("cargadas %d filas de %s", len(rows), filepath.name)
    return rows


def load_all(raw_dir: Path) -> list[dict]:
    all_rows = []
    for f in sorted(raw_dir.glob("*.csv")):
        all_rows.extend(load_csv(f))
    if not all_rows:
        log.warning("sin datos en %s", raw_dir)
    return all_rows


def validate_schema(rows: list[dict], required: set[str]) -> dict:
    if not rows:
        return {"valid": False, "missing": list(required)}
    present = set(rows[0].keys())
    missing = required - present
    return {"valid": len(missing) == 0, "missing": sorted(missing), "rows": len(rows)}
