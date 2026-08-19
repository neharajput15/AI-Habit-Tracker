import streamlit as st
import sqlite3
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


def check_notifications():

    # Refresh the app every 10 seconds
    st_autorefresh(
        interval=10000,
        key="notification_refresh"
    )

    if not st.session_state.get("logged_in"):
        return

    conn = sqlite3.connect("habit_tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, habit_name, reminder_time
        FROM habits
        WHERE user_id = ?
        """,
        (st.session_state.user_id,)
    )

    habits = cursor.fetchall()

    conn.close()

    current_time = datetime.now().strftime("%H:%M")

    for habit_id, habit_name, reminder_time in habits:

        if reminder_time:

            reminder = str(reminder_time)[:5]

            if reminder == current_time:

                st.warning(
                    f"⏰ Reminder!\n\n"
                    f"Time to complete "
                    f"**{habit_name}**!"
                )