from sqlalchemy import Column, DateTime, Integer, JSON, String, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class GatewayRequestModel(Base):

    __tablename__ = "gateway_requests"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "idempotency_key",
            name="uq_client_idempotency_key"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    request_id = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True
    )

    client_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    idempotency_key = Column(
        String(100),
        nullable=False,
        index=True
    )

    request_type = Column(
        String(50),
        nullable=False
    )

    priority = Column(
        String(20),
        nullable=False
    )

    payload = Column(
        JSON,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="RECEIVED"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )