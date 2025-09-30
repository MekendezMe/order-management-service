from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey

from . import Role
from .base import Base
class User(Base):
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] =  mapped_column(String(150))
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    basket: Mapped["Basket"] = relationship("Basket", back_populates="user")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
