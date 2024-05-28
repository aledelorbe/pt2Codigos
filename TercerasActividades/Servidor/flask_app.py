from flask import Flask
from flask import render_template

# Crear la app
flask_app = Flask(__name__)


# DEFINICION DE RUTAS
@flask_app.route('/') 
def index():
   return render_template('inicio.html')

@flask_app.route('/inicio') 
def inicio():
   return render_template('inicio.html')

@flask_app.route('/aplicacion') 
def aplicacion():
   return render_template('aplicacion.html')


# Correr la app
if __name__ == '__name__':
   flask_app.run(debug=True) 