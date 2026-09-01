import streamlit as st
from datetime import datetime

from database import get_connection
from ml_prediction import (
    get_recent_consistency,
    get_last_five_days,
    predict_habit_completion
)


def mobile_home():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    # =====================================================
    # LOAD HABITS
    # =====================================================

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
        st.error(f"Unable to load habits: {e}")
        habits = []

    finally:
        cursor.close()
        conn.close()

    # =====================================================
    # DATE & GREETING
    # =====================================================

    now = datetime.now()

    today_text = now.strftime("%A, %d %B %Y")

    if now.hour < 12:
        greeting = "Good Morning 🌅"
    elif now.hour < 17:
        greeting = "Good Afternoon ☀️"
    elif now.hour < 21:
        greeting = "Good Evening 🌆"
    else:
        greeting = "Good Night 🌙"

    # =====================================================
    # TODAY'S COMPLETION
    # =====================================================

    completed_today = 0
    habit_today_status = {}

    for habit in habits:

        habit_id = habit[0]

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT completed
                FROM progress
                WHERE habit_id = %s
                AND completed_date = CURRENT_DATE::text
                ORDER BY id DESC
                LIMIT 1
                """,
                (habit_id,)
            )

            result = cursor.fetchone()

            completed = int(result[0]) if result else 0

            habit_today_status[habit_id] = completed

            if completed == 1:
                completed_today += 1

        except Exception:
            habit_today_status[habit_id] = 0

        finally:
            cursor.close()
            conn.close()

    # =====================================================
    # STATISTICS
    # =====================================================

    total_habits = len(habits)

    pending_today = max(
        total_habits - completed_today,
        0
    )

    progress_percentage = (
        completed_today / total_habits * 100
        if total_habits > 0
        else 0
    )

    progress_width = min(
        max(progress_percentage, 0),
        100
    )

    # =====================================================
    # CUSTOM CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* ================================
           PAGE
        ================================= */

        .main {
            background: #08060b;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 25px;
            padding-bottom: 40px;
        }


        /* ================================
           APP BRAND
        ================================= */

        .brand-section {
            text-align: center;
            padding: 10px 0 25px 0;
        }

        .brand-icon {
            font-size: 58px;
            line-height: 1;
            margin-bottom: 8px;
        }

        .brand-title {
            color: #ffffff;
            font-size: 40px;
            font-weight: 900;
            margin: 0;
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

        .welcome-box {
            margin-top: 15px;
            margin-bottom: 25px;
        }

        .welcome-title {
            color: #ffffff;
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .welcome-subtitle {
            color: #a998b8;
            font-size: 14px;
        }


        /* ================================
           SECTION
        ================================= */

        .section-title {
            color: #ffffff;
            font-size: 22px;
            font-weight: 800;
            margin-top: 25px;
            margin-bottom: 15px;
        }


        /* ================================
           STAT CARDS
        ================================= */

        .stat-card {
            background: linear-gradient(
                145deg,
                #151019,
                #251333
            );

            border: 1px solid #47245e;

            border-radius: 18px;

            padding: 20px;

            min-height: 135px;

            box-shadow:
                0 8px 25px rgba(0,0,0,0.25);
        }

        .stat-icon {
            font-size: 26px;
            margin-bottom: 8px;
        }

        .stat-title {
            color: #b9a9c7;
            font-size: 13px;
            font-weight: 600;
        }

        .stat-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 900;
            margin-top: 5px;
        }


        /* ================================
           PROGRESS
        ================================= */

        .progress-card {
            background: linear-gradient(
                135deg,
                #241032,
                #3c1857
            );

            border: 1px solid #633686;

            border-radius: 20px;

            padding: 25px;

            box-shadow:
                0 10px 30px rgba(60,20,90,0.30);
        }

        .progress-number {
            color: #c477ff;
            font-size: 45px;
            font-weight: 900;
        }

        .progress-description {
            color: #d0c0d9;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .progress-background {
            width: 100%;
            height: 10px;
            background: #3b2647;
            border-radius: 20px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(
                90deg,
                #7135b5,
                #bd70ff
            );
            border-radius: 20px;
        }

        .message-card {
            background: #17101d;
            border: 1px solid #40264f;
            border-radius: 15px;
            padding: 14px 18px;
            margin-top: 12px;
            color: #d7cadf;
            font-size: 14px;
        }


        /* ================================
           HABITS
        ================================= */

        .habit-card {
            background: linear-gradient(
                145deg,
                #151019,
                #24132e
            );

            border: 1px solid #432650;

            border-radius: 18px;

            padding: 20px;

            margin-bottom: 14px;

            box-shadow:
                0 6px 20px rgba(0,0,0,0.20);
        }

        .habit-name {
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
        }

        .habit-info {
            color: #a998b8;
            font-size: 13px;
            margin-top: 5px;
        }

        .habit-target {
            color: #d7cbe0;
            font-size: 14px;
            margin-top: 12px;
        }

        .habit-consistency {
            color: #c8b9d1;
            font-size: 13px;
            margin-top: 10px;
        }

        .completed-badge {
            display: inline-block;
            background: #173927;
            color: #72e4a2;
            border: 1px solid #286442;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin-top: 12px;
        }

        .pending-badge {
            display: inline-block;
            background: #3b2c18;
            color: #efbd69;
            border: 1px solid #66502b;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin-top: 12px;
        }


        /* ================================
           AI
        ================================= */

        .ai-card {
            background: linear-gradient(
                135deg,
                #30104e,
                #4b2074
            );

            border: 1px solid #70409e;

            border-radius: 20px;

            padding: 24px;

            margin-top: 20px;

            box-shadow:
                0 10px 30px rgba(60,20,90,0.30);
        }

        .ai-title {
            color: #ffffff;
            font-size: 21px;
            font-weight: 800;
        }

        .ai-description {
            color: #d8c7e5;
            font-size: 14px;
            margin-top: 7px;
            line-height: 1.5;
        }


        /* ================================
           BUTTON
        ================================= */

        .stButton > button {
            background: linear-gradient(
                135deg,
                #60259a,
                #833bc3
            ) !important;

            color: white !important;

            border: 1px solid #8e51cf !important;

            border-radius: 12px !important;

            font-weight: 700 !important;

            min-height: 45px !important;
        }

        .stButton > button:hover {
            background: linear-gradient(
                135deg,
                #7130ad,
                #984cdd
            ) !important;

            color: white !important;
        }


        /* ================================
           FOOTER
        ================================= */

        .footer {
            text-align: center;
            color: #76657f;
            font-size: 12px;
            padding: 35px 0 10px 0;
        }


        /* ================================
           MOBILE
        ================================= */

        @media (max-width: 700px) {

            .brand-title {
                font-size: 30px;
            }

            .brand-icon {
                font-size: 48px;
            }

            .welcome-title {
                font-size: 27px;
            }

            .section-title {
                font-size: 20px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # BRAND
    # =====================================================

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
                Build better habits. Track your progress. Become consistent.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # GREETING
    # =====================================================

    st.markdown(
        f"""
        <div class="welcome-box">

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


    # =====================================================
    # OVERVIEW
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
            Today's Overview
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


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

                <div class="stat-icon">⏳</div>

                <div class="stat-title">
                    Pending
                </div>

                <div class="stat-value">
                    {pending_today}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">📈</div>

                <div class="stat-title">
                    Today's Progress
                </div>

                <div class="stat-value">
                    {progress_percentage:.0f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # PROGRESS
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
            Today's Progress
        </div>
        """,
        unsafe_allow_html=True
    )


    if progress_percentage >= 80:

        message = "🌟 Excellent! You're doing amazing today!"

    elif progress_percentage >= 50:

        message = "🌱 You're doing well. Keep going!"

    elif progress_percentage > 0:

        message = "💪 Good start! Complete the remaining habits."

    else:

        message = "🌱 Start today and build your routine!"


    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-number">
                {progress_percentage:.0f}%
            </div>

            <div class="progress-description">
                {completed_today} of {total_habits}
                habits completed today
            </div>

            <div class="progress-background">

                <div
                    class="progress-fill"
                    style="width:{progress_width}%;">
                </div>

            </div>

        </div>

        <div class="message-card">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # MY HABITS
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
            My Habits
        </div>
        """,
        unsafe_allow_html=True
    )


    if not habits:

        st.info(
            "No habits added yet. Add your first habit!"
        )

    else:

        for habit in habits:

            habit_id = habit[0]

            habit_name = habit[1]

            category = (
                habit[2]
                if habit[2]
                else "General"
            )

            target = (
                habit[3]
                if habit[3]
                else "Not set"
            )

            frequency = (
                habit[4]
                if habit[4]
                else "Not set"
            )


            consistency = get_recent_consistency(
                habit_id
            )


            completed = (
                habit_today_status.get(
                    habit_id,
                    0
                ) == 1
            )


            if completed:

                badge = """
                <span class="completed-badge">
                    ✓ Completed
                </span>
                """

            else:

                badge = """
                <span class="pending-badge">
                    Pending
                </span>
                """


            st.markdown(
                f"""
                <div class="habit-card">

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

                    <div class="habit-consistency">
                        Recent consistency:
                        <b>{consistency:.1f}%</b>
                    </div>

                    {badge}

                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # AI PREDICTION
    # =====================================================

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Habit Prediction
            </div>

            <div class="ai-description">
                Use your previous habit history to estimate
                your next completion likelihood.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if habits:

        selected_habit = st.selectbox(
            "Select a habit",
            habits,
            format_func=lambda x: x[1],
            key="home_prediction_habit"
        )


        selected_id = selected_habit[0]


        last_five = get_last_five_days(
            selected_id
        )


        if last_five:

            history = " ".join(
                symbol
                for _, symbol in last_five
            )

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:30px;
                    padding:15px;
                ">
                    {history}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No habit history available yet."
            )


        if st.button(
            "🤖 Predict Completion",
            use_container_width=True,
            key="home_predict_button"
        ):

            prediction, error_message = (
                predict_habit_completion(
                    selected_id
                )
            )


            if prediction is None:

                st.warning(
                    f"⚠️ {error_message}"
                )

            else:

                st.success(
                    f"Predicted completion likelihood: "
                    f"{prediction:.1f}%"
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


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="footer">

            💜 AI Smart Habit Tracker
            <br>
            Build better habits, one day at a time.

        </div>
        """,
        unsafe_allow_html=True
    )