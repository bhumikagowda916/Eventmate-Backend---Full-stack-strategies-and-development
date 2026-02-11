from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from core.db import init_db 
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB connection (uses .env MONGO_URI)
mongo = init_db(app) 

# JWT setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to EventMate API"})

# Import blueprints AFTER initializing app and DB
from routes.events_routes import events_bp
app.register_blueprint(events_bp, url_prefix="/events")

from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from routes.reviews_routes import reviews_bp
app.register_blueprint(reviews_bp, url_prefix="/reviews")

from routes.bookings_routes import bookings_bp
app.register_blueprint(bookings_bp, url_prefix="/bookings")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
