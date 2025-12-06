from pydantic import BaseModel, field_validator

VALID_DENOMINATIONS = {1000, 500, 100, 50, 20, 10, 5, 2, 1}


class CashStockBase(BaseModel):
    denomination: int
    quantity: int

    @field_validator("denomination")
    def validate_denomination(cls, v):
        if v not in VALID_DENOMINATIONS:
            raise ValueError(f"Invalid denomination: {v}")
        return v


class CashStockCreate(CashStockBase):
    pass


class CashStockUpdate(CashStockBase):
    pass


class CashStockRead(CashStockBase):
    id: int

    model_config = {"from_attributes": True}
