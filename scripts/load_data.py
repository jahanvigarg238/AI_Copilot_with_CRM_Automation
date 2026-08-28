import json
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

from app.config import MONGODB_URI, MONGODB_DATABASE


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def convert_dates(records, field):
    for record in records:
        if field in record:
            record[field] = datetime.fromisoformat(
                record[field].replace("Z", "+00:00")
            )

    return records


def load_collection(
    database,
    collection_name,
    filename,
    date_field
):

    records = load_json(filename)

    records = convert_dates(
        records,
        date_field
    )

    collection = database[collection_name]

    # Clear previous development data
    collection.delete_many({})

    if records:
        collection.insert_many(records)

    print(
        f"Loaded {len(records)} records "
        f"into '{collection_name}'"
    )


def create_indexes(database):

    database.calls.create_index(
        [("agent", 1), ("call_time", -1)]
    )

    database.appointments.create_index(
        [("agent", 1), ("appointment_time", -1)]
    )

    database.emails.create_index(
        [("sender", 1), ("timestamp", -1)]
    )

    database.whatsapp.create_index(
        [("agent", 1), ("timestamp", -1)]
    )

    database.whatsapp.create_index(
        [("customer", 1), ("timestamp", -1)]
    )


def main():

    print("Connecting to MongoDB...")

    client = MongoClient(MONGODB_URI)

    client.admin.command("ping")

    database = client[MONGODB_DATABASE]

    print(
        f"Connected to database: "
        f"{MONGODB_DATABASE}"
    )

    load_collection(
        database,
        "calls",
        "call_logs_sample.json",
        "call_time"
    )

    load_collection(
        database,
        "appointments",
        "appointments_sample.json",
        "appointment_time"
    )

    load_collection(
        database,
        "emails",
        "emails_sample.json",
        "timestamp"
    )

    load_collection(
        database,
        "whatsapp",
        "whatsapp_sample.json",
        "timestamp"
    )

    create_indexes(database)

    client.close()

    print("All assignment data loaded successfully.")


if __name__ == "__main__":
    main()