from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)   # unit = THB
    image_url = Column(String, nullable=True)