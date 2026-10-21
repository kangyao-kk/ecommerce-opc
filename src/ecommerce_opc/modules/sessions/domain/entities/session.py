from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ecommerce_opc.modules.sessions.domain.enums import SessionStatus
from ecommerce_opc.modules.sessions.domain.exceptions import (
    InvalidSessionTitleError,
    SessionAlreadyArchivedError,
)


@dataclass
class Session:
    id: UUID
    user_id: UUID
    title: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        title: str = "New Session",
    ) -> "Session":
        normalized_title = title.strip()

        if not normalized_title or len(normalized_title) > 200:
            raise InvalidSessionTitleError(
                "Session title must contain 1 to 200 characters."
            )

        now = datetime.now(timezone.utc)

        return cls(
            id=uuid4(),
            user_id=user_id,
            title=normalized_title,
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def rename(self, title: str) -> None:
        normalized_title = title.strip()

        if not normalized_title or len(normalized_title) > 200:
            raise InvalidSessionTitleError(
                "Session title must contain 1 to 200 characters."
            )

        self.title = normalized_title
        self.updated_at = datetime.now(timezone.utc)

    def archive(self) -> None:
        if self.status == SessionStatus.ARCHIVED:
            raise SessionAlreadyArchivedError(
                "Session has already been archived."
            )

        self.status = SessionStatus.ARCHIVED
        self.updated_at = datetime.now(timezone.utc)