from pydantic import BaseModel
from typing import List


class PaymentItem(BaseModel):
    denomination: int
    count: int


class PurchaseRequest(BaseModel):
    product_id: int
    payment: List[PaymentItem]

    model_config = {"from_attributes": True}


class ChangeResponse(BaseModel):
    denomination: int
    count: int


class PurchaseResponse(BaseModel):
    success: bool
    product_id: int
    paid: int
    price: int
    change: List[ChangeResponse]
    remaining_stock: int
    message: str | None = None
