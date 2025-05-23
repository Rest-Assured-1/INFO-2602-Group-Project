import os
from flask import Flask
from .config import load_config
from .models import db  
from .views import apartment_views
from sqlalchemy import event
from sqlalchemy.engine import Engine

def create_app():
    app = Flask(__name__)
    
    # Config settings here (replace with actual config or config object)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY')

    db.init_app(app)

    app.register_blueprint(apartment_views)

    return app

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()