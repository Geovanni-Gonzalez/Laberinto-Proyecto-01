from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import random
from Administardor import *

admin = Administrador()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/generar_laberinto')
def generar_laberinto():
    tamaño = int(request.args.get('tamaño'))
    fila, columna = tamaño // 2, tamaño // 2
    laberinto = admin.agregar_laberinto(fila, columna)
    
    laberinto_dict = laberinto.to_dict()
    print(json.dumps(laberinto_dict, indent=4))  # Imprimir para verificar
    return jsonify(laberinto_dict)

@app.route('/resolver_laberinto')
def resolver_laberinto():
    pass



if __name__ == '__main__':
    app.run(debug=True)


