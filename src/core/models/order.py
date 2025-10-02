import decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DECIMAL, Numeric

from .base import Base
class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")
    count_products: Mapped[int] = mapped_column(Integer)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.id"))
    status: Mapped["OrderStatus"] = relationship("OrderStatus")

