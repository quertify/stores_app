from flask import Flask
from app.routes.store_routes import main
def create_app():
    app = Flask(__name__)
    
    # Register blueprints (if any)
    app.register_blueprint(main)

    return app