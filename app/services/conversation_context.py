from typing import Optional

from app.models.schemas import QueryIntent


class ConversationContext:

    def __init__(self):
        self.last_intent: Optional[QueryIntent] = None

    def update(
        self,
        intent: QueryIntent
    ):
        self.last_intent = intent

    def resolve(
        self,
        intent: QueryIntent
    ) -> QueryIntent:

        if self.last_intent is None:
            return intent

        previous = self.last_intent

        # If the new query doesn't specify an agent,
        # reuse the previous agent.
        if (
            intent.agent is None
            and previous.agent is not None
            and intent.module == previous.module
        ):
            intent.agent = previous.agent

        # If the new query doesn't specify a customer,
        # reuse the previous customer.
        if (
            intent.customer is None
            and previous.customer is not None
            and intent.module == previous.module
        ):
            intent.customer = previous.customer

        # If the new query doesn't specify a date range,
        # reuse the previous date range.
        if (
            intent.date_range is None
            and previous.date_range is not None
        ):
            intent.date_range = previous.date_range

        return intent