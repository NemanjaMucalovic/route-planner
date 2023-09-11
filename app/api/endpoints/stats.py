import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Query
from app.db.crud import get_all_data, get_count

router = APIRouter()


@router.get("/stats/{time_frame}")
async def get_stats(time_frame: str):
    end_time = datetime.now()
    if time_frame == "day":
        start_time = end_time - timedelta(days=1)
    elif time_frame == "week":
        start_time = end_time - timedelta(weeks=1)
    elif time_frame == "month":
        start_time = end_time - timedelta(days=30)
    else:
        return {"error": "Invalid time frame"}

    # stats = api_stats_collection.find({
    #     "timestamp": {"$gte": start_time, "$lte": end_time}
    # })
    stats = get_count(
        {"timestamp": {"$gte": start_time, "$lte": end_time}}, collection="statistics"
    )

    return {
        "map_calls": stats,
    }
