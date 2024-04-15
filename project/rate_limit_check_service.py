from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class RateLimitCheckResponse(BaseModel):
    """
    A model describing the response for a rate limit check request, detailing the user's current rate limit status.
    """

    remaining_requests: int
    limit_window_seconds: int
    used_requests: int


async def rate_limit_check() -> RateLimitCheckResponse:
    """
    Checks and reports on the current rate limit status of the user.

    This function assumes the availability of a `request` object to verify the API key submitted
    with the request and query the `AccessLog` for the same API key to count the number of requests
    made within the last hour. The rate limit is arbitrarily set here to 1000 requests per hour,
    and the function calculates the used requests and remaining requests accordingly.

    Args: None

    Returns:
    RateLimitCheckResponse: A model describing the response for a rate limit check request, detailing the user's current rate limit status,
                            including the remaining number of requests, the limit window in seconds, and the used requests.

    Example:
        rate_limit_check()
        > RateLimitCheckResponse(remaining_requests=950, limit_window_seconds=3600, used_requests=50)
    """
    current_api_key = "CURRENT_API_KEY_STUB"
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    api_key_record = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": current_api_key}, include={"accessLogs": True}
    )
    if not api_key_record:
        return RateLimitCheckResponse(
            remaining_requests=0, limit_window_seconds=3600, used_requests=0
        )
    recent_access_logs = [
        log for log in api_key_record.accessLogs if log.accessTime > one_hour_ago
    ]
    rate_limit = 1000
    used_requests = len(recent_access_logs)
    remaining_requests = rate_limit - used_requests
    return RateLimitCheckResponse(
        remaining_requests=remaining_requests,
        limit_window_seconds=3600,
        used_requests=used_requests,
    )
