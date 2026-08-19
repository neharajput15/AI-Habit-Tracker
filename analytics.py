import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def analytics():

    st.header("📊 Habit Analytics")

    conn = sqlite3.connect("habit_tracker.db")

    # Get user's habits
    query = """
    SELECT
        h.habit_name,
        h.category,
        p.date,
        p.completed
    FROM habits h
    LEFT JOIN progress p
        ON h.id = p.habit_id
    WHERE h.user_id = ?
    ORDER BY p.date
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(st.session_state.user_id,)
    )

    conn.close()

    # No data
    if df.empty:

        st.info(
            "No habit data available yet."
        )

        return

    # Remove empty dates
    df = df.dropna(
        subset=["date"]
    )

    if df.empty:

        st.info(
            "Complete some habits to see analytics."
        )

        return

    # Convert completed to integer
    df["completed"] = df["completed"].astype(int)

    # -----------------------------
    # Statistics
    # -----------------------------

    total_records = len(df)

    completed_records = df["completed"].sum()

    missed_records = (
        total_records - completed_records
    )

    completion_rate = (
        completed_records / total_records
    ) * 100

    # -----------------------------
    # Metrics
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📋 Total Records",
        total_records
    )

    col2.metric(
        "✅ Completed",
        completed_records
    )

    col3.metric(
        "📈 Completion Rate",
        f"{completion_rate:.1f}%"
    )

    # -----------------------------
    # Completion Chart
    # -----------------------------

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

    ax.set_ylabel("Number of Days")

    ax.set_title(
        "Completed vs Missed"
    )

    st.pyplot(fig)

    # -----------------------------
    # Habit-wise Analysis
    # -----------------------------

    st.subheader(
        "📌 Habit-wise Performance"
    )

    habit_data = (
        df.groupby("habit_name")["completed"]
        .mean() * 100
    )

    habit_data = habit_data.round(1)

    st.dataframe(
        habit_data.rename(
            "Completion %"
        )
    )

    # -----------------------------
    # Best Habit
    # -----------------------------

    if not habit_data.empty:

        best_habit = habit_data.idxmax()

        best_percentage = habit_data.max()

        st.success(
            f"🏆 Best Habit: {best_habit} "
            f"({best_percentage:.1f}% completion)"
        )