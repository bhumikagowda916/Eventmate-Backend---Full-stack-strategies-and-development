# EventMate – Backend REST API

## What this is

This repository contains the backend service for the EventMate event management system. It provides a RESTful API built with Flask to manage user authentication, event creation, and booking workflows.

The backend is designed using a modular architecture so that a separate frontend application can communicate with it through structured HTTP endpoints.

---

## Key capabilities

- User registration and login
- Event creation and retrieval
- Booking creation and management
- Modular route separation
- JSON-based lightweight data persistence
- RESTful API structure
- Postman collection included for endpoint testing

---

## Tech stack

- Python
- Flask
- JSON file-based data storage
- REST API design
- Postman for API validation

---

## Architecture overview

The backend follows a modular structure:

- `app.py` – Application entry point
- `routes/` – API endpoint definitions
- `core/` – Core business logic and database abstraction
- `data/` – JSON-based data storage
- `seed/` – Data seeding scripts
- `tests/` – API test reports and testing resources

This separation improves maintainability and supports future scalability.

---

## API functionality

### Authentication
- POST /register
- POST /login

### Events
- GET /events
- POST /events
- GET /events/<id>

### Bookings
- GET /bookings
- POST /bookings

(All endpoints return JSON responses.)

---

## Running the project locally

### 1. Clone the repository
```
git clone https://github.com/bhumikagowda916/Eventmate-Backend---Full-stack-strategies-and-development.git
```

### 2. Navigate into the project directory
```
cd Eventmate-Backend---Full-stack-strategies-and-development
```

### 3. Create a virtual environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Run the server
```
python app.py
```

The API will run at:
```
http://localhost:5000
```

---

## Data persistence

The system currently uses JSON files stored inside the `data/` directory to simulate a lightweight database. All read/write operations are abstracted through the `core` layer, allowing future migration to a relational database (e.g., PostgreSQL) with minimal structural changes.

---

## Testing

- Postman collection files are included for testing endpoints.
- API can be tested locally against `localhost:5000`.
- The `tests/` directory contains test reports.

---

## Future improvements

- Replace JSON storage with PostgreSQL or MySQL
- Implement JWT-based authentication
- Add password hashing for improved security
- Introduce automated unit and integration testing
- Containerise the application using Docker
- Deploy backend to a cloud platform (Azure / Render)

---

## Purpose of this project

This backend demonstrates:

- Modular Flask application structure
- RESTful API development
- Clean separation of concerns
- Structured repository organisation
- Iterative development with version control

It serves as a foundation for scalable backend service development and production-ready API design.
