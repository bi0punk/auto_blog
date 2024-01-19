import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    json_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Estructurar los datos en el formato JSON requerido
            json_entry = {
                "model": "blog_app.post",
                "pk": int(row['pk']),
                "fields": {
                    "author": int(row['author']),
                    "title": row['title'],
                    "body": row['body'],
                    "created_at": row['created_at'],
                    "image": row['image'],
                    "categories": [int(category) for category in row['categories'].split(',')]
                }
            }
            json_data.append(json_entry)
    # Escribir los datos en formato JSON al archivo
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":
    # Ruta del archivo CSV de entrada
    csv_input_file = 'ruta/del/archivo.csv'
    # Ruta del archivo JSON de salida
    json_output_file = 'ruta/del/archivo.json'
    # Convertir CSV a JSON
    csv_to_json(csv_input_file, json_output_file)