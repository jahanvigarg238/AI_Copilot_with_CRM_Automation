import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RECORD_COUNT = 600

random.seed(42)


# --------------------------------------------------
# Sample CRM values
# --------------------------------------------------

AGENTS = [
    "Priya Sharma",
    "Neha Kapoor",
    "Amit Verma",
    "Rohit Mehta",
    "Ananya Singh",
]

CUSTOMERS = [
    "Rahul Jain",
    "Sneha Rao",
    "Vikram Das",
    "Arjun Malhotra",
    "Kavya Nair",
    "Riya Gupta",
    "Aditya Shah",
    "Meera Joshi",
    "Karan Bansal",
    "Pooja Agarwal",
]

CALL_STATUSES = [
    "completed",
    "completed",
    "completed",
    "failed",
]

APPOINTMENT_STATUSES = [
    "confirmed",
    "confirmed",
    "confirmed",
    "completed",
    "missed",
    "cancelled",
]

EMAIL_SENDERS = [
    "support@crm.io",
    "sales@crm.io",
    "admin@crm.io",
    "noreply@crm.io",
]

EMAIL_RECEIVERS = [
    "customer@example.com",
    "rahul@example.com",
    "sneha@example.com",
    "vikram@example.com",
    "customer1@example.com",
]

EMAIL_SUBJECTS = [
    "Onboarding Help",
    "Product Demo",
    "Follow-up",
    "Account Update",
    "Onboarding Process",
    "Support Request",
    "Pricing Information",
    "Customer Feedback",
    "Welcome to CRM",
    "Technical Support",
]

EMAIL_STATUSES = [
    "delivered",
    "delivered",
    "delivered",
    "sent",
    "failed",
    "bounced",
]

WHATSAPP_STATUSES = [
    "delivered",
    "delivered",
    "delivered",
    "delivered",
    "failed",
]

WHATSAPP_MESSAGES = [
    "Please share your requirements.",
    "Thank you for contacting us.",
    "I will share the details shortly.",
    "Can we schedule a demo?",
    "Your request has been received.",
    "Please let me know a convenient time.",
    "Here are the details you requested.",
    "Thank you for your response.",
    "We will follow up shortly.",
    "Can I help you with anything else?",
]


# --------------------------------------------------
# Utility functions
# --------------------------------------------------

def random_datetime() -> datetime:
    """
    Generate a random datetime from the last 60 days
    to the next 7 days.
    """

    now = datetime.now(timezone.utc)

    start = now - timedelta(days=60)
    end = now + timedelta(days=7)

    total_seconds = int(
        (end - start).total_seconds()
    )

    random_seconds = random.randint(
        0,
        total_seconds
    )

    return start + timedelta(
        seconds=random_seconds
    )


def datetime_to_iso(dt: datetime) -> str:
    """
    Convert datetime to ISO-8601 format.
    """

    return dt.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def save_json(
    filename: str,
    records: list
) -> None:
    """
    Save records to a JSON file.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = DATA_DIR / filename

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created {file_path} "
        f"with {len(records)} records."
    )


# --------------------------------------------------
# Call Logs
# --------------------------------------------------

def generate_calls() -> list:
    """
    Generate Call Log records.
    """

    records = []

    for index in range(1, RECORD_COUNT + 1):

        call_time = random_datetime()

        record = {
            "call_id": f"CL{index:04d}",
            "agent": random.choice(AGENTS),
            "customer": random.choice(CUSTOMERS),
            "call_time": datetime_to_iso(call_time),
            "duration_minutes": random.randint(
                1,
                30
            ),
            "call_status": random.choice(
                CALL_STATUSES
            ),
        }

        records.append(record)

    return records


# --------------------------------------------------
# Appointments
# --------------------------------------------------

def generate_appointments() -> list:
    """
    Generate Appointment records.
    """

    records = []

    for index in range(
        1,
        RECORD_COUNT + 1
    ):

        appointment_time = random_datetime()

        record = {
            "appointment_id": f"APPT{index:04d}",
            "agent": random.choice(AGENTS),
            "customer": random.choice(CUSTOMERS),
            "appointment_time": datetime_to_iso(
                appointment_time
            ),
            "status": random.choice(
                APPOINTMENT_STATUSES
            ),
            "notes": random.choice([
                "Follow-up on demo",
                "Product discussion",
                "Customer follow-up",
                "Initial consultation",
                "Pricing discussion",
                "Technical discussion",
            ]),
        }

        records.append(record)

    return records


# --------------------------------------------------
# Emails
# --------------------------------------------------

def generate_emails() -> list:
    """
    Generate Email Conversation records.
    """

    records = []

    for index in range(
        1,
        RECORD_COUNT + 1
    ):

        timestamp = random_datetime()

        record = {
            "email_id": f"EML{index:04d}",
            "sender": random.choice(
                EMAIL_SENDERS
            ),
            "receiver": random.choice(
                EMAIL_RECEIVERS
            ),
            "subject": random.choice(
                EMAIL_SUBJECTS
            ),
            "timestamp": datetime_to_iso(
                timestamp
            ),
            "status": random.choice(
                EMAIL_STATUSES
            ),
        }

        records.append(record)

    return records


# --------------------------------------------------
# WhatsApp
# --------------------------------------------------

def generate_whatsapp() -> list:
    """
    Generate WhatsApp Business Conversation records.
    """

    records = []

    for index in range(
        1,
        RECORD_COUNT + 1
    ):

        timestamp = random_datetime()

        record = {
            "message_id": f"WA{index:04d}",
            "agent": random.choice(AGENTS),
            "customer": random.choice(CUSTOMERS),
            "timestamp": datetime_to_iso(
                timestamp
            ),
            "message": random.choice(
                WHATSAPP_MESSAGES
            ),
            "status": random.choice(
                WHATSAPP_STATUSES
            ),
        }

        records.append(record)

    return records


# --------------------------------------------------
# Main
# --------------------------------------------------

def main() -> None:
    """
    Generate all CRM datasets.
    """

    print("Generating CRM datasets...")

    calls = generate_calls()

    appointments = generate_appointments()

    emails = generate_emails()

    whatsapp = generate_whatsapp()

    save_json(
        "calls.json",
        calls
    )

    save_json(
        "appointments.json",
        appointments
    )

    save_json(
        "emails.json",
        emails
    )

    save_json(
        "whatsapp.json",
        whatsapp
    )

    print("\nData generation completed.")
    print(f"Records per module: {RECORD_COUNT}")


if __name__ == "__main__":
    main()