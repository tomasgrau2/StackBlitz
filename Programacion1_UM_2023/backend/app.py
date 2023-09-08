from main import create_app
import os
from main import db

#Llamada a la funcion que retorna la app
app = create_app()

#Hay que hacer push del contexto de la app

app.app_context().push()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=os.getenv('PORT'))