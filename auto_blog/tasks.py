from celery import shared_task
import requests
from bs4 import BeautifulSoup
import pandas as pd

@shared_task
def data_scraping():
    url = 'https://www.sismologia.cl/sismicidad/catalogo/2024/07/20240702.html'
    response = requests.get(url)
    response.raise_for_status()  # Verificar que la solicitud fue exitosa
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Imprimir el HTML completo para verificar la estructura
    #print(soup.prettify())
    
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
    
    df.to_csv('sismos_20240702.csv', index=False, encoding='utf-8-sig')
    
    print("Ejecutando tarea programada")
