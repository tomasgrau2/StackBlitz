from .. import db
from . import UsuarioModel

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    r_usuario = db.relationship("Usuario", back_populates="r_profesor")

    def __repr__(self):
        return '<Alumno: %r >' % (self.id)

    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        profesor_json = {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'especialidad': self.especialidad,
            'usuario' : self.usuario.to_json()
        }
        return profesor_json

    def to_json_complete(self):
        profesor_json = {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'especialidad': self.especialidad,
            'usuario' : self.usuario.to_json(),
        }
        return profesor_json


    def to_json_short(self):
        profesor_json = {
            'id': self.id,
            'especialidad': str(self.especialidad),
        }
        return profesor_json

    @staticmethod
    def from_json(clase_json):
        id = clase_json.get('id')
        id_usuario = clase_json.get('id_usuario')
        especialidad = clase_json.get('especialidad')
        return Profesor(id=id,
                    id_usuario=id_usuario,
                    especialidad=especialidad
                    )

