import streamlit as st
import sqlite3
from datetime import date


def get_connection():
    return sqlite3.connect("habit_tracker.db")


def view_habits():

    st.header("📋 My Habits")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, habit_name, category, target, reminder_time, status
        FROM habits
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    habits = cursor.fetchall()

    if not habits:
        st.info("No habits found. Add your first habit!")
        conn.close()
        return

    for habit in habits:

        habit_id = habit[0]

        with st.expander(f"📌 {habit[1]}"):

            st.write(f"**Category:** {habit[2]}")
            st.write(f"**Target:** {habit[3]}")
            st.write(f"**Reminder:** {habit[4]}")
            st.write(f"**Status:** {habit[5]}")

            col1, col2 = st.columns(2)

            # Complete
            with col1:

                if st.button(
                    "✅ Complete",
                    key=f"complete_{habit_id}"
                ):

                    today = str(date.today())

                    # Update habit status
                    cursor.execute(
                        """
                        UPDATE habits
                        SET status='Completed'
                        WHERE id=?
                        """,
                        (habit_id,)
                    )

                    # Save progress
                    cursor.execute(
                        """
                        INSERT INTO progress
                        (habit_id, date, completed, completed_date)
                        VALUES (?, ?, ?, ?)
                        """,
                        (habit_id, today, 1, today)
                    )

                    conn.commit()

                    st.success("Habit Completed! ✅")
                    st.rerun()

            # Delete
            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{habit_id}"
                ):

                    cursor.execute(
                        """
                        DELETE FROM progress
                        WHERE habit_id=?
                        """,
                        (habit_id,)
                    )

                    cursor.execute(
                        """
                        DELETE FROM habits
                        WHERE id=?
                        """,
                        (habit_id,)
                    )

                    conn.commit()

                    st.success("Habit Deleted! 🗑️")
                    st.rerun()

    conn.close()