from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer
from app.core.database import Base


class CashStock(Base):
    __tablename__ = "cash_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    denomination: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # e.g. 1000, 500, 100
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
