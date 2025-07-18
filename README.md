# CRUD User Service API

A modern and minimal REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite** for performing full CRUD (Create, Read, Update, Delete) operations on user data. Includes a simple UI built with **Tailwind CSS**.

### 

https://github.com/user-attachments/assets/285cb7e0-2c50-4587-b7ff-5851f455529b


---

## 🧩 Features

- ✅ Full CRUD API for user data
- 🎯 Partial field updates supported
- 💻 Web UI built with Tailwind CSS
- 🔒 SQLite auto-initialized
- 📄 Swagger API docs at `/docs`
- ⚡ Fast and easy setup

---

## 🛠 Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLite](https://www.sqlite.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Uvicorn](https://www.uvicorn.org/)

---

## ⚙️ Getting Started

### 📦 Prerequisites

- Python 3.8+
- Git
- Virtualenv (recommended)

### 🔧 Installation


## Clone the repo
```bash
git clone https://github.com/Harshitkumargit/crud-user-service-api.git
cd crud-user-service-api
```

## Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Create requirements.txt
```bash
echo "fastapi==0.115.0
uvicorn==0.30.6
sqlalchemy==2.0.35
pydantic==2.9.2" > requirements.txt
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the application
```bash
uvicorn main:app --reload
```

# Usage

## 🌐 Web Interface

### Home Page: Visit http://127.0.0.1:8000/ for an overview.


### Manage Users: Go to http://127.0.0.1:8000/manage-users to:


### Add a user (email, name, optional age).


### Delete a user by ID.


### View all users in a table.
