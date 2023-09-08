from flask_restful import Resource
from flask import request

PAGOS = {
      1: {'nombre':'Miguel', 'apellido':'Angel', 'estado':'0'},
      2: {'nombre':'Enzo', 'apellido':'Perez', 'estado':'1'}
}

class Pago(Resource):
    def get(self,id):
        #Verificar si existe el usuaroi
        if int(id) in PAGOS:
            #retorno usuario
            if PAGOS[int(id)]['estado']=='1':
                return {'message': 'Ultimo pago realizado'}, 200
            else:
                return {'message': 'Ultimo pago no realizado'}, 200
        #Si no existe 404
        return {'message':'El usuario no existe'}, 404
    
    def put(self,id):
        if int(id) in PAGOS:
            pago = PAGOS[int(id)]
            data = request.get_json()
            pago.update(data)
            return '', 201
        return '', 404


