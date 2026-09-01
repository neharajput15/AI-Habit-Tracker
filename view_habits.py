import streamlit as st
from datetime import date

from database import get_connection


# =====================================================
# VIEW HABITS
# =====================================================

def view_habits():

    st.title("My Habits")

    st.caption(
        "View, complete and manage your saved habits."
    )

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

        return


    conn = get_connection()
    cursor = conn.cursor()

    try:

        # =================================================
        # GET HABITS
        # =================================================

        cursor.execute(
            """
            SELECT
                id,
                habit_name,
                category,
                target,
                frequency,
                status
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
                "No habits found. Add your first habit to get started."
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
            frequency = habit[4]
            status = habit[5]


            with st.expander(
                habit_name
            ):

                # -----------------------------------------
                # HABIT INFORMATION
                # -----------------------------------------

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
                        f"**Status:** {status}"
                    )


                st.divider()


                # =================================================
                # ACTION BUTTONS
                # =================================================

                col1, col2 = st.columns(2)


                # =================================================
                # COMPLETE
                # =================================================

                with col1:

                    if status == "Completed":

                        st.success(
                            "Completed"
                        )

                    else:

                        if st.button(
                            "Complete",
                            key=f"complete_{habit_id}",
                            use_container_width=True
                        ):

                            today = str(date.today())

                            try:

                                # ---------------------------------
                                # CHECK TODAY'S RECORD
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
                                # INSERT RECORD
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
                                # UPDATE STATUS
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
                                    "Habit completed."
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
                        "Delete",
                        key=f"delete_{habit_id}",
                        use_container_width=True
                    ):

                        try:

                            # ---------------------------------
                            # DELETE PROGRESS
                            # ---------------------------------

                            cursor.execute(
                                """
                                DELETE FROM progress
                                WHERE habit_id = %s
                                """,
                                (habit_id,)
                            )


                            # ---------------------------------
                            # DELETE HABIT
                            # ---------------------------------

                            cursor.execute(
                                """
                                DELETE FROM habits
                                WHERE id = %s
                                AND user_id = %s
                                """,
                                (
                                    habit_id,
                                    user_id
                                )
                            )


                            conn.commit()


                            st.success(
                                "Habit deleted."
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