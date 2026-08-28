from datetime import datetime, timedelta, timezone

from app.database.connection import db


def get_dataset_reference_date() -> datetime:
    """
    Get the latest timestamp available in the CRM dataset.

    This is used as the reference date for natural-language
    expressions such as 'today', 'this week', and 'last 7 days'.
    """

    latest_dates = []

    # Calls
    call = db.calls.find_one(
        {},
        {"call_time": 1, "_id": 0},
        sort=[("call_time", -1)]
    )

    if call and call.get("call_time"):
        latest_dates.append(call["call_time"])

    # Appointments
    appointment = db.appointments.find_one(
        {},
        {"appointment_time": 1, "_id": 0},
        sort=[("appointment_time", -1)]
    )

    if appointment and appointment.get("appointment_time"):
        latest_dates.append(
            appointment["appointment_time"]
        )

    # Emails
    email = db.emails.find_one(
        {},
        {"timestamp": 1, "_id": 0},
        sort=[("timestamp", -1)]
    )

    if email and email.get("timestamp"):
        latest_dates.append(email["timestamp"])

    # WhatsApp
    whatsapp = db.whatsapp.find_one(
        {},
        {"timestamp": 1, "_id": 0},
        sort=[("timestamp", -1)]
    )

    if whatsapp and whatsapp.get("timestamp"):
        latest_dates.append(
            whatsapp["timestamp"]
        )

    if not latest_dates:
        raise ValueError(
            "No CRM data available to determine "
            "dataset reference date."
        )

    reference_date = max(latest_dates)

    if reference_date.tzinfo is None:
        reference_date = reference_date.replace(
            tzinfo=timezone.utc
        )

    return reference_date


def get_date_range(
    date_range: str | None
):
    """
    Convert a natural-language date range into
    MongoDB-compatible start and end datetimes.

    The calculation is based on the latest date
    present in the assignment dataset.
    """

    reference = get_dataset_reference_date()

    reference_date = reference.date()

    # TODAY
    if date_range == "today":

        start = datetime.combine(
            reference_date,
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        end = start + timedelta(days=1)

        return start, end

    # THIS WEEK
    if date_range == "this_week":

        # Monday = 0
        start_date = (
            reference_date
            - timedelta(
                days=reference_date.weekday()
            )
        )

        start = datetime.combine(
            start_date,
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        end = start + timedelta(days=7)

        return start, end

    # LAST 7 DAYS
    if date_range == "last_7_days":

        end = datetime.combine(
            reference_date + timedelta(days=1),
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        start = end - timedelta(days=7)

        return start, end

    # LAST 3 DAYS
    if date_range == "last_3_days":

        end = datetime.combine(
            reference_date + timedelta(days=1),
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        start = end - timedelta(days=3)

        return start, end

    # LAST MONTH
    if date_range == "last_month":

        first_of_current_month = reference_date.replace(
            day=1
        )

        first_current = datetime.combine(
            first_of_current_month,
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        if first_of_current_month.month == 1:

            previous_month = first_of_current_month.replace(
                year=first_of_current_month.year - 1,
                month=12
            )

        else:

            previous_month = first_of_current_month.replace(
                month=first_of_current_month.month - 1
            )

        start = datetime.combine(
            previous_month,
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        return start, first_current

    # NO DATE FILTER
    return None, None