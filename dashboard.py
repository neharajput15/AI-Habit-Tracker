import streamlit as st
from datetime import date

from database import get_connection
from ml_prediction import (
    predict_habit_completion,
    get_last_five_days,
    get_recent_consistency,
)


# =====================================================
# MODERN DASHBOARD
# =====================================================

def _safe_text(value, default="None"):
    if value is None or str(value).strip() == "":
        return default
    return str(value)


def _get_habits(user_id):
    """Load habits without depending on a frequency column."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, habit_name, category, target, status
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def _today_counts(user_id, habit_ids):
    """Return completed-today count for the user's habits."""
    if not habit_ids:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h ON h.id = p.habit_id
            WHERE h.user_id = %s
              AND p.completed_date = %s
              AND p.completed = 1
            """,
            (user_id, date.today().isoformat()),
        )
        return int(cursor.fetchone()[0] or 0)
    finally:
        cursor.close()
        conn.close()


def _inject_css():
    st.markdown(
        """
        <style>
        /* ---------- Page ---------- */
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            background: linear-gradient(135deg, #6d42d8 0%, #8c5cf0 55%, #a679ff 100%);
            border-radius: 28px;
            padding: 28px 30px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 14px 35px rgba(112, 71, 214, 0.20);
        }

        .hero h1 {
            color: white !important;
            font-size: 30px !important;
            margin: 0 0 5px 0 !important;
        }

        .hero p {
            color: rgba(255,255,255,.88) !important;
            margin: 0 !important;
            font-size: 15px;
        }

        /* ---------- Stat cards ---------- */
        .stat-card {
            background: white;
            border: 1px solid #eee8fb;
            border-radius: 22px;
            padding: 20px;
            min-height: 150px;
            box-shadow: 0 8px 25px rgba(60, 35, 110, .07);
        }

        .dark .stat-card {
            background: #211b2c;
            border-color: #3b304d;
        }

        .stat-icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .stat-title {
            color: #777080;
            font-size: 13px;
            font-weight: 600;
        }

        .stat-value {
            color: #241b2f;
            font-size: 30px;
            font-weight: 800;
            margin-top: 4px;
        }

        /* ---------- Section ---------- */
        .section-title {
            font-size: 22px;
            font-weight: 800;
            margin: 26px 0 12px 0;
        }

        /* ---------- Progress card ---------- */
        .progress-card {
            background: linear-gradient(135deg, #f7f2ff, #fbf9ff);
            border: 1px solid #e9ddff;
            border-radius: 24px;
            padding: 25px;
            margin: 8px 0 20px 0;
        }

        .progress-number {
            color: #7444d8;
            font-size: 38px;
            font-weight: 850;
        }

        .progress-text {
            color: #766c80;
            font-size: 14px;
            margin-top: -5px;
        }

        .message-card {
            background: white;
            border: 1px solid #eee8f7;
            border-radius: 18px;
            padding: 15px 18px;
            margin-top: 12px;
            color: #5c5264;
        }

        /* ---------- Habit cards ---------- */
        .habit-card {
            background: white;
            border: 1px solid #eee8f7;
            border-radius: 22px;
            padding: 19px 20px;
            margin-bottom: 13px;
            box-shadow: 0 7px 20px rgba(60, 35, 110, .05);
        }

        .habit-name {
            color: #2a2231;
            font-size: 18px;
            font-weight: 800;
        }

        .habit-info {
            color: #8a7f91;
            font-size: 13px;
            margin-top: 4px;
        }

        .habit-target {
            color: #665b70;
            font-size: 14px;
            margin-top: 10px;
        }

        .status-done {
            display: inline-block;
            background: #e8f8ee;
            color: #22834a;
            padding: 6px 11px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }

        .status-pending {
            display: inline-block;
            background: #fff4df;
            color: #b36b00;
            padding: 6px 11px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            border-radius: 14px !important;
            min-height: 45px !important;
            font-weight: 700 !important;
        }

        /* ---------- Prediction ---------- */
        .prediction-card {
            background: linear-gradient(135deg, #f8f4ff, #ffffff);
            border: 1px solid #e9ddff;
            border-radius: 24px;
            padding: 24px;
        }

        /* ---------- Footer ---------- */
        .footer {
            text-align: center;
            color: #918797;
            font-size: 13px;
            padding: 28px 0 8px 0;
        }

        @media (max-width: 700px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .hero {
                padding: 22px;
                border-radius: 22px;
            }
            .hero h1 {
                font-size: 25px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def dashboard():
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    _inject_css()

    # =================================================
    # LOAD DATA
    # =================================================
    try:
        habits = _get_habits(user_id)
    except Exception as e:
        st.error(f"Unable to load dashboard: {e}")
        return

    total_habits = len(habits)
    habit_ids = [h[0] for h in habits]

    try:
        completed_today = _today_counts(user_id, habit_ids)
    except Exception as e:
        st.error(f"Unable to load today's progress: {e}")
        return

    pending_today = max(total_habits - completed_today, 0)
    today_percentage = (
        completed_today / total_habits if total_habits else 0
    )

    # =================================================
    # HERO
    # =================================================
    name = _safe_text(st.session_state.get("name"), "there")

    st.markdown(
        f"""
        <div class="hero">
            <h1>Welcome back, {name} 👋</h1>
            <p>Stay consistent and make progress every day. • {date.today().strftime("%A, %d %B %Y")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =================================================
    # TODAY'S OVERVIEW
    # =================================================
    st.markdown('<div class="section-title">Today\'s Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("📋", "Total Habits", total_habits),
        ("✅", "Completed Today", completed_today),
        ("⏳", "Pending", pending_today),
        ("📈", "Today's Progress", f"{today_percentage * 100:.0f}%"),
    ]

    for col, (icon, title, value) in zip((c1, c2, c3, c4), cards):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-icon">{icon}</div>
                    <div class="stat-title">{title}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =================================================
    # TODAY'S PROGRESS
    # =================================================
    st.markdown('<div class="section-title">Today\'s Progress</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="progress-card">
            <div class="progress-number">{today_percentage * 100:.0f}%</div>
            <div class="progress-text">
                {completed_today} of {total_habits} habits completed today
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(float(today_percentage))

    if total_habits == 0:
        st.info("Add your first habit to start tracking your progress.")
    elif today_percentage == 1:
        st.success("🎉 Excellent! You completed all your habits today.")
    elif today_percentage >= 0.5:
        st.info("💪 Good progress! Keep going and complete the remaining habits.")
    else:
        st.warning("🌱 Start small. Complete one habit now and build your momentum.")

    # =================================================
    # MY HABITS
    # =================================================
    st.markdown('<div class="section-title">My Habits</div>', unsafe_allow_html=True)

    if not habits:
        st.info("No habits added yet. Use **Add Habit** to create your first habit.")
    else:
        for habit_id, habit_name, category, target, status in habits:
            try:
                consistency = get_recent_consistency(habit_id)
            except Exception:
                consistency = 0

            done = str(status).lower() == "completed"

            status_html = (
                '<span class="status-done">✓ Completed</span>'
                if done
                else '<span class="status-pending">Pending</span>'
            )

            st.markdown(
                f"""
                <div class="habit-card">
                    <div class="habit-name">{_safe_text(habit_name)}</div>
                    <div class="habit-info">
                        {_safe_text(category)} &nbsp; • &nbsp; Daily
                    </div>
                    <div class="habit-target">
                        Target: <b>{_safe_text(target)}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            p1, p2 = st.columns([4, 1])
            with p1:
                st.caption(f"Recent consistency: {consistency:.1f}%")
                st.progress(min(max(float(consistency) / 100, 0.0), 1.0))
            with p2:
                st.markdown(status_html, unsafe_allow_html=True)

    # =================================================
    # AI / ML PREDICTION
    # =================================================
    st.markdown('<div class="section-title">🤖 AI Habit Prediction</div>', unsafe_allow_html=True)
    st.caption(
        "Use your previous habit history to estimate your next completion likelihood."
    )

    if habits:
        selected_habit = st.selectbox(
            "Select a habit for prediction",
            habits,
            format_func=lambda x: x[1],
            key="modern_dashboard_habit_select",
        )

        habit_id = selected_habit[0]
        habit_name = selected_habit[1]

        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="habit-name">{_safe_text(habit_name)}</div>
                <div class="habit-info">Recent 5-day habit history</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        last_five = get_last_five_days(habit_id)

        if last_five:
            history = " ".join(symbol for _, symbol in last_five)
            st.markdown(f"### {history}")

            for record_date, symbol in last_five:
                st.caption(f"{symbol} {record_date}")

            consistency = get_recent_consistency(habit_id)
            st.metric("Recent Consistency", f"{consistency:.1f}%")
        else:
            st.info("No habit history available yet.")

        if st.button(
            "Predict Completion",
            use_container_width=True,
            key="modern_predict_completion",
        ):
            prediction, message = predict_habit_completion(habit_id)

            if prediction is None:
                st.warning(message)
                st.info(
                    "Complete or miss this habit for at least 5 days "
                    "to generate an ML prediction."
                )
            else:
                st.metric(
                    "Completion Likelihood",
                    f"{prediction:.1f}%",
                )
                st.progress(
                    min(max(float(prediction) / 100, 0.0), 1.0)
                )

                if prediction >= 70:
                    st.success(
                        "Your consistency is strong. Keep following your current routine."
                    )
                elif prediction >= 40:
                    st.warning(
                        "Your consistency is moderate. Try completing this habit at the same time every day."
                    )
                else:
                    st.info(
                        "Your completion likelihood is low. Try a smaller target and a fixed time."
                    )

    # =================================================
    # FOOTER
    # =================================================
    st.markdown(
        """
        <div class="footer">
            AI Smart Habit Tracker • Build better habits, one day at a time.
        </div>
        """,
        unsafe_allow_html=True,
    )
