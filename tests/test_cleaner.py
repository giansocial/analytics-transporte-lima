import pytest
import pandas as pd
from src.transform.cleaner import clean_transport_data, add_period


def test_clean_parses_numbers():
    df = pd.DataFrame({
        "sistema": ["Metro"], "anio": [2023], "mes": [1],
        "pasajeros": ["10,500,000"],
    })
    result = clean_transport_data(df)
    assert result["pasajeros"].iloc[0] == 10500000


def test_clean_drops_invalid():
    df = pd.DataFrame({
        "sistema": ["Metro", "Bus"], "anio": [2023, 2023], "mes": [1, 2],
        "pasajeros": ["10000000", "abc"],
    })
    result = clean_transport_data(df)
    assert len(result) == 1


def test_clean_removes_dupes():
    df = pd.DataFrame({
        "sistema": ["Metro", "Metro"], "anio": [2023, 2023], "mes": [1, 1],
        "pasajeros": ["10000000", "10000000"],
    })
    result = clean_transport_data(df)
    assert len(result) == 1


def test_add_period():
    df = pd.DataFrame({"anio": [2023], "mes": [3]})
    result = add_period(df)
    assert result["periodo"].iloc[0] == "2023-03"
