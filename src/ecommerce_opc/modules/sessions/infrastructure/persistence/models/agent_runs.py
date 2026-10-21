from datetime import datetime
from uuid import UUID as PythonUUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
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


class AgentRunModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_runs"
    __table_args__ = (
        UniqueConstraint(
            "turn_id",
            "run_number",
            name="uq_agent_runs_turn_id_run_number",
        ),
        CheckConstraint(
            "run_number > 0",
            name="run_number_positive",
        ),
        CheckConstraint(
            "status IN ('running', 'succeeded', 'failed', 'cancelled')",
            name="status_valid",
        ),
    )

    turn_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("turns.id", ondelete="RESTRICT"),
        nullable=False,
    )

    run_number: Mapped[int] = mapped_column(
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

    error_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )