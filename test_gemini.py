from google import genai

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Say hello and tell me you are working."
)

print(response.text)