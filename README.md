# My Vending Machine API

A simple Vending Machine backend API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**.  
This project is Docker-ready and supports both local development and Docker deployment.

---

## Features

- CRUD for Products
- Cash management (insert / withdraw)
- Purchase products with stock check and change calculation
- Health check endpoint
- Database migrations with Alembic
- Dockerized backend + PostgreSQL

---

## Prerequisites

- Python 3.14+
- Docker & Docker Compose
- Git

---

## Environment Variables

Create a `.env` file in the `backend/` folder (or copy `.env.example`) and set your values:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/vending
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_DB=vending
```

You can copy the example file:

```
cp .env.example .env
```

## Running Locally

1. Create virtual environment:

```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run database migrations:

```
alembic upgrade head
```

4. Run the API server:

```
uvicorn app.main:app --reload
```

API will run at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

## Running with Docker Compose

1. Build and start services:

```
docker-compose up --build
```

2. The backend API will be available at: http://localhost:8000

3. PostgreSQL is exposed at port 5432 (configured in docker-compose)

## Alembic Migrations

Create a new migration after changing models:

```
alembic revision --autogenerate -m "Migration message"
```

Apply migrations:

```
alembic upgrade head
```

## API Endpoints (basic)

- GET /api/v1/products -> list products
- POST /api/v1/products -> create product
- GET /api/v1/products/{id} -> get product
- PUT /api/v1/products/{id} -> update product
- DELETE /api/v1/products/{id} -> delete product
- POST /api/v1/purchase -> purchase a product
- GET /health -> health check
