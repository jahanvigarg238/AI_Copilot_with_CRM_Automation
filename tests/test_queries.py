from datetime import datetime, timezone

from app.utils.date_utils import get_date_range


def test_today_range():

    fake_now = datetime(
        2026,
        8,
        28,
        12,
        0,
        tzinfo=timezone.utc
    )

    start, end = get_date_range(
        "today",
        fake_now
    )

    assert start.day == 28
    assert start.hour == 0

    assert end.day == 29
    assert end.hour == 0


def test_this_week_range():

    fake_now = datetime(
        2026,
        8,
        28,
        12,
        0,
        tzinfo=timezone.utc
    )

    start, end = get_date_range(
        "this_week",
        fake_now
    )

    assert start.weekday() == 0

    assert (
        (end - start).days == 7
    )


def test_last_7_days():

    fake_now = datetime(
        2026,
        8,
        28,
        12,
        0,
        tzinfo=timezone.utc
    )

    start, end = get_date_range(
        "last_7_days",
        fake_now
    )

    assert (
        (end - start).days == 7
    )


def test_last_3_days():

    fake_now = datetime(
        2026,
        8,
        28,
        12,
        0,
        tzinfo=timezone.utc
    )

    start, end = get_date_range(
        "last_3_days",
        fake_now
    )

    assert (
        (end - start).days == 3
    )


def test_last_month():

    fake_now = datetime(
        2026,
        8,
        28,
        12,
        0,
        tzinfo=timezone.utc
    )

    start, end = get_date_range(
        "last_month",
        fake_now
    )

    assert start.month == 7
    assert start.day == 1

    assert end.month == 8
    assert end.day == 1