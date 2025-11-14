import os
import sys

# Add parent directory to path to import our app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

try:
    from app import app, init_db
    
    # Initialize database on first import
    with app.app_context():
        try:
            init_db()
            print("Database initialized successfully for production")
        except Exception as e:
            print(f"Database initialization error: {e}")
            # Continue anyway, database might already exist
    
    # Export the app for Vercel
    application = app
    
except Exception as e:
    print(f"Error importing app: {e}")
    # Create a minimal Flask app as fallback
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error():
        return f"Application failed to load: {str(e)}", 500

if __name__ == "__main__":
    application.run()