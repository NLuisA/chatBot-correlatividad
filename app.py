from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Cargar la base de datos de correlatividad
with open('correlatividad.json', 'r') as f:
    correlatividad = json.load(f)

@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/correlatividad', methods=['GET'])
def obtener_correlatividad():
    materia_ingresada = request.args.get('materia', '').strip().lower()

    # Buscar la materia ignorando mayúsculas/minúsculas
    materia_encontrada = None
    for materia_real in correlatividad['materias']:
        if materia_ingresada == materia_real.lower():
            materia_encontrada = materia_real
            break

    if materia_encontrada:
        data = correlatividad['materias'][materia_encontrada]
        cursar = data['para_cursar']
        rendir = data['para_rendir']

        respuesta = f" Para **cursar** *{materia_encontrada}* necesitás: "
        respuesta += ", ".join(cursar) if cursar else "nada, podés cursarla directamente."

        respuesta += f"\n\n Para **rendir** *{materia_encontrada}* necesitás: "
        respuesta += ", ".join(rendir) if rendir else "nada, podés rendirla directamente."

        return jsonify({"mensaje": respuesta})
    else:
        return jsonify({"mensaje": f"No encontré información para la materia '{materia_ingresada}' "}), 404

if __name__ == '__main__':
    app.run(debug=True)
