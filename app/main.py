from fastapi import FastAPI, HTTPException

from app.models.schemas import (
    UserQuery,
)

from app.services.query_parser import (
    parse_query,
)

from app.services.response_service import (
    execute_query,
    build_response,
)

from app.utils.date_utils import (
    get_date_range,
)
from app.services.conversation_context import (
    ConversationContext,
)


app = FastAPI(
    title="CRM AI Copilot",
    description="Natural-language CRM query assistant",
    version="1.0.0",
)
conversation_context = ConversationContext()


@app.get("/")
def root():

    return {
        "message": "CRM AI Copilot is running"
    }


@app.get("/health")
def health():

    from app.database.connection import (
        check_database_connection,
    )

    return {
        "status": "healthy",
        "mongodb": check_database_connection(),
    }


@app.post("/ask")
def ask(query: UserQuery):

    try:

        # --------------------------
        # NLP
        # --------------------------

        intent = parse_query(
            query.query
        )
        intent = conversation_context.resolve(
            intent
        )

        conversation_context.update(
            intent
        )   

        # --------------------------
        # DATE RESOLUTION
        # --------------------------

        start, end = get_date_range(
            intent.date_range
        )

        # --------------------------
        # MONGODB
        # --------------------------

        result = execute_query(
            intent,
            start,
            end,
        )

        # --------------------------
        # NATURAL RESPONSE
        # --------------------------

        return build_response(
            user_question=query.query,
            intent=intent,
            result=result,
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )