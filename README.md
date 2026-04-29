# 📌 Issue Tracker (FastAPI + PostgreSQL)

A mini Issue Tracking System built using FastAPI, SQLAlchemy, PostgreSQL, and Docker.

---

## 🚀 Features

- User Authentication (JWT)
- Project Management
- Issue Creation & Management
- Assign Issues to Users
- Issue Status Updates
- PostgreSQL Database
- Dockerized Setup (App + DB)

---

## 📦 Clone Repository

```bash
git clone git@github.com-vishal3064:walavishal/issuetracker.git
cd issuetracker
```

---

## ⚙️ Run with Docker (Recommended)

### Build and start containers
```bash
docker-compose up --build
```

### Run in background
```bash
docker-compose up -d --build
```

### Stop containers
```bash
docker-compose down
```

### Reset database
```bash
docker-compose down -v
```

---

## 🌐 Access

- API Docs: http://localhost:8000/docs
- API Base: http://localhost:8000

---

## 🐍 Local Setup

### Create venv
```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run server
```bash
uvicorn app.main:app --reload
```

---

## 🗄️ DB Config (Docker)

- Host: db
- Port: 5432
- DB: issuetracker
- User: postgres
- Password: postgres
