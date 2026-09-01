import streamlit as st
from datetime import date, datetime

from database import get_connection
from ml_prediction import (
    get_recent_consistency,
    predict_habit_completion
)


def mobile_home():

    # =========================================================
    # PAGE CSS
    # =========================================================

    st.markdown(
        """
        <style>

        /* ================================
           MAIN PAGE
        ================================= */

        .stApp {
            background: #08080d;
            color: white;
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        /* ================================
           BRAND
        ================================= */

        .brand-section {
            text-align: center;
            padding: 15px 10px 25px 10px;
        }

        .brand-icon {
            font-size: 60px;
            line-height: 1;
            margin-bottom: 10px;
        }

        .brand-title {
            color: white;
            font-size: 40px;
            font-weight: 900;
            letter-spacing: -1px;
        }

        .brand-subtitle {
            color: #b9a9c7;
            font-size: 15px;
            margin-top: 8px;
        }

        /* ================================
           WELCOME
        ================================= */

        .welcome-section {
            text-align: center;
            margin-top: 10px;
            margin-bottom: 30px;
        }

        .welcome-title {
            color: white;
            font-size: 34px;
            font-weight: 800;
        }

        .welcome-subtitle {
            color: #a99bb4;
            font-size: 15px;
            margin-top: 8px;
        }

        /* ================================
           SECTION TITLE
        ================================= */

        .section-title {
            color: white;
            font-size: 22px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 18px;
        }

        /* ================================
           STAT CARDS
        ================================= */

        .stat-card {
            background: #111118;
            border: 1px solid #292333;
            border-radius: 18px;
            padding: 22px;
            min-height: 145px;
            text-align: left;
        }

        .stat-icon {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .stat-label {
            color: #a99bb4;
            font-size: 14px;
            font-weight: 600;
        }

        .stat-value {
            color: white;
            font-size: 32px;
            font-weight: 900;
            margin-top: 4px;
        }

        /* ================================
           PROGRESS
        ================================= */

        .progress-card {
            background: #111118;
            border: 1px solid #292333;
            border-radius: 20px;
            padding: 25px;
            margin-top: 25px;
        }

        .progress-title {
            color: white;
            font-size: 20px;
            font-weight: 800;
        }

        .progress-number {
            color: #c084fc;
            font-size: 40px;
            font-weight: 900;
            margin-top: 10px;
        }

        .progress-text {
            color: #a99bb4;
            font-size: 14px;
        }

        .progress-bar-bg {
            width: 100%;
            height: 12px;
            background: #292333;
            border-radius: 20px;
            margin-top: 18px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background: #a855f7;
            border-radius: 20px;
        }

        .motivation {
            color: #d8cbe0;
            font-size: 14px;
            margin-top: 15px;
        }

        /* ================================
           HABIT CARDS
        ================================= */

        .habit-card {
            background: #111118;
            border: 1px solid #292333;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .habit-name {
            color: white;
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .habit-info {
            color: #aaa0b0;
            font-size: 14px;
            margin-bottom: 12px;
        }

        .habit-category {
            display: inline-block;
            background: #241735;
            color: #d8a8ff;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .habit-status {
            color: #aaa0b0;
            font-size: 13px;
        }

        /* ================================
           AI SECTION
        ================================= */

        .ai-card {
            background: #111118;
            border: 1px solid #292333;
            border-radius: 20px;
            padding: 25px;
            margin-top: 25px;
        }

        .ai-title {
            color: white;
            font-size: 21px;
            font-weight: 800;
        }

        .ai-subtitle {
            color: #a99bb4;
            font-size: 14px;
            margin-top: 6px;
            margin-bottom: 20px;
        }

        .prediction-box {
            background: #1a1223;
            border: 1px solid #43245c;
            border-radius: 15px;
            padding: 20px;
            margin-top: 15px;
        }

        .prediction-value {
            color: #c084fc;
            font-size: 35px;
            font-weight: 900;
        }

        .prediction-text {
            color: #b9a9c7;
            font-size: 14px;
        }

        /* ================================
           STREAMLIT BUTTONS
        ================================= */

        .stButton > button {
            background: #a855f7;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: #9333ea;
            color: white;
        }

        /* ================================
           FOOTER
        ================================= */

        .footer {
            text-align: center;
            color: #71677a;
            font-size: 13px;
            margin-top: 40px;
            padding-top: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # BRAND
    # =========================================================

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # GET USER
    # =========================================================

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    # =========================================================
    # LOAD HABITS
    # =========================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, habit_name, category, target, frequency, status
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        habits = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    # =========================================================
    # TODAY'S DATE
    # =========================================================

    today = date.today()

    # =========================================================
    # COMPLETED TODAY
    # =========================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h ON p.habit_id = h.id
            WHERE h.user_id = %s
              AND p.completed_date = CURRENT_DATE
              AND p.completed = 1
            """,
            (user_id,)
        )

        completed_today = cursor.fetchone()[0]

    finally:
        cursor.close()
        conn.close()

    total_habits = len(habits)
    pending = max(total_habits - completed_today, 0)

    if total_habits > 0:
        progress = round(
            (completed_today / total_habits) * 100
        )
    else:
        progress = 0

    # =========================================================
    # GREETING
    # =========================================================

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning 🌅"
    elif hour < 17:
        greeting = "Good Afternoon ☀️"
    elif hour < 21:
        greeting = "Good Evening 🌆"
    else:
        greeting = "Good Night 🌙"

    today_text = today.strftime("%A, %d %B %Y")

    st.markdown(
        f"""
        <div class="welcome-section">

            <div class="welcome-title">
                {greeting}
            </div>

            <div class="welcome-subtitle">
                Stay consistent and make progress every day.
                &nbsp; • &nbsp;
                {today_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # TODAY'S OVERVIEW
    # =========================================================

    st.markdown(
        """
        <div class="section-title">
            📊 Today's Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    📋
                </div>

                <div class="stat-label">
                    Total Habits
                </div>

                <div class="stat-value">
                    {total_habits}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ✅
                </div>

                <div class="stat-label">
                    Completed Today
                </div>

                <div class="stat-value">
                    {completed_today}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ⏳
                </div>

                <div class="stat-label">
                    Pending
                </div>

                <div class="stat-value">
                    {pending}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🎯
                </div>

                <div class="stat-label">
                    Today's Progress
                </div>

                <div class="stat-value">
                    {progress}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # DAILY PROGRESS
    # =========================================================

    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-title">
                🎯 Daily Progress
            </div>

            <div class="progress-number">
                {progress}%
            </div>

            <div class="progress-text">
                {completed_today} of {total_habits}
                habits completed today
            </div>

            <div class="progress-bar-bg">
                <div
                    class="progress-bar-fill"
                    style="width:{progress}%;">
                </div>
            </div>

            <div class="motivation">
                🔥
                {"Great work! You're more than halfway there." if progress >= 50
                else "Keep going! Every small step counts."}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # MY HABITS
    # =========================================================

    st.markdown(
        """
        <div class="section-title">
            📝 My Habits
        </div>
        """,
        unsafe_allow_html=True
    )

    if not habits:

        st.info("No habits added yet. Add your first habit!")

    else:

        for habit in habits:

            habit_id = habit[0]
            habit_name = habit[1]
            category = habit[2] or "General"
            target = habit[3] or "-"
            frequency = habit[4] or "Daily"
            status = habit[5] or "Pending"

            # Get consistency
            try:
                consistency = get_recent_consistency(habit_id)
            except Exception:
                consistency = 0

            # Check today's status
            conn = get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    SELECT completed
                    FROM progress
                    WHERE habit_id = %s
                      AND completed_date = CURRENT_DATE
                    LIMIT 1
                    """,
                    (habit_id,)
                )

                result = cursor.fetchone()

            finally:
                cursor.close()
                conn.close()

            if result and result[0] == 1:
                display_status = "Completed"
            else:
                display_status = "Pending"

            st.markdown(
                f"""
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
                """,
                unsafe_allow_html=True
            )

    # =========================================================
    # AI HABIT PREDICTION
    # =========================================================

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Habit Prediction
            </div>

            <div class="ai-subtitle">
                Machine Learning prediction based on
                your recent habit history.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if habits:

        habit_options = {
            f"{h[1]}": h[0]
            for h in habits
        }

        selected_habit = st.selectbox(
            "Select a habit for prediction",
            list(habit_options.keys())
        )

        selected_id = habit_options[selected_habit]

        if st.button("🔮 Predict Completion"):

            prediction, error = predict_habit_completion(
                selected_id
            )

            if error:

                st.warning(error)

            else:

                st.markdown(
                    f"""
                    <div class="prediction-box">

                        <div class="prediction-value">
                            {prediction}%
                        </div>

                        <div class="prediction-text">
                            Predicted probability of completing
                            <b>{selected_habit}</b> tomorrow.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("Add a habit to use AI prediction.")

    # =========================================================
    # FOOTER
    # =========================================================

    st.markdown(
        """
        <div class="footer">
            💜 AI Smart Habit Tracker
            <br>
            Build better habits. Stay consistent.
        </div>
        """,
        unsafe_allow_html=True
    )