from typing import Annotated

from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from ecommerce_opc.api.schemas.sessions import (
    SessionCreateRequest,
    SessionListResponse,
    SessionRenameRequest,
    SessionResponse,
)
from ecommerce_opc.infrastructure.database.session import get_db_session
from ecommerce_opc.modules.sessions.application.session_service import (
    SessionService,
)
from ecommerce_opc.modules.sessions.infrastructure.persistence.repositories.sqlalchemy_session_repository import (
    SQLAlchemySessionRepository,
)


router = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_session_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SessionService:
    """组装会话用例所需的依赖。"""
    repository = SQLAlchemySessionRepository(db_session)
    return SessionService(repository)


SessionServiceDep = Annotated[
    SessionService,
    Depends(get_session_service),
]


@router.post(
    "",
    response_model=SessionResponse,
    status_code=201,
)
async def create_session(
    request: SessionCreateRequest,
    service: SessionServiceDep,
) -> SessionResponse:
    session = await service.create_session(
        user_id=request.user_id,
        title=request.title,
    )
    return SessionResponse.model_validate(session)


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
async def get_session(
    session_id: UUID,
    service: SessionServiceDep,
) -> SessionResponse:
    session = await service.get_session(session_id)

    if session is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return SessionResponse.model_validate(session)



@router.get(
    "",
    response_model=SessionListResponse,
)
async def list_sessions(
    user_id: UUID,
    service: SessionServiceDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> SessionListResponse:
    sessions = await service.list_sessions(
        user_id=user_id,
        offset=offset,
        limit=limit,
    )

    return SessionListResponse(
        items=[
            SessionResponse.model_validate(session)
            for session in sessions
        ],
        total_returned=len(sessions),
        offset=offset,
        limit=limit,
    )