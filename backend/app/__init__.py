from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # Enable CORS for all routes and all origins
    CORS(app)
    # Alternatively, restrict CORS to a specific origin:
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
