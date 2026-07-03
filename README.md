# Auto Blog

[![CI](https://github.com/bi0punk/auto_blog/actions/workflows/ci.yml/badge.svg)](https://github.com/bi0punk/auto_blog/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Blog automatizado de sismología para Chile. Scrapea datos del sitio [sismologia.cl](https://www.sismologia.cl), los procesa y los publica como posts de blog.

## Tabla de contenidos

- [Características](#características)
- [Stack](#stack)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [CI](#ci)
- [Configuración](#configuración)
- [Datos](#datos)
- [Limitaciones y roadmap](#limitaciones-y-roadmap)
- [Licencia](#licencia)

## Características

- Scraping periódico de sismologia.cl (vía Celery Beat).
- Procesamiento y normalización de datos (magnitude, lat/lon, UTC time).
- Publicación automática como posts de blog.
- Frontend con DataTables + Plotly.js para visualizar sismos.
- Feed RSS.

## Stack

- **Backend**: Django 5.1
- **Task Queue**: Celery 5.4 + Redis (broker)
- **Scraping**: BeautifulSoup4 + Requests + Pandas
- **Frontend**: HTML5 + CSS + jQuery + DataTables + Plotly.js
- **Calidad**: ruff (lint), Django tests

## Arquitectura

```
        ┌──────────────┐  scrape   ┌──────────────┐
        │ Celery Beat   │ ────────► │ sismologia.cl │
        │ (schedule)    │           └──────┬───────┘
        └──────┬───────┘                  │
               │                          ▼
        ┌──────▼───────┐          ┌──────────────┐
        │ Celery worker │ ◄────── │  parser       │ (BS4/pandas)
        │  auto_blog    │          └──────────────┘
        └──────┬───────┘
               │ inserta Post
               ▼
        ┌──────────────┐   render   ┌──────────────┐
        │  Django ORM   │ ─────────► │  Blog UI      │ (/blog/)
        │  + SQLite     │            │ DataTables+   │
        └──────────────┘            │ Plotly        │
                                    └──────────────┘
```

## Requisitos

- Python 3.12+
- Redis (para Celery)
- Conexión a internet (para scraping de sismologia.cl)

## Instalación

```bash
git clone https://github.com/bi0punk/auto_blog
cd auto_blog
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # editar SECRET_KEY, ALLOWED_HOSTS
python manage.py migrate

# Redis
redis-server

# Celery (en terminales separadas)
celery -A auto_blog worker -l info
celery -A auto_blog beat -l info

# Servidor
python manage.py runserver
```

Visitar `http://localhost:8000/blog/`.

## Uso

1. Configura `.env` (ver [Configuración](#configuración)).
2. Arranca Redis + Celery worker + Celery beat + Django.
3. Celery Beat dispara el scraping en el schedule definido; los sismos nuevos se publican como posts.
4. Revisa el blog en `/blog/` y el feed RSS.

Datos de ejemplo en `sismos_20240702.csv`.

## Tests

```bash
DEBUG=True SECRET_KEY=test ALLOWED_HOSTS=localhost DATABASE_URL=sqlite://:memory: \
  python manage.py test blog auto_blog
```

Tests existentes: helpers de parsing (`_parse_float`, `_parse_lat_lon`, `_parse_utc_time`) en `auto_blog/tests.py` + tests del modelo `Post` en `blog/tests.py`.

## CI

GitHub Actions (`.github/workflows/ci.yml`) sobre Python 3.12:

- **lint** — `ruff check .`
- **test** — `python manage.py check` + `python manage.py test` (con SQLite in-memory, sin Redis).

## Configuración

Variables en `.env` (ver `.env.example`):

- `DEBUG` — `True`/`False`.
- `SECRET_KEY` — clave Django.
- `ALLOWED_HOSTS` — hosts permitidos.
- `DATABASE_URL` — URL de DB (default `sqlite:///db.sqlite3`).
- `REDIS_URL` — broker Celery (default `redis://localhost:6379/0`).

## Datos

- `db.sqlite3` — SQLite local (gitignored, se genera con `migrate`).
- `sismos_20240702.csv` — dataset de ejemplo commiteado (referencia).
- Posts persistidos en la tabla `Post` del ORM.

## Limitaciones y roadmap

- **Limitación**: depende del HTML de sismologia.cl; cambios en el sitio pueden romper el scraper.
- **Limitación**: sin tests del scraper end-to-end (requiere red).
- **Roadmap**: alertas por Telegram, tests del scraper con fixtures HTML, dashboard histórico.

## Licencia

MIT — ver [LICENSE](LICENSE).
