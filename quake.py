import requests
from bs4 import BeautifulSoup
import datetime
import csv
import json
import pandas as pd

fecha_actual = datetime.datetime.now()
formato_url = fecha_actual.strftime('%Y/%m/%Y%m%d')
url = f'https://www.sismologia.cl/sismicidad/catalogo/{formato_url}.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='sismologia detalle')
    data = []

    if table:
        headers = ['Fecha Local', 'Lugar', 'Fecha UTC', 'Latitud', 'Longitud', 'Profundidad', 'Magnitud']
        errores_file_name = 'errores_formato.txt'
        
        with open(errores_file_name, 'w', encoding='utf-8') as errores_file:
            for row in table.find_all('tr')[1:]:
                try:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    if cols:
                        fecha_local_y_lugar = cols[0]
                        fecha_local = fecha_local_y_lugar[:19]
                        lugar = fecha_local_y_lugar[19:].strip()

                        lat_long = cols[2].split(' ')
                        latitud = lat_long[0]
                        longitud = lat_long[1] if len(lat_long) > 1 else ''

                        modified_row = [fecha_local, lugar, cols[1], latitud, longitud] + cols[3:]
                        data.append(modified_row)
                except Exception as e:
                    errores_file.write(f"Error procesando fila: {cols}\nError: {str(e)}\n")
                    continue  # Ccontinúa con la siguiente fila después de escribir el error

        csv_file_name = 'sismologia_datos_modificado.csv'
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Datos guardados en {csv_file_name}")

        json_file_name = 'sismologia_datos_modificado.json'
        with open(json_file_name, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        print(f"Datos guardados en {json_file_name}")

        df = pd.read_csv(csv_file_name)
        print(df)

    else:
        print("Tabla no encontrada.")
else:
    print(f"Error en la petición web: {response.status_code}")
