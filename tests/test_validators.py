import pytest
import pandas as pd
from src.quality.validators import check_completeness, check_uniqueness, run_quality_report


def _df():
    return pd.DataFrame({
        "sistema": ["Metro", "Bus"],
        "anio": [2023, 2023],
        "mes": [1, 2],
        "pasajeros": [10000000, 5000000],
    })


def test_completeness():
    result = check_completeness(_df(), ["sistema", "pasajeros"])
    assert result["score"] == 100.0


def test_uniqueness():
    result = check_uniqueness(_df(), ["sistema", "anio", "mes"])
    assert result["duplicados"] == 0


def test_quality_report():
    report = run_quality_report(_df())
    assert report["score_total"] > 90
