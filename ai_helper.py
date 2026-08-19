import streamlit as st
import sqlite3

from google import genai
from nlp_helper import analyze_habit

from ml_prediction import (
    predict_habit_completion,
    get_recent_consistency
)


# =====================================================
# GEMINI CONFIGURATION
# =====================================================

# API key is stored securely in Streamlit Secrets
API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(
    api_key=API_KEY
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect("habit_tracker.db")


# =====================================================
# GET USER HABITS
# =====================================================

def get_user_habits():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, habit_name
        FROM habits
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (st.session_state.user_id,)
    )

    habits = cursor.fetchall()

    conn.close()

    return habits


# =====================================================
# AI HABIT ASSISTANT
# =====================================================

def ai_assistant():

    st.header("🤖 AI Habit Assistant")

    # =================================================
    # ML-BASED HABIT COACH
    # =================================================

    st.subheader("📊 Smart Habit Coach")

    habits = get_user_habits()

    if habits:

        selected_habit = st.selectbox(
            "Select a habit for AI analysis",
            habits,
            format_func=lambda x: x[1],
            key="ai_habit_select"
        )

        habit_id = selected_habit[0]
        habit_name = selected_habit[1]

        # ---------------------------------------------
        # GET CONSISTENCY
        # ---------------------------------------------

        consistency = get_recent_consistency(
            habit_id
        )

        # ---------------------------------------------
        # GET ML PREDICTION
        # ---------------------------------------------

        prediction, prediction_message = (
            predict_habit_completion(
                habit_id
            )
        )

        st.write(
            f"### 📚 {habit_name}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📊 Recent Consistency",
                f"{consistency:.1f}%"
            )

        with col2:

            if prediction is not None:

                st.metric(
                    "🤖 Completion Likelihood",
                    f"{prediction:.1f}%"
                )

            else:

                st.metric(
                    "🤖 Completion Likelihood",
                    "Not available"
                )

        # ---------------------------------------------
        # AI RECOMMENDATION
        # ---------------------------------------------

        st.write(
            "### 💡 Smart Recommendation"
        )

        if prediction is None:

            st.info(
                "Complete or miss this habit for at least "
                "5 days to receive an ML-based recommendation."
            )

        else:

            if prediction >= 70:

                st.success(
                    "🎯 Excellent! Your habit consistency "
                    "is strong. Keep following your routine."
                )

            elif prediction >= 40:

                st.warning(
                    "⚠️ Your consistency is moderate. "
                    "Try completing this habit at the same "
                    "time every day."
                )

            else:

                st.error(
                    "📌 Your completion likelihood is low. "
                    "Set a fixed time, start with a small target, "
                    "and avoid skipping the habit."
                )

            # -----------------------------------------
            # AI BUTTON
            # -----------------------------------------

            if st.button(
                "✨ Generate Personalized AI Advice",
                use_container_width=True
            ):

                prompt = f"""
You are an AI habit coach.

Habit:
{habit_name}

Recent consistency:
{consistency:.1f}%

ML predicted completion likelihood:
{prediction:.1f}%

Give the user:
1. One short observation about their habit.
2. Three practical improvement tips.
3. One simple daily goal.
4. One motivational sentence.

Keep the answer simple and suitable for a student.
Do not use complicated words.
"""

                try:

                    with st.spinner(
                        "🤖 AI is preparing personalized advice..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt
                        )

                    st.subheader(
                        "💡 Personalized AI Advice"
                    )

                    if response.text:

                        st.write(
                            response.text
                        )

                    else:

                        st.warning(
                            "Gemini did not return a response."
                        )

                except Exception as e:

                    st.error(
                        "Unable to connect to Gemini AI."
                    )

                    st.caption(
                        f"Gemini Error: {e}"
                    )

    else:

        st.info(
            "➕ Add a habit first to use the Smart Habit Coach."
        )

    # =================================================
    # GENERATIVE AI
    # =================================================

    st.markdown("---")

    st.subheader(
        "✨ General AI Habit Suggestions"
    )

    user_input = st.text_area(
        "Tell me about your habits or goals",
        placeholder=(
            "Example: I want to study Java "
            "for 2 hours every day..."
        ),
        key="general_ai_input"
    )

    if st.button(
        "✨ Generate AI Suggestion",
        key="general_ai_button"
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

1. Daily routine
2. Habit improvement suggestions
3. Short motivation
4. Weekly goal

Keep the answer simple, practical and encouraging.
"""

            try:

                with st.spinner(
                    "🤖 AI is preparing suggestions..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                st.subheader(
                    "💡 AI Suggestions"
                )

                if response.text:

                    st.write(
                        response.text
                    )

                else:

                    st.warning(
                        "Gemini did not return any response."
                    )

            except Exception as e:

                st.error(
                    "Unable to connect to Gemini AI."
                )

                st.caption(
                    f"Gemini Error: {e}"
                )

    # =================================================
    # NLP HABIT ANALYZER
    # =================================================

    st.markdown("---")

    st.subheader(
        "🧠 NLP Habit Analyzer"
    )

    text = st.text_input(
        "Describe your habit",
        placeholder=(
            "Example: I want to study Java "
            "for 2 hours every day"
        ),
        key="nlp_habit_input"
    )

    if st.button(
        "🧠 Analyze Habit",
        key="nlp_button"
    ):

        if not text.strip():

            st.warning(
                "Please describe your habit."
            )

        else:

            try:

                result = analyze_habit(
                    text
                )

                st.write(
                    "### 📊 NLP Result"
                )

                st.write(
                    f"**Habit:** {result['habit']}"
                )

                st.write(
                    f"**Duration:** {result['duration']}"
                )

                st.write(
                    f"**Frequency:** {result['frequency']}"
                )

                st.write(
                    f"**Category:** {result['category']}"
                )

            except Exception as e:

                st.error(
                    "Unable to analyze the habit."
                )

                st.caption(
                    f"NLP Error: {e}"
                )