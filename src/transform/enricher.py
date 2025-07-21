import pandas as pd
import numpy as np


def add_yoy_change(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["sistema", "anio", "mes"])
    df["pas_anterior"] = df.groupby(["sistema", "mes"])["pasajeros"].shift(1)
    mask = df["pas_anterior"] > 0
    df.loc[mask, "var_yoy_pct"] = (
        (df.loc[mask, "pasajeros"] - df.loc[mask, "pas_anterior"])
        / df.loc[mask, "pas_anterior"] * 100
    ).round(2)
    df = df.drop(columns=["pas_anterior"])
    return df


def system_share(df: pd.DataFrame) -> pd.DataFrame:
    annual = df.groupby(["sistema", "anio"])["pasajeros"].sum().reset_index()
    total = annual.groupby("anio")["pasajeros"].transform("sum")
    annual["participacion_pct"] = (annual["pasajeros"] / total * 100).round(2)
    return annual.sort_values(["anio", "participacion_pct"], ascending=[True, False])


def seasonal_pattern(df: pd.DataFrame) -> pd.DataFrame:
    monthly_avg = df.groupby(["sistema", "mes"])["pasajeros"].mean().reset_index()
    global_avg = df.groupby("sistema")["pasajeros"].mean()

    monthly_avg["indice"] = monthly_avg.apply(
        lambda row: round(row["pasajeros"] / global_avg[row["sistema"]] * 100, 1)
        if global_avg[row["sistema"]] > 0 else 0,
        axis=1,
    )
    return monthly_avg


def covid_recovery(df: pd.DataFrame) -> pd.DataFrame:
    base = df[df["anio"] == 2019].groupby(["sistema", "mes"])["pasajeros"].sum()
    results = []
    for anio in sorted(df["anio"].unique()):
        if anio <= 2019:
            continue
        current = df[df["anio"] == anio].groupby(["sistema", "mes"])["pasajeros"].sum()
        for (sistema, mes), base_val in base.items():
            cur_val = current.get((sistema, mes), 0)
            pct = round(cur_val / base_val * 100, 1) if base_val > 0 else 0
            results.append({
                "sistema": sistema,
                "anio": anio,
                "mes": mes,
                "recuperacion_pct": pct,
            })
    return pd.DataFrame(results)


def peak_hours_analysis(df: pd.DataFrame) -> pd.DataFrame:
    if "hora_pico" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(["sistema", "hora_pico"])["pasajeros"]
        .mean()
        .round(0)
        .reset_index()
        .sort_values(["sistema", "pasajeros"], ascending=[True, False])
    )
