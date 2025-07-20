from flask import Flask
import os
from routes.chat_routes import chat_bp

def create_app():
    """
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)

    # --- Flask Configuration ---
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    app.register_blueprint(chat_bp)
    return app

if __name__ == '__main__':
    # Create the Flask app instance
    app = create_app()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5001)