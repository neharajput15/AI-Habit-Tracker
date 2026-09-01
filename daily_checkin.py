import streamlit as st
from datetime import date

from database import get_connection


# =====================================================
# DAILY CHECK-IN
# =====================================================

def daily_checkin():

    st.title("Daily Habit Check-in")

    st.caption(
        "Record whether you completed your habit today."
    )

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

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
                target,
                frequency
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        habits = cursor.fetchall()


        # =================================================
        # NO HABITS
        # =================================================

        if not habits:

            st.info(
                "No habits found. Add a habit first."
            )

            return


        # =================================================
        # SELECT HABIT
        # =================================================

        selected = st.selectbox(
            "Select Habit",
            habits,
            format_func=lambda x: x[1],
            key="checkin_habit_select"
        )

        habit_id = selected[0]
        habit_name = selected[1]
        category = selected[2]
        target = selected[3]
        frequency = selected[4]

        today = date.today().isoformat()


        # =================================================
        # HABIT DETAILS
        # =================================================

        st.subheader(habit_name)

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                f"**Target:** {target}"
            )

        with col2:

            st.write(
                f"**Frequency:** {frequency}"
            )

            st.write(
                f"**Date:** {today}"
            )


        st.divider()


        # =================================================
        # CHECK TODAY'S RECORD
        # =================================================

        cursor.execute(
            """
            SELECT id, completed
            FROM progress
            WHERE habit_id = %s
            AND completed_date = %s
            LIMIT 1
            """,
            (
                habit_id,
                today
            )
        )

        existing = cursor.fetchone()


        # =================================================
        # ALREADY CHECKED IN
        # =================================================

        if existing:

            if existing[1] == 1:

                st.success(
                    "This habit has already been marked as completed today."
                )

            else:

                st.warning(
                    "This habit has already been marked as missed today."
                )

            return


        # =================================================
        # CHECK-IN
        # =================================================

        st.write(
            "Record today's status:"
        )

        col1, col2 = st.columns(2)


        # =================================================
        # COMPLETED
        # =================================================

        with col1:

            if st.button(
                "Completed",
                use_container_width=True,
                key=f"checkin_complete_{habit_id}"
            ):

                try:

                    cursor.execute(
                        """
                        INSERT INTO progress
                        (
                            habit_id,
                            completed_date,
                            completed
                        )
                        VALUES (%s, %s, %s)
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
                        SET status = %s
                        WHERE id = %s
                        AND user_id = %s
                        """,
                        (
                            "Completed",
                            habit_id,
                            user_id
                        )
                    )


                    conn.commit()


                    st.success(
                        "Habit marked as completed."
                    )

                    st.rerun()


                except Exception as e:

                    conn.rollback()

                    st.error(
                        f"Unable to save check-in: {e}"
                    )


        # =================================================
        # MISSED
        # =================================================

        with col2:

            if st.button(
                "Missed",
                use_container_width=True,
                key=f"checkin_missed_{habit_id}"
            ):

                try:

                    cursor.execute(
                        """
                        INSERT INTO progress
                        (
                            habit_id,
                            completed_date,
                            completed
                        )
                        VALUES (%s, %s, %s)
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
                        SET status = %s
                        WHERE id = %s
                        AND user_id = %s
                        """,
                        (
                            "Pending",
                            habit_id,
                            user_id
                        )
                    )


                    conn.commit()


                    st.warning(
                        "Habit marked as missed."
                    )

                    st.rerun()


                except Exception as e:

                    conn.rollback()

                    st.error(
                        f"Unable to save check-in: {e}"
                    )


    except Exception as e:

        conn.rollback()

        st.error(
            f"Unable to load daily check-in: {e}"
        )


    finally:

        cursor.close()
        conn.close()