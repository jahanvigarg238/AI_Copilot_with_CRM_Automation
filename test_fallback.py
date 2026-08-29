from app.services.fallback_nlu import (
    parse_fallback,
)


questions = [

    "How many calls did Priya make this week?",

    "Show me unsuccessful calls from the past 7 days.",

    "What is the average duration of completed calls?",

    "Show today's confirmed appointments.",

    "How many appointments did Neha have this week?",

    "Which appointments were missed in the last 7 days?",

    "Show emails from support@crm.io this week.",

    "How many onboarding emails were there last month?",

    "Show emails that weren't delivered.",

    "Show Amit's WhatsApp messages today.",

    "How many WhatsApp messages were delivered?",

    "What's the most recent message to Vikram Das?",
]


for question in questions:

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    try:

        intent = parse_fallback(
            question
        )

        print("\nINTENT:")

        print(
            intent.model_dump_json(
                indent=2
            )
        )

    except Exception as error:

        print("\nERROR:")
        print(error)