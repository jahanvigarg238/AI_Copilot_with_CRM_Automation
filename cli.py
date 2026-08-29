from app.services.query_parser import parse_query
from app.services.response_service import (
    execute_query,
    build_response,
)
from app.utils.date_utils import get_date_range


def main():

    print("=" * 55)
    print("              CRM AI COPILOT")
    print("=" * 55)
    print()
    print(
        "Ask questions about calls, appointments, "
        "emails, or WhatsApp."
    )
    print("Type 'exit' to quit.")
    print()

    while True:

        user_query = input("You: ").strip()

        if user_query.lower() in {
            "exit",
            "quit",
        }:
            print("\nGoodbye!")
            break

        if not user_query:
            print(
                "Please enter a CRM question."
            )
            continue

        try:

            # -----------------------------
            # NLP
            # -----------------------------

            intent = parse_query(
                user_query
            )

            # -----------------------------
            # DATE RANGE
            # -----------------------------

            start, end = get_date_range(
                intent.date_range
            )

            # -----------------------------
            # DATABASE
            # -----------------------------

            result = execute_query(
                intent,
                start,
                end,
            )

            # -----------------------------
            # RESPONSE
            # -----------------------------

            response = build_response(
                user_question=user_query,
                intent=intent,
                result=result,
            )

            print(
                f"\nCopilot: {response.answer}\n"
            )

        except Exception as error:

            print(
                f"\nError: {error}\n"
            )


if __name__ == "__main__":
    main()