from app.schemas import RequestType


def process_report_generation(payload: dict) -> str:
    return "Report generation request accepted"


def process_data_export(payload: dict) -> str:
    return "Data export request accepted"


def process_data_import(payload: dict) -> str:
    return "Data import request accepted"


def process_notification(payload: dict) -> str:
    return "Notification request accepted"


def process_request(
    request_type: RequestType,
    payload: dict
) -> str:

    processors = {
        RequestType.REPORT_GENERATION: process_report_generation,
        RequestType.DATA_EXPORT: process_data_export,
        RequestType.DATA_IMPORT: process_data_import,
        RequestType.NOTIFICATION: process_notification,
    }

    processor = processors[request_type]

    return processor(payload)
