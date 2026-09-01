import streamlit as st
from datetime import date

from database import get_connection
from ml_prediction import get_recent_consistency


# =====================================================
# MOBILE / MODERN HOME DASHBOARD
# =====================================================

def mobile_home():

    user_id = st.session_state.get("user_id")
    name = st.session_state.get("name", "User")

    if not user_id:
        st.warning("Please login first.")
        return


    # =================================================
    # CUSTOM DESIGN
    # =================================================

    st.markdown(
        """
        <style>

        /* Main page */
        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Header */
        .welcome-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .welcome-subtitle {
            color: #777;
            font-size: 15px;
            margin-bottom: 25px;
        }

        /* Stat cards */
        .stat-card {
            background: linear-gradient(
                135deg,
                #ffffff,
                #f7f3ff
            );
            border: 1px solid #eee5ff;
            border-radius: 20px;
            padding: 20px;
            min-height: 145px;
            box-shadow: 0 5px 20px rgba(100, 70, 180, 0.08);
        }

        .stat-icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .stat-title {
            color: #777;
            font-size: 14px;
            font-weight: 500;
        }

        .stat-value {
            font-size: 30px;
            font-weight: 700;
            margin-top: 4px;
        }

        /* Progress card */
        .progress-card {
            background: linear-gradient(
                135deg,
                #eee5ff,
                #f8f5ff
            );
            border-radius: 24px;
            padding: 25px;
            margin-top: 20px;
            border: 1px solid #e5d8ff;
        }

        .progress-number {
            font-size: 42px;
            font-weight: 700;
        }

        .progress-text {
            color: #666;
            font-size: 15px;
        }

        .progress-bar-bg {
            height: 12px;
            background: #ddd3f5;
            border-radius: 20px;
            margin-top: 18px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(
                90deg,
                #7650e8,
                #9b75ff
            );
            border-radius: 20px;
        }

        /* Habit cards */
        .habit-card {
            background: white;
            border: 1px solid #eeeeee;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        }

        .habit-name {
            font-size: 20px;
            font-weight: 650;
            margin-bottom: 6px;
        }

        .habit-info {
            color: #777;
            font-size: 14px;
            margin-bottom: 12px;
        }

        .target-text {
            font-size: 14px;
            margin-bottom: 10px;
        }

        .completed-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            background: #e7f8ed;
            color: #21884a;
            font-size: 13px;
            font-weight: 600;
        }

        .pending-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            background: #fff4df;
            color: #a66a00;
            font-size: 13px;
            font-weight: 600;
        }

        /* AI section */
        .ai-card {
            background: linear-gradient(
                135deg,
                #f0eaff,
                #ffffff
            );
            border: 1px solid #dfd2ff;
            border-radius: 24px;
            padding: 25px;
            margin-top: 25px;
        }

        .ai-title {
            font-size: 23px;
            font-weight: 700;
        }

        .ai-subtitle {
            color: #777;
            margin-bottom: 10px;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 14px !important;
            min-height: 45px;
            font-weight: 600;
        }

        /* Mobile */
        @media (max-width: 700px) {

            .welcome-title {
                font-size: 26px;
            }

            .stat-card {
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
                status
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        habits = cursor.fetchall()


        # Today's completed habits
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h
                ON p.habit_id = h.id
            WHERE h.user_id = %s
            AND p.completed_date = %s
            AND p.completed = 1
            """,
            (user_id, date.today().isoformat())
        )

        completed_today = cursor.fetchone()[0]


    except Exception as e:

        st.error(f"Unable to load dashboard: {e}")
        return

    finally:

        cursor.close()
        conn.close()


    # =================================================
    # STATISTICS
    # =================================================

    total_habits = len(habits)

    completed_today = int(completed_today)

    pending_today = max(
        total_habits - completed_today,
        0
    )

    progress = (
        completed_today / total_habits
        if total_habits > 0
        else 0
    )

    progress_percent = int(progress * 100)


    # =================================================
    # WELCOME
    # =================================================

    today_text = date.today().strftime(
        "%A, %d %B %Y"
    )

    st.markdown(
        f"""
        <div class="welcome-title">
            Welcome back, {name} 👋
        </div>

        <div class="welcome-subtitle">
            Stay consistent and make progress every day.
            &nbsp; • &nbsp; {today_text}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # TODAY'S OVERVIEW
    # =================================================

    st.markdown(
        "### Today's Overview"
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
                    {progress_percent}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =================================================
    # PROGRESS
    # =================================================

    st.markdown(
        f"""
        <div class="progress-card">

            <div class="progress-number">
                {progress_percent}%
            </div>

            <div class="progress-text">
                {completed_today} of {total_habits}
                habits completed today
            </div>

            <div class="progress-bar-bg">

                <div
                    class="progress-bar-fill"
                    style="width:{progress_percent}%">
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # MOTIVATION
    # =================================================

    if progress_percent == 100 and total_habits > 0:

        st.success(
            "🎉 Amazing! You completed all your habits today!"
        )

    elif progress_percent >= 70:

        st.success(
            "💪 Good progress! Keep going and complete the remaining habits."
        )

    elif progress_percent > 0:

        st.info(
            "🌱 You're making progress. Keep building your routine!"
        )

    elif total_habits > 0:

        st.warning(
            "🚀 Start your first habit today!"
        )


    # =================================================
    # MY HABITS
    # =================================================

    st.markdown("### My Habits")

    if not habits:

        st.info(
            "No habits added yet. Click 'Add Habit' to get started."
        )

    else:

        for i in range(0, len(habits), 2):

            cols = st.columns(2)

            for j in range(2):

                index = i + j

                if index >= len(habits):
                    break

                habit = habits[index]

                habit_id = habit[0]
                habit_name = habit[1]
                category = habit[2] or "General"
                target = habit[3] or "Not specified"
                status = habit[4] or "Pending"


                # Recent consistency
                try:
                    consistency = get_recent_consistency(
                        habit_id
                    )
                except Exception:
                    consistency = 0


                is_completed = status == "Completed"

                badge = (
                    '<span class="completed-badge">✓ Completed</span>'
                    if is_completed
                    else
                    '<span class="pending-badge">Pending</span>'
                )


                with cols[j]:

                    st.markdown(
                        f"""
                        <div class="habit-card">

                            <div class="habit-name">
                                {habit_name}
                            </div>

                            <div class="habit-info">
                                {category}
                            </div>

                            <div class="target-text">
                                Target: <b>{target}</b>
                            </div>

                            <div style="margin-bottom:12px;">
                                Recent consistency:
                                <b>{consistency:.1f}%</b>
                            </div>

                            {badge}

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


    if habits:

        selected = st.selectbox(
            "Select a habit for prediction",
            habits,
            format_func=lambda x: x[1],
            key="home_prediction_habit"
        )

        selected_id = selected[0]
        selected_name = selected[1]


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


        # Import only when required
        from ml_prediction import (
            get_last_five_days,
            predict_habit_completion
        )


        history = get_last_five_days(
            selected_id
        )


        if history:

            symbols = " ".join(
                symbol
                for _, symbol in history
            )

            st.markdown(
                f"### {symbols}"
            )

            for record_date, symbol in history:

                st.write(
                    f"{symbol}  {record_date}"
                )


            prediction, message = (
                predict_habit_completion(
                    selected_id
                )
            )


            if prediction is not None:

                st.metric(
                    "Completion Likelihood",
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

            else:

                st.info(
                    message
                )

        else:

            st.info(
                "No habit history available yet."
            )


    # =================================================
    # FOOTER
    # =================================================

    st.divider()

    st.caption(
        "AI Smart Habit Tracker • Build better habits, one day at a time."
    )