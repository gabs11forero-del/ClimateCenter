from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

ARCHIVO_DATASET = 'registro_clima.csv'

if not os.path.exists(ARCHIVO_DATASET):
    with open(ARCHIVO_DATASET, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha_Hora', 'Zona', 'Temperatura_C', 'Humedad_Aire_%', 'Humedad_Suelo_%', 'Luminosidad_%', 'Precipitacion_%'])

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/tiempo-real')
def tiempo_real():
    return render_template('tiempo_real.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/api/guardar_datos', methods=['POST'])
def guardar_datos():
    data = request.json
    zona = data.get("zona")
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_DATASET, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([ahora, zona, data.get("temperatura"), data.get("humedad_aire"), data.get("humedad_suelo"), data.get("luminosidad"), data.get("precipitacion")])
    return jsonify({"status": "éxito"}), 200

@app.route('/api/leer_csv', methods=['GET'])
def leer_csv():
    ultimos_datos = {
        "Urbana": {"temperatura": "--", "humedad_aire": "--", "humedad_suelo": "--", "luminosidad": "--", "precipitacion": "--", "fecha_hora": "--"},
        "Rural": {"temperatura": "--", "humedad_aire": "--", "humedad_suelo": "--", "luminosidad": "--", "precipitacion": "--", "fecha_hora": "--"},
        "Montania": {"temperatura": "--", "humedad_aire": "--", "humedad_suelo": "--", "luminosidad": "--", "precipitacion": "--", "fecha_hora": "--"}
    }
    if not os.path.exists(ARCHIVO_DATASET):
        return jsonify(ultimos_datos)
    try:
        with open(ARCHIVO_DATASET, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zona = row.get('Zona')
                if zona in ultimos_datos:
                    ultimos_datos[zona] = {
                        "temperatura": row.get('Temperatura_C', '--'),
                        "humedad_aire": row.get('Humedad_Aire_%', '--'),
                        "humedad_suelo": row.get('Humedad_Suelo_%', '--'),
                        "luminosidad": row.get('Luminosidad_%', '--'),
                        "precipitacion": row.get('Precipitacion_%', '--'),
                        "fecha_hora": row.get('Fecha_Hora', '--')
                    }
    except Exception as e:
        print(f"Error: {e}")
    return jsonify(ultimos_datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)