from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import random
from Administrador import *

admin = Administrador()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/generar_laberinto')
def generar_laberinto():
    try:
        tamaño = int(request.args.get('tamaño'))
        fila, columna = tamaño // 2, tamaño // 2
        laberinto = admin.agregar_laberinto(fila, columna)
        
        laberinto_dict = laberinto.to_dict()
        print(json.dumps(laberinto_dict, indent=4))  # Imprimir para verificar
        return jsonify(laberinto_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resolver_laberinto')
def resolver_laberinto():
    try:
        id_laberinto = request.args.get('id_laberinto')  # Obtén como cadena
        metodo = request.args.get('algoritmo')  # Asegúrate de usar el mismo nombre que en el frontend
        fila= int(request.args.get('fila'))
        columna= int(request.args.get('columna'))
        
        laberinto = admin.resolver_laberinto(id_laberinto, metodo, (fila,columna),metodo)
        
        if laberinto is None:
            return jsonify({"error": "Laberinto no encontrado."}), 404
        
        laberinto_dict = laberinto.to_dict()
        solucion= laberinto.camino_solucion

        if not isinstance(solucion, list):
            return jsonify({"error": "La solución no es una lista."}), 500
        
        return jsonify({"laberinto": laberinto_dict, "solucion": solucion})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guardar_solucion', methods=['POST'])
def guardar_solucion():
    solution_data = request.json  # Assume the solution data is sent as JSON
    file_name = 'solucion_laberinto.json'  # Change as needed

    with open(file_name, 'w') as f:
        json.dump(solution_data, f)
    
    return jsonify({"message": "Solución guardada exitosamente."})

@app.route('/cargar_solucion', methods=['GET'])
def cargar_solucion():
    file_name = 'solucion_laberinto.json'  # Change as needed
    
    try:
        with open(file_name, 'r') as f:
            solution_data = json.load(f)
        return jsonify(solution_data)
    except FileNotFoundError:
        return jsonify({"error": "No se encontró la solución guardada."}), 404

if __name__ == '__main__':
    app.run(debug=True)


