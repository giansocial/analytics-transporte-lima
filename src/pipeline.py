import argparse
import json
import time

import pandas as pd

from src.config.settings import RAW_DIR, PROCESSED_DIR
from src.extract.data_loader import load_all
from src.transform.cleaner import clean_transport_data, add_period
from src.transform.enricher import add_yoy_change, system_share, seasonal_pattern, covid_recovery
from src.quality.validators import run_quality_report
from src.load.exporter import init_db, load_to_db, export_csv
from src.utils.logger import get_logger

log = get_logger(__name__)


def run_pipeline(raw_dir=None) -> dict:
    t0 = time.time()
    raw_dir = raw_dir or RAW_DIR

    rows = load_all(raw_dir)
    if not rows:
        return {"error": "sin datos"}

    df = pd.DataFrame(rows)
    df = clean_transport_data(df)
    df = add_period(df)

    quality = run_quality_report(df)
    df = add_yoy_change(df)

    conn = init_db()
    loaded = load_to_db(df, conn)
    conn.close()

    export_csv(df, PROCESSED_DIR, "pasajeros_enriquecidos")

    shares = system_share(df)
    export_csv(shares, PROCESSED_DIR, "participacion_sistema")

    seasonal = seasonal_pattern(df)
    export_csv(seasonal, PROCESSED_DIR, "estacionalidad")

    if 2020 in df["anio"].values:
        rec = covid_recovery(df)
        export_csv(rec, PROCESSED_DIR, "recuperacion_covid")

    elapsed = round(time.time() - t0, 1)
    log.info("pipeline completado en %.1fs", elapsed)

    return {
        "filas_procesadas": len(df),
        "filas_cargadas": loaded,
        "calidad_pct": quality["score_total"],
        "sistemas": sorted(df["sistema"].unique().tolist()),
        "duracion_seg": elapsed,
    }


def main():
    parser = argparse.ArgumentParser(description="Analytics transporte Lima")
    args = parser.parse_args()
    result = run_pipeline()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
