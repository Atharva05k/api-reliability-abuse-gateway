from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class RequestType(str, Enum):
    REPORT_GENERATION = "REPORT_GENERATION"
    DATA_EXPORT = "DATA_EXPORT"
    DATA_IMPORT = "DATA_IMPORT"
    NOTIFICATION = "NOTIFICATION"


class GatewayRequest(BaseModel):
    client_id: str = Field(
        min_length=3,
        max_length=50
    )

    request_type: RequestType

    priority: Priority = Priority.NORMAL

    payload: dict


class GatewayResponse(BaseModel):
    request_id: str
    status: str
    message: str
    client_id: str
    request_type: RequestType
    priority: Priority
    received_at: datetime