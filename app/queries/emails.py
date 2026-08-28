from datetime import datetime
from typing import Any, Dict, List

from app.database.connection import db


emails_collection = db["emails"]


def get_emails_by_sender(
    sender: str,
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Get emails sent by a specific sender
    within a date range.
    """

    query = {
        "sender": sender,
        "timestamp": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return list(
        emails_collection.find(
            query,
            {"_id": 0}
        ).sort(
            "timestamp",
            -1
        )
    )


def count_emails_by_subject_keyword(
    keyword: str,
    start_date: datetime,
    end_date: datetime
) -> int:
    """
    Count emails whose subject contains
    a specific keyword within a date range.
    """

    query = {
        "subject": {
            "$regex": keyword,
            "$options": "i"
        },
        "timestamp": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return emails_collection.count_documents(query)


def get_undelivered_emails() -> List[Dict[str, Any]]:
    """
    Get emails that were not delivered successfully.
    """

    query = {
        "status": {
            "$nin": [
                "delivered",
                "sent"
            ]
        }
    }

    return list(
        emails_collection.find(
            query,
            {"_id": 0}
        ).sort(
            "timestamp",
            -1
        )
    )
