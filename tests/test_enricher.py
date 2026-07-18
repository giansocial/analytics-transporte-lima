import pandas as pd
import numpy as np
from src.transform.enricher import (
    add_yoy_change, system_share, seasonal_pattern, covid_recovery,
)


def _df():
    rows = []
    for anio in [2019, 2020, 2021, 2022, 2023]:
        for mes in [1, 6, 12]:
            base = 10000000 if anio not in (2020, 2021) else 4000000
            rows.append({
                "sistema": "Metro Linea 1",
                "anio": anio, "mes": mes,
                "pasajeros": base + np.random.randint(-1000000, 1000000),
            })
            rows.append({
                "sistema": "Metropolitano",
                "anio": anio, "mes": mes,
                "pasajeros": int(base * 0.7) + np.random.randint(-500000, 500000),
            })
    return pd.DataFrame(rows)


def test_yoy_column():
    result = add_yoy_change(_df())
    assert "var_yoy_pct" in result.columns


def test_yoy_first_year_null():
    result = add_yoy_change(_df())
    first = result[result["anio"] == 2019]
    assert first["var_yoy_pct"].isna().all()


def test_system_share():
    shares = system_share(_df())
    assert "participacion_pct" in shares.columns
    for anio in shares["anio"].unique():
        total = shares[shares["anio"] == anio]["participacion_pct"].sum()
        assert abs(total - 100) < 0.5


def test_seasonal_pattern():
    seasonal = seasonal_pattern(_df())
    assert "indice" in seasonal.columns


def test_covid_recovery():
    rec = covid_recovery(_df())
    assert "recuperacion_pct" in rec.columns
    assert not rec.empty
