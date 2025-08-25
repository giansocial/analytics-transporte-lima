import logging
import sqlite3
from pathlib import Path
import pandas as pd

from src.config.settings import DB_PATH

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS dim_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_tiempo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    periodo TEXT NOT NULL,
    trimestre INTEGER NOT NULL,
    UNIQUE(anio, mes)
);

CREATE TABLE IF NOT EXISTS fact_pasajeros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sistema_id INTEGER NOT NULL,
    tiempo_id INTEGER NOT NULL,
    pasajeros INTEGER NOT NULL,
    var_yoy_pct REAL,
    FOREIGN KEY (sistema_id) REFERENCES dim_sistema(id),
    FOREIGN KEY (tiempo_id) REFERENCES dim_tiempo(id),
    UNIQUE(sistema_id, tiempo_id)
);
"""


def init_db(db_path: Path = None) -> sqlite3.Connection:
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def _get_or_create(conn, table, col, value):
    cur = conn.execute(f"SELECT id FROM {table} WHERE {col} = ?", (value,))
    row = cur.fetchone()
    if row:
        return row[0]
    conn.execute(f"INSERT INTO {table} ({col}) VALUES (?)", (value,))
    conn.commit()
    return conn.execute(f"SELECT id FROM {table} WHERE {col} = ?", (value,)).fetchone()[0]


def load_to_db(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    loaded = 0
    for _, row in df.iterrows():
        sistema_id = _get_or_create(conn, "dim_sistema", "nombre", row["sistema"])
        anio, mes = int(row["anio"]), int(row["mes"])
        periodo = f"{anio}-{str(mes).zfill(2)}"
        trimestre = (mes - 1) // 3 + 1

        cur = conn.execute("SELECT id FROM dim_tiempo WHERE anio=? AND mes=?", (anio, mes))
        t = cur.fetchone()
        if t:
            tid = t[0]
        else:
            conn.execute(
                "INSERT INTO dim_tiempo (anio, mes, periodo, trimestre) VALUES (?,?,?,?)",
                (anio, mes, periodo, trimestre),
            )
            conn.commit()
            tid = conn.execute("SELECT id FROM dim_tiempo WHERE anio=? AND mes=?", (anio, mes)).fetchone()[0]

        conn.execute(
            "INSERT OR REPLACE INTO fact_pasajeros (sistema_id, tiempo_id, pasajeros, var_yoy_pct) VALUES (?,?,?,?)",
            (sistema_id, tid, int(row["pasajeros"]), row.get("var_yoy_pct")),
        )
        loaded += 1
    conn.commit()
    log.info("cargados %d registros", loaded)
    return loaded


def export_csv(df: pd.DataFrame, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{name}.csv"
    df.to_csv(out, index=False)
    return out
