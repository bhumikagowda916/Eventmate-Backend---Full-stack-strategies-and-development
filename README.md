EventMate – Backend API
Overview

EventMate is a RESTful backend service built to support a full-stack event management application. The API handles user authentication, event creation, and booking workflows using a modular Flask-based architecture.

The system is designed with separation of concerns in mind, dividing authentication, event logic, and booking operations into structured route modules. This backend communicates with a frontend client via HTTP requests and returns JSON responses.

Core Features

User registration and login

Event creation and retrieval

Booking management

Modular route architecture

JSON-based data persistence

RESTful API design principles

Postman collection for endpoint testing

Tech Stack

Language: Python

Framework: Flask

Data Storage: JSON files (lightweight persistence layer)

API Testing: Postman

Architecture Style: Modular REST API

Architecture

The backend is organised into logical components:

eventmate-backend/
│
├── app.py                # Application entry point
├── requirements.txt      # Python dependencies
│
├── routes/               # API endpoint definitions
│   ├── auth_routes.py
│   ├── events_routes.py
│   └── bookings_routes.py
│
├── core/                 # Core business logic & utilities
│   └── db.py
│
├── data/                 # JSON-based data storage
│   ├── users.json
│   ├── events.json
│   └── bookings.json
│
├── tests/                # Testing files & API reports
│
└── seed/                 # Data seeding scripts

API Functionality

Authentication:

Register new users

Login validation

Events:

Create event

View all events

Retrieve event by ID

Bookings:

Create booking

View bookings

Associate bookings with events

All endpoints follow REST principles and return JSON responses.

Running the Project Locally
1. Clone repository
git clone https://github.com/YOUR_USERNAME/Eventmate-Backend---Full-stack-strategies-and-development.git

2. Navigate into project
cd Eventmate-Backend---Full-stack-strategies-and-development

3. Create virtual environment

Windows:

python -m venv venv
venv\Scripts\activate


Mac/Linux:

python3 -m venv venv
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Run server
python app.py


The API will run on:

http://localhost:5000

Testing the API

A Postman collection is included to test endpoints easily.

Import:

EventMate.postman_collection.json

EventMate.postman_environment.json

into Postman and execute requests against the local server.

Design Decisions

JSON files were used for lightweight persistence during development.

Routes are separated into dedicated modules to improve maintainability.

Data handling logic is abstracted into db.py to reduce duplication.

REST conventions were followed for clean and predictable endpoint structure.

Future Improvements

Replace JSON storage with relational database (PostgreSQL or MySQL)

Implement JWT-based authentication

Add input validation and error handling middleware

Introduce automated unit testing

Deploy backend to cloud platform (Azure or Render)
