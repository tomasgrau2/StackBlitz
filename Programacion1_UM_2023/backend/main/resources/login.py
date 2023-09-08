from flask_restful import Resource
from flask import request

USUARIOS = {
    1: {'usuario':'pepe_32', 'contraseña':'pepe123'}
}

class Login(Resource):
    def post(self):
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Validar usuario y contraseña
        for usuario in USUARIOS.values():
            if usuario['usuario'] == username and usuario['contraseña'] == password:
                return {'message': 'Inicio de sesión exitoso'}, 200
        else:
            return {'message': 'Credenciales inválidas'}, 401

        