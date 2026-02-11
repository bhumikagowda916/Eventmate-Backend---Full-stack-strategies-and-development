from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from core.db import mongo

# Create Blueprint
reviews_bp = Blueprint('reviews', __name__)

# Get all reviews for a specific event
@reviews_bp.route('/<string:event_id>', methods=['GET'])
def get_reviews(event_id):
    try:
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)}, {"reviews": 1})
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event.get("reviews", [])), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add a new review
@reviews_bp.route('/<string:event_id>', methods=['POST'])
@jwt_required()
def add_review(event_id):
    try:
        data = request.get_json()
        if not data or "comment" not in data or "rating" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        review = {
            "_id": str(ObjectId()),
            "user_id": data.get("user_id"),
            "comment": data["comment"],
            "rating": data["rating"],
            "date": data.get("date", "")
        }

        result = mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$push": {"reviews": review}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Event not found"}), 404

        return jsonify({"message": "Review added successfully", "review_id": review["_id"]}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update review
@reviews_bp.route('/<string:event_id>/<string:review_id>', methods=['PUT'])
@jwt_required()
def update_review(event_id, review_id):
    try:
        data = request.get_json()
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})

        if not event:
            return jsonify({"error": "Event not found"}), 404

        reviews = event.get("reviews", [])
        updated = False

        for review in reviews:
            # safely check if '_id' key exists
            if review.get("_id") == review_id:
                review["comment"] = data.get("comment", review.get("comment"))
                review["rating"] = data.get("rating", review.get("rating"))
                review["date"] = data.get("date", review.get("date"))
                updated = True
                break

        if not updated:
            return jsonify({"error": "Review not found"}), 404

        mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": {"reviews": reviews}}
        )
        return jsonify({"message": "Review updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete review
@reviews_bp.route('/<string:event_id>/<string:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(event_id, review_id):
    try:
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        reviews = event.get("reviews", [])
        # Safely filter by _id even if key missing
        new_reviews = [r for r in reviews if str(r.get("_id", "")) != review_id]

        if len(new_reviews) == len(reviews):
            return jsonify({"error": "Review not found"}), 404

        mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": {"reviews": new_reviews}}
        )

        return jsonify({"message": "Review deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

