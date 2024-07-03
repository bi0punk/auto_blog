from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración de Django para el proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_blog.settings')

# Crea una instancia de Celery con el nombre del proyecto
app = Celery('auto_blog')

# Carga la configuración de Celery desde el archivo de configuraciones de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre las tareas en los módulos de tareas de todas las aplicaciones instaladas
app.autodiscover_tasks()

# Tarea de depuración para probar la conexión
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


""" from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_blog.settings')

app = Celery('auto_blog')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Asegúrate de que esta línea esté presente en tu configuración
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') """