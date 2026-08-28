from datetime import datetime
from typing import Any, Dict, List

from app.database.connection import db


# MongoDB collection for appointments
appointments_collection = db["appointments"]


def get_confirmed_appointments(
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Get all confirmed appointments within a given date range.
    """

    query = {
        "status": "confirmed",
        "appointment_time": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return list(
        appointments_collection.find(
            query,
            {
                "_id": 0
            }
        ).sort(
            "appointment_time",
            1
        )
    )


def count_appointments_by_agent(
    agent: str,
    start_date: datetime,
    end_date: datetime
) -> int:
    """
    Count appointments for an agent
    within a given date range.
    """

    query = {
        "agent": agent,
        "appointment_time": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return appointments_collection.count_documents(query)


def get_missed_appointments(
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Get all missed appointments within a given date range.
    """

    query = {
        "status": "missed",
        "appointment_time": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return list(
        appointments_collection.find(
            query,
            {
                "_id": 0
            }
        ).sort(
            "appointment_time",
            -1
        )
    )