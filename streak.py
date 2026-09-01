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
                date.fromisoformat(
                    str(row[0])
                )
            )

        except (ValueError, TypeError):

            continue


    if not completed_dates:
        return 0


    today = date.today()


    # =================================================
    # START FROM TODAY OR YESTERDAY
    # =================================================

    if today in completed_dates:

        current_day = today

    else:

        current_day = today - timedelta(days=1)


    # =================================================
    # CALCULATE STREAK
    # =================================================

    streak = 0

    while current_day in completed_dates:

        streak += 1

        current_day -= timedelta(days=1)


    return streak


# =====================================================
# SHOW STREAKS
# =====================================================

def show_streaks():

    st.title("Habit Streaks")

    st.caption(
        "Track how consistently you maintain your habits."
    )


    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning(
            "Please login first."
        )

        return


    conn = get_connection()
    cursor = conn.cursor()


    try:

        # =================================================
        # GET USER HABITS
        # =================================================

        cursor.execute(
            """
            SELECT
                id,
                habit_name,
                category,
                frequency
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


    # =================================================
    # NO HABITS
    # =================================================

    if not habits:

        st.info(
            "No habits found. Add a habit to start tracking your streak."
        )

        return


    # =================================================
    # DISPLAY STREAKS
    # =================================================

    for habit_id, habit_name, category, frequency in habits:

        streak = get_current_streak(
            habit_id
        )


        with st.container(border=True):

            st.subheader(
                habit_name
            )

            st.caption(
                f"{category}  •  {frequency}"
            )


            st.metric(
                "Current Streak",
                f"{streak} days"
            )


            if streak == 0:

                st.caption(
                    "Complete this habit regularly to build a streak."
                )

            elif streak == 1:

                st.caption(
                    "Good start. Try to continue tomorrow."
                )

            else:

                st.caption(
                    "Keep going and maintain your consistency."
                )