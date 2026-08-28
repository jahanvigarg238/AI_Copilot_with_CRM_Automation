from datetime import datetime, timedelta, timezone
from typing import Tuple


def get_now() -> datetime:
    """
    Return the current UTC datetime.
    """
    return datetime.now(timezone.utc)


def get_date_range(
    date_range: str,
    now: datetime | None = None
) -> Tuple[datetime, datetime]:
    """
    Convert a natural-language date range into
    a start and end datetime.

    Returns:
        (start_datetime, end_datetime)
    """

    if now is None:
        now = get_now()

    date_range = date_range.lower().strip()

    # -----------------------------------------
    # TODAY
    # -----------------------------------------
    if date_range == "today":

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = start + timedelta(days=1)

        return start, end

    # -----------------------------------------
    # THIS WEEK
    # Monday -> Sunday
    # -----------------------------------------
    if date_range == "this_week":

        start = (
            now
            - timedelta(days=now.weekday())
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = start + timedelta(days=7)

        return start, end

    # -----------------------------------------
    # LAST 7 DAYS
    # -----------------------------------------
    if date_range == "last_7_days":

        end = now
        start = now - timedelta(days=7)

        return start, end

    # -----------------------------------------
    # LAST 3 DAYS
    # -----------------------------------------
    if date_range == "last_3_days":

        end = now
        start = now - timedelta(days=3)

        return start, end

    # -----------------------------------------
    # LAST MONTH
    # -----------------------------------------
    if date_range == "last_month":

        first_day_this_month = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = first_day_this_month

        previous_month_last_day = (
            first_day_this_month - timedelta(days=1)
        )

        start = previous_month_last_day.replace(
            day=1
        )

        return start, end

    raise ValueError(
        f"Unsupported date range: {date_range}"
    )