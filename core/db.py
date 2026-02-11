from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

def init_db(app):
    """Initialize MongoDB connection with Flask app"""
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    return mongo
