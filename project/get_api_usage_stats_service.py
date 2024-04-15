from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class GetApiUsageStatsResponse(BaseModel):
    """
    Structure representing the API usage analytics, including request volumes and popular endpoints.
    """

    endpoint: str
    request_count: int
    last_access: datetime


async def get_api_usage_stats() -> GetApiUsageStatsResponse:
    """
    Provides statistics on API usage.

    This function retrieves the analytics record with the highest request count from the database and converts it into a GetApiUsageStatsResponse structure.

    Returns:
        GetApiUsageStatsResponse: Structure representing the API usage analytics, including request volumes and popular endpoints.

    Example:
        response = await get_api_usage_stats()
        > GetApiUsageStatsResponse(endpoint='/joke', request_count=200, last_access=datetime.now())
    """
    max_request_record = await prisma.models.Analytics.prisma().find_first(
        where=None, order={"requestCount": "desc"}
    )
    if max_request_record:
        return GetApiUsageStatsResponse(
            endpoint=max_request_record.endpoint,
            request_count=max_request_record.requestCount,
            last_access=max_request_record.lastAccess
            if max_request_record.lastAccess
            else datetime.now(),
        )
    else:
        return GetApiUsageStatsResponse(
            endpoint="N/A", request_count=0, last_access=datetime.now()
        )
