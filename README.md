# AI-Enhanced Volunteer Matching Platform — Backend

## What this is
This repository contains the backend for an AI-driven volunteering platform designed to help organisations and volunteers connect more effectively. The backend provides REST APIs for user accounts, opportunity management, feedback handling, and AI-powered matching features.

The system is built as a modular service so the frontend (separate repository) can communicate with it through API endpoints.

## Key capabilities
- Account registration and login (volunteers and organisations)
- Volunteer profile management (skills, interests, availability, location)
- Opportunity posting and browsing (create, update, view)
- Feedback submission and storage
- AI-assisted features:
  - Opportunity recommendations using similarity matching
  - Engagement prediction using a classification model
  - Sentiment analysis of feedback text

## Tech stack (edit if needed)
- Language: [Python / JavaScript]
- Backend framework: [Flask / Django / Node.js + Express]
- Database: [SQLite / MySQL / PostgreSQL / MongoDB]
- ML/NLP: [scikit-learn, TF-IDF, KNN/Cosine Similarity, Decision Tree/Naive Bayes]
- APIs: REST

## High-level architecture
- Frontend (React) calls backend via REST endpoints
- Backend handles validation, authentication, database operations
- ML/NLP logic produces:
  - match scores / rankings
  - engagement likelihood prediction
  - sentiment labels/scores for feedback

## Project structure (example)
- `src/` or `app/` — main backend application
- `routes/` or `views/` — API endpoints
- `models/` — database models / schemas
- `ml/` — recommendation, prediction, sentiment components
- `requirements.txt` or `package.json` — dependencies

## How to run locally

### Option 1 — Python (Flask/Django)
1. Create a virtual environment
   - Windows:
     `python -m venv venv`  
     `venv\Scripts\activate`
   - macOS/Linux:
     `python3 -m venv venv`  
     `source venv/bin/activate`

2. Install dependencies  
   `pip install -r requirements.txt`

3. Start the server  
   - Flask example: `python app.py`
   - Django example: `python manage.py runserver`

Backend will run on: `http://localhost:[PORT]`  
(PORT depends on your configuration.)

### Option 2 — Node.js (Express)
1. Install dependencies  
   `npm install`

2. Start the server  
   `npm start` (or `node server.js` depending on your setup)

Backend will run on: `http://localhost:[PORT]`

## Configuration notes
- Do not commit secrets (API keys, passwords).
- Use a `.env` file locally for configuration.
- Make sure `.env` stays ignored via `.gitignore`.

## API endpoints (fill with your real ones)
- `POST /auth/register`
- `POST /auth/login`
- `GET /opportunities`
- `POST /opportunities`
- `GET /recommendations`
- `POST /feedback`

## Future improvements
- Add stronger validation and consistent error responses
- Add role-based access control (admin/organisation/volunteer)
- Add automated tests for endpoints
- Containerise with Docker
- Deploy the API (Azure / Render / Railway)
