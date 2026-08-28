from app.models.schemas import QueryIntent
from app.services.gemini_service import parse_with_gemini


SUPPORTED_MODULES = {
    "calls",
    "appointments",
    "emails",
    "whatsapp"
}


SUPPORTED_DATE_RANGES = {
    "today",
    "this_week",
    "last_7_days",
    "last_3_days",
    "last_month"
}


def normalize_text(value):
    """Normalize optional string values."""

    if value is None:
        return None

    value = value.strip()

    return value if value else None


def parse_query(user_query: str) -> QueryIntent:
    """
    Convert natural language into a validated QueryIntent.
    """

    raw_intent = parse_with_gemini(user_query)

    intent = QueryIntent(
        module=normalize_text(
            raw_intent.get("module")
        ),
        intent=normalize_text(
            raw_intent.get("intent")
        ),
        agent=normalize_text(
            raw_intent.get("agent")
        ),
        customer=normalize_text(
            raw_intent.get("customer")
        ),
        sender=normalize_text(
            raw_intent.get("sender")
        ),
        status=normalize_text(
            raw_intent.get("status")
        ),
        keyword=normalize_text(
            raw_intent.get("keyword")
        ),
        date_range=normalize_text(
            raw_intent.get("date_range")
        ),
        filters=raw_intent.get(
            "filters",
            {}
        )
    )

    if intent.module not in SUPPORTED_MODULES:
        raise ValueError(
            f"Unsupported CRM module: {intent.module}"
        )

    if (
        intent.date_range is not None
        and intent.date_range not in SUPPORTED_DATE_RANGES
    ):
        raise ValueError(
            f"Unsupported date range: "
            f"{intent.date_range}"
        )

    return intent