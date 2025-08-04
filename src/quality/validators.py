import logging
import pandas as pd

log = logging.getLogger(__name__)


def check_completeness(df: pd.DataFrame, cols: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 0.0, "detalles": {}}
    det = {}
    for c in cols:
        if c in df.columns:
            det[c] = round((1 - df[c].isnull().sum() / total) * 100, 1)
        else:
            det[c] = 0.0
    return {"score": round(sum(det.values()) / len(det), 1), "detalles": det}


def check_uniqueness(df: pd.DataFrame, keys: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 100.0, "duplicados": 0}
    dupes = df.duplicated(subset=keys).sum()
    return {"score": round((1 - dupes / total) * 100, 1), "duplicados": int(dupes)}


def run_quality_report(df: pd.DataFrame) -> dict:
    required = ["sistema", "anio", "mes", "pasajeros"]
    comp = check_completeness(df, required)
    uniq = check_uniqueness(df, ["sistema", "anio", "mes"])
    total = comp["score"] * 0.5 + uniq["score"] * 0.5
    report = {
        "score_total": round(total, 1),
        "completitud": comp,
        "unicidad": uniq,
        "filas": len(df),
    }
    log.info("calidad: %.1f%%", total)
    return report
