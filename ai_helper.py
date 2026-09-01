import streamlit as st

from google import genai
from database import get_connection

from ml_prediction import (
    predict_habit_completion,
    get_recent_consistency
)


# =====================================================
# GEMINI CONFIGURATION
# =====================================================

API_KEY = st.secrets.get("GEMINI_API_KEY", "")

client = None

if API_KEY:
    try:
        client = genai.Client(
            api_key=API_KEY
        )
    except Exception:
        client = None


# =====================================================
# GET USER HABITS
# =====================================================

def get_user_habits():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT id, habit_name
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (st.session_state.user_id,)
        )

        habits = cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

    return habits


# =====================================================
# GENERATE AI RESPONSE
# =====================================================

def generate_ai_response(prompt):

    if client is None:

        return None, (
            "Gemini AI is not configured. "
            "Please add GEMINI_API_KEY in Streamlit Secrets."
        )

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response and response.text:

            return response.text, None

        return None, "Gemini did not return a response."

    except Exception as e:

        return None, str(e)


# =====================================================
# AI ASSISTANT
# =====================================================

def ai_assistant():

    st.title("AI Habit Assistant")

    st.caption(
        "Get habit insights, suggestions and simple recommendations."
    )


    # =================================================
    # SMART HABIT COACH
    # =================================================

    st.subheader("Smart Habit Coach")

    habits = get_user_habits()


    if habits:

        selected_habit = st.selectbox(
            "Select a habit",
            habits,
            format_func=lambda x: x[1],
            key="ai_habit_select"
        )

        habit_id = selected_habit[0]
        habit_name = selected_habit[1]


        # =================================================
        # CONSISTENCY
        # =================================================

        consistency = get_recent_consistency(
            habit_id
        )


        # =================================================
        # ML PREDICTION
        # =================================================

        prediction, prediction_message = (
            predict_habit_completion(
                habit_id
            )
        )


        st.markdown(
            f"### {habit_name}"
        )


        # =================================================
        # METRICS
        # =================================================

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Recent Consistency",
                f"{consistency:.1f}%"
            )


        with col2:

            if prediction is not None:

                st.metric(
                    "Completion Likelihood",
                    f"{prediction:.1f}%"
                )

            else:

                st.metric(
                    "Completion Likelihood",
                    "Not available"
                )


        # =================================================
        # SMART RECOMMENDATION
        # =================================================

        st.markdown(
            "#### Smart Recommendation"
        )


        if prediction is None:

            st.info(
                "Complete or miss this habit for at least "
                "5 days to receive an ML-based recommendation."
            )

        else:

            if prediction >= 70:

                st.success(
                    "Your consistency is strong. "
                    "Keep following your current routine."
                )

            elif prediction >= 40:

                st.warning(
                    "Your consistency is moderate. "
                    "Try completing this habit at the same "
                    "time each day."
                )

            else:

                st.info(
                    "Your completion likelihood is low. "
                    "Try a smaller target and set a fixed time "
                    "for the habit."
                )


            # =================================================
            # PERSONALIZED AI ADVICE
            # =================================================

            if st.button(
                "Generate Personalized Advice",
                use_container_width=True,
                key="personalized_advice_button"
            ):

                prompt = f"""
You are a simple AI habit coach.

Habit:
{habit_name}

Recent consistency:
{consistency:.1f}%

ML predicted completion likelihood:
{prediction:.1f}%

Give:

1. One short observation.
2. Three practical tips.
3. One simple daily goal.
4. One short motivational sentence.

Use simple language suitable for a college student.
Keep the response concise.
"""


                with st.spinner(
                    "Preparing personalized advice..."
                ):

                    response_text, error = (
                        generate_ai_response(
                            prompt
                        )
                    )


                if response_text:

                    st.markdown(
                        "#### Personalized Advice"
                    )

                    st.write(
                        response_text
                    )

                else:

                    st.error(
                        "Unable to generate AI advice."
                    )

                    st.caption(
                        error
                    )


    else:

        st.info(
            "Add a habit first to use the Smart Habit Coach."
        )


    # =================================================
    # GENERAL AI SUGGESTIONS
    # =================================================

    st.divider()

    st.subheader(
        "AI Habit Suggestions"
    )

    st.caption(
        "Describe your goals and get suggestions for improving your routine."
    )


    user_input = st.text_area(
        "Your habits or goals",
        placeholder=(
            "Example: I want to study Java for 2 hours every day."
        ),
        key="general_ai_input"
    )


    if st.button(
        "Generate Suggestions",
        key="general_ai_button",
        use_container_width=True
    ):

        if not user_input.strip():

            st.warning(
                "Please enter your habits or goals."
            )

        else:

            prompt = f"""
You are an AI productivity assistant
for a Smart Habit Tracker.

User's habits and goals:
{user_input}

Provide:

1. A simple daily routine.
2. Three habit improvement suggestions.
3. One short motivation.
4. One weekly goal.

Keep the response practical, simple and concise.
"""


            with st.spinner(
                "Generating suggestions..."
            ):

                response_text, error = (
                    generate_ai_response(
                        prompt
                    )
                )


            if response_text:

                st.markdown(
                    "#### Suggestions"
                )

                st.write(
                    response_text
                )

            else:

                st.error(
                    "Unable to generate suggestions."
                )

                st.caption(
                    error
                )