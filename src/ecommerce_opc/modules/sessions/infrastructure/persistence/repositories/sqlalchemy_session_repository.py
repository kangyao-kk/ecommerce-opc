
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ecommerce_opc.modules.sessions.domain.entities.session import Session
from ecommerce_opc.modules.sessions.domain.repositories.session_repository import (
    SessionRepository,
)
from ecommerce_opc.modules.sessions.infrastructure.persistence.mappers import (
    to_domain,
    to_model,
)
from ecommerce_opc.modules.sessions.infrastructure.persistence.models.session import (
    SessionModel,
)


class SQLAlchemySessionRepository(SessionRepository):
    """基于 SQLAlchemy 的会话仓储实现。"""

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def save(self, session: Session) -> None:
        model = await self._db_session.get(SessionModel, session.id)

        if model is None:
            self._db_session.add(to_model(session))
        else:
            model.title = session.title
            model.status = session.status.value
            model.updated_at = session.updated_at

        await self._db_session.flush()

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> Session | None:
        model = await self._db_session.get(SessionModel, session_id)

        if model is None:
            return None

        return to_domain(model)

    async def list_by_user_id(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Session]:
        statement = (
            select(SessionModel)
            .where(SessionModel.user_id == user_id)
            .order_by(SessionModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.scalars(statement)
        return [to_domain(model) for model in result.all()]
