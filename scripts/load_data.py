import json
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

from app.config import MONGODB_URI, MONGODB_DATABASE


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_file(file_path: Path) -> list:
    """Load records from a JSON file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            f"{file_path} must contain a JSON list."
        )

    return data


def convert_dates(
    records: list,
    date_field: str
) -> list:
    """
    Convert ISO timestamp strings into Python datetime objects.
    """

    for record in records:

        if date_field in record:
            value = record[date_field]

            if isinstance(value, str):
                record[date_field] = datetime.fromisoformat(
                    value.replace("Z", "+00:00")
                )

    return records


def load_collection(
    database,
    collection_name: str,
    file_name: str,
    date_field: str
) -> None:
    """Load JSON records into MongoDB."""

    file_path = DATA_DIR / file_name

    records = load_json_file(file_path)

    records = convert_dates(
        records,
        date_field
    )

    collection = database[collection_name]

    # Reset collection during development.
    collection.delete_many({})

    if records:
        collection.insert_many(records)

    print(
        f"Loaded {len(records)} records "
        f"into '{collection_name}'."
    )


def create_indexes(database) -> None:
    """
    Create indexes for frequently queried fields.
    """

    database["calls"].create_index(
        [("agent", 1), ("call_time", -1)]
    )

    database["calls"].create_index(
        [("call_status", 1), ("call_time", -1)]
    )

    database["appointments"].create_index(
        [("agent", 1), ("appointment_time", -1)]
    )

    database["appointments"].create_index(
        [("status", 1), ("appointment_time", -1)]
    )

    database["emails"].create_index(
        [("sender", 1), ("timestamp", -1)]
    )

    database["emails"].create_index(
        [("timestamp", -1)]
    )

    database["whatsapp"].create_index(
        [("agent", 1), ("timestamp", -1)]
    )

    database["whatsapp"].create_index(
        [("customer", 1), ("timestamp", -1)]
    )

    print("Indexes created successfully.")


def main() -> None:
    """Load all CRM datasets."""

    print("Connecting to MongoDB...")

    client = MongoClient(MONGODB_URI)

    database = client[MONGODB_DATABASE]

    client.admin.command("ping")

    print(
        f"Connected to database: {MONGODB_DATABASE}"
    )

    load_collection(
        database,
        "calls",
        "calls.json",
        "call_time"
    )

    load_collection(
        database,
        "appointments",
        "appointments.json",
        "appointment_time"
    )

    load_collection(
        database,
        "emails",
        "emails.json",
        "timestamp"
    )

    load_collection(
        database,
        "whatsapp",
        "whatsapp.json",
        "timestamp"
    )

    create_indexes(database)

    client.close()

    print("All CRM data loaded successfully.")


if __name__ == "__main__":
    main()