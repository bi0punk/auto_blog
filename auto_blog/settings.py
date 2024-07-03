import os
from pathlib import Path
from celery.schedules import crontab
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_uq764a!9!%r$i3i=0r-97(^)zibdt+jd80u!^)sh@0slql)r$'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auto_blog',
    'blog',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auto_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auto_blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Asegúrate de que la ruta de tus archivos estáticos sea correcta
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "blog/static/blog",
]

# Define dónde se recopilarán los archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# Configuración para Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Configuración para Celery Beat
CELERY_BEAT_SCHEDULE = {
    'mi-tarea-programada': {
        'task': 'auto_blog.tasks.data_scraping',  # Asegúrate de que esta ruta es correcta
        'schedule': crontab(minute='*'),  # Ejecutar cada minuto
        #'schedule': crontab(minute=0, hour=9),  # Ejecutar a las 00:00 cada día'schedule': crontab(minute=0, hour=0),  # Ejecutar a las 00:00 cada día
        #'schedule': timedelta(days=1),  # Ejecutar cada 24 horas
    },
    'load-fixture-every-hour': {
        'task': 'auto_blog.tasks.load_fixture',
        'schedule': crontab(minute='*'),  # Cada hora en el minuto 0
    },
}




# Si quieres usar un backend de resultados diferente, añade la configuración aquí
# CELERY_RESULT_BACKEND = 'django-db'  # O cualquier otro backend que prefieras
