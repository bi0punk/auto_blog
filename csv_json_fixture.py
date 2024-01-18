import csv
import json

# Nombre de archivo CSV de entrada y salida
csv_file = 'data2.csv'
json_file = 'sismos_fixture.json'

# Lista para almacenar los datos convertidos a formato JSON
quake_data = []

# Leer el archivo CSV
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Crear un diccionario para cada fila en el formato deseado
        quake_entry = {
            "model": "blog_app.post",
            "pk": reader.line_num - 1,  # Puedes ajustar esto según tus necesidades
            "fields": {
                "author": 1,  # Agrega el valor adecuado para el autor
                "title": row['Fecha Local / Lugar'],
                "body": f"{row['Fecha Local / Lugar']} {row['Fecha UTC']} {row['Latitud / Longitud']} {row['Profundidad']} {row['Magnitud (2)']}",
                "created_at": "",  # Agrega el valor adecuado para la fecha de creación
                "image": "",  # Agrega el valor adecuado para la imagen
                "categories": []  # Agrega el valor adecuado para las categorías
            }
        }
        quake_data.append(quake_entry)

# Escribir el resultado en un archivo JSON
with open(json_file, 'w') as json_output:
    json.dump(quake_data, json_output, indent=2)

print(f'Conversion completa. Datos guardados en {json_file}')
