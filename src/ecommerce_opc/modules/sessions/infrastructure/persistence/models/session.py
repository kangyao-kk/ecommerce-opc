from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_opc.infrastructure.database.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class SessionModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'archived')",
            name="status_valid",
        ),
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="new session",
    )

    user_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )