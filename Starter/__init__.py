from flask import Flask
import psycopg2.extras
from os import path

DB_HOST = "localhost"
DB_NAME = "socketio"
DB_USER = "postgres"
DB_PASS = "5599"
DB_PORT = "5432"

def create_app():
    app = Flask(__name__)
    app.secret_key = "gygs"
    
    views_blueprint = None
    auth_blueprint = None
    
    try:
        from .views import views
        views_blueprint = views
    except ImportError as e:
        print(f"Error importing views blueprint: {e}")
    
    try:
        from .auth import auth
        auth_blueprint = auth
    except ImportError as e:
        print(f"Error importing auth blueprint: {e}")
    
    if views_blueprint:
        app.register_blueprint(views_blueprint, url_prefix="/")
    
    if auth_blueprint:
        app.register_blueprint(auth_blueprint, url_prefix="/")
    
    return app
