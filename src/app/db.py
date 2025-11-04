# src/app/db.py
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app, test_config=None):
    if test_config and 'SQLALCHEMY_DATABASE_URI' in test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = test_config['SQLALCHEMY_DATABASE_URI']
        print("Using test database configuration")
    else:
        database_url = os.getenv("DATABASE_URL")
        
        if database_url:
            if database_url.startswith('psql '):
                database_url = database_url[4:].strip()
            
            database_url = database_url.strip("'\"")
            
            if 'channel_binding=require' in database_url:
                database_url = database_url.replace('&channel_binding=require', '')
                database_url = database_url.replace('?channel_binding=require', '?')
                if database_url.endswith('?'):
                    database_url = database_url[:-1]
        
        print(f"Using database URL: {database_url[:50]}...")  # Log first 50 chars
        
        if not database_url:
            # Fallback for local development
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            default_sqlite_path = os.path.join(project_root, "takeapaw.db")
            database_url = f"sqlite:///{default_sqlite_path}"
            print("⚠️  Using SQLite fallback database")

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    if 'sqlalchemy' not in app.extensions:
        db.init_app(app)
        migrate.init_app(app, db)
    
    return db