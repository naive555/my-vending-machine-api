from sqlalchemy import Column, Integer
from app.core.database import Base

class CashStock(Base):
    __tablename__ = "cash_stock"

    id = Column(Integer, primary_key=True)
    denomination = Column(Integer, nullable=False)  # e.g. 1000, 500, 100
    quantity = Column(Integer, nullable=False, default=0)