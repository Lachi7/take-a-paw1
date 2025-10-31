import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    # brand-new Flask app (no legacy import)
    flask_app = Flask(__name__, static_folder="static", template_folder="templates")

    # secret key
    if not getattr(flask_app, "secret_key", None):
        flask_app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

    # DB
    from .db import init_db
    init_db(flask_app)

    # blueprints
    from .routes.auth import bp as auth_bp
    from .routes.pets import bp as pets_bp
    from .routes.admin import bp as admin_bp
    from .routes.quiz import bp as quiz_bp
    from .routes.system import bp as system_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(pets_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(quiz_bp)
    flask_app.register_blueprint(system_bp)

    print("🔗 Registered routes:")
    for r in flask_app.url_map.iter_rules():
        print(" ", r)

    return flask_app
