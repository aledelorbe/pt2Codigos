from flask_app import flask_app
from dash_app import crearDashApp

# Crear la aplicación Dash y conectarla a la aplicación Flask
def crear_app():
    dash_app = crearDashApp(flask_app)

    return dash_app

if __name__ == "__main__":
    dash = crear_app()
    flask_app.run(debug=True)

