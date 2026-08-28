from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.config import (
    MONGODB_URI,
    MONGODB_DATABASE
)


client = MongoClient(
    MONGODB_URI
)

db = client[
    MONGODB_DATABASE
]


def check_database_connection() -> bool:
    """
    Check whether MongoDB is reachable.
    """

    try:
        client.admin.command("ping")
        return True

    except ConnectionFailure:
        return False