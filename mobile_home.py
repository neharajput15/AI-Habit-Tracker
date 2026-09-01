import streamlit as st
from datetime import date, datetime

from database import get_connection
from ml_prediction import (
    get_recent_consistency,
    predict_habit_completion,
)


def mobile_home():

    # ---------------------------------------------------------
    # LOAD HABITS
    # ---------------------------------------------------------
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, habit_name, category, target, frequency, status
        FROM habits
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (st.session_state["user_id"],),
    )

    habits = cursor.fetchall()

    cursor.close()
    conn.close()

    # ---------------------------------------------------------
    # TODAY'S DATE
    # ---------------------------------------------------------
    today = date.today()
    today_text = today.strftime("%A, %d %B %Y")

    # ---------------------------------------------------------
    # GREETING
    # ---------------------------------------------------------
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good Morning 🌅"
    elif current_hour < 17:
        greeting = "Good Afternoon ☀️"
    elif current_hour < 21:
        greeting = "Good Evening 🌆"
    else:
        greeting = "Good Night 🌙"

    # ---------------------------------------------------------
    # TODAY'S COMPLETION
    # ---------------------------------------------------------
    completed_today = 0

    if habits:
        habit_ids = [habit[0] for habit in habits]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progress
            WHERE habit_id = ANY(%s)
            AND completed_date = CURRENT_DATE::text
            AND completed = 1
            """,
            (habit_ids,),
        )

        result = cursor.fetchone()
        completed_today = result[0] if result else 0

        cursor.close()
        conn.close()

    total_habits = len(habits)
    pending_today = max(total_habits - completed_today, 0)

    if total_habits > 0:
        today_progress = completed_today / total_habits
    else:
        today_progress = 0

    # ---------------------------------------------------------
    # MAIN CSS
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>

        /* ---------- PAGE ---------- */

        .stApp {
            background: #08080d;
            color: white;
        }

        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* ---------- BRAND ---------- */

        .brand-section {
            text-align: center;
            padding: 20px 10px 25px 10px;
            margin-bottom: 10px;
        }

        .brand-icon {
            font-size: 60px;
            line-height: 1;
            margin-bottom: 10px;
        }

        .brand-title {
            color: #ffffff;
            font-size: 40px;
            font-weight: 900;
            letter-spacing: 0.5px;
        }

        .brand-subtitle {
            color: #b9a9c7;
            font-size: 15px;
            margin-top: 8px;
        }

        /* ---------- WELCOME ---------- */

        .welcome-box {
            background: linear-gradient(
                135deg,
                #171020,
                #0e0c14
            );

            border: 1px solid #322044;
            border-radius: 20px;

            padding: 25px 30px;
            margin: 10px 0 25px 0;

            box-shadow: 0 10px 35px rgba(130, 70, 180, 0.12);
        }

        .welcome-title {
            font-size: 30px;
            font-weight: 800;
            color: white;
        }

        .welcome-subtitle {
            color: #b9a9c7;
            font-size: 14px;
            margin-top: 7px;
        }

        /* ---------- SECTION TITLE ---------- */

        .section-title {
            font-size: 24px;
            font-weight: 800;
            color: white;
            margin-top: 20px;
            margin-bottom: 15px;
        }

        /* ---------- STAT CARDS ---------- */

        .stat-card {
            background: linear-gradient(
                145deg,
                #15111c,
                #0d0b12
            );

            border: 1px solid #30203e;
            border-radius: 18px;

            padding: 20px;

            min-height: 125px;

            box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        }

        .stat-label {
            color: #a99ab6;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .stat-value {
            color: #ffffff;
            font-size: 32px;
            font-weight: 900;
        }

        .stat-icon {
            font-size: 25px;
            margin-bottom: 5px;
        }

        /* ---------- PROGRESS ---------- */

        .progress-card {
            background: linear-gradient(
                135deg,
                #171020,
                #0d0b12
            );

            border: 1px solid #39234b;
            border-radius: 20px;

            padding: 25px;
            margin-top: 25px;
            margin-bottom: 25px;
        }

        .progress-title {
            font-size: 20px;
            font-weight: 800;
            color: white;
        }

        .progress-number {
            font-size: 35px;
            font-weight: 900;
            color: #c084fc;
            margin-top: 5px;
        }

        .progress-text {
            color: #aaa0b1;
            font-size: 14px;
            margin-top: 5px;
        }

        /* ---------- HABIT CARD ---------- */

        .habit-card {
            background: #110d16;

            border: 1px solid #30203e;
            border-radius: 18px;

            padding: 20px;
            margin-bottom: 15px;

            transition: 0.2s;
        }

        .habit-card:hover {
            border-color: #7c3aed;
            box-shadow: 0 8px 25px rgba(124,58,237,0.12);
        }

        .habit-name {
            color: white;
            font-size: 19px;
            font-weight: 800;
        }

        .habit-info {
            color: #a99ab6;
            font-size: 13px;
            margin-top: 7px;
        }

        .habit-category {
            display: inline-block;
            background: #241631;
            color: #c084fc;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 12px;
            margin-top: 10px;
        }

        .habit-status {
            color: #b9a9c7;
            font-size: 13px;
            margin-top: 8px;
        }

        /* ---------- AI PREDICTION ---------- */

        .ai-card {
            background: linear-gradient(
                135deg,
                #1b1025,
                #0d0b12
            );

            border: 1px solid #4c2864;
            border-radius: 20px;

            padding: 25px;
            margin-top: 25px;
            margin-bottom: 25px;
        }

        .ai-title {
            color: #ffffff;
            font-size: 21px;
            font-weight: 800;
        }

        .ai-subtitle {
            color: #a99ab6;
            font-size: 13px;
            margin-top: 5px;
        }

        .prediction-value {
            color: #c084fc;
            font-size: 38px;
            font-weight: 900;
            margin-top: 15px;
        }

        /* ---------- FOOTER ---------- */

        .footer {
            text-align: center;
            color: #756a7d;
            font-size: 12px;
            margin-top: 45px;
            padding: 20px;
        }

        /* ---------- STREAMLIT BUTTON ---------- */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #4c2864;
            background: #171020;
            color: white;
        }

        .stButton > button:hover {
            border-color: #a855f7;
            color: #d8b4fe;
        }

        /* ---------- PROGRESS BAR ---------- */

        .stProgress > div > div {
            background-color: #8b5cf6;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # BRAND
    # ---------------------------------------------------------
    st.markdown(
        """
        <div class="brand-section">

            <div class="brand-icon">💜</div>

            <div class="brand-title">
                AI Smart Habit Tracker
            </div>

            <div class="brand-subtitle">
                Build better habits. Track your progress. Become consistent.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # WELCOME
    # ---------------------------------------------------------
    st.markdown(
        f"""
        <div class="welcome-box">

            <div class="welcome-title">
                {greeting}
            </div>

            <div class="welcome-subtitle">
                Stay consistent and make progress every day.
                &nbsp; • &nbsp; {today_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # OVERVIEW
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-title">📊 Today\'s Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-label">Total Habits</div>
                <div class="stat-value">{total_habits}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-label">Completed Today</div>
                <div class="stat-value">{completed_today}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">⏳</div>
                <div class="stat-label">Pending</div>
                <div class="stat-value">{pending_today}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-label">Today's Progress</div>
                <div class="stat-value">
                    {int(today_progress * 100)}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # PROGRESS CARD
    # ---------------------------------------------------------
    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-title">
                🎯 Daily Progress
            </div>

            <div class="progress-number">
                {int(today_progress * 100)}%
            </div>

            <div class="progress-text">
                {completed_today} of {total_habits} habits completed today
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(today_progress)

    if total_habits == 0:
        st.info("No habits added yet. Add your first habit to get started! 💜")

    elif today_progress == 1:
        st.success("🎉 Amazing! You completed all your habits today!")

    elif today_progress >= 0.5:
        st.info("🔥 Great work! You're more than halfway there.")

    else:
        st.info("💪 Keep going! Complete your habits and build your streak.")

    # ---------------------------------------------------------
    # MY HABITS
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-title">📝 My Habits</div>',
        unsafe_allow_html=True,
    )

    if habits:

        for habit in habits:

            habit_id = habit[0]
            habit_name = habit[1]
            category = habit[2] or "General"
            target = habit[3] or "Daily"
            frequency = habit[4] or "Daily"
            status = habit[5] or "Pending"

            try:
                consistency = get_recent_consistency(habit_id)
            except Exception:
                consistency = 0

            st.markdown(
                f"""
                <div class="habit-card">

                    <div class="habit-name">
                        {habit_name}
                    </div>

                    <div class="habit-info">
                        🎯 Target: {target}
                        &nbsp;&nbsp;•&nbsp;&nbsp;
                        🔁 Frequency: {frequency}
                    </div>

                    <div class="habit-category">
                        {category}
                    </div>

                    <div class="habit-status">
                        Status: {status}
                        &nbsp;&nbsp;•&nbsp;&nbsp;
                        Consistency: {consistency}%
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------------------------------------------------
    # AI PREDICTION
    # ---------------------------------------------------------
    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Habit Prediction
            </div>

            <div class="ai-subtitle">
                Machine Learning prediction based on your recent habit history.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if habits:

        prediction_options = {
            habit[0]: habit[1]
            for habit in habits
        }

        selected_habit_id = st.selectbox(
            "Select a habit for prediction",
            options=list(prediction_options.keys()),
            format_func=lambda x: prediction_options[x],
        )

        if st.button("🔮 Predict Next Completion", use_container_width=True):

            try:
                prediction, error = predict_habit_completion(
                    selected_habit_id
                )

                if error:
                    st.warning(error)
                else:
                    st.markdown(
                        f"""
                        <div class="prediction-value">
                            {prediction}%
                        </div>

                        <div class="habit-info">
                            Estimated chance of completing this habit tomorrow.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error(f"Prediction error: {e}")

    else:
        st.info("Add habits first to use AI prediction.")

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    st.markdown(
        """
        <div class="footer">
            💜 AI Smart Habit Tracker
            <br>
            Build better habits. Become consistent.
        </div>
        """,
        unsafe_allow_html=True,
    )