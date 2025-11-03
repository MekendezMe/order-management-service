from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class ReviewFile(Base):
    __tablename__ = "review_files"
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    review: Mapped["Review"] = relationship("Review")
    file_url: Mapped[str] = mapped_column(String(300))