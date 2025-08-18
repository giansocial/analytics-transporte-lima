# Analytics Transporte - Lima

¿Sabías que Lima mueve más de 10 millones de viajes diarios pero su sistema de transporte masivo apenas cubre el 15% de la demanda? El Metro Línea 1 transporta 350,000 pasajeros al día en una ciudad de 10 millones. Durante la pandemia, la movilidad cayó un 80% y algunos sistemas tardaron más de dos años en recuperar niveles pre-COVID.

Soy Gian Cruz. Construí este pipeline para analizar los datos de pasajeros del Metro, el Metropolitano (BRT) y los corredores complementarios publicados por la ATU y el MTC. Mide estacionalidad, participación de mercado por sistema, variaciones interanuales y genera un índice de recuperación COVID con base 2019.

## Qué hace

- Carga datos de pasajeros desde CSVs (datos abiertos ATU/MTC)
- Limpia, normaliza y elimina registros inválidos
- Calcula variación interanual (YoY) por sistema
- Genera participación de mercado por sistema/año
- Patrón de estacionalidad mensual
- Índice de recuperación COVID (base 2019)
- Carga a warehouse SQLite

## Instalación

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

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| ATU - Datos Abiertos | Autoridad de Transporte Urbano de Lima y Callao | [https://www.atu.gob.pe/datos-abiertos/](https://www.atu.gob.pe/datos-abiertos/) |
| MTC - Estadísticas de transporte | Ministerio de Transportes - estadísticas de transporte urbano | [https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html](https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html) |
| OSITRAN | Organismo supervisor de la infraestructura de transporte | [https://www.ositran.gob.pe/](https://www.ositran.gob.pe/) |
