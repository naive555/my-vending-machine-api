from fastapi import APIRouter
from app.api.v1 import products, product_stock, purchase, cash_stock


api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    product_stock.router, prefix="/product-stock", tags=["product_stock"]
)
api_router.include_router(purchase.router, prefix="/purchase", tags=["purchase"])
api_router.include_router(cash_stock.router, prefix="/cash-stock", tags=["cash_stock"])
