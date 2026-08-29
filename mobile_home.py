import streamlit as st
from datetime import date

from database import get_connection


# =====================================================
# HOME
# =====================================================

def mobile_home():

    user_id = st.session_state.get(
        "user_id"
    )

    name = st.session_state.get(
        "name",
        "User"
    )

    if not user_id:

        st.warning(
            "Please login first."
        )

        return

    today = str(date.today())

    # =================================================
    # GET HABITS
    # =================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                habit_name,
                category,
                target
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        habits = cursor.fetchall()

        # =================================================
        # COMPLETED TODAY
        # =================================================

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
            f"Unable to load home data: {e}"
        )

        return

    finally:

        cursor.close()
        conn.close()

    # =================================================
    # HEADER
    # =================================================

    st.title(
        "📈 Smart Habit Tracker"
    )

    st.subheader(
        f"Good Day, {name} 👋"
    )

    st.caption(
        "Let's build better habits today. 🌱"
    )

    # =================================================
    # STATISTICS
    # =================================================

    total_habits = len(habits)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📋 Total Habits",
            total_habits
        )

    with col2:

        st.metric(
            "✅ Completed Today",
            f"{completed_today}/{total_habits}"
        )

    st.divider()

    # =================================================
    # TODAY'S HABITS
    # =================================================

    st.subheader(
        "Today's Habits 🎯"
    )

    if not habits:

        st.info(
            "No habits added yet."
        )

        st.write(
            "Use ➕ Add Habit to create your first habit."
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

        # ---------------------------------------------
        # CHECK TODAY'S PROGRESS
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
            and int(progress[0]) == 1
        )

        # =================================================
        # CARD
        # =================================================

        with st.container(border=True):

            if completed:

                st.subheader(
                    f"✅ {habit_name}"
                )

            else:

                st.subheader(
                    f"⭕ {habit_name}"
                )

            st.caption(
                f"📂 {category}  •  🎯 {target}"
            )

            # ---------------------------------------------
            # COMPLETED
            # ---------------------------------------------

            if completed:

                st.success(
                    "Completed today 🎉"
                )

                st.caption(
                    "🔥 Great job! Keep your streak going!"
                )

            # ---------------------------------------------
            # NOT COMPLETED
            # ---------------------------------------------

            else:

                st.warning(
                    "Not completed today"
                )

                if st.button(
                    "✅ Complete",
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
                        # UPDATE EXISTING RECORD
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
                        # INSERT NEW RECORD
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
                            f"{habit_name} completed! 🎉"
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
    # TODAY'S PROGRESS
    # =================================================

    st.divider()

    st.subheader(
        "📈 Today's Progress"
    )

    if total_habits > 0:

        percentage = (
            completed_today /
            total_habits
        )

    else:

        percentage = 0

    percentage = min(
        max(percentage, 0.0),
        1.0
    )

    st.progress(
        percentage
    )

    st.write(
        f"**{completed_today} of "
        f"{total_habits} habits completed "
        f"({percentage * 100:.0f}%)**"
    )

    # =================================================
    # MOTIVATION
    # =================================================

    if total_habits == 0:

        st.info(
            "🌱 Add your first habit to get started!"
        )

    elif completed_today == total_habits:

        st.success(
            "🎉 Amazing! You completed all "
            "your habits today!"
        )

    elif completed_today > 0:

        st.info(
            "💪 Good progress! Keep going!"
        )

    else:

        st.info(
            "🌱 Start your day by completing "
            "your first habit!"
        )