
from ecommerce_opc.modules.sessions.domain.entities.session import Session
from ecommerce_opc.modules.sessions.domain.enums import SessionStatus
from ecommerce_opc.modules.sessions.infrastructure.persistence.models.session import (
    SessionModel,
)


def to_domain(model: SessionModel) -> Session:
    return Session(
        id=model.id,
        user_id=model.user_id,
        title=model.title,
        status=SessionStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def to_model(session: Session) -> SessionModel:
    return SessionModel(
        id=session.id,
        user_id=session.user_id,
        title=session.title,
        status=session.status.value,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )
