from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are the query-understanding component of a CRM AI Copilot.

Your job is ONLY to understand the user's natural-language
question and convert it into a structured QueryIntent.

The available CRM modules are:

1. calls
2. appointments
3. emails
4. whatsapp

Supported intents include:

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

Important rules:

- Never invent data.
- Never calculate the final business answer.
- Never write MongoDB queries.
- Extract the relevant agent, customer, sender,
  status, keyword, and date range when present.
- Use null when a field is not relevant.
- date_range must use one of:
  today
  this_week
  last_7_days
  last_3_days
  last_month
- For questions that do not belong to these CRM capabilities,
  identify them as unsupported.
"""


def parse_with_gemini(query: str) -> dict:
    """
    Send the user query to Gemini and receive
    structured JSON.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=query,
        config={
            "system_instruction": SYSTEM_INSTRUCTION,
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "module": {
                        "type": "STRING"
                    },
                    "intent": {
                        "type": "STRING"
                    },
                    "agent": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "customer": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "sender": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "status": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "keyword": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "date_range": {
                        "type": "STRING",
                        "nullable": True
                    },
                    "filters": {
                        "type": "OBJECT"
                    }
                },
                "required": [
                    "module",
                    "intent",
                    "agent",
                    "customer",
                    "sender",
                    "status",
                    "keyword",
                    "date_range",
                    "filters"
                ]
            }
        }
    )

    return response.parsed