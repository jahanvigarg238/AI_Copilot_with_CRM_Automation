from typing import Any


def generate_answer(
    user_question: str,
    module: str,
    intent: str,
    result: Any,
    query_intent=None,
) -> str:

    # ==========================================
    # NO RESULTS
    # ==========================================

    if result is None:
        return "I couldn't find any matching records."

    if isinstance(result, list) and not result:
        return "I couldn't find any matching records."

    # ==========================================
    # CALLS
    # ==========================================

    if module == "calls":

        # Count
        if intent == "count":

            agent = None

            if query_intent:
                agent = getattr(
                    query_intent,
                    "agent",
                    None
                )

            if agent:
                return (
                    f"{agent} made {result} "
                    f"calls this week."
                )

            return (
                f"There were {result} calls."
            )

        # Average
        if intent == "average":

            return (
                f"The average duration of "
                f"completed calls is {result} minutes."
            )

        # List
        if intent == "list":

            count = len(result)

            return (
                f"I found {count} failed calls "
                f"in the last 7 days."
            )

    # ==========================================
    # APPOINTMENTS
    # ==========================================

    if module == "appointments":

        if intent == "count":

            agent = None

            if query_intent:
                agent = getattr(
                    query_intent,
                    "agent",
                    None
                )

            if agent:
                return (
                    f"{agent} had {result} "
                    f"appointments this week."
                )

            return (
                f"There were {result} appointments."
            )

        if intent == "list":

            count = len(result)

            return (
                f"I found {count} matching "
                f"appointments."
            )

    # ==========================================
    # EMAILS
    # ==========================================

    if module == "emails":

        if intent == "count":

            return (
                f"There were {result} "
                f"matching emails."
            )

        if intent == "list":

            count = len(result)

            return (
                f"I found {count} matching emails."
            )

    # ==========================================
    # WHATSAPP
    # ==========================================

    if module == "whatsapp":

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
                    f"failed."
                )

            return (
                f"There were {result} "
                f"WhatsApp messages."
            )

        if intent == "list":

            count = len(result)

            return (
                f"I found {count} WhatsApp messages."
            )

        if intent == "latest":

            if isinstance(result, dict):

                message = result.get(
                    "message"
                )

                if message:

                    return (
                        f'The latest message was: '
                        f'"{message}"'
                    )

            return (
                "I found the latest WhatsApp message."
            )

    # ==========================================
    # FALLBACK
    # ==========================================

    return str(result)