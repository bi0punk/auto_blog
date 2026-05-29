# Auto Blog

Blog automatizado de sismología para Chile. Scrapea datos del sitio [sismologia.cl](https://www.sismologia.cl), los procesa y los publica como posts de blog.

## Stack

- **Backend:** Django 5.1
- **Task Queue:** Celery 5.4 + Redis
- **Scraping:** BeautifulSoup4 + Requests + Pandas
- **Frontend:** HTML5 + CSS + jQuery + DataTables + Plotly.js

## Setup

```bash
# Clonar el repo
git clone <repo>
cd auto_blog

# Crear y activar venv
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.sample .env
# Editar .env con tus valores

# Migrar BD
python manage.py migrate

# Iniciar Redis (requerido para Celery)
redis-server

# Iniciar Celery worker
celery -A auto_blog worker -l info

# Iniciar Celery Beat (para tareas programadas)
celery -A auto_blog beat -l info

# Iniciar servidor de desarrollo
python manage.py runserver
```

Visitar `http://localhost:8000/blog/` para ver los posts.
