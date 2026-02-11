from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from core.db import mongo

events_bp = Blueprint("events", __name__)

# BASIC CRUD 

# Get all events (with pagination + sorting)
@events_bp.route("/", methods=["GET"])
def get_events():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    sort_field = request.args.get("sort", "date")
    skip = (page - 1) * limit

    events = list(mongo.db.events.find().sort(sort_field, 1).skip(skip).limit(limit))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events), 200


# Get a single event by ID
@events_bp.route("/<string:event_id>", methods=["GET"])
def get_event(event_id):
    try:
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404
        event["_id"] = str(event["_id"])
        return jsonify(event), 200
    except Exception:
        return jsonify({"error": "Invalid event ID"}), 400


# Create new event (Admin only)
@events_bp.route("/", methods=["POST"])
@jwt_required()
def create_event():
    data = request.get_json()
    if not data or "name" not in data or "date" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    event = {
        "name": data["name"],
        "description": data.get("description", ""),
        "category": data.get("category", "General"),
        "price": float(data.get("price", 0)),
        "available_seats": int(data.get("available_seats", 100)),
        "location": data.get("location", {}),
        "date": data["date"],
        "created_at": data.get("created_at", "")
    }

    result = mongo.db.events.insert_one(event)
    return jsonify({
        "message": "Event created successfully",
        "event_id": str(result.inserted_id)
    }), 201


# Update an event
@events_bp.route("/<string:event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    try:
        data = request.get_json()
        result = mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"message": "Event updated successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid event ID"}), 400


# Delete an event
@events_bp.route("/<string:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    try:
        result = mongo.db.events.delete_one({"_id": ObjectId(event_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid event ID"}), 400


#ADVANCED QUERIES

# Search events
@events_bp.route("/search", methods=["GET"])
def search_events():
    query = {}
    category = request.args.get("category")
    city = request.args.get("city")
    location = request.args.get("location")
    max_price = request.args.get("max_price")

    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if city:
        query["city"] = {"$regex": city, "$options": "i"}
    if location:
        query["location.name"] = {"$regex": location, "$options": "i"}
    if max_price:
        query["price"] = {"$lte": float(max_price)}

    events = list(mongo.db.events.find(query))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events), 200


# Nearby events
@events_bp.route("/nearby", methods=["GET"])
def nearby_events():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = float(request.args.get("radius", 10)) * 1000  # km → meters

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude required"}), 400

    lat = float(lat)
    lon = float(lon)

    events = list(mongo.db.events.find({
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": radius
            }
        }
    }))

    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events), 200

# Aggregation: top categories
@events_bp.route("/stats/categories", methods=["GET"])
def category_stats():
    stats = list(mongo.db.events.aggregate([
        {"$group": {"_id": "$category", "total_events": {"$sum": 1}}},
        {"$sort": {"total_events": -1}},
        {"$limit": 3}
    ]))
    return jsonify(stats), 200

