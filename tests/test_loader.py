import pytest
from pathlib import Path
from src.extract.data_loader import load_csv, load_all, validate_schema

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_csv():
    rows = load_csv(FIXTURES / "transporte_sample.csv")
    assert len(rows) > 0
    assert "sistema" in rows[0]


def test_load_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv(FIXTURES / "nope.csv")


def test_load_all():
    rows = load_all(FIXTURES)
    assert len(rows) > 30


def test_load_all_empty(tmp_path):
    rows = load_all(tmp_path)
    assert rows == []


def test_validate_ok():
    rows = [{"sistema": "Metro", "anio": "2023", "mes": "1", "pasajeros": "100"}]
    result = validate_schema(rows, {"sistema", "anio", "mes", "pasajeros"})
    assert result["valid"] is True


def test_validate_missing():
    rows = [{"sistema": "Metro"}]
    result = validate_schema(rows, {"sistema", "anio", "mes", "pasajeros"})
    assert result["valid"] is False
