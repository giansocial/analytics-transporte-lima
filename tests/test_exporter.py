import pytest
import pandas as pd
from src.load.exporter import init_db, load_to_db, export_csv


@pytest.fixture
def db(tmp_path):
    conn = init_db(tmp_path / "test.db")
    yield conn
    conn.close()


def _df():
    return pd.DataFrame({
        "sistema": ["Metro", "Bus"],
        "anio": [2023, 2023],
        "mes": [1, 2],
        "pasajeros": [10000000, 5000000],
        "var_yoy_pct": [5.2, None],
    })


def test_init_tables(db):
    cur = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in cur.fetchall()}
    assert "fact_pasajeros" in tables


def test_load_inserts(db):
    assert load_to_db(_df(), db) == 2


def test_load_upsert(db):
    load_to_db(_df(), db)
    load_to_db(_df(), db)
    cur = db.execute("SELECT COUNT(*) FROM fact_pasajeros")
    assert cur.fetchone()[0] == 2


def test_export_csv(tmp_path):
    path = export_csv(_df(), tmp_path, "test")
    assert path.exists()
