from typing import Any
from uuid import UUID as PythonUUID

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_opc.infrastructure.database.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class SessionEventModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "session_events"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "sequence",
            name="uq_session_events_session_id_sequence",
        ),
        CheckConstraint(
            "sequence > 0",
            name="sequence_positive",
        ),
    )

    session_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="RESTRICT"),
        nullable=False,
    )

    turn_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("turns.id", ondelete="RESTRICT"),
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )