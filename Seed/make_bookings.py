import json, random, os
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect manually to MongoDB
client = MongoClient(MONGO_URI)
db = client["eventmate"]

random.seed(20)

def generate_bookings():
    users = list(db.users.find({}, {"_id": 1}))
    events = list(db.events.find({}, {"_id": 1, "name": 1}))

    if not users or not events:
        print(" No users or events found. Please check your database.")
        return

    bookings = []

    for i in range(70):
        user = random.choice(users)
        event = random.choice(events)

        booking = {
            "_id": ObjectId(),  # Real ObjectId
            "user_id": ObjectId(user["_id"]),  # Stored as ObjectId, not string
            "event_id": ObjectId(event["_id"]),  # Stored as ObjectId, not string
            "ticket_count": random.randint(1, 5),
            "status": random.choice(["confirmed", "cancelled", "pending"]),
            "created_at": datetime.utcnow(),
        }

        bookings.append(booking)

    # Insert directly into MongoDB
    db.bookings.delete_many({})  # optional: clear old test data
    db.bookings.insert_many(bookings)
    print("Inserted 70 bookings into MongoDB with valid ObjectIds.")

    # Also save a readable version locally
    exportable_bookings = [
        {
            "_id": str(b["_id"]),
            "user_id": str(b["user_id"]),
            "event_id": str(b["event_id"]),
            "ticket_count": b["ticket_count"],
            "status": b["status"],
            "created_at": b["created_at"].isoformat(),
        }
        for b in bookings
    ]

    os.makedirs("data", exist_ok=True)
    with open("data/bookings.json", "w", encoding="utf-8") as f:
        json.dump(exportable_bookings, f, indent=4)

    print("Also saved bookings.json locally for reference.")


if __name__ == "__main__":
    generate_bookings()
