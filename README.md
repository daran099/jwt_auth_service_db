# JWT Auth Service

## Description

REST API authentication service built with FastAPI.

The project implements:

* JWT authentication
* Refresh token rotation
* Role-based authorization
* PostgreSQL integration
* Dockerized deployment
* Automated tests with Pytest

---

## Tech Stack

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* PyJWT
* Passlib (Argon2)
* Docker
* Pytest

---

## Project Structure

```text
jwt_auth_service_db/
├── core/           # Config, dependencies, security
├── db/             # Database engine and session
├── models/         # SQLAlchemy models
├── repositories/   # Database query layer
├── routes/         # API endpoints
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── tests/          # Automated tests
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```

---

## Features

* User registration and login
* JWT access tokens
* Refresh token rotation
* Logout support
* Password hashing with Argon2
* Admin/User roles
* PostgreSQL persistence
* Docker support
* API and service layer tests

---

## Running the Project

Build and start containers:

```bash
docker compose up --build
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint    | Description          |
| ------ | ----------- | -------------------- |
| POST   | `/register` | Register new user    |
| POST   | `/login`    | Login user           |
| POST   | `/refresh`  | Refresh access token |
| POST   | `/logout`   | Logout user          |

---

## Running Tests

```bash
pytest
```

---

## Notes

The project follows a layered architecture with separated routes, services, and database access logic.
