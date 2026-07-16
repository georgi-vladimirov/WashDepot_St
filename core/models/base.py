from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class BaseModel(Base):
    """Abstract base model providing common fields and utilities for all models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    date_modified: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )