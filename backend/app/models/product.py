from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # unit = THB
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
