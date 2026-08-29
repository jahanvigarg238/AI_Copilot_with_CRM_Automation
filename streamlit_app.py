import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CRM AI Copilot",
    page_icon="🤖",
    layout="wide",
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 CRM AI Copilot")

st.markdown(
    """
    Ask questions about your CRM data using
    natural language.

    You can query **Calls, Appointments, Emails,
    and WhatsApp conversations**.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("CRM Modules")

    st.markdown(
        """
        **📞 Calls**

        **📅 Appointments**

        **📧 Emails**

        **💬 WhatsApp**
        """
    )

    st.divider()

    st.subheader("Example Questions")

    example_questions = [
        "How many calls did Priya Sharma make this week?",
        "List all failed calls in the last 7 days.",
        "What is the average call duration for completed calls?",
        "List all confirmed appointments for today.",
        "Show emails that were not delivered successfully.",
        "Find the latest message sent to Vikram Das.",
    ]

    for question in example_questions:

        if st.button(
            question,
            use_container_width=True,
        ):
            st.session_state.question = question


# --------------------------------------------------
# Question input
# --------------------------------------------------

question = st.text_input(
    "Ask your CRM question",
    value=st.session_state.get(
        "question",
        ""
    ),
    placeholder=(
        "e.g. How many calls did Priya Sharma "
        "make this week?"
    ),
)


# --------------------------------------------------
# Ask button
# --------------------------------------------------

if st.button(
    "Ask Copilot",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter a CRM question."
        )

    else:

        with st.spinner(
            "Analyzing your question..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "query": question
                    },
                    timeout=60,
                )

                if response.status_code == 200:

                    result = response.json()

                    # --------------------------
                    # Natural language answer
                    # --------------------------

                    st.success(
                        "Query completed"
                    )

                    st.markdown(
                        "### Answer"
                    )

                    st.info(
                        result.get(
                            "answer",
                            "No answer returned."
                        )
                    )

                    # --------------------------
                    # Query information
                    # --------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "CRM Module",
                            result.get(
                                "module",
                                "Unknown"
                            ),
                        )

                    with col2:

                        st.metric(
                            "Intent",
                            result.get(
                                "intent",
                                "Unknown"
                            ),
                        )

                    # --------------------------
                    # Raw data
                    # --------------------------

                    data = result.get(
                        "data"
                    )

                    if data is not None:

                        with st.expander(
                            "View database result"
                        ):

                            st.json(data)

                else:

                    try:
                        error_detail = response.json().get(
                            "detail",
                            response.text
                        )
                    except Exception:
                        error_detail = response.text

                    st.error(
                        f"API Error: {error_detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the CRM API. "
                    "Make sure FastAPI is running on "
                    "http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request took too long. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "CRM AI Copilot • Natural Language CRM Analytics"
)