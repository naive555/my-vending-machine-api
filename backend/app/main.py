from fastapi import FastAPI
from app.api.router import api_router


app = FastAPI(title="Vending Machine API")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Vending Machine Backend Running"}