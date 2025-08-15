# Analytics Transporte - Lima

Soy Gian Cruz.

Pipeline de analisis del transporte publico masivo de Lima Metropolitana. Procesa datos de pasajeros del Metro Linea 1, el Metropolitano (BRT) y los corredores complementarios. Mide estacionalidad, participacion por sistema y el impacto del COVID-19 en la movilidad urbana.

Lima mueve mas de 10 millones de viajes diarios. El sistema de transporte masivo (Metro + Metropolitano + Corredores) transporta una fraccion de eso, pero su crecimiento y recuperacion post-pandemia son indicadores clave de la movilidad urbana.

## Que hace

- Carga datos de pasajeros desde CSVs (datos abiertos ATU/MTC)
- Limpia, normaliza y elimina registros invalidos
- Calcula variacion interanual (YoY) por sistema
- Genera participacion de mercado por sistema/anio
- Patron de estacionalidad mensual
- Indice de recuperacion COVID (base 2019)
- Carga a warehouse SQLite

## Instalacion

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python -m src.pipeline
```

## Tests

```bash
pytest tests/ -v
```

## Stack

- Python 3.10+
- pandas + numpy
- SQLite
- pytest

## Estructura

```
analytics-transporte-lima/
├── src/
│   ├── config/settings.py
│   ├── extract/data_loader.py
│   ├── transform/
│   │   ├── cleaner.py
│   │   └── enricher.py
│   ├── quality/validators.py
│   ├── load/exporter.py
│   ├── utils/logger.py
│   └── pipeline.py
├── tests/
└── requirements.txt
```

---

## What it does

Analytics pipeline for Lima's mass transit system. Processes ridership data for Metro Line 1, Metropolitano (BRT), and complementary bus corridors. Measures seasonality, system market share, and COVID-19 impact on urban mobility.

---

## Fuentes de datos

| Fuente | Descripcion | Enlace |
|--------|-------------|--------|
| ATU - Datos Abiertos | Autoridad de Transporte Urbano de Lima y Callao | [https://www.atu.gob.pe/datos-abiertos/](https://www.atu.gob.pe/datos-abiertos/) |
| MTC - Estadisticas de transporte | Ministerio de Transportes - estadisticas de transporte urbano | [https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html](https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html) |
| OSITRAN | Organismo supervisor de la infraestructura de transporte | [https://www.ositran.gob.pe/](https://www.ositran.gob.pe/) |
