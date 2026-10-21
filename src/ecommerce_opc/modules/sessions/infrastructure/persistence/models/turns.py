from datetime import datetime
from uuid import UUID as PythonUUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_opc.infrastructure.database.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class TurnModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "turns"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "sequence",
            name="uq_turns_session_id_sequence",
        ),
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
        CheckConstraint(
            "status IN ('running', 'succeeded', 'failed', 'cancelled')",
            name="status_valid",
        ),
    )

    session_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="RESTRICT"),
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="running",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )