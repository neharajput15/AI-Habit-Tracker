import streamlit as st

from database import get_connection


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

    target = st.text_input(
        "Target (Example: 2 Hours, 8 Glasses, 30 Minutes)"
    )

    reminder_time = st.time_input(
        "Reminder Time"
    )

    if st.button("Save Habit"):

        if not habit_name.strip() or not target.strip():
            st.warning("Please fill all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO habits
                (user_id, habit_name, category, target, reminder_time, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    st.session_state.user_id,
                    habit_name.strip(),
                    category,
                    target.strip(),
                    str(reminder_time),
                    "Pending"
                )
            )

            conn.commit()

            st.success(
                "✅ Habit Added Successfully!"
            )

            st.balloons()

        except Exception as e:

            conn.rollback()

            st.error(
                f"Unable to add habit: {e}"
            )

        finally:

            cursor.close()
            conn.close()