from datetime import datetime
from typing import Any, Dict, List

from app.database.connection import db


# MongoDB collection for call logs
calls_collection = db["calls"]


def count_calls_by_agent(
    agent: str,
    start_date: datetime,
    end_date: datetime
) -> int:
    """
    Count the number of calls made by an agent
    within a given date range.
    """

    query = {
        "agent": agent,
        "call_time": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return calls_collection.count_documents(query)


def get_failed_calls(
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Get all failed calls within a given date range.
    """

    query = {
        "call_status": "failed",
        "call_time": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return list(
        calls_collection.find(
            query,
            {
                "_id": 0
            }
        ).sort(
            "call_time",
            -1
        )
    )


def get_average_completed_call_duration() -> float:
    """
    Calculate the average duration of completed calls.
    """

    pipeline = [
        {
            "$match": {
                "call_status": "completed"
            }
        },
        {
            "$group": {
                "_id": None,
                "average_duration": {
                    "$avg": "$duration_minutes"
                }
            }
        }
    ]

    result = list(
        calls_collection.aggregate(pipeline)
    )

    if not result:
        return 0.0

    return round(
        result[0]["average_duration"],
        2
    )