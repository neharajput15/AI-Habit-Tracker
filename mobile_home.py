import streamlit as st
from datetime import date

from database import get_connection


# =====================================================
# HOME
# =====================================================

def mobile_home():

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

        return

    today = str(date.today())


    # =================================================
    # DATABASE CONNECTION
    # =================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ---------------------------------------------
        # GET USER HABITS
        # ---------------------------------------------

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


        # ---------------------------------------------
        # COMPLETED TODAY
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h
            ON p.habit_id = h.id
            WHERE h.user_id = %s
            AND p.completed_date = %s
            AND p.completed = 1
            """,
            (
                user_id,
                today
            )
        )

        completed_today = cursor.fetchone()[0]


    except Exception as e:

        st.error(
            f"Unable to load home page: {e}"
        )

        return


    finally:

        cursor.close()
        conn.close()


    # =================================================
    # CALCULATIONS
    # =================================================

    total_habits = len(habits)

    pending_habits = max(
        total_habits - completed_today,
        0
    )


    if total_habits > 0:

        percentage = (
            completed_today / total_habits
        )

    else:

        percentage = 0


    # =================================================
    # HEADER
    # =================================================

    st.title("Smart Habit Tracker")

    st.caption(
        "Build better habits, track your progress, "
        "and stay consistent."
    )


    # =================================================
    # SUMMARY
    # =================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Habits",
            total_habits
        )


    with col2:

        st.metric(
            "Completed Today",
            completed_today
        )


    with col3:

        st.metric(
            "Pending",
            pending_habits
        )


    # =================================================
    # TODAY'S PROGRESS
    # =================================================

    st.divider()

    st.subheader(
        "Today's Progress"
    )


    st.progress(
        min(
            max(
                percentage,
                0.0
            ),
            1.0
        )
    )


    st.caption(
        f"{completed_today} of {total_habits} habits completed "
        f"({percentage * 100:.0f}%)"
    )


    # =================================================
    # TODAY'S HABITS
    # =================================================

    st.divider()

    st.subheader(
        "Today's Habits"
    )


    if not habits:

        st.info(
            "No habits added yet. "
            "Use Add Habit to create your first habit."
        )

        return


    # =================================================
    # HABIT CARDS
    # =================================================

    for habit in habits:

        habit_id = habit[0]
        habit_name = habit[1]
        category = habit[2]
        target = habit[3]
        frequency = habit[4]


        # ---------------------------------------------
        # GET TODAY'S STATUS
        # ---------------------------------------------

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT completed
                FROM progress
                WHERE habit_id = %s
                AND completed_date = %s
                """,
                (
                    habit_id,
                    today
                )
            )

            progress = cursor.fetchone()


        finally:

            cursor.close()
            conn.close()


        completed = (
            progress is not None
            and progress[0] == 1
        )


        # =================================================
        # CARD
        # =================================================

        with st.container(border=True):

            st.markdown(
                f"### {habit_name}"
            )

            st.caption(
                f"{category}  •  {frequency}"
            )

            st.write(
                f"Target: {target}"
            )


            # -----------------------------------------
            # COMPLETED
            # -----------------------------------------

            if completed:

                st.success(
                    "Completed today."
                )

                st.caption(
                    "Keep your consistency going."
                )


            # -----------------------------------------
            # NOT COMPLETED
            # -----------------------------------------

            else:

                st.info(
                    "Not completed today."
                )


                if st.button(
                    "Complete",
                    key=f"home_complete_{habit_id}",
                    use_container_width=True
                ):

                    conn = get_connection()
                    cursor = conn.cursor()

                    try:

                        # ---------------------------------
                        # CHECK EXISTING RECORD
                        # ---------------------------------

                        cursor.execute(
                            """
                            SELECT id
                            FROM progress
                            WHERE habit_id = %s
                            AND completed_date = %s
                            """,
                            (
                                habit_id,
                                today
                            )
                        )

                        existing = cursor.fetchone()


                        # ---------------------------------
                        # UPDATE RECORD
                        # ---------------------------------

                        if existing:

                            cursor.execute(
                                """
                                UPDATE progress
                                SET completed = %s
                                WHERE id = %s
                                """,
                                (
                                    1,
                                    existing[0]
                                )
                            )


                        # ---------------------------------
                        # CREATE RECORD
                        # ---------------------------------

                        else:

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


                        # ---------------------------------
                        # UPDATE HABIT STATUS
                        # ---------------------------------

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
                            f"{habit_name} completed."
                        )

                        st.rerun()


                    except Exception as e:

                        conn.rollback()

                        st.error(
                            f"Unable to complete habit: {e}"
                        )


                    finally:

                        cursor.close()
                        conn.close()


    # =================================================
    # DAILY SUMMARY
    # =================================================

    st.divider()

    st.subheader(
        "Daily Summary"
    )


    if completed_today == total_habits and total_habits > 0:

        st.success(
            "All habits completed today."
        )

    elif completed_today > 0:

        st.info(
            "Good progress. "
            "Keep working on your remaining habits."
        )

    else:

        st.info(
            "No habits completed yet today."
        )