from collections import defaultdict
from threading import Lock
from typing import Any


_metrics_lock = Lock()

_total_requests = 0
_requests_by_method = defaultdict(int)
_responses_by_status = defaultdict(int)
_total_duration_ms = 0.0


def record_request(
    method: str,
    status_code: int,
    duration_ms: float,
) -> None:
    global _total_requests
    global _total_duration_ms

    with _metrics_lock:
        _total_requests += 1
        _requests_by_method[method] += 1
        _responses_by_status[str(status_code)] += 1
        _total_duration_ms += duration_ms


def get_metrics_snapshot() -> dict[str, Any]:
    with _metrics_lock:
        if _total_requests > 0:
            average_duration_ms = round(
                _total_duration_ms / _total_requests,
                2,
            )
        else:
            average_duration_ms = 0.0

        return {
            "total_requests": _total_requests,
            "requests_by_method": dict(_requests_by_method),
            "responses_by_status": dict(_responses_by_status),
            "average_duration_ms": average_duration_ms,
        }