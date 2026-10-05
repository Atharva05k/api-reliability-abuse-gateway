from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import GatewayRequest, GatewayResponse
from app.database import get_db
from app.models import GatewayRequestModel




app = FastAPI(
    title="API Reliability & Abuse Detection Gateway",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "API Reliability & Abuse Detection Gateway is running"
    }


@app.post(
    "/requests",
    response_model=GatewayResponse,
    status_code=status.HTTP_201_CREATED
)

def create_request(
    request: GatewayRequest,
    db: Session = Depends(get_db)
):

    request_id = str(uuid4())

    request_record = GatewayRequestModel(
        request_id=request_id,
        client_id=request.client_id,
        request_type=request.request_type.value,
        priority=request.priority.value,
        payload=request.payload,
        status="RECEIVED"
    )

    db.add(request_record)
    db.commit()
    db.refresh(request_record)

    return GatewayResponse(
        request_id=request_record.request_id,
        status=request_record.status,
        message="Request received successfully",
        client_id=request_record.client_id,
        request_type=request_record.request_type,
        priority=request_record.priority,
        received_at=request_record.created_at
    )

@app.get(
    "/requests/{request_id}",
    response_model=GatewayResponse
)
def get_request(
    request_id: str,
    db: Session = Depends(get_db)
):

    request_record = (
        db.query(GatewayRequestModel)
        .filter(
            GatewayRequestModel.request_id == request_id
        )
        .first()
    )

    if request_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )

    return GatewayResponse(
        request_id=request_record.request_id,
        status=request_record.status,
        message="Request retrieved successfully",
        client_id=request_record.client_id,
        request_type=request_record.request_type,
        priority=request_record.priority,
        received_at=request_record.created_at
    )
