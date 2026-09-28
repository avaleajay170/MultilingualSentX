from flask import Flask
from flask_cors import CORS
from app.db.connection import init_db
from app.routes.analyze import analyze_bp
from app.routes.dashboard import dashboard_bp
from app.routes.bulk import bulk_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()

    @app.route("/")
    def home():
        return "MultilingualSentX backend is running."

    app.register_blueprint(analyze_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(bulk_bp)

    return app