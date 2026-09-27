from flask import Flask
from app.db.connection import init_db
from app.routes.analyze import analyze_bp

def create_app():
    app = Flask(__name__)

    init_db()

    @app.route("/")
    def home():
        return "MultilingualSentX backend is running."

    app.register_blueprint(analyze_bp)

    return app