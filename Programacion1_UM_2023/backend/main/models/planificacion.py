from .. import db


alumnos_planificaciones = db.Table("alumnos_planificaciones",
    db.Column("id_alumnos",db.Integer,db.ForeignKey("alumno.id"),primary_key=True),
    db.Column("id_planificacion",db.Integer,db.ForeignKey("planificacion.id"),primary_key=True),
    )


class Planificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lunes = db.Column(db.String, nullable=False)
    martes = db.Column(db.String, nullable=False)
    miercoles = db.Column(db.String, nullable=False)
    jueves = db.Column(db.String, nullable=False)
    viernes = db.Column(db.String, nullable=False)
    alumnos = db.relationship('Alumno', secondary=alumnos_planificaciones, backref=db.backref('planificaciones', lazy='dynamic'))

    def __repr__(self):
        return '<Planificacion: %r >' % (self.id)

    def to_json(self):
        planificacion_json = {
            'id': self.id,
            'lunes': str(self.lunes),
            'martes': str(self.martes),
            'miercoles': str(self.miercoles),
            'jueves': str(self.jueves),
            'viernes': str(self.viernes),
        }
        return planificacion_json

    @staticmethod
    def from_json(planificacion_json):
        id = planificacion_json.get('id')
        lunes = planificacion_json.get('lunes')
        martes = planificacion_json.get('martes')
        miercoles = planificacion_json.get('miercoles')
        jueves = planificacion_json.get('jueves')
        viernes = planificacion_json.get('viernes')
        return Planificacion(id=id,
                    lunes=lunes,
                    martes=martes,
                    miercoles=miercoles,
                    jueves=jueves,
                    viernes=viernes,
                    )
