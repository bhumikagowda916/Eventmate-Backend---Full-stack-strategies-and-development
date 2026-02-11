from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from bson import ObjectId
from core.db import mongo

auth_bp = Blueprint('auth', __name__)

# REGISTER USER 
@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        if mongo.db.users.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400

        hashed_pw = generate_password_hash(password)
        mongo.db.users.insert_one({
            "username": username,
            "password": hashed_pw
        })

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# LOGIN USER 
@auth_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        user = mongo.db.users.find_one({"username": username})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=2))

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# GET USER PROFILE
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# UPDATE USER PROFILE 
@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        updates = {}
        if "username" in data:
            updates["username"] = data["username"]
        if "password" in data:
            updates["password"] = generate_password_hash(data["password"])

        if not updates:
            return jsonify({"error": "No valid fields to update"}), 400

        result = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# DELETE USER PROFILE 
@auth_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    try:
        user_id = get_jwt_identity()
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User account deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
