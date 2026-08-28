from google import genai

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)
from app.models.schemas import QueryIntent


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are the natural-language query understanding
component of a CRM AI Copilot.

Your job is ONLY to understand the user's question
and convert it into a structured QueryIntent.

Do NOT answer the question.

Do NOT invent CRM data.

Do NOT write MongoDB queries.

Supported CRM modules:

calls
appointments
emails
whatsapp

Supported intents:

calls:
- count
- list
- average

appointments:
- list
- count

emails:
- list
- count

whatsapp:
- list
- count
- latest

Supported date ranges:

today
this_week
last_7_days
last_3_days
last_month

Rules:

1. Extract the agent when the user mentions an agent.
2. Extract the customer when the user mentions a customer.
3. Extract the email sender when applicable.
4. Extract status when applicable.
5. Extract a subject keyword when applicable.
6. Convert natural language dates into the supported
   date_range values.
7. Use null for fields that are not relevant.

Examples:

Question:
How many calls did Priya Sharma make this week?

Output:
module = calls
intent = count
agent = Priya Sharma
date_range = this_week

Question:
List all failed calls in the last 7 days.

Output:
module = calls
intent = list
status = failed
date_range = last_7_days

Question:
What is the average call duration for completed calls?

Output:
module = calls
intent = average

Question:
List all confirmed appointments for today.

Output:
module = appointments
intent = list
status = confirmed
date_range = today

Question:
How many appointments has Neha Kapoor had this week?

Output:
module = appointments
intent = count
agent = Neha Kapoor
date_range = this_week

Question:
Find missed appointments in the last 7 days.

Output:
module = appointments
intent = list
status = missed
date_range = last_7_days

Question:
List all emails sent by support@crm.io this week.

Output:
module = emails
intent = list
sender = support@crm.io
date_range = this_week

Question:
How many emails had onboarding in the subject last month?

Output:
module = emails
intent = count
keyword = onboarding
date_range = last_month

Question:
Show emails that were not delivered successfully.

Output:
module = emails
intent = list
status = undelivered

Question:
List all WhatsApp messages sent by Amit Verma today.

Output:
module = whatsapp
intent = list
agent = Amit Verma
date_range = today

Question:
How many WhatsApp messages were delivered vs failed
in the last 3 days?

Output:
module = whatsapp
intent = count
date_range = last_3_days

Question:
Find the latest message sent to Vikram Das.

Output:
module = whatsapp
intent = latest
customer = Vikram Das
"""


def parse_with_gemini(
    query: str
) -> QueryIntent:

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=query,
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
            "response_mime_type": "application/json",
            "response_schema": QueryIntent,
        },
    )

    if response.parsed:
        return response.parsed

    return QueryIntent.model_validate_json(
        response.text
    )