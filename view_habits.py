import streamlit as st
from datetime import date

from database import get_connection


# =====================================================
# VIEW HABITS
# =====================================================

def view_habits():

    st.header("📋 My Habits")

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
                reminder_time,
                status
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (st.session_state.user_id,)
        )

        habits = cursor.fetchall()

        if not habits:

            st.info(
                "No habits found. Add your first habit!"
            )

            return

        # =================================================
        # DISPLAY HABITS
        # =================================================

        for habit in habits:

            habit_id = habit[0]
            habit_name = habit[1]
            category = habit[2]
            target = habit[3]
            reminder_time = habit[4]
            status = habit[5]

            with st.expander(
                f"📌 {habit_name}"
            ):

                st.write(
                    f"**Category:** {category}"
                )

                st.write(
                    f"**Target:** {target}"
                )

                st.write(
                    f"**Reminder:** {reminder_time}"
                )

                st.write(
                    f"**Status:** {status}"
                )

                col1, col2 = st.columns(2)

                # =================================================
                # COMPLETE
                # =================================================

                with col1:

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{habit_id}",
                        use_container_width=True
                    ):

                        today = date.today()

                        try:

                            # -----------------------------------------
                            # CHECK TODAY'S PROGRESS
                            # -----------------------------------------

                            cursor.execute(
                                """
                                SELECT id, completed
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

                            # -----------------------------------------
                            # ALREADY COMPLETED
                            # -----------------------------------------

                            if existing and existing[1] == 1:

                                st.info(
                                    "This habit is already completed today. ✅"
                                )

                            # -----------------------------------------
                            # UPDATE MISSED RECORD
                            # -----------------------------------------

                            elif existing:

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
                                        st.session_state.user_id
                                    )
                                )

                                conn.commit()

                                st.success(
                                    "Habit Completed! 🎉"
                                )

                                st.rerun()

                            # -----------------------------------------
                            # INSERT NEW RECORD
                            # -----------------------------------------

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
                                        st.session_state.user_id
                                    )
                                )

                                conn.commit()

                                st.success(
                                    "Habit Completed! 🎉"
                                )

                                st.rerun()

                        except Exception as e:

                            conn.rollback()

                            st.error(
                                f"Unable to complete habit: {e}"
                            )

                # =================================================
                # DELETE
                # =================================================

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{habit_id}",
                        use_container_width=True
                    ):

                        try:

                            # Delete progress
                            cursor.execute(
                                """
                                DELETE FROM progress
                                WHERE habit_id = %s
                                """,
                                (habit_id,)
                            )

                            # Delete habit
                            cursor.execute(
                                """
                                DELETE FROM habits
                                WHERE id = %s
                                AND user_id = %s
                                """,
                                (
                                    habit_id,
                                    st.session_state.user_id
                                )
                            )

                            conn.commit()

                            st.success(
                                "Habit Deleted! 🗑️"
                            )

                            st.rerun()

                        except Exception as e:

                            conn.rollback()

                            st.error(
                                f"Unable to delete habit: {e}"
                            )

    except Exception as e:

        st.error(
            f"Unable to load habits: {e}"
        )

    finally:

        cursor.close()
        conn.close()