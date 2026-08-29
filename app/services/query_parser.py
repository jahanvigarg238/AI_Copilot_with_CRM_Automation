from app.models.schemas import QueryIntent

from app.services.gemini_service import (
    parse_with_gemini,
)

from app.services.fallback_nlu import (
    parse_fallback,
)


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


def validate_intent(
    intent: QueryIntent
) -> QueryIntent:

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


def parse_query(
    user_query: str
) -> QueryIntent:

    try:

        # Primary NLP engine
        intent = parse_with_gemini(
            user_query
        )

        return validate_intent(intent)

    except Exception as error:

        error_text = str(error).lower()

        # Use local NLU when Gemini quota/API
        # is temporarily unavailable.
        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota" in error_text
            or "rate limit" in error_text
            or "503" in error_text
            or "500" in error_text
        ):

            print(
                "Gemini unavailable. "
                "Using fallback NLU."
            )

            intent = parse_fallback(
                user_query
            )

            return validate_intent(intent)

        # Don't hide genuine programming errors
        raise