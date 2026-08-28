from datetime import datetime
from typing import Any, Dict, List

from app.database.connection import db


whatsapp_collection = db["whatsapp"]


def get_messages_by_agent(
    agent: str,
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Get WhatsApp messages sent by an agent
    within a date range.
    """

    query = {
        "agent": agent,
        "timestamp": {
            "$gte": start_date,
            "$lt": end_date
        }
    }

    return list(
        whatsapp_collection.find(
            query,
            {"_id": 0}
        ).sort(
            "timestamp",
            1
        )
    )


def get_delivery_status_counts(
    start_date: datetime,
    end_date: datetime
) -> Dict[str, int]:
    """
    Count delivered and failed WhatsApp messages
    within a date range.
    """

    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start_date,
                    "$lt": end_date
                },
                "status": {
                    "$in": [
                        "delivered",
                        "failed"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {
                    "$sum": 1
                }
            }
        }
    ]

    result = list(
        whatsapp_collection.aggregate(pipeline)
    )

    counts = {
        "delivered": 0,
        "failed": 0
    }

    for item in result:
        status = item["_id"]
        counts[status] = item["count"]

    return counts


def get_latest_message_to_customer(
    customer: str
) -> Dict[str, Any] | None:
    """
    Get the latest WhatsApp message sent
    to a specific customer.
    """

    query = {
        "customer": customer
    }

    message = whatsapp_collection.find_one(
        query,
        {"_id": 0},
        sort=[
            ("timestamp", -1)
        ]
    )

    return message