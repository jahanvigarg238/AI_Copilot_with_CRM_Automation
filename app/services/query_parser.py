from app.models.schemas import QueryIntent
from app.services.gemini_service import parse_with_gemini


SUPPORTED_MODULES = {
    "calls",
    "appointments",
    "emails",
    "whatsapp",
}


SUPPORTED_DATE_RANGES = {
    "today",
    "this_week",
    "last_7_days",
    "last_3_days",
    "last_month",
}


def parse_query(
    user_query: str
) -> QueryIntent:

    intent = parse_with_gemini(
        user_query
    )

    if intent.module not in SUPPORTED_MODULES:

        raise ValueError(
            f"Unsupported CRM module: "
            f"{intent.module}"
        )

    if (
        intent.date_range is not None
        and intent.date_range
        not in SUPPORTED_DATE_RANGES
    ):

        raise ValueError(
            f"Unsupported date range: "
            f"{intent.date_range}"
        )

    return intent