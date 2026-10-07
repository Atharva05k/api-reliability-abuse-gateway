# API Reliability & Abuse Detection Gateway

A production-style backend API built with **FastAPI and PostgreSQL** to demonstrate reliable request processing, duplicate protection, deterministic abuse detection, structured error handling, observability, and automated API testing.

The gateway accepts client requests, validates and authenticates them, prevents duplicate processing using idempotency keys, evaluates short-term request bursts using deterministic rule-based risk levels, and blocks excessive traffic using HTTP `429 Too Many Requests`.

This project was built as a backend engineering portfolio project with a focus on:

- API reliability
- Defensive backend design
- Request validation
- Idempotency
- Abuse and burst detection
- Database persistence
- Structured logging
- Metrics
- Automated testing
- Clean backend architecture

---

## Tech Stack

- Python 3.13
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- psycopg
- Uvicorn
- python-dotenv
- Pytest
- HTTPX / FastAPI TestClient
- Postman
- Git
- GitHub

---

# Core Features

## API Request Processing

- REST API built with FastAPI
- Pydantic request validation
- Enum-based request type validation
- Enum-based priority validation
- UUID-based request identifiers
- Request processing and routing layer
- Service-layer architecture

Supported request types:

- `REPORT_GENERATION`
- `DATA_EXPORT`
- `DATA_IMPORT`
- `NOTIFICATION`

Supported priorities:

- `LOW`
- `NORMAL`
- `HIGH`
- `URGENT`

---

## PostgreSQL Persistence

Requests are persisted in PostgreSQL using SQLAlchemy ORM.

The project includes:

- PostgreSQL database integration
- SQLAlchemy models
- Database session management
- Persistent request storage
- Request retrieval by ID
- Stored risk levels
- Unique idempotency protection

Database used during development:

```text
api_gateway