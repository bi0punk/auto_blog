from celery import shared_task
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from django.conf import settings
import json
from datetime import datetime
from django.core.management import call_command
from django.utils import timezone


@shared_task
def data_scraping():
    url = 'https://www.sismologia.cl/sismicidad/catalogo/2024/07/20240704.html'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar que la solicitud fue exitosa
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar la tabla usando la clase 'sismologia detalle'
    table = soup.find('table', class_='sismologia detalle')
    if table is None:
        print("No se encontró ninguna tabla con la clase 'sismologia detalle' en el HTML.")
        return
    
    print("Tabla encontrada en el HTML.")

    # Verificar si la tabla tiene encabezados y filas
    headers = [header.get_text(strip=True) for header in table.find_all('th')]
    rows = table.find_all('tr')[1:]  # Omitir la primera fila si contiene los encabezados
    
    if not headers:
        print("No se encontraron encabezados en la tabla.")
        return
    
    if not rows:
        print("No se encontraron filas en la tabla.")
        return
    
    print(f"Encabezados encontrados: {headers}")

    data = []
    for row in rows:
        columns = row.find_all('td')
        data.append([column.get_text(strip=True) for column in columns])
    
    df = pd.DataFrame(data, columns=headers)
    
    if df.empty:
        print("El DataFrame está vacío.")
    else:
        print(df)

    # Crear una lista de diccionarios con la estructura de fixtures
    fixtures = []
    for index, row in df.iterrows():
        fixture = {
            "model": "blog.post",
            "pk": index + 1,
            "fields": {
                "title": f"Sismo en {row.iloc[0]}",
                "content": f"Magnitud: {row.iloc[1]}, Profundidad: {row.iloc[2]}, Fecha y Hora: {row.iloc[3]}",
                "created_at": datetime.now().isoformat()
            }
        }
        fixtures.append(fixture)

    # Guardar el JSON en el directorio de fixtures sin BOM
    fixtures_dir = os.path.join(settings.BASE_DIR, 'auto_blog', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)
    json_file_path = os.path.join(fixtures_dir, 'sismos_20240704.json')
    
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(fixtures, json_file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo JSON: {e}")
        return
    
    print("Ejecutando tarea programada")


@shared_task
def load_fixture():
    fixture_path = os.path.join(settings.BASE_DIR, 'auto_blog', 'fixtures', 'sismos_20240704.json')
    if os.path.exists(fixture_path):
        try:
            call_command('loaddata', fixture_path)
            print("Fixture loaded successfully")
        except Exception as e:
            print(f"Error loading fixture: {e}")
    else:
        print(f"No fixture named 'sismos_20240702.json' found at {fixture_path}")