import streamlit as st
import pandas as pd
from datetime import datetime

from database import get_connection

from ml_prediction import (
    predict_habit_completion,
    get_last_five_days,
    get_recent_consistency
)


# =====================================================
# DASHBOARD - MODERN PURPLE / BLACK UI
# =====================================================

def dashboard():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    # =================================================
    # MODERN UI CSS
    # =================================================

    st.markdown(
        """
        <style>

        /* ---------- MAIN AREA ---------- */

        .dashboard-wrapper {
            max-width: 1100px;
            margin: auto;
        }

        .welcome-title {
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .welcome-subtitle {
            font-size: 15px;
            opacity: 0.70;
            margin-bottom: 24px;
        }


        /* ---------- PURPLE HEADER ---------- */

        .hero-card {
            background: linear-gradient(
                135deg,
                #12001f,
                #32105f,
                #6d35d9
            );

            border-radius: 24px;
            padding: 28px;
            margin-bottom: 24px;

            box-shadow:
                0 12px 35px rgba(104, 57, 190, 0.28);
        }

        .hero-small {
            color: #d9c7ff;
            font-size: 14px;
            margin-bottom: 7px;
        }

        .hero-title {
            color: white !important;
            font-size: 28px;
            font-weight: 800;
            margin: 0;
        }

        .hero-text {
            color: #eee5ff !important;
            font-size: 14px;
            margin-top: 8px;
        }


        /* ---------- STAT CARDS ---------- */

        .stat-card {
            background: linear-gradient(
                145deg,
                #16001f,
                #24103b
            );

            border: 1px solid #5c3b82;

            border-radius: 20px;

            padding: 20px;

            min-height: 145px;

            box-shadow:
                0 8px 25px rgba(0,0,0,0.20);
        }

        .stat-icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .stat-title {
            color: #d8c8ea !important;
            font-size: 13px;
            font-weight: 600;
        }

        .stat-value {
            color: white !important;
            font-size: 30px;
            font-weight: 800;
            margin-top: 5px;
        }


        /* ---------- SECTION ---------- */

        .section-title {
            font-size: 22px;
            font-weight: 800;
            margin-top: 28px;
            margin-bottom: 15px;
        }


        /* ---------- PROGRESS CARD ---------- */

        .progress-card {
            background: linear-gradient(
                135deg,
                #1b062b,
                #32105b
            );

            border-radius: 22px;

            padding: 24px;

            border: 1px solid #654298;

            box-shadow:
                0 8px 25px rgba(0,0,0,0.18);
        }

        .progress-number {
            color: white !important;
            font-size: 42px;
            font-weight: 900;
        }

        .progress-text {
            color: #d8c9e8 !important;
            font-size: 14px;
        }


        /* ---------- HABIT CARD ---------- */

        .habit-card {
            background: linear-gradient(
                145deg,
                #15001e,
                #251033
            );

            border: 1px solid #4d3268;

            border-radius: 20px;

            padding: 20px;

            margin-bottom: 14px;

            box-shadow:
                0 7px 20px rgba(0,0,0,0.16);
        }

        .habit-name {
            color: white !important;
            font-size: 19px;
            font-weight: 750;
        }

        .habit-info {
            color: #cfc0dd !important;
            font-size: 13px;
            margin-top: 5px;
        }

        .habit-target {
            color: #e3d5ef !important;
            font-size: 13px;
            margin-top: 10px;
        }

        .percentage {
            color: #b98cff !important;
            font-size: 20px;
            font-weight: 800;
        }


        /* ---------- STATUS ---------- */

        .completed-status {
            display: inline-block;

            background: #2c1644;

            color: #d8b8ff !important;

            border: 1px solid #754bb2;

            border-radius: 30px;

            padding: 5px 12px;

            font-size: 12px;

            font-weight: 700;
        }

        .pending-status {
            display: inline-block;

            background: #24182c;

            color: #e5c9ff !important;

            border: 1px solid #634b72;

            border-radius: 30px;

            padding: 5px 12px;

            font-size: 12px;

            font-weight: 700;
        }


        /* ---------- AI CARD ---------- */

        .ai-card {
            background: linear-gradient(
                135deg,
                #100019,
                #32105d,
                #5420a1
            );

            border-radius: 24px;

            padding: 25px;

            border: 1px solid #7144ae;

            box-shadow:
                0 12px 30px rgba(86, 39, 150, 0.25);
        }

        .ai-title {
            color: white !important;
            font-size: 23px;
            font-weight: 800;
        }

        .ai-text {
            color: #e4d9f0 !important;
            font-size: 14px;
        }


        /* ---------- HISTORY ---------- */

        .history-box {
            background: #170020;

            border-radius: 18px;

            padding: 18px;

            border: 1px solid #4d3168;
        }

        .history-icons {
            font-size: 28px;
            letter-spacing: 7px;
        }


        /* ---------- STREAMLIT BUTTON ---------- */

        .stButton > button {

            background: linear-gradient(
                135deg,
                #6d35d9,
                #8d5cf0
            ) !important;

            color: white !important;

            border: none !important;

            border-radius: 14px !important;

            font-weight: 700 !important;

            min-height: 45px;

            transition: 0.2s;
        }

        .stButton > button:hover {

            background: linear-gradient(
                135deg,
                #7b42e8,
                #9b6aff
            ) !important;

            transform: translateY(-1px);
        }


        /* ---------- SELECTBOX ---------- */

        div[data-baseweb="select"] > div {

            border-radius: 14px !important;

            border: 1px solid #67418a !important;
        }


        /* ---------- PROGRESS ---------- */

        .stProgress > div > div > div > div {

            background: linear-gradient(
                90deg,
                #6d35d9,
                #a477ff
            ) !important;
        }


        /* ---------- MOBILE ---------- */

        @media (max-width: 700px) {

            .welcome-title {
                font-size: 27px;
            }

            .hero-title {
                font-size: 23px;
            }

            .stat-card {
                min-height: 120px;
                padding: 15px;
            }

            .stat-value {
                font-size: 25px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # GET HABITS
    # =================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
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
            """,
            (user_id,)
        )

        habits = cursor.fetchall()

    except Exception as e:

        st.error(f"Unable to load dashboard: {e}")
        return

    finally:

        cursor.close()
        conn.close()


    # =================================================
    # USER NAME
    # =================================================

    name = st.session_state.get("name", "there")

    today = datetime.now().strftime("%A, %d %B %Y")


    # =================================================
    # HEADER
    # =================================================

    st.markdown(
        '<div class="dashboard-wrapper">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="welcome-title">
            Welcome back, {name} 👋
        </div>

        <div class="welcome-subtitle">
            Stay consistent and make progress every day.
            &nbsp; • &nbsp; {today}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # NO HABITS
    # =================================================

    if not habits:

        st.markdown(
            """
            <div class="hero-card">

                <div class="hero-small">
                    AI SMART HABIT TRACKER
                </div>

                <div class="hero-title">
                    Start building better habits 🌱
                </div>

                <div class="hero-text">
                    Add your first habit and start tracking
                    your daily progress.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("No habits added yet.")

        st.markdown("</div>", unsafe_allow_html=True)

        return


    # =================================================
    # TODAY'S DATA
    # =================================================

    total_habits = len(habits)

    completed_habits = sum(
        1
        for habit in habits
        if habit[5] == "Completed"
    )

    pending_habits = max(
        total_habits - completed_habits,
        0
    )

    progress = (
        completed_habits / total_habits
        if total_habits > 0
        else 0
    )


    # =================================================
    # HERO CARD
    # =================================================

    st.markdown(
        """
        <div class="hero-card">

            <div class="hero-small">
                ✨ TODAY'S FOCUS
            </div>

            <div class="hero-title">
                Small steps, big results.
            </div>

            <div class="hero-text">
                Keep your routine strong and complete
                your habits one day at a time.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # STATISTICS
    # =================================================

    st.markdown(
        '<div class="section-title">Today\'s Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">📋</div>

                <div class="stat-title">
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

                <div class="stat-icon">✅</div>

                <div class="stat-title">
                    Completed Today
                </div>

                <div class="stat-value">
                    {completed_habits}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">⏳</div>

                <div class="stat-title">
                    Pending
                </div>

                <div class="stat-value">
                    {pending_habits}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">📈</div>

                <div class="stat-title">
                    Today's Progress
                </div>

                <div class="stat-value">
                    {progress * 100:.0f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =================================================
    # PROGRESS
    # =================================================

    st.markdown(
        '<div class="section-title">Today\'s Progress</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-number">
                {progress * 100:.0f}%
            </div>

            <div class="progress-text">
                {completed_habits} of {total_habits}
                habits completed today
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress)


    # =================================================
    # MOTIVATION
    # =================================================

    if progress >= 1:

        message = (
            "🎉 Amazing! You completed all your habits today!"
        )

    elif progress >= 0.7:

        message = (
            "💪 Good progress! Keep going and complete "
            "the remaining habits."
        )

    elif progress >= 0.4:

        message = (
            "🌱 You're making progress. Keep building "
            "your routine."
        )

    else:

        message = (
            "✨ Every small step counts. Start with "
            "one habit today."
        )


    st.info(message)


    # =================================================
    # MY HABITS
    # =================================================

    st.markdown(
        '<div class="section-title">My Habits</div>',
        unsafe_allow_html=True
    )


    for habit in habits:

        habit_id = habit[0]
        habit_name = habit[1]
        category = habit[2] or "General"
        target = habit[3] or "Not set"
        frequency = habit[4] or "None"
        status = habit[5] or "Pending"


        # ---------------------------------------------
        # CONSISTENCY
        # ---------------------------------------------

        try:

            consistency = get_recent_consistency(
                habit_id
            )

        except Exception:

            consistency = 0


        # ---------------------------------------------
        # STATUS
        # ---------------------------------------------

        if status == "Completed":

            status_html = """
            <span class="completed-status">
                ✓ Completed
            </span>
            """

        else:

            status_html = """
            <span class="pending-status">
                Pending
            </span>
            """


        # ---------------------------------------------
        # HABIT CARD
        # ---------------------------------------------

        st.markdown(
            f"""
            <div class="habit-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:flex-start;
                    gap:10px;
                ">

                    <div>

                        <div class="habit-name">
                            {habit_name}
                        </div>

                        <div class="habit-info">
                            {category}
                            &nbsp; • &nbsp;
                            {frequency}
                        </div>

                        <div class="habit-target">
                            Target:
                            <b>{target}</b>
                        </div>

                    </div>

                    <div>
                        {status_html}
                    </div>

                </div>

                <br>

                <div class="habit-info">
                    Recent consistency
                </div>

                <div class="percentage">
                    {consistency:.1f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(
                max(
                    consistency / 100,
                    0.0
                ),
                1.0
            )
        )


    # =================================================
    # AI PREDICTION
    # =================================================

    st.markdown(
        '<div class="section-title">🤖 AI Habit Prediction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                Smart Habit Prediction
            </div>

            <div class="ai-text">
                Use your previous habit history to estimate
                your next completion likelihood.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")


    # =================================================
    # SELECT HABIT
    # =================================================

    selected_habit = st.selectbox(
        "Select a habit for prediction",
        habits,
        format_func=lambda x: x[1],
        key="dashboard_habit_select"
    )

    habit_id = selected_habit[0]
    habit_name = selected_habit[1]


    st.markdown(
        f"""
        <div class="habit-card">

            <div class="habit-name">
                {habit_name}
            </div>

            <div class="habit-info">
                Recent 5-day habit history
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # HISTORY
    # =================================================

    last_five = get_last_five_days(
        habit_id
    )

    if last_five:

        history = " ".join(
            symbol
            for _, symbol in last_five
        )

        st.markdown(
            f"""
            <div class="history-box">

                <div class="history-icons">
                    {history}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        for record_date, symbol in last_five:

            st.caption(
                f"{symbol}  {record_date}"
            )


        consistency = get_recent_consistency(
            habit_id
        )

        st.metric(
            "Recent Consistency",
            f"{consistency:.1f}%"
        )

    else:

        st.info(
            "No habit history available yet."
        )


    # =================================================
    # PREDICTION BUTTON
    # =================================================

    if st.button(
        "✨ Predict Completion",
        use_container_width=True,
        key="predict_completion_button"
    ):

        prediction, message = (
            predict_habit_completion(
                habit_id
            )
        )


        # ---------------------------------------------
        # NOT ENOUGH DATA
        # ---------------------------------------------

        if prediction is None:

            st.warning(
                f"⚠️ {message}"
            )

            st.caption(
                "Complete or miss this habit for at least "
                "5 days to generate an ML prediction."
            )


        # ---------------------------------------------
        # PREDICTION
        # ---------------------------------------------

        else:

            st.markdown(
                f"""
                <div class="progress-card">

                    <div class="progress-text">
                        COMPLETION LIKELIHOOD
                    </div>

                    <div class="progress-number">
                        {prediction:.1f}%
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(
                    max(
                        prediction / 100,
                        0.0
                    ),
                    1.0
                )
            )


            # -----------------------------------------
            # RECOMMENDATION
            # -----------------------------------------

            if prediction >= 70:

                st.success(
                    "🌟 Your consistency is strong. "
                    "Keep following your current routine!"
                )

            elif prediction >= 40:

                st.warning(
                    "💪 Your consistency is moderate. "
                    "Try completing this habit at the "
                    "same time every day."
                )

            else:

                st.info(
                    "🌱 Your completion likelihood is low. "
                    "Try a smaller target and set a fixed "
                    "time for this habit."
                )


    # =================================================
    # FOOTER
    # =================================================

    st.markdown(
        """
        <br>

        <div style="
            text-align:center;
            opacity:0.55;
            font-size:12px;
            padding:20px;
        ">

            AI Smart Habit Tracker
            • Build better habits, one day at a time.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )