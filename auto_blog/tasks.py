from celery import shared_task

@shared_task
def data_scraping():
    # Código de tu tarea a ejecutar periódicamente
    print("Ejecutando tarea programada")
