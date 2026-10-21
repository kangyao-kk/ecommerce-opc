
from uuid import UUID

from ecommerce_opc.modules.sessions.domain.entities.session import Session
from ecommerce_opc.modules.sessions.domain.exceptions import (
    SessionDomainError,
    SessionNotFoundError
)
from ecommerce_opc.modules.sessions.domain.repositories.session_repository import (
    SessionRepository,
)


class SessionService:
    """会话用例的应用服务。"""

    def __init__(self, repository: SessionRepository) -> None:
        self._repository = repository

    async def create_session(
        self,
        user_id: UUID,
        title: str = "New Session",
    ) -> Session:
        session = Session.create(user_id=user_id, title=title)
        await self._repository.save(session)
        return session

    async def get_session(
        self,
        session_id: UUID,
    ) -> Session | None:
        return await self._repository.get_by_id(session_id)

    async def list_sessions(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Session]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal to 0")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        return await self._repository.list_by_user_id(
            user_id=user_id,
            offset=offset,
            limit=limit,
        )

    async def rename_session(
        self,
        session_id: UUID,
        title: str,
    ) -> Session:
        session = await self._require_session(session_id)
        session.rename(title)
        await self._repository.save(session)
        return session

    async def archive_session(self, session_id: UUID) -> Session:
        session = await self._require_session(session_id)
        session.archive()
        await self._repository.save(session)
        return session

    async def _require_session(self, session_id: UUID) -> Session:
        session = await self._repository.get_by_id(session_id)
        if session is None:
            raise SessionNotFoundError(
                f"Session {session_id} was not found."
            )
        return session


