from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Natural language CRM question"
    )


class QueryIntent(BaseModel):
    module: str
    intent: str

    agent: Optional[str] = None
    customer: Optional[str] = None
    sender: Optional[str] = None

    status: Optional[str] = None
    keyword: Optional[str] = None

    date_range: Optional[str] = None

    filters: Dict[str, Any] = Field(
        default_factory=dict
    )


class CopilotResponse(BaseModel):
    answer: str
    module: Optional[str] = None
    intent: Optional[str] = None
    data: Any = None