from pydantic import BaseModel


class ProductStockBase(BaseModel):
    product_id: int
    quantity: int


class ProductStockCreate(ProductStockBase):
    pass


class ProductStockUpdate(BaseModel):
    quantity: int | None = None


class ProductStockRead(ProductStockBase):
    id: int

    model_config = {"from_attributes": True}
