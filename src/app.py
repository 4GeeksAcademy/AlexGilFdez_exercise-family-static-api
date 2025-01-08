"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body =  members
    
    return jsonify(response_body), 200

@app.route ('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "id" not in body:
        return jsonify ({'msg': 'El campo id es obligatorio'}), 400
    if "first_name" not in body:
        return jsonify ({'msg': 'El campo first_name es obligatorio'}), 400
    if "age" not in body:
        return jsonify ({'msg': 'El campo age es obligatorio'}), 400
    if "lucky_numbers" not in body:
        return jsonify ({'msg': 'El campo lucky_numbers es obligatorio'}), 400
    new_member = {
        'id': body['id'],
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': ['lucky_numbers']
    }
    new_members = jackson_family.add_member(new_member)
    return jsonify({'msg': 'ok', 'members': new_members}), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({'msg': 'Miembro no encontrado'}), 404
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member_by_id(id):
    success = jackson_family.delete_member(id)
    if not success:
        return jsonify({'msg': 'Miembro no encontrado'}), 404
    return jsonify({'done': True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
