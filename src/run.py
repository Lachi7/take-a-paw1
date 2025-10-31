# run.py
from app import create_app

if __name__ == "__main__":
    app = create_app()
    print("🎯 Starting Flask development server...")
    print("🌐 App at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
