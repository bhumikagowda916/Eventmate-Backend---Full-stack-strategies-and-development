import json, random, uuid
from datetime import datetime, timedelta

random.seed(7)

# Cities and coordinates (lon, lat)
CITIES = {
    "London": (-0.1276, 51.5072),
    "Manchester": (-2.2426, 53.4808),
    "Birmingham": (-1.8904, 52.4862),
    "Leeds": (-1.5491, 53.8008),
    "Glasgow": (-4.2518, 55.8642),
    "Liverpool": (-2.9779, 53.4084),
    "Bristol": (-2.5879, 51.4545),
    "Edinburgh": (-3.1883, 55.9533),
    "Nottingham": (-1.1496, 52.9548),
    "Cardiff": (-3.1791, 51.4816),
}

# Categories + tags
CATEGORIES = {
    "Music": ["music", "live", "local"],
    "Sports": ["sports", "fitness", "competition"],
    "Food & Drink": ["food & drink", "tasting", "local"],
    "Technology": ["technology", "innovation", "talks"],
    "Art & Culture": ["art & culture", "gallery", "creative"],
    "Comedy": ["comedy", "standup", "fun"],
    "Fitness": ["fitness", "wellness", "outdoors"],
    "Education & Workshops": ["education", "workshop", "skills"],
    "Business & Networking": ["business", "networking", "startup"],
    "Film & Media": ["film", "screening", "media"],
}

REVIEW_COMMENTS = [
    "Loved it!", "Great event!", "Very well organized.", "Could be better.",
    "Amazing experience!", "Would attend again!", "Had a great time!"
]

def random_date_2025():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 31)
    d = start + timedelta(days=random.randint(0, (end - start).days))
    return d.strftime("%Y-%m-%d")

def object_id_like(n: int) -> str:
    """Generate a unique 24-char hex string (like a MongoDB ObjectId)."""
    return (uuid.uuid4().hex[:18] + f"{n:06x}")[:24]

def make_event(n: int) -> dict:
    city = random.choice(list(CITIES.keys()))
    lon, lat = CITIES[city]
    category = random.choice(list(CATEGORIES.keys()))
    return {
        "name": f"{category} Event {n}",      # ✅ Removed city name
        "city": city,                         # ✅ Added city field
        "category": category,
        "date": random_date_2025(),
        "price": round(random.uniform(5.0, 99.0), 2),
        "available_seats": random.randint(20, 200),
        "tags": CATEGORIES[category],
        "location": {
            "type": "Point",
            "coordinates": [round(lon, 4), round(lat, 4)]
        },
        "reviews": [
            {
                "user_id": random.randint(100, 300),
                "comment": random.choice(REVIEW_COMMENTS),
                "rating": random.randint(3, 5),
                "date": random_date_2025()
            },
            {
                "user_id": random.randint(100, 300),
                "comment": random.choice(REVIEW_COMMENTS),
                "rating": random.randint(3, 5),
                "date": random_date_2025()
            }
        ]
    }

# Generate 100 events
events = [make_event(i + 1) for i in range(100)]

# Save to JSON
with open("events.json", "w", encoding="utf-8") as f:
    json.dump(events, f, indent=4)

print("Created events.json with 100 events (with separate city field).")
