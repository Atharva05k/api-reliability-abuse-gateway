# API Reliability & Abuse Detection Gateway

A production-style Python backend project built with FastAPI and PostgreSQL for processing, validating, storing, and monitoring API requests.

The project is being developed incrementally to demonstrate backend engineering concepts such as API design, database persistence, request processing, authentication, idempotency, abuse detection, risk scoring, logging, and testing.

## Tech Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- psycopg
- Uvicorn
- Pytest
- Git & GitHub

## Current Features

- FastAPI REST API
- Pydantic request validation
- Request type and priority validation using Enums
- UUID-based request identifiers
- PostgreSQL database integration
- SQLAlchemy ORM models
- Database session management
- Persistent request storage
- Retrieve requests by request ID
- Proper HTTP status codes
- 404 handling for missing requests
- Service-layer architecture

## API Endpoints

### Health Check

```http
GET /