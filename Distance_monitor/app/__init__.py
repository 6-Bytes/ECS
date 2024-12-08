from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions here if needed
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app




