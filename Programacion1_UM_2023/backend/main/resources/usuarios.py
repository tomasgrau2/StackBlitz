from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from sqlalchemy import func, desc, asc
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required

#Defino el recurso usuario
class Usuario(Resource): #A la clase usuario le indico que va a ser del tipo recurso(Resource)
    #obtener recurso
    @jwt_required(optional=True)
    @role_required(roles = ["admin"])
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        current_identity = get_jwt_identity()
        if current_identity:
            return usuario.to_json_complete()
        else:
            return usuario.to_json()
        
    #eliminar recurso
    @role_required(roles = ["admin"])
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    #Modificar el recurso usuario
    @role_required(roles = ["admin"])
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json() , 201

#Coleccion de recurso Usuarios
class Usuarios(Resource):
    #obtener lista de los usuarios
    @jwt_required()
    @role_required(roles = ["admin"])
    def get(self):    
        page = 1
        per_page = 10
        usuarios = db.session.query(UsuarioModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

         ### FILTROS ###
        
        #Busqueda por apellido
        if request.args.get('apellido'):
            usuarios=usuarios.filter(UsuarioModel.apellido.like("%"+request.args.get('apellido')+"%"))
            
        #Busqueda por DNI
        if request.args.get('dni'):
            usuarios=usuarios.filter(UsuarioModel.dni.like("%"+request.args.get('dni')+"%"))
            
        #Ordeno por edad de menor a mayor
        if request.args.get('sortby_edad'):
            usuarios=usuarios.order_by(asc(UsuarioModel.edad))

        ### FIN FILTROS ####
        
        usuarios = usuarios.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)

        return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios],
                  'total': usuarios.total,
                  'pages': usuarios.pages,
                  'page': page
                })

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201





