from flask_app import flask_app
from dash_app import crearDashApp

# Crear la aplicación Dash y conectarla a la aplicación Flask
dash_app = crearDashApp(flask_app)


if __name__ == "__main__":
    flask_app.run(debug=True)
