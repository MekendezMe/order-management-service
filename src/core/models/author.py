from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey

from .base import Base
class Author(Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    products: Mapped[list["Product"]] = relationship("Product")