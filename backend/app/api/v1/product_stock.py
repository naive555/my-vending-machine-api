from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.product_stock import ProductStock
from app.schemas.product_stock import (
    ProductStockCreate,
    ProductStockRead,
    ProductStockUpdate,
)

router = APIRouter()


@router.get("/{product_id}", response_model=ProductStockRead)
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    stock = db.query(ProductStock).filter_by(product_id=product_id).first()
    if not stock:
        raise HTTPException(404, "Product stock not found")

    return stock


@router.get("/", response_model=list[ProductStockRead])
def list_product_stock(db: Session = Depends(get_db)):
    return db.query(ProductStock).all()


@router.post("/", response_model=ProductStockRead)
def create_product_stock(payload: ProductStockCreate, db: Session = Depends(get_db)):
    stock = ProductStock(**payload.model_dump())

    existing_product = db.query(Product).filter_by(id=stock.product_id).first()
    if not existing_product:
        raise HTTPException(404, "Product not found")

    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.put("/{product_id}", response_model=ProductStockRead)
def update_product_stock(
    product_id: int, payload: ProductStockUpdate, db: Session = Depends(get_db)
):
    stock = db.query(ProductStock).filter_by(product_id=product_id).first()
    if not stock:
        raise HTTPException(404, "Product stock not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(stock, key, value)

    db.commit()
    db.refresh(stock)
    return stock


@router.delete("/{product_id}")
def delete_stock(product_id: int, db: Session = Depends(get_db)):
    stock = db.query(ProductStock).filter_by(product_id=product_id).first()
    if not stock:
        raise HTTPException(404, "Product stock not found")

    db.delete(stock)
    db.commit()
    return {"success": True}
