from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from sqlalchemy import func
from datetime import datetime


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
