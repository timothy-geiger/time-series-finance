from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
