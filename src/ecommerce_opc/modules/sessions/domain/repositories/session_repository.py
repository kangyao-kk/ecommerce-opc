from abc import ABC, abstractmethod
from uuid import UUID

from ecommerce_opc.modules.sessions.domain.entities.session import Session


class SessionRepository(ABC):

    @abstractmethod
    async def save(self, session: Session) -> None:
        """保存或更新会话。"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        session_id: UUID,
    ) -> Session | None:
        """根据会话 ID 查询会话。"""
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Session]:
        """分页查询指定用户的会话。"""
        raise NotImplementedError