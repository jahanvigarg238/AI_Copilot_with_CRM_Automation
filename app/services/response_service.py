from typing import Any

from app.models.schemas import QueryIntent
from app.queries import (
    calls,
    appointments,
    emails,
    whatsapp,
)
from app.utils.date_utils import get_date_range


def execute_query(
    intent: QueryIntent
) -> Any:
    """
    Route a validated QueryIntent to the
    appropriate deterministic MongoDB query.
    """

    module = intent.module
    action = intent.intent

    # =========================================
    # CALLS
    # =========================================

    if module == "calls":

        if action == "count":

            if not intent.agent:
                raise ValueError(
                    "Please specify the agent."
                )

            if not intent.date_range:
                raise ValueError(
                    "Please specify a date range."
                )

            start, end = get_date_range(
                intent.date_range
            )

            return calls.count_calls_by_agent(
                intent.agent,
                start,
                end
            )

        if action == "list":

            if intent.status != "failed":
                raise ValueError(
                    "Currently, call list queries "
                    "support failed calls."
                )

            if not intent.date_range:
                raise ValueError(
                    "Please specify a date range."
                )

            start, end = get_date_range(
                intent.date_range
            )

            return calls.get_failed_calls(
                start,
                end
            )

        if action == "average":

            return (
                calls
                .get_average_completed_call_duration()
            )

    # =========================================
    # APPOINTMENTS
    # =========================================

    if module == "appointments":

        if action == "list":

            if intent.status == "confirmed":

                if not intent.date_range:
                    raise ValueError(
                        "Please specify a date range."
                    )

                start, end = get_date_range(
                    intent.date_range
                )

                return (
                    appointments
                    .get_confirmed_appointments(
                        start,
                        end
                    )
                )

            if intent.status == "missed":

                if not intent.date_range:
                    raise ValueError(
                        "Please specify a date range."
                    )

                start, end = get_date_range(
                    intent.date_range
                )

                return (
                    appointments
                    .get_missed_appointments(
                        start,
                        end
                    )
                )

        if action == "count":

            if not intent.agent:
                raise ValueError(
                    "Please specify the agent."
                )

            if not intent.date_range:
                raise ValueError(
                    "Please specify a date range."
                )

            start, end = get_date_range(
                intent.date_range
            )

            return (
                appointments
                .count_appointments_by_agent(
                    intent.agent,
                    start,
                    end
                )
            )

    # =========================================
    # EMAILS
    # =========================================

    if module == "emails":

        if action == "list":

            if intent.sender:

                if not intent.date_range:
                    raise ValueError(
                        "Please specify a date range."
                    )

                start, end = get_date_range(
                    intent.date_range
                )

                return (
                    emails
                    .get_emails_by_sender(
                        intent.sender,
                        start,
                        end
                    )
                )

            if intent.status in {
                "failed",
                "bounced",
                "undelivered"
            }:

                return (
                    emails
                    .get_undelivered_emails()
                )

        if action == "count":

            if intent.keyword:

                if not intent.date_range:
                    raise ValueError(
                        "Please specify a date range."
                    )

                start, end = get_date_range(
                    intent.date_range
                )

                return (
                    emails
                    .count_emails_by_subject_keyword(
                        intent.keyword,
                        start,
                        end
                    )
                )

    # =========================================
    # WHATSAPP
    # =========================================

    if module == "whatsapp":

        if action == "list":

            if not intent.agent:
                raise ValueError(
                    "Please specify the agent."
                )

            if not intent.date_range:
                raise ValueError(
                    "Please specify a date range."
                )

            start, end = get_date_range(
                intent.date_range
            )

            return (
                whatsapp
                .get_messages_by_agent(
                    intent.agent,
                    start,
                    end
                )
            )

        if action == "count":

            if not intent.date_range:
                raise ValueError(
                    "Please specify a date range."
                )

            start, end = get_date_range(
                intent.date_range
            )

            return (
                whatsapp
                .get_delivery_status_counts(
                    start,
                    end
                )
            )

        if action == "latest":

            if not intent.customer:
                raise ValueError(
                    "Please specify the customer."
                )

            return (
                whatsapp
                .get_latest_message_to_customer(
                    intent.customer
                )
            )

    raise ValueError(
        "I couldn't map that question to a "
        "supported CRM operation."
    )


def format_answer(
    intent: QueryIntent,
    result: Any
) -> str:
    """
    Convert raw MongoDB results into a concise
    user-friendly response.
    """

    # Calls
    if (
        intent.module == "calls"
        and intent.intent == "count"
    ):
        return (
            f"{intent.agent} made "
            f"{result} calls "
            f"{intent.date_range.replace('_', ' ')}."
        )

    if (
        intent.module == "calls"
        and intent.intent == "average"
    ):
        return (
            "The average duration of completed "
            f"calls is {result} minutes."
        )

    if (
        intent.module == "calls"
        and intent.intent == "list"
    ):
        return (
            f"I found {len(result)} failed calls "
            f"in {intent.date_range.replace('_', ' ')}."
        )

    # Appointments
    if (
        intent.module == "appointments"
        and intent.intent == "count"
    ):
        return (
            f"{intent.agent} had "
            f"{result} appointments "
            f"{intent.date_range.replace('_', ' ')}."
        )

    if (
        intent.module == "appointments"
        and intent.intent == "list"
    ):
        status = intent.status or "matching"

        return (
            f"I found {len(result)} "
            f"{status} appointments "
            f"{intent.date_range.replace('_', ' ')}."
        )

    # Emails
    if (
        intent.module == "emails"
        and intent.intent == "count"
    ):
        return (
            f"I found {result} emails with "
            f"'{intent.keyword}' in the subject "
            f"during {intent.date_range.replace('_', ' ')}."
        )

    if (
        intent.module == "emails"
        and intent.intent == "list"
    ):
        return (
            f"I found {len(result)} matching emails."
        )

    # WhatsApp
    if (
        intent.module == "whatsapp"
        and intent.intent == "count"
    ):
        return (
            f"In the {intent.date_range.replace('_', ' ')}, "
            f"{result['delivered']} messages were delivered "
            f"and {result['failed']} failed."
        )

    if (
        intent.module == "whatsapp"
        and intent.intent == "latest"
    ):
        if not result:
            return (
                f"No WhatsApp message was found "
                f"for {intent.customer}."
            )

        return (
            f"The latest message to {intent.customer} "
            f"was: \"{result['message']}\""
        )

    if (
        intent.module == "whatsapp"
        and intent.intent == "list"
    ):
        return (
            f"I found {len(result)} WhatsApp messages "
            f"from {intent.agent}."
        )

    return "I found the requested CRM information."