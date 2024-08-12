"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Crear la instancia de la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar el sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Obtén todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2) Recupera solo un miembro
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3) Añadir (POST) un miembro
@app.route('/member', methods=['POST'])
def add_member():
    try:
        new_member = request.json
        
        # Verificar que los campos obligatorios están presentes
        if not new_member or not all(k in new_member for k in ("first_name", "age", "lucky_numbers")):
            return jsonify({"error": "Missing required fields"}), 400
        
        jackson_family.add_member(new_member)
        return jsonify({"message": "Member added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4) ELIMINA un miembro
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            jackson_family.delete_member(member_id)
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Esto solo corre si ejecutas `$ python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
