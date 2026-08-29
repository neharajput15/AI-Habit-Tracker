import streamlit as st
from datetime import date, timedelta

from database import get_connection


# =====================================================
# GET CURRENT STREAK
# =====================================================

def get_current_streak(habit_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT completed_date
            FROM progress
            WHERE habit_id = %s
            AND completed = 1
            ORDER BY completed_date DESC
            """,
            (habit_id,)
        )

        records = cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

    if not records:
        return 0

    completed_dates = set()

    for row in records:

        try:
            completed_dates.add(
                date.fromisoformat(str(row[0]))
            )
        except ValueError:
            continue

    if not completed_dates:
        return 0

    today = date.today()

    # If today is not completed,
    # start checking from yesterday.
    if today in completed_dates:
        current_day = today
    else:
        current_day = today - timedelta(days=1)

    streak = 0

    while current_day in completed_dates:

        streak += 1

        current_day -= timedelta(days=1)

    return streak


# =====================================================
# SHOW STREAKS
# =====================================================

def show_streaks():

    st.subheader("🔥 Habit Streaks")

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

        return

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
            (user_id,)
        )

        habits = cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

    if not habits:

        st.info("No habits found.")

        return

    for habit_id, habit_name in habits:

        streak = get_current_streak(habit_id)

        st.write(
            f"### 📌 {habit_name}"
        )

        if streak > 0:

            st.success(
                f"🔥 Current Streak: {streak} days"
            )

        else:

            st.info(
                "🔥 Current Streak: 0 days"
            )