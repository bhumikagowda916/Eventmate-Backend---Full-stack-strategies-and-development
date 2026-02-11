import json, random, uuid
from datetime import datetime

random.seed(10)

def object_id_like(n: int) -> str:
    """Generate a pseudo MongoDB ObjectId."""
    return (uuid.uuid4().hex[:18] + f"{n:06x}")[:24]

# Example names for users
NAMES = [
    "Alice", "Bob", "Charlie", "David", "Ella", "Finn", "Grace", "Henry", "Ivy", "Jack",
    "Kara", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Ryan", "Sophia", "Tom",
    "Uma", "Vera", "Will", "Xena", "Yara"
]

users = []
for i, name in enumerate(NAMES[:25], start=1):
    username = name.lower() + str(random.randint(100,999))
    user = {
        "_id": object_id_like(i),
        "username": username,
        "email": f"{username}@example.com",
        "password": "Password123",  # plaintext for dataset, hashed in real app
        "role": "admin" if i <= 3 else "user",
        "created_at": datetime.utcnow().isoformat()
    }
    users.append(user)

with open("users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=4)

print(" Created users.json with 25 users.")
