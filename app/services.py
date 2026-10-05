from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import GatewayRequestModel
from app.schemas import GatewayRequest


def create_request_record(
    db: Session,
    request: GatewayRequest
) -> GatewayRequestModel:

    request_record = GatewayRequestModel(
        request_id=str(uuid4()),
        client_id=request.client_id,
        request_type=request.request_type.value,
        priority=request.priority.value,
        payload=request.payload,
        status="RECEIVED"
    )

    db.add(request_record)
    db.commit()
    db.refresh(request_record)

    return request_record


def get_request_by_id(
    db: Session,
    request_id: str
) -> GatewayRequestModel | None:

    return (
        db.query(GatewayRequestModel)
        .filter(
            GatewayRequestModel.request_id == request_id
        )
        .first()
    )