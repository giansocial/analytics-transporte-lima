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

## Fuentes de datos

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| ATU - Datos Abiertos | Autoridad de Transporte Urbano de Lima y Callao | [https://www.atu.gob.pe/datos-abiertos/](https://www.atu.gob.pe/datos-abiertos/) |
| MTC - Estadísticas de transporte | Ministerio de Transportes - estadísticas de transporte urbano | [https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html](https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html) |
| OSITRAN | Organismo supervisor de la infraestructura de transporte | [https://www.ositran.gob.pe/](https://www.ositran.gob.pe/) |

## Licencia

MIT

---

# Transit Analytics - Lima

Did you know Lima handles over 10 million daily trips but its mass transit system covers only 15% of the demand? Metro Line 1 carries 350,000 passengers per day in a city of 10 million. During the pandemic, ridership dropped 80% and some systems took over two years to recover pre-COVID levels.

I'm Gian Cruz. I built this pipeline to analyze ridership data from the Metro, the Metropolitano (BRT), and complementary bus corridors published by the ATU and MTC. It measures seasonality, market share by system, year-over-year variations, and generates a COVID recovery index benchmarked against 2019.

## Quick start

```bash
git clone https://github.com/giansocial/analytics-transporte-lima.git
cd analytics-transporte-lima
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
```

## Data sources

| Source | Description | Link |
|--------|-------------|------|
| ATU - Open Data | Lima and Callao Urban Transport Authority | [https://www.atu.gob.pe/datos-abiertos/](https://www.atu.gob.pe/datos-abiertos/) |
| MTC - Transport Statistics | Ministry of Transport - urban transit statistics | [https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html](https://portal.mtc.gob.pe/estadisticas/transportes/estadistica_transporte_urbano.html) |

## License

MIT
