import datetime
import pandas as pd
import time
import urllib.error
from urllib.request import urlopen

# Obtener la fecha actual
fecha_actual = datetime.date.today()
anio = fecha_actual.year
mes = fecha_actual.month

# Calcular el último día del mes actual
ultimo_dia_mes = (fecha_actual.replace(day=1, month=mes % 12 + 1, year=anio) - datetime.timedelta(days=1)).day

BASE_LINK = 'https://www.sismologia.cl/sismicidad/catalogo/'

with open('data2.csv', mode='a', encoding='utf-8') as file:
    while fecha_actual.month == mes:
        cadena = f"{anio}/{fecha_actual:%m}/{anio}{fecha_actual:%m}{fecha_actual:%d}"
        fecha_actual += datetime.timedelta(days=1)
        if fecha_actual.day > ultimo_dia_mes:
            break
        data_scraping = BASE_LINK + cadena + '.html'
        print(data_scraping)
        
        try:
            # Intentar abrir la URL
            with urlopen(data_scraping) as f:
                tables = pd.read_html(f)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("Error 403: Forbidden - La URL no está disponible")
            else:
                print(f"Error HTTP {e.code}: {e.reason}")
            continue
        except Exception as e:
            print(f"Error al abrir la URL: {e}")
            continue

        df1 = tables[1]
        df1.to_csv(file, index=False, header=True)
        print(df1)
    time.sleep(5)
        
