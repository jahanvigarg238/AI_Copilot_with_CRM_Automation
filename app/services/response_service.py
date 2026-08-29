from typing import Any

from app.models.schemas import (
    CopilotResponse,
    QueryIntent,
)

from app.services.answer_generator import (
    generate_answer,
)

from app.queries import (
    calls,
    appointments,
    emails,
    whatsapp,
)


def execute_query(
    intent: QueryIntent,
    start,
    end,
) -> Any:

    # ==========================================
    # CALLS
    # ==========================================

    if intent.module == "calls":

        # Count calls by agent
        if intent.intent == "count":

            if not intent.agent:
                raise ValueError(
                    "Please specify the agent whose "
                    "calls you want to count."
                )

            return calls.count_calls_by_agent(
                agent=intent.agent,
                start_date=start,
                end_date=end,
            )

        # Failed calls
        if (
            intent.intent == "list"
            and intent.status == "failed"
        ):

            return calls.get_failed_calls(
                start_date=start,
                end_date=end,
            )

        # Average completed call duration
        if intent.intent == "average":

            return (
                calls
                .get_average_completed_call_duration()
            )

    # ==========================================
    # APPOINTMENTS
    # ==========================================

    if intent.module == "appointments":

        # Count appointments by agent
        if intent.intent == "count":

            if not intent.agent:
                raise ValueError(
                    "Please specify the agent whose "
                    "appointments you want to count."
                )

            return (
                appointments
                .count_appointments_by_agent(
                    agent=intent.agent,
                    start_date=start,
                    end_date=end,
                )
            )

        # Confirmed appointments
        if (
            intent.intent == "list"
            and intent.status == "confirmed"
        ):

            return (
                appointments
                .get_confirmed_appointments(
                    start_date=start,
                    end_date=end,
                )
            )

        # Missed appointments
        if (
            intent.intent == "list"
            and intent.status == "missed"
        ):

            return (
                appointments
                .get_missed_appointments(
                    start_date=start,
                    end_date=end,
                )
            )

    # ==========================================
    # EMAILS
    # ==========================================

    if intent.module == "emails":

        # Emails from a specific sender
        if (
            intent.intent == "list"
            and intent.sender
        ):

            return emails.get_emails_by_sender(
                sender=intent.sender,
                start_date=start,
                end_date=end,
            )

        # Emails containing a subject keyword
        if (
            intent.intent == "count"
            and intent.keyword
        ):

            return (
                emails
                .count_emails_by_subject_keyword(
                    keyword=intent.keyword,
                    start_date=start,
                    end_date=end,
                )
            )

        # Undelivered emails
        if (
            intent.intent == "list"
            and intent.status == "failed"
        ):

            return (
                emails
                .get_undelivered_emails()
            )

    # ==========================================
    # WHATSAPP
    # ==========================================

    if intent.module == "whatsapp":

        # Messages sent by an agent
        if (
            intent.intent == "list"
            and intent.agent
        ):

            return (
                whatsapp
                .get_messages_by_agent(
                    agent=intent.agent,
                    start_date=start,
                    end_date=end,
                )
            )

        # Delivery status counts
        if intent.intent == "count":

            return (
                whatsapp
                .get_delivery_status_counts(
                    start_date=start,
                    end_date=end,
                )
            )

        # Latest message to customer
        if intent.intent == "latest":

            if not intent.customer:
                raise ValueError(
                    "Please specify the customer."
                )

            return (
                whatsapp
                .get_latest_message_to_customer(
                    customer=intent.customer,
                )
            )

    raise ValueError(
        f"Unsupported query: "
        f"{intent.module} / {intent.intent}"
    )


def build_response(
    user_question: str,
    intent: QueryIntent,
    result: Any,
) -> CopilotResponse:

    answer = generate_answer(
        user_question=user_question,
        module=intent.module,
        intent=intent.intent,
        result=result,
        query_intent=intent,
    )

    return CopilotResponse(
        answer=answer,
        module=intent.module,
        intent=intent.intent,
        data=result,
    )