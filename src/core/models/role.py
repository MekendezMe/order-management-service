from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from sqlalchemy import String


class Role(Base):
    name: Mapped[str] = mapped_column(String(30), unique=True)
    users: Mapped[list["User"]] = relationship("User")