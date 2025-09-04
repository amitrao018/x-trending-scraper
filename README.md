X Trending Scraper

A full-stack application that scrapes the top 5 trending topics from X (formerly Twitter) and displays them on a dashboard.

Backend: FastAPI + Selenium + PostgreSQL

Frontend: React.js

The scraper logs in to X, fetches the top trends, stores them in a database, and serves the data via an API.

Features

Scrapes top 5 trending topics under the “What’s Happening” section.

Logs each run with:

Unique ID

Trend names

Run timestamp

IP address

Stores data in PostgreSQL.

Frontend dashboard displays trends in a clean, responsive interface.

Fully deployed and accessible publicly.

Live Demo

Backend (API/Server): https://x-trending-scraper-1.onrender.com

Frontend (Web Dashboard): https://x-trending-scraper-ten.vercel.app/

Tech Stack

Backend:

Python 3.13

FastAPI

Selenium (Chrome WebDriver)

SQLAlchemy (PostgreSQL)

Requests

dotenv

Frontend:

React.js

Fetch API / Axios (for backend data)

CSS (responsive design)

Installation
Backend

Clone the repo:

git clone https://github.com/amitrao018/x-trending-scraper.git
cd x-trending-scraper/backend


Install dependencies:

pip install -r requirements.txt


Set environment variables in .env:

X_USERNAME=your_x_username
X_PASSWORD=your_x_password
DATABASE_URL=postgresql://user:password@host:port/dbname


Run the server:

uvicorn app.main:app --reload

Frontend

Navigate to frontend:

cd ../frontend


Install dependencies:

npm install


Run the React app:

npm run dev

Usage
Trigger a Scrape

Send a POST request to the backend:

curl -X POST https://x-trending-scraper-1.onrender.com/runs


Response JSON example:

{
  "run_time": "2025-09-04T10:15:00Z",
  "trend1": "#Trending1",
  "trend2": "#Trending2",
  "trend3": "#Trending3",
  "trend4": "#Trending4",
  "trend5": "#Trending5",
  "ip_address": "123.123.123.123"
}

Frontend Dashboard

Open https://x-trending-scraper-ten.vercel.app/
 to view the top trends in real-time.

Project Structure
x-trending-scraper/
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── scraper.py       # Selenium scraper
│   │   └── models.py        # SQLAlchemy models
│   ├── requirements.txt
│   └── apt.txt              # OS dependencies (Chrome)
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── package.json
│
└── README.md

Notes

Make sure apt.txt is in the backend folder for Render deployment to install Chrome dependencies.

Use .env to store sensitive credentials.

Each scraper run uses the server's IP. For rotating IPs, integrate ProxyMesh or another proxy service.

The scraper requires Chrome to be installed on the server. Render automatically installs it using apt.txt.

Author

Amit Rao – Frontend & Backend Developer
Mumbai, India

GitHub: amitrao018
