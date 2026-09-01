import streamlit as st

from database import get_connection


# =====================================================
# ADD HABIT
# =====================================================

def add_habit():

    st.title("Add New Habit")

    st.caption(
        "Create a habit and set your target and frequency."
    )

    # =================================================
    # HABIT DETAILS
    # =================================================

    habit_name = st.text_input(
        "Habit Name",
        placeholder="Example: Study Java"
    )

    category = st.selectbox(
        "Category",
        [
            "Study",
            "Health",
            "Fitness",
            "Personal"
        ]
    )

    target = st.text_input(
        "Target",
        placeholder="Example: Study for 2 hours"
    )

    frequency = st.selectbox(
        "Frequency",
        [
            "Daily",
            "2 times per week",
            "3 times per week",
            "4 times per week",
            "5 times per week",
            "Weekly"
        ]
    )

    # =================================================
    # ADD BUTTON
    # =================================================

    if st.button(
        "Add Habit",
        use_container_width=True
    ):

        if not habit_name.strip():

            st.warning(
                "Please enter a habit name."
            )

            return

        if not target.strip():

            st.warning(
                "Please enter a target."
            )

            return

        # =================================================
        # DATABASE
        # =================================================

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO habits
                (
                    user_id,
                    habit_name,
                    category,
                    target,
                    frequency,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    st.session_state.user_id,
                    habit_name.strip(),
                    category,
                    target.strip(),
                    frequency,
                    "Pending"
                )
            )

            conn.commit()

            st.success(
                "Habit added successfully."
            )

            st.rerun()

        except Exception as e:

            conn.rollback()

            st.error(
                f"Unable to add habit: {e}"
            )

        finally:

            cursor.close()
            conn.close()