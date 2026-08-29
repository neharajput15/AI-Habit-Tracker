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

    st.header("📊 Dashboard")

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

        return

    # =================================================
    # BASIC HABIT STATISTICS
    # =================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ---------------------------------------------
        # TOTAL HABITS
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM habits
            WHERE user_id = %s
            """,
            (user_id,)
        )

        total = cursor.fetchone()[0]

        # ---------------------------------------------
        # COMPLETED HABITS
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM habits
            WHERE user_id = %s
            AND status = %s
            """,
            (
                user_id,
                "Completed"
            )
        )

        completed = cursor.fetchone()[0]

    except Exception as e:

        st.error(
            f"Unable to load dashboard: {e}"
        )

        return

    finally:

        cursor.close()
        conn.close()

    pending = total - completed

    # =================================================
    # SUMMARY CARDS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📋 Total Habits",
            total
        )

    with col2:

        st.metric(
            "✅ Completed",
            completed
        )

    with col3:

        st.metric(
            "⏳ Pending",
            pending
        )

    # =================================================
    # OVERALL PROGRESS
    # =================================================

    if total > 0:

        percentage = (
            completed / total
        ) * 100

    else:

        percentage = 0

    st.subheader(
        "📈 Overall Progress"
    )

    st.progress(
        min(
            max(
                int(percentage),
                0
            ),
            100
        )
    )

    st.write(
        f"Completion: {percentage:.1f}%"
    )

    # =================================================
    # PIE CHART
    # =================================================

    if total > 0:

        labels = [
            "Completed",
            "Pending"
        ]

        values = [
            completed,
            pending
        ]

        fig, ax = plt.subplots()

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Habit Completion"
        )

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.info(
            "No habits available."
        )

    # =================================================
    # ML PREDICTION
    # =================================================

    st.markdown("---")

    st.subheader(
        "🤖 ML Habit Completion Prediction"
    )

    # =================================================
    # GET USER HABITS
    # =================================================

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT id, habit_name
            FROM habits
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        habits = cursor.fetchall()

    except Exception as e:

        st.error(
            f"Unable to load habits: {e}"
        )

        return

    finally:

        cursor.close()
        conn.close()

    # =================================================
    # NO HABITS
    # =================================================

    if not habits:

        st.info(
            "➕ Add a habit first to use ML prediction."
        )

        return

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

    st.write(
        f"### 📚 {habit_name}"
    )

    # =================================================
    # RECENT HISTORY
    # =================================================

    last_five = get_last_five_days(
        habit_id
    )

    if last_five:

        st.write(
            "#### 📅 Recent Habit History"
        )

        st.write(
            f"**Last {len(last_five)} recorded days:**"
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
                f"{symbol} {record_date}"
            )

        # ---------------------------------------------
        # CONSISTENCY
        # ---------------------------------------------

        consistency = get_recent_consistency(
            habit_id
        )

        st.metric(
            "📊 Recent Consistency",
            f"{consistency:.1f}%"
        )

    else:

        st.info(
            "No check-in history available yet."
        )

    # =================================================
    # PREDICTION BUTTON
    # =================================================

    st.markdown("---")

    if st.button(
        "🔮 Predict Completion",
        use_container_width=True,
        key="predict_completion_button"
    ):

        prediction, message = (
            predict_habit_completion(
                habit_id
            )
        )

        # ---------------------------------------------
        # NOT ENOUGH DATA
        # ---------------------------------------------

        if message:

            st.warning(
                f"⚠️ {message}"
            )

            st.info(
                "Complete or miss this habit for at least "
                "5 days to generate an ML prediction."
            )

        # ---------------------------------------------
        # PREDICTION AVAILABLE
        # ---------------------------------------------

        else:

            st.metric(
                "🤖 Completion Likelihood",
                f"{prediction:.1f}%"
            )

            st.progress(
                min(
                    max(
                        int(prediction),
                        0
                    ),
                    100
                )
            )

            # -----------------------------------------
            # RECOMMENDATION
            # -----------------------------------------

            if prediction >= 70:

                st.success(
                    "🎯 Excellent consistency! "
                    "You are likely to complete this habit."
                )

            elif prediction >= 40:

                st.warning(
                    "⚠️ Your consistency is moderate. "
                    "Try to complete this habit regularly."
                )

            else:

                st.error(
                    "📌 Your completion likelihood is low. "
                    "Try setting a fixed time for this habit."
                )