from flask import Flask
from dotenv import load_dotenv
import os
from routes.api import api_bp
from models.database import initialize_database

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize database
initialize_database()

# Register API blueprint
app.register_blueprint(api_bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
