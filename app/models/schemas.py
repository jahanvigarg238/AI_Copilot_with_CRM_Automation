from typing import Any, Optional

from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Natural language CRM question"
    )


class QueryIntent(BaseModel):
    module: str = Field(
        description="CRM module: calls, appointments, emails, or whatsapp"
    )

    intent: str = Field(
        description="Operation to perform"
    )

    agent: Optional[str] = Field(
        default=None,
        description="CRM agent name"
    )

    customer: Optional[str] = Field(
        default=None,
        description="Customer name"
    )

    sender: Optional[str] = Field(
        default=None,
        description="Email sender"
    )

    status: Optional[str] = Field(
        default=None,
        description="Status such as failed, missed, confirmed"
    )

    keyword: Optional[str] = Field(
        default=None,
        description="Keyword to search for"
    )

    date_range: Optional[str] = Field(
        default=None,
        description="Date range such as today, this_week, last_7_days"
    )


class CopilotResponse(BaseModel):
    answer: str
    module: Optional[str] = None
    intent: Optional[str] = None
    data: Any = None