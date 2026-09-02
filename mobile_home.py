import streamlit as st
import textwrap
from datetime import date, datetime

from database import get_connection
from ml_prediction import (
    get_recent_consistency,
    predict_habit_completion
)


# =========================================================
# HTML RENDER HELPER
# =========================================================

def render_html(html):
    st.html(textwrap.dedent(html).strip())


# =========================================================
# MOBILE HOME
# =========================================================

def mobile_home():

    # =====================================================
    # CSS
    # =====================================================

    st.markdown("""
    <style>

    .stApp {
        background: #08080d;
        color: white;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* BRAND */

    .brand-section {
        text-align: center;
        padding: 25px 20px 35px 20px;
    }

    .brand-icon {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
    }

    .brand-subtitle {
        color: #a9a0bd;
        font-size: 15px;
    }

    /* WELCOME */

    .welcome-card {
        background: #1a1b22;
        border: 1px solid #292934;
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        margin-bottom: 35px;
    }

    .welcome-title {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .welcome-subtitle {
        color: #b5adca;
        font-size: 14px;
        line-height: 1.8;
    }

    /* SECTION */

    .section-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 18px;
    }

    /* STAT CARDS */

    .stat-card {
        background: #111117;
        border: 1px solid #2c2b38;
        border-radius: 16px;
        padding: 25px 20px;
        min-height: 120px;
        margin-bottom: 18px;
    }

    .stat-icon {
        font-size: 25px;
        margin-bottom: 12px;
    }

    .stat-label {
        color: #b7a8d5;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .stat-number {
        color: white;
        font-size: 28px;
        font-weight: 800;
    }

    /* PROGRESS */

    .progress-card {
        background: #111117;
        border: 1px solid #2c2b38;
        border-radius: 16px;
        padding: 25px;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .progress-title {
        color: white;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .progress-number {
        color: #a855f7;
        font-size: 35px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .progress-text {
        color: #aaa2b9;
        font-size: 14px;
        margin-bottom: 15px;
    }

    .progress-track {
        width: 100%;
        height: 10px;
        background: #292833;
        border-radius: 20px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(
            90deg,
            #7c3aed,
            #a855f7
        );
        border-radius: 20px;
    }

    /* HABITS */

    .habit-card {
        background: #111117;
        border: 1px solid #2c2b38;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .habit-name {
        color: white;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .habit-info {
        color: #aaa2b9;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .habit-category {
        display: inline-block;
        background: #241438;
        color: #c084fc;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-bottom: 12px;
    }

    .habit-status {
        color: #c5bdcf;
        font-size: 13px;
    }

    /* AI */

    .ai-card {
        background: linear-gradient(
            135deg,
            #17101f,
            #111117
        );
        border: 1px solid #49315e;
        border-radius: 16px;
        padding: 25px;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .ai-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .ai-description {
        color: #aaa2b9;
        font-size: 14px;
    }

    .prediction-result {
        background: #241438;
        border: 1px solid #49315e;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        text-align: center;
    }

    .prediction-number {
        color: #c084fc;
        font-size: 32px;
        font-weight: 800;
    }

    .prediction-label {
        color: #b9aeca;
        font-size: 13px;
    }

    /* FOOTER */

    .footer {
        text-align: center;
        color: #756d81;
        font-size: 12px;
        padding: 30px 10px 10px 10px;
    }

    /* BUTTON */

    div.stButton > button {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #9333ea
        );
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            90deg,
            #9333ea,
            #a855f7
        );
        color: white;
    }

    /* SELECTBOX */

    div[data-baseweb="select"] > div {
        background-color: #111117;
        border-color: #383443;
    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # BRAND
    # =====================================================

    render_html("""
    <div class="brand-section">

        <div class="brand-icon">
            💜
        </div>

        <div class="brand-title">
            AI Smart Habit Tracker
        </div>

        <div class="brand-subtitle">
            Build better habits. Track your progress.
            Become consistent.
        </div>

    </div>
    """)


    # =====================================================
    # LOGIN CHECK
    # =====================================================

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return


    # =====================================================
    # GET HABITS
    # =====================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                habit_name,
                category,
                target,
                frequency,
                status
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
        """, (user_id,))

        habits = cursor.fetchall()


        # =================================================
        # COMPLETED TODAY
        # =================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h
                ON p.habit_id = h.id
            WHERE h.user_id = %s
              AND p.completed_date = CURRENT_DATE
              AND p.completed = 1
        """, (user_id,))

        completed_today = cursor.fetchone()[0]

    finally:
        cursor.close()
        conn.close()


    # =====================================================
    # CALCULATE STATS
    # =====================================================

    total_habits = len(habits)

    pending = max(
        total_habits - completed_today,
        0
    )

    if total_habits > 0:

        progress_percentage = round(
            (completed_today / total_habits) * 100
        )

    else:

        progress_percentage = 0


    progress_percentage = max(
        0,
        min(progress_percentage, 100)
    )


    # =====================================================
    # GREETING
    # =====================================================

    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good Morning 🌅"

    elif current_hour < 17:
        greeting = "Good Afternoon ☀️"

    else:
        greeting = "Good Evening 🌙"


    today = date.today().strftime(
        "%A, %d %B %Y"
    )


    # =====================================================
    # WELCOME
    # =====================================================

    render_html(f"""
    <div class="welcome-card">

        <div class="welcome-title">
            {greeting}
        </div>

        <div class="welcome-subtitle">
            Stay consistent and make progress every day.
            <br>
            {today}
        </div>

    </div>
    """)


    # =====================================================
    # TODAY'S OVERVIEW
    # =====================================================

    render_html("""
    <div class="section-title">
        📊 Today's Overview
    </div>
    """)


    # =====================================================
    # STAT CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        render_html(f"""
        <div class="stat-card">

            <div class="stat-icon">
                📋
            </div>

            <div class="stat-label">
                Total Habits
            </div>

            <div class="stat-number">
                {total_habits}
            </div>

        </div>
        """)


    with col2:

        render_html(f"""
        <div class="stat-card">

            <div class="stat-icon">
                ✅
            </div>

            <div class="stat-label">
                Completed Today
            </div>

            <div class="stat-number">
                {completed_today}
            </div>

        </div>
        """)


    with col3:

        render_html(f"""
        <div class="stat-card">

            <div class="stat-icon">
                ⏳
            </div>

            <div class="stat-label">
                Pending
            </div>

            <div class="stat-number">
                {pending}
            </div>

        </div>
        """)


    # =====================================================
    # DAILY PROGRESS
    # =====================================================

    render_html(f"""
    <div class="progress-card">

        <div class="progress-title">
            🎯 Daily Progress
        </div>

        <div class="progress-number">
            {progress_percentage}%
        </div>

        <div class="progress-text">
            {completed_today} of {total_habits}
            habits completed today
        </div>

        <div class="progress-track">

            <div
                class="progress-fill"
                style="width: {progress_percentage}%;">
            </div>

        </div>

    </div>
    """)


    # =====================================================
    # MY HABITS
    # =====================================================

    render_html("""
    <div class="section-title">
        📚 My Habits
    </div>
    """)


    # =====================================================
    # NO HABITS
    # =====================================================

    if not habits:

        render_html("""
        <div class="habit-card">

            <div class="habit-name">
                No habits added yet
            </div>

            <div class="habit-info">
                Start by adding your first habit.
            </div>

        </div>
        """)


    # =====================================================
    # HABIT CARDS
    # =====================================================

    for habit in habits:

        habit_id = habit[0]
        habit_name = habit[1]
        category = habit[2] or "General"
        target = habit[3] or "-"
        frequency = habit[4] or "Daily"


        # -----------------------------------------------
        # CONSISTENCY
        # -----------------------------------------------

        try:

            consistency = get_recent_consistency(
                habit_id
            )

        except Exception:

            consistency = 0


        # -----------------------------------------------
        # TODAY'S STATUS
        # -----------------------------------------------

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                SELECT completed
                FROM progress
                WHERE habit_id = %s
                  AND completed_date = CURRENT_DATE
                LIMIT 1
            """, (habit_id,))

            result = cursor.fetchone()

        finally:

            cursor.close()
            conn.close()


        if result and int(result[0]) == 1:

            display_status = "Completed"

        else:

            display_status = "Pending"


        # -----------------------------------------------
        # HABIT CARD
        # -----------------------------------------------

        render_html(f"""
        <div class="habit-card">

            <div class="habit-name">
                {habit_name}
            </div>

            <div class="habit-info">
                🎯 Target: {target}
                &nbsp; • &nbsp;
                🔁 Frequency: {frequency}
            </div>

            <div class="habit-category">
                {category}
            </div>

            <div class="habit-status">
                📌 Status: {display_status}
                &nbsp; • &nbsp;
                📈 Consistency: {consistency}%
            </div>

        </div>
        """)


    # =====================================================
    # AI PREDICTION CARD
    # =====================================================

    render_html("""
    <div class="ai-card">

        <div class="ai-title">
            🤖 AI Habit Prediction
        </div>

        <div class="ai-description">
            Select a habit to predict the probability
            of completing it tomorrow using ML.
        </div>

    </div>
    """)


    # =====================================================
    # AI SELECTBOX
    # =====================================================

    if habits:

        habit_options = {
            habit[1]: habit[0]
            for habit in habits
        }

        selected_habit_name = st.selectbox(
            "Select Habit",
            list(habit_options.keys())
        )

        selected_habit_id = habit_options[
            selected_habit_name
        ]


        # =================================================
        # PREDICT BUTTON
        # =================================================

        if st.button(
            "🔮 Predict Tomorrow",
            use_container_width=True
        ):

            prediction, error = (
                predict_habit_completion(
                    selected_habit_id
                )
            )

            if error:

                st.warning(error)

            else:

                render_html(f"""
                <div class="prediction-result">

                    <div class="prediction-number">
                        {prediction}%
                    </div>

                    <div class="prediction-label">
                        Probability of completing
                        "{selected_habit_name}" tomorrow
                    </div>

                </div>
                """)


    # =====================================================
    # FOOTER
    # =====================================================

    render_html("""
    <div class="footer">

        💜 AI Smart Habit Tracker

        <br>

        Build habits. Stay consistent. Grow every day.

    </div>
    """)