from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, Product

router = APIRouter()

@router.post("/", response_model=Product)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    obj = Product(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()