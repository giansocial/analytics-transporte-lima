import logging
import pandas as pd

log = logging.getLogger(__name__)


def clean_transport_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    col_map = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=col_map)

    for col in ["anio", "mes"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df = df.dropna(subset=[col])
            df[col] = df[col].astype(int)

    if "pasajeros" in df.columns:
        df["pasajeros"] = (
            df["pasajeros"].astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["pasajeros"] = pd.to_numeric(df["pasajeros"], errors="coerce")
        df = df.dropna(subset=["pasajeros"])
        df["pasajeros"] = df["pasajeros"].astype(int)

    if "sistema" in df.columns:
        df["sistema"] = df["sistema"].str.strip()

    before = len(df)
    df = df.drop_duplicates()
    dupes = before - len(df)
    if dupes > 0:
        log.info("eliminados %d duplicados", dupes)

    return df.reset_index(drop=True)


def add_period(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "anio" in df.columns and "mes" in df.columns:
        df["periodo"] = df["anio"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2)
    return df
