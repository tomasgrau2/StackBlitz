from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProfesorModel, ClaseModel, UsuarioModel
from sqlalchemy import func, desc
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required


class UsuariosProfesores(Resource):
    #obtener lista de los Profesores
    @jwt_required()
    @role_required(roles = ['admin', 'profesor', 'alumno'])
    def get(self):
        page = 1
        per_page = 10
        profesores = db.session.query(ProfesorModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

                ### FILTROS ###
        
        #Busqueda por especialidad
        if request.args.get('especialidad'):
            profesores=profesores.filter(ProfesorModel.especialidad.like("%"+request.args.get('especialidad')+"%"))
        
        #Ordeno por especialidad
        if request.args.get('sortby_especialidad'):
            profesores=profesores.order_by(desc(ProfesorModel.especialidad))
            
        #Ordeno por id de usuario
        if request.args.get('sortby_nrUsuario'):
            profesores=profesores.outerjoin(ProfesorModel.id_usuario).group_by(ProfesorModel.id).order_by(func.count(UsuarioModel.id).desc())
        
        ### FIN FILTROS ####
        
        profesores = profesores.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)

        return jsonify({'profesores': [profesor.to_json() for profesor in profesores],
                  'total': profesores.total,
                  'pages': profesores.pages,
                  'page': page
                })
    
    @role_required(roles = ['admin'])
    def post(self):
        clases_ids = request.get_json().get('clases')
        profesor = ProfesorModel.from_json(request.get_json())
        
        if clases_ids:
            clases = ClaseModel.query.filter(ClaseModel.id.in_(clases_ids)).all()
            profesor.clases.extend(clases)
            
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json(), 201

class UsuarioProfesor(Resource): #A la clase UsuarioProfesor le indico que va a ser del tipo recurso(Resource)
    @jwt_required()
    @role_required(roles = ['admin', 'profesor', 'alumno'])
    def get(self, id):
        profesor = db.session.query(ProfesorModel).get_or_404(id)
        return profesor.to_json()
    
    @jwt_required()
    @role_required(roles = ['admin'])
    def delete(self, id):
        profesor = db.session.query(ProfesorModel).get_or_404(id)
        db.session.delete(profesor)
        db.session.commit()
        return '', 204
    @jwt_required()
    @role_required(roles = ['admin'])
    #Modificar el recurso usuario
    def put(self, id):
        profesor = db.session.query(ProfesorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(profesor, key, value)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json() , 201
