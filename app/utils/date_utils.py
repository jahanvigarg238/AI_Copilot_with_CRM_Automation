from datetime import datetime, timedelta
from typing import Optional


def get_dataset_reference_date() -> datetime:
    """
    Reference date for the synthetic CRM dataset.

    The supplied development data ends on
    March 28, 2025.
    """

    return datetime(
        2025,
        3,
        28,
        12,
        0,
        0
    )


def get_date_range(
    date_range: str,
    now: Optional[datetime] = None
):
    """
    Resolve a supported relative date range.

    If `now` is supplied, it is used as the reference
    date. This is useful for unit tests.

    If `now` is not supplied, the reference date of the
    synthetic CRM dataset is used.
    """

    if now is None:
        now = get_dataset_reference_date()

    # Keep the same naive datetime format as MongoDB data.
    if now.tzinfo is not None:
        now = now.replace(tzinfo=None)

    date_range = date_range.strip().lower()

    # ==================================================
    # TODAY
    # ==================================================

    if date_range == "today":

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = start + timedelta(days=1)

        return start, end

    # ==================================================
    # THIS WEEK
    # ==================================================

    if date_range == "this_week":

        # Monday = 0
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

    # ==================================================
    # LAST 7 DAYS
    # ==================================================

    if date_range == "last_7_days":

        end = now

        start = now - timedelta(days=7)

        return start, end

    # ==================================================
    # LAST 3 DAYS
    # ==================================================

    if date_range == "last_3_days":

        end = now

        start = now - timedelta(days=3)

        return start, end

    # ==================================================
    # LAST MONTH
    # ==================================================

    if date_range == "last_month":

        current_month_start = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = current_month_start

        previous_month_last_day = (
            current_month_start
            - timedelta(days=1)
        )

        start = previous_month_last_day.replace(
            day=1
        )

        return start, end

    # ==================================================
    # INVALID RANGE
    # ==================================================

    raise ValueError(
        f"Unsupported date range: {date_range}"
    )