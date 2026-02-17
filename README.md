# 🔗 URL Shortener

A production-ready URL shortener built using FastAPI and PostgreSQL.

## 🚀 Features

- Base62 encoding
- PostgreSQL persistence
- Click analytics
- Dashboard UI
- Docker support

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Bootstrap
- Docker

## ▶ Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Set environment variables in .env

3. Run:
   uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000

## 🐳 Run With Docker

docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
