from app.services.query_parser import parse_query


questions = [
    "How many calls did Priya Sharma make this week?",
    "List all failed calls in the last 7 days.",
    "What is the average call duration for completed calls?",
    "List all confirmed appointments for today.",
    "How many appointments has Neha Kapoor had this week?",
    "Find missed appointments in the last 7 days.",
    "List all emails sent by support@crm.io this week.",
    "How many emails had onboarding in the subject last month?",
    "Show emails that were not delivered successfully.",
    "List all WhatsApp messages sent by Amit Verma today.",
    "How many WhatsApp messages were delivered vs failed in the last 3 days?",
    "Find the latest message sent to Vikram Das."
]


for question in questions:

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    try:

        intent = parse_query(
            question
        )

        print("\nGEMINI OUTPUT:")

        print(
            intent.model_dump_json(
                indent=2
            )
        )

    except Exception as error:from app.services.query_parser import parse_query


questions = [
    "How many calls did Priya Sharma make this week?",
    "List all failed calls in the last 7 days.",
    "What is the average call duration for completed calls?",
    "List all confirmed appointments for today.",
    "How many appointments has Neha Kapoor had this week?",
    "Find missed appointments in the last 7 days.",
    "List all emails sent by support@crm.io this week.",
    "How many emails had onboarding in the subject last month?",
    "Show emails that were not delivered successfully.",
    "List all WhatsApp messages sent by Amit Verma today.",
    "How many WhatsApp messages were delivered vs failed in the last 3 days?",
    "Find the latest message sent to Vikram Das.",
]


for question in questions:

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    try:

        intent = parse_query(question)

        print("\nGEMINI OUTPUT:")

        print(
            intent.model_dump_json(
                indent=2
            )
        )

    except Exception as error:

        print("\nERROR:")
        print(error)

        print("\nERROR:")
        print(error)