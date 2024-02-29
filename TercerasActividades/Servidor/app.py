from flask import Flask
from flask import render_template

# Crear la app
app = Flask(__name__)


# DEFINICION DE RUTAS
@app.route('/') 
def index():
   return render_template('inicio.html')

@app.route('/inicio') 
def inicio():
   return render_template('inicio.html')

@app.route('/aplicacion') 
def aplicacion():
   return render_template('aplicacion.html')

@app.route('/conjuntos') 
def conjuntos():
   return render_template('conjuntos.html')

# Correr la app
if __name__ == '__name__':
    app.run(debug=True) 