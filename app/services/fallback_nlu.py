import re

from app.models.schemas import QueryIntent


AGENTS = {
    "priya": "Priya Sharma",
    "priya sharma": "Priya Sharma",
    "neha": "Neha Kapoor",
    "neha kapoor": "Neha Kapoor",
    "amit": "Amit Verma",
    "amit verma": "Amit Verma",
}

CUSTOMERS = {
    "vikram": "Vikram Das",
    "vikram das": "Vikram Das",
}


def normalize_date(text: str):

    text = text.lower()

    if "today" in text:
        return "today"

    if (
        "this week" in text
        or "current week" in text
        or "so far this week" in text
    ):
        return "this_week"

    if (
        "last 7 days" in text
        or "past 7 days" in text
        or "last seven days" in text
    ):
        return "last_7_days"

    if (
        "last 3 days" in text
        or "past 3 days" in text
        or "last three days" in text
    ):
        return "last_3_days"

    if (
        "last month" in text
        or "previous month" in text
    ):
        return "last_month"

    return None


def extract_agent(text: str):

    text_lower = text.lower()

    for key, value in AGENTS.items():

        if key in text_lower:
            return value

    return None


def extract_customer(text: str):

    text_lower = text.lower()

    for key, value in CUSTOMERS.items():

        if key in text_lower:
            return value

    return None


def parse_fallback(
    query: str
) -> QueryIntent:

    text = query.lower()

    date_range = normalize_date(text)

    agent = extract_agent(text)

    customer = extract_customer(text)

    # --------------------------------
    # CALLS
    # --------------------------------

    if "call" in text:

        if (
            "average" in text
            or "on average" in text
            or "duration" in text
        ):

            return QueryIntent(
                module="calls",
                intent="average",
                status=(
                    "completed"
                    if "completed" in text
                    else None
                ),
                date_range=date_range,
            )

        if (
            "failed" in text
            or "unsuccessful" in text
            or "didn't connect" in text
        ):

            return QueryIntent(
                module="calls",
                intent="list",
                status="failed",
                date_range=date_range,
            )

        if (
            "how many" in text
            or "count" in text
            or "number" in text
            or "how active" in text
        ):

            return QueryIntent(
                module="calls",
                intent="count",
                agent=agent,
                date_range=date_range,
            )

    # --------------------------------
    # APPOINTMENTS
    # --------------------------------

    if (
        "appointment" in text
        or "meeting" in text
    ):

        if (
            "missed" in text
            or "no show" in text
        ):

            return QueryIntent(
                module="appointments",
                intent="list",
                status="missed",
                date_range=date_range,
            )

        if "confirmed" in text:

            return QueryIntent(
                module="appointments",
                intent="list",
                status="confirmed",
                date_range=date_range,
            )

        if (
            "how many" in text
            or "count" in text
            or "number" in text
        ):

            return QueryIntent(
                module="appointments",
                intent="count",
                agent=agent,
                date_range=date_range,
            )

    # --------------------------------
    # EMAILS
    # --------------------------------

    if (
        "email" in text
        or "emails" in text
    ):

        sender = None

        match = re.search(
            r"[\w.+-]+@[\w.-]+\.\w+",
            text,
        )

        if match:
            sender = match.group(0)

        keyword = (
            "onboarding"
            if "onboarding" in text
            else None
        )

        if (
            "failed" in text
            or "not delivered" in text
            or "unsuccessful" in text
        ):

            return QueryIntent(
                module="emails",
                intent="list",
                sender=sender,
                status="failed",
                keyword=keyword,
                date_range=date_range,
            )

        if (
            "how many" in text
            or "count" in text
            or "number" in text
        ):

            return QueryIntent(
                module="emails",
                intent="count",
                sender=sender,
                keyword=keyword,
                date_range=date_range,
            )

        return QueryIntent(
            module="emails",
            intent="list",
            sender=sender,
            keyword=keyword,
            date_range=date_range,
        )

    # --------------------------------
    # WHATSAPP
    # --------------------------------

    if (
        "whatsapp" in text
        or "message" in text
    ):

        if (
            "latest" in text
            or "most recent" in text
            or "last message" in text
        ):

            return QueryIntent(
                module="whatsapp",
                intent="latest",
                customer=customer,
            )

        return QueryIntent(
            module="whatsapp",
            intent="count"
            if (
                "how many" in text
                or "count" in text
            )
            else "list",
            agent=agent,
            customer=customer,
            date_range=date_range,
        )

    raise ValueError(
        "I couldn't understand this CRM question."
    )