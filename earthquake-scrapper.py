import datetime
import pandas as pd
import time

anio = int(input("Ingresa el año que deseas extraer información: "))
mes = int(input("Ingresa el mes (1-12) que deseas extraer información: "))
fecha_actual = datetime.date(anio, mes, 1)
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
        tables = pd.read_html(data_scraping)
        df1 = tables[1]
        df1.to_csv(file, index=False, header=True)
        print(df1)
        time.sleep(5)
