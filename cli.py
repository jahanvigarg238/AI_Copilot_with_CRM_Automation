from app.services.query_parser import parse_query
from app.services.response_service import (
    execute_query,
    format_answer,
)


def main():

    print("=" * 50)
    print("             CRM AI COPILOT")
    print("=" * 50)

    print(
        "\nAsk questions about calls, appointments, "
        "emails, or WhatsApp."
    )

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        user_query = input("You: ").strip()

        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        if not user_query:
            continue

        try:

            intent = parse_query(
                user_query
            )

            result = execute_query(
                intent
            )

            answer = format_answer(
                intent,
                result
            )

            print(
                f"\nCopilot: {answer}\n"
            )

        except Exception as error:

            print(
                f"\nCopilot: I couldn't process "
                f"that request. {error}\n"
            )


if __name__ == "__main__":
    main()