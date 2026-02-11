from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from core.db import mongo

bookings_bp = Blueprint("bookings", __name__)

# GET ALL BOOKINGS 
@bookings_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_bookings():
    try:
        user_id = str(get_jwt_identity())

        query = {"user_id": {"$in": [user_id, ObjectId(user_id)]}}

        if "status" in request.args:
            query["status"] = request.args["status"]

        bookings = list(mongo.db.bookings.find(query))

        for b in bookings:
            b["_id"] = str(b["_id"])
            if isinstance(b.get("event_id"), ObjectId):
                b["event_id"] = str(b["event_id"])
            if isinstance(b.get("user_id"), ObjectId):
                b["user_id"] = str(b["user_id"])
            if isinstance(b.get("created_at"), datetime):
                b["created_at"] = b["created_at"].isoformat()

        return jsonify(bookings), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET SINGLE BOOKING 
@bookings_bp.route("/<string:booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    try:
        booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})

        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking["_id"] = str(booking["_id"])
        if isinstance(booking.get("event_id"), ObjectId):
            booking["event_id"] = str(booking["event_id"])
        if isinstance(booking.get("user_id"), ObjectId):
            booking["user_id"] = str(booking["user_id"])
        if isinstance(booking.get("created_at"), datetime):
            booking["created_at"] = booking["created_at"].isoformat()

        return jsonify(booking), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


#CREATE NEW BOOKING
@bookings_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    try:
        user_id = str(get_jwt_identity())
        data = request.get_json()

        if not data or "event_id" not in data:
            return jsonify({"error": "Missing required field: event_id"}), 400

        event_id = data["event_id"]
        ticket_count = int(data.get("ticket_count", 1))

        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        if event["available_seats"] < ticket_count:
            return jsonify({"error": "Not enough available seats"}), 400

        # Check for duplicate confirmed booking
        existing = mongo.db.bookings.find_one({
            "user_id": user_id,
            "event_id": ObjectId(event_id),
            "status": "confirmed"
        })
        if existing:
            return jsonify({"error": "You already booked this event"}), 400

        booking = {
            "user_id": user_id,
            "event_id": ObjectId(event_id),
            "ticket_count": ticket_count,
            "status": "confirmed",
            "created_at": datetime.utcnow()
        }

        result = mongo.db.bookings.insert_one(booking)

        # Reduce available seats in event
        mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$inc": {"available_seats": -ticket_count}}
        )

        booking["_id"] = str(result.inserted_id)
        booking["event_id"] = str(booking["event_id"])
        booking["created_at"] = booking["created_at"].isoformat()

        return jsonify({"message": "Booking successful", "booking": booking}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#UPDATE BOOKING STATUS
@bookings_bp.route("/<string:booking_id>", methods=["PUT"])
@jwt_required()
def update_booking(booking_id):
    try:
        user_id = str(get_jwt_identity())
        data = request.get_json()

        if not data or "status" not in data:
            return jsonify({"error": "Missing status field"}), 400

        result = mongo.db.bookings.update_one(
            {"_id": ObjectId(booking_id), "user_id": {"$in": [user_id, ObjectId(user_id)]}},
            {"$set": {"status": data["status"]}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Booking not found"}), 404

        return jsonify({"message": "Booking updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# DELETE BOOKING 
@bookings_bp.route("/<string:booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):
    try:
        user_id = str(get_jwt_identity())

        booking = mongo.db.bookings.find_one({
            "_id": ObjectId(booking_id),
            "user_id": {"$in": [user_id, ObjectId(user_id)]}
        })
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        mongo.db.bookings.delete_one({"_id": ObjectId(booking_id)})

        # Restore available seats when deleted
        mongo.db.events.update_one(
            {"_id": booking["event_id"]},
            {"$inc": {"available_seats": booking.get("ticket_count", 1)}}
        )

        return jsonify({"message": "Booking deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
