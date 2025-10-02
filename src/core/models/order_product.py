import decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DECIMAL, Numeric

from . import User, Order, Product
from .base import Base
class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship("Order")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship("Product")
    count: Mapped[int] = mapped_column(Integer)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))