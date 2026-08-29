import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database import get_connection


# =====================================================
# ANALYTICS
# =====================================================

def analytics():

    st.header("📊 Habit Analytics")

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning("Please login first.")

        return

    # =================================================
    # DATABASE CONNECTION
    # =================================================

    conn = get_connection()

    try:

        # =================================================
        # GET USER'S HABIT PROGRESS
        # =================================================

        query = """
        SELECT
            h.habit_name,
            h.category,
            p.completed_date,
            p.completed
        FROM habits h
        LEFT JOIN progress p
            ON h.id = p.habit_id
        WHERE h.user_id = %s
        ORDER BY p.completed_date
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(user_id,)
        )

    except Exception as e:

        st.error(
            f"Unable to load analytics: {e}"
        )

        return

    finally:

        conn.close()

    # =================================================
    # NO DATA
    # =================================================

    if df.empty:

        st.info(
            "No habit data available yet."
        )

        return

    # =================================================
    # REMOVE EMPTY DATES
    # =================================================

    df = df.dropna(
        subset=["completed_date"]
    )

    if df.empty:

        st.info(
            "Complete some habits to see analytics."
        )

        return

    # =================================================
    # CONVERT DATA
    # =================================================

    df["completed"] = pd.to_numeric(
        df["completed"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["completed"]
    )

    df["completed"] = df[
        "completed"
    ].astype(int)

    # =================================================
    # STATISTICS
    # =================================================

    total_records = len(df)

    completed_records = int(
        df["completed"].sum()
    )

    missed_records = (
        total_records - completed_records
    )

    if total_records > 0:

        completion_rate = (
            completed_records /
            total_records
        ) * 100

    else:

        completion_rate = 0

    # =================================================
    # METRICS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📋 Total Records",
            total_records
        )

    with col2:

        st.metric(
            "✅ Completed",
            completed_records
        )

    with col3:

        st.metric(
            "📈 Completion Rate",
            f"{completion_rate:.1f}%"
        )

    # =================================================
    # COMPLETION CHART
    # =================================================

    st.subheader(
        "📈 Completion Overview"
    )

    chart_data = pd.DataFrame({
        "Status": [
            "Completed",
            "Missed"
        ],
        "Count": [
            completed_records,
            missed_records
        ]
    })

    fig, ax = plt.subplots()

    ax.bar(
        chart_data["Status"],
        chart_data["Count"]
    )

    ax.set_ylabel(
        "Number of Days"
    )

    ax.set_title(
        "Completed vs Missed"
    )

    st.pyplot(fig)

    plt.close(fig)

    # =================================================
    # HABIT-WISE ANALYSIS
    # =================================================

    st.subheader(
        "📌 Habit-wise Performance"
    )

    habit_data = (
        df.groupby("habit_name")["completed"]
        .mean()
        * 100
    )

    habit_data = habit_data.round(1)

    st.dataframe(
        habit_data.rename(
            "Completion %"
        )
    )

    # =================================================
    # BEST HABIT
    # =================================================

    if not habit_data.empty:

        best_habit = habit_data.idxmax()

        best_percentage = habit_data.max()

        st.success(
            f"🏆 Best Habit: {best_habit} "
            f"({best_percentage:.1f}% completion)"
        )