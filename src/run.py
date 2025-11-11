# run.py
from app import create_app
from app.db import db

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Creates all tables defined in your models
        print("✅ Tables created (if they didn't exist)")
    print("🎯 Starting Flask development server...")
    print("🌐 App at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
