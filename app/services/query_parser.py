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


# --------------------------------------------------
# Entity normalization
# --------------------------------------------------

AGENT_ALIASES = {
    "priya": "Priya Sharma",
    "priya sharma": "Priya Sharma",

    "neha": "Neha Kapoor",
    "neha kapoor": "Neha Kapoor",

    "amit": "Amit Verma",
    "amit verma": "Amit Verma",
}


CUSTOMER_ALIASES = {
    "vikram": "Vikram Das",
    "vikram das": "Vikram Das",
}


def normalize_agent(agent: str | None) -> str | None:

    if not agent:
        return None

    cleaned = agent.strip().lower()

    return AGENT_ALIASES.get(
        cleaned,
        agent.strip()
    )


def normalize_customer(
    customer: str | None
) -> str | None:

    if not customer:
        return None

    cleaned = customer.strip().lower()

    return CUSTOMER_ALIASES.get(
        cleaned,
        customer.strip()
    )


def normalize_intent(
    intent: QueryIntent
) -> QueryIntent:

    # Normalize agent names
    if intent.agent:

        intent.agent = normalize_agent(
            intent.agent
        )

    # Normalize customer names
    if intent.customer:

        intent.customer = normalize_customer(
            intent.customer
        )

    # Normalize module
    if intent.module:

        intent.module = (
            intent.module
            .strip()
            .lower()
        )

    # Normalize intent
    if intent.intent:

        intent.intent = (
            intent.intent
            .strip()
            .lower()
        )

    # Normalize status
    if intent.status:

        intent.status = (
            intent.status
            .strip()
            .lower()
        )

    # Normalize date range
    if intent.date_range:

        intent.date_range = (
            intent.date_range
            .strip()
            .lower()
        )

    return intent


def validate_intent(
    intent: QueryIntent
) -> QueryIntent:

    intent = normalize_intent(
        intent
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


def parse_query(
    user_query: str
) -> QueryIntent:

    try:

        # ------------------------------------------
        # Primary NLP engine
        # ------------------------------------------

        intent = parse_with_gemini(
            user_query
        )

        return validate_intent(
            intent
        )

    except Exception as error:

        error_text = str(error).lower()

        # ------------------------------------------
        # Fallback NLU
        # ------------------------------------------

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

            return validate_intent(
                intent
            )

        # Don't hide genuine programming errors
        raise