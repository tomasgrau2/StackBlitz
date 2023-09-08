from .. import db 
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(10), nullable=False, server_default='users')
    r_alumno = db.relationship('Alumno', back_populates='r_usuario',cascade='all, delete-orphan')
    r_profesor = db.relationship('Profesor', back_populates='r_usuario',cascade='all, delete-orphan')


    #Getter de la contraseña plana no permite leerla
    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')
    #Setter de la contraseña toma un valor en texto plano
    # calcula el hash y lo guarda en el atributo contrasena
    @plain_password.setter
    def plain_password(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)
    #Método que compara una contraseña en texto plano con el hash guardado en la db
    def validate_pass(self,contrasena):
        return check_password_hash(self.contrasena, contrasena)


    def __repr__(self):
        return '<Usuario: %r >' % (self.nombre)
    #Convertir objeto en JSON
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'apellido': str(self.apellido),
            'dni': int(self.dni),
            'edad': int(self.edad),
            'email':str(self.email),
            'contrasena': str(self.contrasena),

        }
        return usuario_json

    def to_json_complete(self):
        r_alumno = [r_alumno.to_json() for r_alumno in self.r_alumno]
        r_profesor = [r_profesor.to_json() for r_profesor in self.r_profesor]
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'apellido': str(self.apellido),
            'dni': int(self.dni),
            'edad': int(self.edad),
            'email':str(self.email),
            'contrasena': str(self.contrasena),
            'r_alumno':r_alumno,
            'r_profesor':r_profesor
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
        }
        return usuario_json

    @staticmethod
    #Convertir JSON a objeto
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        apellido = usuario_json.get('apellido')
        dni = usuario_json.get('dni')
        edad = usuario_json.get('edad')
        email = usuario_json.get('email')
        contrasena = usuario_json.get('contrasena')
        rol = usuario_json.get('rol')
        return Usuario(id=id,
                    nombre=nombre,
                    apellido=apellido,
                    dni=dni,
                    edad=edad,
                    email=email,
                    plain_password=contrasena,
                    rol=rol
                    )