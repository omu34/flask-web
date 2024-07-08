from flask import Flask
import psycopg2.extras
from os import path

DB_HOST = "localhost"
DB_NAME = "astudents"
DB_USER = "postgres"
DB_PASS = "55"
DB_PORT = "55"

def create_app():
    app = Flask(__name__)
    app.secret_key = "gygs"
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
