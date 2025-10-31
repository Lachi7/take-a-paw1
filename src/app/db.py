import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    # Absolute path beside run.py (…/src/takeapaw.db)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_sqlite_path = os.path.join(project_root, "takeapaw.db")
    sqlite_uri = f"sqlite:///{default_sqlite_path}"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", sqlite_uri)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)
    return db
