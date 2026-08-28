from fastapi import FastAPI, HTTPException

from app.database.connection import check_database_connection
from app.models.schemas import (
    CopilotResponse,
    UserQuery,
)
from app.services.query_parser import parse_query
from app.services.response_service import (
    execute_query,
    format_answer,
)


app = FastAPI(
    title="CRM AI Copilot",
    description=(
        "Natural-language AI Copilot for "
        "CRM interaction data stored in MongoDB."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "CRM AI Copilot is running."
    }


@app.get("/health")
def health_check():

    database_connected = (
        check_database_connection()
    )

    return {
        "status": (
            "healthy"
            if database_connected
            else "unhealthy"
        ),
        "mongodb": database_connected,
    }


@app.post(
    "/ask",
    response_model=CopilotResponse
)
def ask_copilot(
    request: UserQuery
):

    try:

        # Step 1:
        # Understand natural language
        intent = parse_query(
            request.query
        )

        # Step 2:
        # Execute deterministic MongoDB query
        result = execute_query(
            intent
        )

        # Step 3:
        # Generate concise response
        answer = format_answer(
            intent,
            result
        )

        return CopilotResponse(
            answer=answer,
            module=intent.module,
            intent=intent.intent,
            data=result
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred: "
                f"{str(error)}"
            )
        )