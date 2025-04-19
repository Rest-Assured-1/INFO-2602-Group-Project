from flask import Flask
from .models import db  # assuming you use SQLAlchemy
from .views import apartment_views  # Import from views/__init__.py

def create_app():
    app = Flask(__name__)
    
    # Config settings here (replace with actual config or config object)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your-secret-key'

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(apartment_views)

    return app
