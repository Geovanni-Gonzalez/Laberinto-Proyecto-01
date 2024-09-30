from flask import Flask, render_template, jsonify, request
import json
import random
from Administardor import *


app = Flask(__name__)
admin = Administrador()

@app.route('/')
def index():
    return render_template('index.html', titulo="Laberinto")

@app.route('/generar_laberinto', methods=['GET'])
def generar_laberinto():
    tamaño = int(request.args.get('tamaño', 10))
    laberinto = admin.agregar_laberinto(tamaño, tamaño)
    return jsonify(laberinto)


if __name__ == '__main__':
    app.run(debug=True)


