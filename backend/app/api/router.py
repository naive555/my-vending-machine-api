from fastapi import APIRouter
from app.api.v1 import products, purchase, cash


api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(purchase.router, prefix="/purchase", tags=["purchase"])
api_router.include_router(cash.router, prefix="/cash", tags=["cash"])
