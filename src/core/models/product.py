import decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DECIMAL, Numeric

from . import Author
from .base import Base
class Product(Base):
    article: Mapped[str] = mapped_column(String(9), unique=True)
    name: Mapped[str] =  mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author")
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    discount_price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String(200))
    minimal_age: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

