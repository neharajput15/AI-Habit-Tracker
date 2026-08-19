import streamlit as st
import sqlite3
from datetime import date


# =====================================================
# DATABASE
# =====================================================

def get_connection():

    return sqlite3.connect(
        "habit_tracker.db"
    )


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

    cursor.execute(
        """
        SELECT
            id,
            habit_name,
            category,
            target
        FROM habits
        WHERE user_id = ?
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
        WHERE h.user_id = ?
        AND p.date = ?
        AND p.completed = 1
        """,
        (
            user_id,
            today
        )
    )

    completed_today = cursor.fetchone()[0]

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
        # CHECK PROGRESS
        # ---------------------------------------------

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT completed
            FROM progress
            WHERE habit_id = ?
            AND date = ?
            """,
            (
                habit_id,
                today
            )
        )

        progress = cursor.fetchone()

        conn.close()


        completed = (
            progress is not None
            and progress[0] == 1
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


            if completed:

                st.success(
                    "Completed today 🎉"
                )

                st.caption(
                    "🔥 Great job! Keep your streak going!"
                )


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


                    # ---------------------------------
                    # CHECK EXISTING RECORD
                    # ---------------------------------

                    cursor.execute(
                        """
                        SELECT id
                        FROM progress
                        WHERE habit_id = ?
                        AND date = ?
                        """,
                        (
                            habit_id,
                            today
                        )
                    )

                    existing = cursor.fetchone()


                    # ---------------------------------
                    # UPDATE
                    # ---------------------------------

                    if existing:

                        cursor.execute(
                            """
                            UPDATE progress
                            SET completed = 1,
                                completed_date = ?
                            WHERE id = ?
                            """,
                            (
                                today,
                                existing[0]
                            )
                        )


                    # ---------------------------------
                    # INSERT
                    # ---------------------------------

                    else:

                        cursor.execute(
                            """
                            INSERT INTO progress
                            (
                                habit_id,
                                date,
                                completed,
                                completed_date
                            )
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                habit_id,
                                today,
                                1,
                                today
                            )
                        )


                    conn.commit()

                    conn.close()


                    st.success(
                        f"{habit_name} completed! 🎉"
                    )

                    st.rerun()


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


    st.progress(
    min(max(percentage, 0.0), 1.0)
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