from fastapi import FastAPI
from sqlalchemy import text
from app.api.router import api_router
from app.core.database import engine

app = FastAPI(title="Vending Machine API")

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Vending Machine Backend Running"}


@app.get("/health")
def health_check():
    from app.core.database import engine

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
