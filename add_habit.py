import streamlit as st
import sqlite3


# ----------------------------
# Database Connection
# ----------------------------
def get_connection():
    return sqlite3.connect("habit_tracker.db")


# ----------------------------
# Add Habit Function
# ----------------------------
def add_habit():

    st.header("➕ Add New Habit")

    habit_name = st.text_input("Habit Name")

    category = st.selectbox(
        "Category",
        [
            "Study",
            "Health",
            "Fitness",
            "Personal",
            "Work"
        ]
    )

    target = st.text_input("Target (Example: 2 Hours, 8 Glasses, 30 Minutes)")

    reminder_time = st.time_input("Reminder Time")

    if st.button("Save Habit"):

        if habit_name == "" or target == "":
            st.warning("Please fill all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO habits
            (user_id, habit_name, category, target, reminder_time, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                st.session_state.user_id,
                habit_name,
                category,
                target,
                str(reminder_time),
                "Pending"
            )
        )

        conn.commit()
        conn.close()

        st.success("✅ Habit Added Successfully!")

        st.balloons()