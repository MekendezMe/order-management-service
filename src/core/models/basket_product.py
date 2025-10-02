import decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DECIMAL, Numeric

from .base import Base
class BasketProduct(Base):
    __tablename__ = "basket_products"
    basket_id: Mapped[int] = mapped_column(ForeignKey("baskets.id"))
    basket: Mapped["Basket"] = relationship("Basket")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship("Product")
    count: Mapped[int] = mapped_column(Integer)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))