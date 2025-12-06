from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.purchase import PurchaseRequest, PurchaseResponse
from app.core.database import get_db
from app.services.purchase_service import purchase_product

router = APIRouter()


@router.post("/", response_model=PurchaseResponse)
def purchase(payload: PurchaseRequest, db: Session = Depends(get_db)):
    payment_list = [
        {"denomination": payment.denomination, "count": payment.count}
        for payment in payload.payment
    ]

    with db.begin():
        result = purchase_product(db, payload.product_id, payment_list)
        if not result.get("success"):
            raise HTTPException(400, result.get("message"))

        change_items = result.get("change", [])

        return {
            "success": True,
            "product_id": result["product_id"],
            "paid": result["paid"],
            "price": result["price"],
            "change": change_items,
            "remaining_stock": result["remaining_stock"],
            "message": result.get("message"),
        }
