# Campus Parking Slot Tracker

A lightweight web application built with Python and Flask to track real-time parking space availability across campus parking lots. Features real-time vehicle check-in and checkout, dynamic slot counting, automated input validation, and continuous integration and deployment (CI/CD) pipelines.

---

## Live Deployment
- **Production URL:** [https://campus-parking-tracker.onrender.com](https://campus-parking-tracker.onrender.com)
- **Health Endpoint:** [https://campus-parking-tracker.onrender.com/health](https://campus-parking-tracker.onrender.com/health)
- **Slots API:** [https://campus-parking-tracker.onrender.com/api/slots](https://campus-parking-tracker.onrender.com/api/slots)

---

## Features
- **Real-Time Availability:** Dynamic counters tracking total, occupied, and remaining parking bays.
- **Vehicle In/Out Management:** Park vehicles with automatic timestamp logging and exit clearance.
- **RESTful Endpoints:** Standardized JSON endpoints for slot stats and health monitoring.
- **Automated CI/CD Pipeline:** GitHub Actions automation running code linting and unit test suites on push.
- **Automated Deployment:** Production deployment on Render triggered via webhook upon successful test completion.

---

## Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Frontend:** HTML5, CSS (Bootstrap-styled dashboard)
- **Testing & Quality:** Pytest, Flake8
- **CI/CD:** GitHub Actions
- **Hosting:** Render Web Services

---

## How It Works (DevOps Flow)
1. Code changes are pushed to the `main` branch on GitHub.
2. A GitHub Actions workflow runs `flake8` to check for syntax issues and `pytest` to run unit tests.
3. If tests pass, GitHub Actions calls the Render Deploy Hook via a webhook secret (`RENDER_DEPLOY_HOOK`).
4. Render pulls the latest commit and runs the app with Gunicorn.
5. If any test fails, deployment is blocked automatically.

---

## Local Setup & Installation

### 1. Clone repo
git clone https://github.com/agees06/campus-parking-tracker.git
cd campus-parking-tracker

### 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install packages
pip install -r requirements.txt

### 4. Start Flask server
python3 app.py

Open `http://127.0.0.1:5000` in your browser.

## Running Tests & Checks

Run unit tests:
pytest -v

Run linter:
flake8 app.py test_app.py --count --select=E9,F63,F7,F82 --show-source --statistics