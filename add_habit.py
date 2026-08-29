import streamlit as st

from database import get_connection


# =====================================================
# ADD HABIT
# =====================================================

def add_habit():

    st.header("➕ Add New Habit")

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

    # =================================================
    # ADD BUTTON
    # =================================================

    if st.button(
        "➕ Add Habit",
        use_container_width=True
    ):

        if not habit_name.strip():

            st.warning(
                "Please enter a habit name."
            )

            return

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
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    st.session_state.user_id,
                    habit_name.strip(),
                    category,
                    target.strip(),
                    "Pending"
                )
            )

            conn.commit()

            st.success(
                "Habit added successfully! 🎉"
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