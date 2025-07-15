from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"

for _d in (RAW_DIR, PROCESSED_DIR, LOG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "transporte.db"

ATU_DATOS_URL = "https://www.atu.gob.pe/datos-abiertos/"
MTC_STATS_URL = (
    "https://portal.mtc.gob.pe/estadisticas/transportes/"
    "estadistica_transporte_urbano.html"
)

LINEAS_METRO = {
    "Linea 1": {"estaciones": 26, "km": 34.0, "color": "amarillo"},
    "Linea 2": {"estaciones": 8, "km": 5.2, "color": "azul"},
}

CORREDORES = [
    "TGA (Tacna-Garcilazo-Arequipa)",
    "Javier Prado",
    "San Juan de Lurigancho",
    "Comas-SMP",
    "Brasil",
]

METROPOLITANO = {
    "estaciones": 38,
    "km_troncal": 36.0,
    "alimentadores": 22,
}

MESES = list(range(1, 13))
ANIO_INICIO = 2019
ANIO_FIN = 2024
