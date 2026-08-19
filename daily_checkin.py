import streamlit as st
import sqlite3
from datetime import date


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect("habit_tracker.db")


# =====================================================
# DAILY CHECK-IN
# =====================================================

def daily_checkin():

    st.header("📅 Daily Habit Check-in")

    conn = get_connection()
    cursor = conn.cursor()

    # =================================================
    # GET USER'S HABITS
    # =================================================

    cursor.execute(
        """
        SELECT id, habit_name
        FROM habits
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (st.session_state.user_id,)
    )

    habits = cursor.fetchall()

    if not habits:

        st.info("➕ Please add a habit first.")

        conn.close()
        return

    # =================================================
    # SELECT HABIT
    # =================================================

    selected = st.selectbox(
        "Select Habit",
        habits,
        format_func=lambda x: x[1]
    )

    habit_id = selected[0]
    habit_name = selected[1]

    today = str(date.today())

    st.markdown(f"### 📌 {habit_name}")

    # =================================================
    # CHECK TODAY'S RECORD
    # =================================================

    cursor.execute(
        """
        SELECT id, completed
        FROM progress
        WHERE habit_id = ?
        AND completed_date = ?
        """,
        (habit_id, today)
    )

    existing = cursor.fetchone()

    # =================================================
    # ALREADY CHECKED IN
    # =================================================

    if existing:

        if existing[1] == 1:

            st.success(
                "✅ Today's habit is already marked as Completed."
            )

        else:

            st.warning(
                "❌ Today's habit is already marked as Missed."
            )

        conn.close()
        return

    # =================================================
    # CHECK-IN BUTTONS
    # =================================================

    col1, col2 = st.columns(2)

    # -------------------------------------------------
    # COMPLETED
    # -------------------------------------------------

    with col1:

        if st.button(
            "✅ Completed",
            use_container_width=True
        ):

            cursor.execute(
                """
                INSERT INTO progress
                (habit_id, completed_date, completed)
                VALUES (?, ?, ?)
                """,
                (
                    habit_id,
                    today,
                    1
                )
            )

            cursor.execute(
                """
                UPDATE habits
                SET status = 'Completed'
                WHERE id = ?
                """,
                (habit_id,)
            )

            conn.commit()
            conn.close()

            st.success(
                "🎉 Habit marked as Completed!"
            )

            st.rerun()

    # -------------------------------------------------
    # MISSED
    # -------------------------------------------------

    with col2:

        if st.button(
            "❌ Missed",
            use_container_width=True
        ):

            cursor.execute(
                """
                INSERT INTO progress
                (habit_id, completed_date, completed)
                VALUES (?, ?, ?)
                """,
                (
                    habit_id,
                    today,
                    0
                )
            )

            cursor.execute(
                """
                UPDATE habits
                SET status = 'Pending'
                WHERE id = ?
                """,
                (habit_id,)
            )

            conn.commit()
            conn.close()

            st.warning(
                "Habit marked as Missed ❌"
            )

            st.rerun()

    conn.close()