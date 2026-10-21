from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ecommerce_opc.modules.sessions.domain.enums import SessionStatus


class SessionCreateRequest(BaseModel):
    """创建会话的请求参数。"""

    user_id: UUID
    title: str = Field(default="New Session", max_length=200)


class SessionRenameRequest(BaseModel):
    """重命名会话的请求参数。"""

    title: str = Field(min_length=1, max_length=200)


class SessionResponse(BaseModel):
    """会话响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime


class SessionListResponse(BaseModel):
    """会话列表响应模型。"""

    items: list[SessionResponse]
    total_returned: int
    offset: int
    limit: int