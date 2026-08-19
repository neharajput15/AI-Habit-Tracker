import sqlite3
from datetime import date, timedelta
import streamlit as st


def get_current_streak(habit_id):

    conn = sqlite3.connect("habit_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT date
        FROM progress
        WHERE habit_id = ?
        AND completed = 1
        ORDER BY date DESC
        """,
        (habit_id,)
    )

    records = cursor.fetchall()

    conn.close()

    if not records:
        return 0

    completed_dates = {
        date.fromisoformat(row[0])
        for row in records
    }

    today = date.today()

    # If today is not completed,
    # start checking from yesterday.
    if today not in completed_dates:
        current_day = today - timedelta(days=1)
    else:
        current_day = today

    streak = 0

    while current_day in completed_dates:

        streak += 1

        current_day -= timedelta(days=1)

    return streak


def show_streaks():

    st.subheader("🔥 Habit Streaks")

    conn = sqlite3.connect("habit_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, habit_name
        FROM habits
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    habits = cursor.fetchall()

    conn.close()

    if not habits:

        st.info("No habits found.")

        return

    for habit_id, habit_name in habits:

        streak = get_current_streak(
            habit_id
        )

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