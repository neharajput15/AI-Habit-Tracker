import streamlit as st
import matplotlib.pyplot as plt

from database import get_connection

from ml_prediction import (
    predict_habit_completion,
    get_last_five_days,
    get_recent_consistency
)


# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return

    # =================================================
    # GET USER HABITS
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

    except Exception as e:

        st.error(f"Unable to load dashboard: {e}")
        return

    finally:

        cursor.close()
        conn.close()


    # =================================================
    # HEADER
    # =================================================

    st.title("📊 Progress Dashboard")

    st.caption(
        "Track your habits, monitor consistency and improve every day."
    )

    st.divider()


    # =================================================
    # NO HABITS
    # =================================================

    if not habits:

        st.info(
            "🌱 No habits added yet. Add your first habit to start tracking."
        )

        return


    # =================================================
    # BASIC STATISTICS
    # =================================================

    total_habits = len(habits)

    completed_habits = sum(
        1
        for habit in habits
        if habit[5] == "Completed"
    )

    pending_habits = max(
        total_habits - completed_habits,
        0
    )

    percentage = (
        completed_habits / total_habits
        if total_habits > 0
        else 0
    )


    # =================================================
    # SUMMARY CARDS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📋 Total Habits",
            total_habits
        )

    with col2:

        st.metric(
            "✅ Completed",
            completed_habits
        )

    with col3:

        st.metric(
            "⏳ Pending",
            pending_habits
        )


    # =================================================
    # TODAY'S OVERALL PROGRESS
    # =================================================

    st.divider()

    st.subheader("📈 Overall Progress")

    st.progress(
        min(
            max(
                percentage,
                0.0
            ),
            1.0
        )
    )

    st.write(
        f"**{completed_habits} of {total_habits} habits completed "
        f"({percentage * 100:.0f}%)**"
    )


    # =================================================
    # COMPLETION CHART
    # =================================================

    st.divider()

    st.subheader("📊 Completion Overview")

    labels = [
        "Completed",
        "Pending"
    ]

    values = [
        completed_habits,
        pending_habits
    ]

    if sum(values) > 0:

        fig, ax = plt.subplots(
            figsize=(5, 3.5)
        )

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Habit Completion"
        )

        st.pyplot(
            fig,
            use_container_width=False
        )

        plt.close(fig)


    # =================================================
    # MY HABITS
    # =================================================

    st.divider()

    st.subheader("🎯 My Habits")

    for habit in habits:

        habit_id = habit[0]
        habit_name = habit[1]
        category = habit[2]
        target = habit[3]
        frequency = habit[4]
        status = habit[5]


        # =================================================
        # RECENT CONSISTENCY
        # =================================================

        consistency = get_recent_consistency(
            habit_id
        )


        # =================================================
        # HABIT CARD
        # =================================================

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                st.subheader(
                    f"📌 {habit_name}"
                )

                st.caption(
                    f"📂 {category}  •  🔄 {frequency}"
                )

                st.write(
                    f"🎯 Target: {target}"
                )

            with col2:

                if status == "Completed":

                    st.success(
                        "Completed"
                    )

                else:

                    st.warning(
                        "Pending"
                    )


            # =================================================
            # CONSISTENCY
            # =================================================

            st.write(
                f"Consistency: **{consistency:.1f}%**"
            )

            st.progress(
                min(
                    max(
                        consistency / 100,
                        0.0
                    ),
                    1.0
                )
            )


    # =================================================
    # ML PREDICTION
    # =================================================

    st.divider()

    st.subheader("🤖 Smart Habit Prediction")

    st.caption(
        "Use your previous habit history to estimate your next completion likelihood."
    )


    # =================================================
    # SELECT HABIT
    # =================================================

    selected_habit = st.selectbox(
        "Select a habit",
        habits,
        format_func=lambda x: x[1],
        key="dashboard_habit_select"
    )

    habit_id = selected_habit[0]
    habit_name = selected_habit[1]


    st.markdown(
        f"### 📌 {habit_name}"
    )


    # =================================================
    # RECENT HISTORY
    # =================================================

    last_five = get_last_five_days(
        habit_id
    )

    if last_five:

        st.markdown(
            "#### 🗓️ Recent History"
        )

        history = " ".join(
            symbol
            for _, symbol in last_five
        )

        st.markdown(
            f"### {history}"
        )

        for record_date, symbol in last_five:

            st.write(
                f"{symbol}  {record_date}"
            )


        # =================================================
        # CONSISTENCY
        # =================================================

        consistency = get_recent_consistency(
            habit_id
        )

        st.metric(
            "📈 Recent Consistency",
            f"{consistency:.1f}%"
        )

    else:

        st.info(
            "📝 No check-in history available yet."
        )


    # =================================================
    # PREDICT BUTTON
    # =================================================

    st.divider()

    if st.button(
        "🤖 Predict Completion",
        use_container_width=True,
        key="predict_completion_button"
    ):

        prediction, message = (
            predict_habit_completion(
                habit_id
            )
        )


        # =================================================
        # NOT ENOUGH DATA
        # =================================================

        if prediction is None:

            st.warning(
                f"⚠️ {message}"
            )

            st.info(
                "Complete or miss this habit for at least "
                "5 days to generate an ML prediction."
            )


        # =================================================
        # PREDICTION AVAILABLE
        # =================================================

        else:

            st.markdown(
                "#### 🎯 Completion Likelihood"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "ML Prediction",
                    f"{prediction:.1f}%"
                )

            with col2:

                if prediction >= 70:

                    st.success(
                        "High"
                    )

                elif prediction >= 40:

                    st.warning(
                        "Moderate"
                    )

                else:

                    st.error(
                        "Low"
                    )


            st.progress(
                min(
                    max(
                        prediction / 100,
                        0.0
                    ),
                    1.0
                )
            )


            # =================================================
            # SMART RECOMMENDATION
            # =================================================

            st.markdown(
                "#### 💡 Smart Recommendation"
            )

            if prediction >= 70:

                st.success(
                    "🔥 Your consistency is strong. "
                    "Keep following your current routine."
                )

            elif prediction >= 40:

                st.warning(
                    "💪 Your consistency is moderate. "
                    "Try completing this habit at the same "
                    "time every day."
                )

            else:

                st.info(
                    "🌱 Your completion likelihood is low. "
                    "Try a smaller target and set a fixed "
                    "time for this habit."
                )


    # =================================================
    # FINAL MOTIVATION
    # =================================================

    st.divider()

    if completed_habits == total_habits:

        st.success(
            "🎉 Excellent! You completed all your habits!"
        )

    elif completed_habits > 0:

        st.info(
            "💪 Good progress! Keep going and complete the remaining habits."
        )

    else:

        st.info(
            "🌱 Start with one habit today. Small steps create big results."
        )