from typing import Any


def get_time_phrase(
    user_question: str,
    default: str = ""
) -> str:
    """
    Convert common time expressions in the user's
    question into a natural-language phrase.
    """

    text = user_question.lower()

    if "today" in text:
        return "today"

    if (
        "last 7 days" in text
        or "past 7 days" in text
        or "last seven days" in text
        or "past seven days" in text
    ):
        return "in the last 7 days"

    if (
        "last 3 days" in text
        or "past 3 days" in text
        or "last three days" in text
        or "past three days" in text
    ):
        return "in the last 3 days"

    if (
        "last month" in text
        or "previous month" in text
    ):
        return "last month"

    if (
        "this week" in text
        or "current week" in text
        or "so far this week" in text
    ):
        return "this week"

    return default


def generate_answer(
    user_question: str,
    module: str,
    intent: str,
    result: Any,
    query_intent=None,
) -> str:
    """
    Convert database results into concise,
    natural-language responses.
    """

    time_phrase = get_time_phrase(
        user_question
    )

    # ==================================================
    # EMPTY RESULTS
    # ==================================================

    if result is None:

        return (
            "I couldn't find any matching records "
            "for your request."
        )

    if isinstance(result, list) and len(result) == 0:

        return (
            "I couldn't find any matching records "
            "for your request."
        )

    # ==================================================
    # CALLS
    # ==================================================

    if module == "calls":

        agent = None
        status = None

        if query_intent:

            agent = getattr(
                query_intent,
                "agent",
                None
            )

            status = getattr(
                query_intent,
                "status",
                None
            )

        # ----------------------------------------------
        # Count calls
        # ----------------------------------------------

        if intent == "count":

            if agent:

                return (
                    f"{agent} made {result} calls"
                    + (
                        f" {time_phrase}"
                        if time_phrase
                        else ""
                    )
                    + "."
                )

            return (
                f"There were {result} calls"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Failed calls
        # ----------------------------------------------

        if (
            intent == "list"
            and status == "failed"
        ):

            return (
                f"I found {len(result)} failed calls"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Average call duration
        # ----------------------------------------------

        if intent == "average":

            return (
                "Completed calls had an average "
                f"duration of {result} minutes."
            )

    # ==================================================
    # APPOINTMENTS
    # ==================================================

    if module == "appointments":

        agent = None
        status = None

        if query_intent:

            agent = getattr(
                query_intent,
                "agent",
                None
            )

            status = getattr(
                query_intent,
                "status",
                None
            )

        # ----------------------------------------------
        # Count appointments
        # ----------------------------------------------

        if intent == "count":

            if agent:

                return (
                    f"{agent} had {result} appointments"
                    + (
                        f" {time_phrase}"
                        if time_phrase
                        else ""
                    )
                    + "."
                )

            return (
                f"There were {result} appointments"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Agent-specific natural-language question
        #
        # Example:
        # "Can you tell me Neha's appointments
        #  this week?"
        #
        # The router returns an integer even though
        # Gemini may classify the intent as "list".
        # ----------------------------------------------

        if (
            intent == "list"
            and agent
            and not status
            and isinstance(result, int)
        ):

            return (
                f"{agent} had {result} appointments"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Confirmed appointments
        # ----------------------------------------------

        if (
            intent == "list"
            and status == "confirmed"
        ):

            return (
                f"I found {len(result)} confirmed "
                f"appointments"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Missed appointments
        # ----------------------------------------------

        if (
            intent == "list"
            and status == "missed"
        ):

            return (
                f"I found {len(result)} missed "
                f"appointments"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

    # ==================================================
    # EMAILS
    # ==================================================

    if module == "emails":

        sender = None
        keyword = None
        status = None

        if query_intent:

            sender = getattr(
                query_intent,
                "sender",
                None
            )

            keyword = getattr(
                query_intent,
                "keyword",
                None
            )

            status = getattr(
                query_intent,
                "status",
                None
            )

        # ----------------------------------------------
        # Emails by sender
        # ----------------------------------------------

        if (
            intent == "list"
            and sender
        ):

            return (
                f"I found {len(result)} emails "
                f"sent by {sender}"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Subject keyword count
        # ----------------------------------------------

        if (
            intent == "count"
            and keyword
        ):

            return (
                f"There were {result} emails "
                f"with '{keyword}' in the subject"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Undelivered emails
        # ----------------------------------------------

        if (
            intent == "list"
            and status == "failed"
        ):

            return (
                f"I found {len(result)} emails "
                "that were not delivered successfully."
            )

    # ==================================================
    # WHATSAPP
    # ==================================================

    if module == "whatsapp":

        agent = None
        customer = None

        if query_intent:

            agent = getattr(
                query_intent,
                "agent",
                None
            )

            customer = getattr(
                query_intent,
                "customer",
                None
            )

        # ----------------------------------------------
        # Delivery status counts
        # ----------------------------------------------

        if intent == "count":

            if isinstance(result, dict):

                delivered = result.get(
                    "delivered",
                    0
                )

                failed = result.get(
                    "failed",
                    0
                )

                return (
                    f"{delivered} WhatsApp messages "
                    f"were delivered and {failed} "
                    f"failed"
                    + (
                        f" {time_phrase}"
                        if time_phrase
                        else ""
                    )
                    + "."
                )

            return (
                f"There were {result} WhatsApp messages"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Messages by agent
        # ----------------------------------------------

        if (
            intent == "list"
            and agent
        ):

            return (
                f"I found {len(result)} WhatsApp "
                f"messages sent by {agent}"
                + (
                    f" {time_phrase}"
                    if time_phrase
                    else ""
                )
                + "."
            )

        # ----------------------------------------------
        # Latest message
        # ----------------------------------------------

        if intent == "latest":

            if isinstance(result, dict):

                message = result.get(
                    "message"
                )

                if message:

                    if customer:

                        return (
                            f'The latest message sent '
                            f'to {customer} was: '
                            f'"{message}"'
                        )

                    return (
                        f'The latest message was: '
                        f'"{message}"'
                    )

            return (
                "I found the latest WhatsApp message."
            )

    # ==================================================
    # GENERIC FALLBACK
    # ==================================================

    if isinstance(result, list):

        return (
            f"I found {len(result)} matching "
            f"{module} records."
        )

    return str(result)