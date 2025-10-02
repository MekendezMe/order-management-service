import decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DECIMAL, Numeric

from .base import Base
class Basket(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")
    status_id: Mapped[int] = mapped_column(ForeignKey("basket_statuses.id"))
    status: Mapped["BasketStatus"] = relationship("BasketStatus")