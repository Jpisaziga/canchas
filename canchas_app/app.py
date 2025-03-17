from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Ruta al archivo JSON que almacena el estado de las canchas
CANCHAS_FILE = 'canchas.json'

# Cargar el estado de las canchas desde el archivo JSON
def cargar_canchas():
    if not os.path.exists(CANCHAS_FILE):
        # Si el archivo no existe, crear una lista de canchas por defecto
        canchas = [
            {"id": 1, "nombre": "Cancha 1", "disponible": True},
            {"id": 2, "nombre": "Cancha 2", "disponible": True},
            {"id": 3, "nombre": "Cancha 3", "disponible": True},
        ]
        with open(CANCHAS_FILE, 'w') as f:
            json.dump(canchas, f)
    else:
        with open(CANCHAS_FILE, 'r') as f:
            canchas = json.load(f)
    return canchas

# Guardar el estado de las canchas en el archivo JSON
def guardar_canchas(canchas):
    with open(CANCHAS_FILE, 'w') as f:
        json.dump(canchas, f)

@app.route('/')
def index():
    canchas = cargar_canchas()
    return render_template('index.html', canchas=canchas)

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    canchas = cargar_canchas()
    cancha = next((c for c in canchas if c['id'] == id), None)
    
    if request.method == 'POST':
        estado = request.form.get('disponible') == 'on'
        cancha['disponible'] = estado
        guardar_canchas(canchas)
        return redirect(url_for('index'))
    
    return render_template('actualizar.html', cancha=cancha)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")