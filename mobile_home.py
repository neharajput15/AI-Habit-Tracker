import streamlit as st
from datetime import datetime

from database import get_connection

from ml_prediction import (
    get_recent_consistency,
    get_last_five_days,
    predict_habit_completion
)


# =====================================================
# MOBILE HOME
# =====================================================

def mobile_home():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return


    # =================================================
    # LOAD HABITS
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

        st.error(f"Unable to load habits: {e}")
        return

    finally:

        cursor.close()
        conn.close()


    # =================================================
    # DATE & TIME
    # =================================================

    now = datetime.now()

    today_text = now.strftime(
        "%A, %d %B %Y"
    )

    current_hour = now.hour

    if current_hour < 12:

        greeting = "Good Morning 🌅"

    elif current_hour < 17:

        greeting = "Good Afternoon ☀️"

    elif current_hour < 21:

        greeting = "Good Evening 🌆"

    else:

        greeting = "Good Night 🌙"


    # =================================================
    # TODAY'S COMPLETION
    # =================================================

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

            record = cursor.fetchone()

            if record:

                completed = int(record[0])

            else:

                completed = 0

            habit_today_status[habit_id] = completed

            if completed == 1:

                completed_today += 1

        except Exception:

            habit_today_status[habit_id] = 0

        finally:

            cursor.close()
            conn.close()


    # =================================================
    # STATISTICS
    # =================================================

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


    # =================================================
    # MAIN CSS
    # =================================================

    st.markdown(
        """
        <style>

        /* ==========================================
           MAIN PAGE
        ========================================== */

        .home-wrapper {
            padding: 10px 5px 20px 5px;
        }


        /* ==========================================
           GREETING
        ========================================== */

        .welcome-title {
            font-size: 34px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 5px;
        }

        .welcome-subtitle {
            font-size: 14px;
            color: #b9a6c8;
            margin-bottom: 25px;
        }


        /* ==========================================
           SECTION TITLE
        ========================================== */

        .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 28px;
            margin-bottom: 16px;
        }


        /* ==========================================
           STAT CARDS
        ========================================== */

        .stat-card {
            background: linear-gradient(
                145deg,
                #17101f,
                #281338
            );

            border: 1px solid #48245f;

            border-radius: 18px;

            padding: 20px;

            min-height: 135px;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.25);
        }

        .stat-icon {
            font-size: 25px;
            margin-bottom: 10px;
        }

        .stat-title {
            color: #b9a6c8;
            font-size: 13px;
            font-weight: 600;
        }

        .stat-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 800;
            margin-top: 5px;
        }


        /* ==========================================
           PROGRESS CARD
        ========================================== */

        .progress-card {
            background: linear-gradient(
                135deg,
                #241032,
                #3a1655
            );

            border: 1px solid #5b3179;

            border-radius: 20px;

            padding: 25px;

            margin-top: 5px;

            box-shadow:
                0 10px 30px rgba(45, 15, 65, 0.30);
        }

        .progress-number {
            font-size: 42px;
            font-weight: 900;
            color: #b875ff;
        }

        .progress-text {
            color: #cdbbd8;
            font-size: 14px;
            margin-bottom: 16px;
        }

        .progress-bar-bg {
            height: 10px;
            width: 100%;

            background: #392346;

            border-radius: 20px;

            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;

            background: linear-gradient(
                90deg,
                #7438c5,
                #b96dff
            );

            border-radius: 20px;
        }


        /* ==========================================
           MESSAGE
        ========================================== */

        .message-card {
            background: #18111f;

            border: 1px solid #3d274b;

            border-radius: 16px;

            padding: 15px 18px;

            margin-top: 14px;

            color: #ddd0e5;

            font-size: 14px;
        }


        /* ==========================================
           HABIT CARD
        ========================================== */

        .habit-card {
            background: linear-gradient(
                145deg,
                #17101f,
                #24132f
            );

            border: 1px solid #432654;

            border-radius: 18px;

            padding: 20px;

            margin-bottom: 14px;

            box-shadow:
                0 6px 20px rgba(0, 0, 0, 0.20);
        }

        .habit-name {
            color: #ffffff;

            font-size: 18px;

            font-weight: 800;

            margin-bottom: 5px;
        }

        .habit-info {
            color: #b9a6c8;

            font-size: 13px;

            margin-bottom: 12px;
        }

        .target-text {
            color: #ddd2e5;

            font-size: 14px;

            margin-bottom: 10px;
        }


        /* ==========================================
           BADGES
        ========================================== */

        .completed-badge {
            display: inline-block;

            background: #173b2a;

            color: #72e3a3;

            border: 1px solid #286343;

            padding: 5px 11px;

            border-radius: 20px;

            font-size: 12px;

            font-weight: 700;
        }

        .pending-badge {
            display: inline-block;

            background: #3b2b17;

            color: #f2bd68;

            border: 1px solid #66502a;

            padding: 5px 11px;

            border-radius: 20px;

            font-size: 12px;

            font-weight: 700;
        }


        /* ==========================================
           AI CARD
        ========================================== */

        .ai-card {
            background: linear-gradient(
                135deg,
                #321358,
                #4b2077
            );

            border: 1px solid #7040a5;

            border-radius: 20px;

            padding: 24px;

            margin-top: 10px;

            box-shadow:
                0 10px 30px rgba(65, 25, 100, 0.30);
        }

        .ai-title {
            color: #ffffff;

            font-size: 21px;

            font-weight: 800;

            margin-bottom: 8px;
        }

        .ai-subtitle {
            color: #d9c6e8;

            font-size: 14px;

            line-height: 1.5;
        }


        /* ==========================================
           BUTTONS
        ========================================== */

        .stButton > button {

            background: linear-gradient(
                135deg,
                #5c2491,
                #7b36c4
            ) !important;

            color: white !important;

            border: 1px solid #8c50d0 !important;

            border-radius: 12px !important;

            font-weight: 700 !important;

            min-height: 45px !important;
        }

        .stButton > button:hover {

            background: linear-gradient(
                135deg,
                #7130ad,
                #9349dc
            ) !important;

            color: white !important;
        }


        /* ==========================================
           SELECTBOX
        ========================================== */

        div[data-baseweb="select"] > div {

            background-color: #1d1425 !important;

            border: 1px solid #4a2a5d !important;

            color: white !important;

            border-radius: 12px !important;
        }


        /* ==========================================
           FOOTER
        ========================================== */

        .footer-text {

            text-align: center;

            color: #806d8e;

            font-size: 12px;

            padding: 30px 0 10px 0;
        }


        /* ==========================================
           MOBILE
        ========================================== */

        @media (max-width: 700px) {

            .welcome-title {
                font-size: 28px;
            }

            .section-title {
                font-size: 20px;
            }

            .stat-card {
                padding: 15px;
                min-height: 120px;
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
    # WELCOME
    # =================================================

    st.markdown(
        f"""
        <div class="home-wrapper">

            <div class="welcome-title">
                {greeting}
            </div>

            <div class="welcome-subtitle">
                Stay consistent and make progress every day.
                &nbsp; • &nbsp; {today_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # TODAY'S OVERVIEW
    # =================================================

    st.markdown(
        """
        <div class="section-title">
            Today's Overview
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    # -------------------------------------------------
    # TOTAL
    # -------------------------------------------------

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    📋
                </div>

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


    # -------------------------------------------------
    # COMPLETED
    # -------------------------------------------------

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ✅
                </div>

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


    # -------------------------------------------------
    # PENDING
    # -------------------------------------------------

    with col3:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ⏳
                </div>

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


    # -------------------------------------------------
    # PROGRESS
    # -------------------------------------------------

    with col4:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    📈
                </div>

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


    # =================================================
    # TODAY'S PROGRESS
    # =================================================

    st.markdown(
        """
        <div class="section-title">
            Today's Progress
        </div>
        """,
        unsafe_allow_html=True
    )


    progress_width = min(
        max(progress_percentage, 0),
        100
    )


    if progress_percentage >= 80:

        message = (
            "🌟 Excellent! You're doing amazing today!"
        )

    elif progress_percentage >= 50:

        message = (
            "🌱 You're making progress. "
            "Keep building your routine!"
        )

    elif progress_percentage > 0:

        message = (
            "💪 Good start! Keep going and "
            "complete the remaining habits."
        )

    else:

        message = (
            "🌱 Start today and build your routine!"
        )


    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-number">
                {progress_percentage:.0f}%
            </div>

            <div class="progress-text">
                {completed_today} of {total_habits}
                habits completed today
            </div>

            <div class="progress-bar-bg">

                <div
                    class="progress-bar-fill"
                    style="width:{progress_width}%">
                </div>

            </div>

        </div>

        <div class="message-card">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # MY HABITS
    # =================================================

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
                else "None"
            )


            # -----------------------------------------
            # CONSISTENCY
            # -----------------------------------------

            consistency = get_recent_consistency(
                habit_id
            )


            # -----------------------------------------
            # TODAY STATUS
            # -----------------------------------------

            is_completed = (
                habit_today_status.get(
                    habit_id,
                    0
                ) == 1
            )


            if is_completed:

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


            # -----------------------------------------
            # HABIT CARD
            # -----------------------------------------

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

                    <div class="target-text">
                        Target:
                        <b>{target}</b>
                    </div>

                    <div style="
                        margin-bottom:12px;
                        color:#cbbbd6;
                    ">
                        Recent consistency:
                        <b>{consistency:.1f}%</b>
                    </div>

                    {badge}

                </div>
                """,
                unsafe_allow_html=True
            )


    # =================================================
    # AI PREDICTION
    # =================================================

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Habit Prediction
            </div>

            <div class="ai-subtitle">
                Use your previous habit history to estimate
                your next completion likelihood.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # PREDICTION
    # =================================================

    if habits:

        selected_habit = st.selectbox(
            "Select a habit for prediction",
            habits,
            format_func=lambda x: x[1],
            key="home_prediction_habit"
        )


        selected_id = selected_habit[0]

        selected_name = selected_habit[1]


        st.markdown(
            f"""
            <div class="habit-card">

                <div class="habit-name">
                    {selected_name}
                </div>

                <div class="habit-info">
                    Recent 5-day habit history
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ---------------------------------------------
        # RECENT HISTORY
        # ---------------------------------------------

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
                    font-size:30px;
                    text-align:center;
                    padding:12px;
                ">
                    {history}
                </div>
                """,
                unsafe_allow_html=True
            )

            for record_date, symbol in last_five:

                st.write(
                    f"{symbol} {record_date}"
                )

        else:

            st.info(
                "No habit history available yet."
            )


        # ---------------------------------------------
        # PREDICTION BUTTON
        # ---------------------------------------------

        if st.button(
            "🤖 Predict Completion",
            use_container_width=True,
            key="home_predict_button"
        ):

            prediction, message = (
                predict_habit_completion(
                    selected_id
                )
            )


            if prediction is None:

                st.warning(
                    f"⚠️ {message}"
                )

                st.info(
                    "Complete or miss this habit for "
                    "at least 5 days to generate an "
                    "ML prediction."
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


    # =================================================
    # FOOTER
    # =================================================

    st.markdown(
        """
        <div class="footer-text">

            AI Smart Habit Tracker
            •
            Build better habits, one day at a time.

        </div>
        """,
        unsafe_allow_html=True
    )