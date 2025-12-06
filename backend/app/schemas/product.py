from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: int
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = {"from_attributes": True}
