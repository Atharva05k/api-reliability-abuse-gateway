from fastapi import (
    Depends, 
    FastAPI,
    Header, 
    HTTPException,
    Response, 
    Security, 
    status
)
from sqlalchemy.orm import Session

from app.schemas import GatewayRequest, GatewayResponse
from app.database import get_db
from app.services import (
    create_request_record, 
    get_request_by_id,
    get_request_by_idempotency_key,
)
from app.processors import process_request
from app.auth import verify_api_key



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
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(verify_api_key)]
)

def create_request(
    request: GatewayRequest,
    response: Response,
    idempotency_key: str = Header(
        ...,
        alias="X-Idempotency-Key"
    ),
    db: Session = Depends(get_db)
):

    existing_request = get_request_by_idempotency_key(
        db,
        request.client_id,
        idempotency_key
    )

    if existing_request is not None:

        same_request = (
            existing_request.request_type == request.request_type.value
            and existing_request.priority == request.priority.value
            and existing_request.payload == request.payload
        )

        if not same_request:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Idempotency key has already been used "
                    "for a different request"
                )
            )

        response.status_code = status.HTTP_200_OK

        return GatewayResponse(
            request_id=existing_request.request_id,
            status=existing_request.status,
            message=(
                "Duplicate request detected; "
                "returning existing request"
            ),
            client_id=existing_request.client_id,
            request_type=existing_request.request_type,
            priority=existing_request.priority,
            received_at=existing_request.created_at
        )

    request_record = create_request_record(
        db,
        request,
        idempotency_key
    )

    processing_message = process_request(
        request.request_type,
        request.payload
    )

    return GatewayResponse(
        request_id=request_record.request_id,
        status=request_record.status,
        message=processing_message,
        client_id=request_record.client_id,
        request_type=request_record.request_type,
        priority=request_record.priority,
        received_at=request_record.created_at
    )

@app.get(
    "/requests/{request_id}",
    response_model=GatewayResponse,
    dependencies=[Security(verify_api_key)]
)

def get_request(
    request_id: str,
    db: Session = Depends(get_db)
):

    request_record = get_request_by_id(
        db,
        request_id
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

