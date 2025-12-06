from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cash_stock import CashStock
from app.schemas.cash_stock import CashStockCreate, CashStockRead, CashStockUpdate

router = APIRouter()


@router.get("/{cash_id}", response_model=CashStockRead)
def get_cash_stock(cash_id: int, db: Session = Depends(get_db)):
    product = db.query(CashStock).filter(CashStock.id == cash_id).first()
    if not product:
        raise HTTPException(404, "Cash Stock not found")
    return product


@router.get("/", response_model=list[CashStockRead])
def list_cash_stock(db: Session = Depends(get_db)):
    return db.query(CashStock).order_by(CashStock.denomination.desc()).all()


@router.post("/", response_model=CashStockRead)
def create_cash_stock(payload: CashStockCreate, db: Session = Depends(get_db)):
    existing = db.query(CashStock).filter_by(denomination=payload.denomination).first()
    if existing:
        raise HTTPException(400, "Denomination already exists")

    cash = CashStock(**payload.model_dump())
    db.add(cash)
    db.commit()
    db.refresh(cash)
    return cash


@router.put("/{cash_id}", response_model=CashStockRead)
def update_cash_stock(
    cash_id: int, payload: CashStockUpdate, db: Session = Depends(get_db)
):
    cash = db.query(CashStock).filter(CashStock.id == cash_id).first()
    if not cash:
        raise HTTPException(404, "Cash Stock not found")

    existing = (
        db.query(CashStock)
        .filter(CashStock.denomination == payload.denomination, CashStock.id != cash_id)
        .first()
    )
    if existing:
        raise HTTPException(400, "Denomination already exists")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(cash, key, value)

    db.commit()
    db.refresh(cash)
    return cash


@router.delete("/{cash_id}")
def delete_cash_stock(cash_id: int, db: Session = Depends(get_db)):
    cash = db.query(CashStock).filter(CashStock.id == cash_id).first()
    if not cash:
        raise HTTPException(404, "Cash Stock not found")

    db.delete(cash)
    db.commit()
    return {"success": True}
