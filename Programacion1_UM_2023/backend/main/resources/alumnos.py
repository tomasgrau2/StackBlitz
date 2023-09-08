from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import AlumnoModel, PlanificacionModel, UsuarioModel
from sqlalchemy import func, desc, asc
from main.auth.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
class UsuariosAlumnos(Resource):
    #obtener lista de los alumnos
    @jwt_required()
    @role_required(roles = ["admin",'profesor'])
    def get(self):
        page = 1
        per_page = 10
        alumnos = db.session.query(AlumnoModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        #Busqueda por nro_socio
        if request.args.get('nro_socio'):
            alumnos=alumnos.filter(AlumnoModel.nro_socio.like("%"+request.args.get('nro_socio')+"%"))
            
        #Busqueda por id_usuario
        if request.args.get('id_usuario'):
            alumnos=alumnos.filter(AlumnoModel.id_usuario.like("%"+request.args.get('id_usuario')+"%"))
            
        #Orden por id_usuario
        if request.args.get('sortby_usuarios'):
            alumnos=alumnos.order_by(desc(AlumnoModel.id_usuario))

        #Obtener valor paginado
        alumnos = alumnos.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)


        return jsonify({'alumnos': [alumno.to_json() for alumno in alumnos],
                  'total': alumnos.total,
                  'pages': alumnos.pages,
                  'page': page
                })
    
    @jwt_required()
    @role_required(roles = ['admin', 'profesor'])
    def post(self):
        planificaciones_ids = request.get_json().get('planificaciones')
        alumno = AlumnoModel.from_json(request.get_json())
        
        if planificaciones_ids:
            planificaciones = PlanificacionModel.query.filter(PlanificacionModel.id.in_(planificaciones_ids)).all()
            alumno.planificaciones.extend(planificaciones)
            
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201

class UsuarioAlumno(Resource): #A la clase usuarioalumno le indico que va a ser del tipo recurso(Resource)
    #obtener recurso
    @jwt_required()
    @role_required(roles = ['admin', 'profesor'])
    def get(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        return alumno.to_json()
    
    #eliminar recurso
    @jwt_required()
    @role_required(roles = ['admin', 'profesor'])
    def delete(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        db.session.delete(alumno)
        db.session.commit()
        return '', 204
    #Modificar el recurso usuario
    @jwt_required()
    @role_required(roles = ['admin', 'profesor'])
    def put(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(alumno, key, value)
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json() , 201
