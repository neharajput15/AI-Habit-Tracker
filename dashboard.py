import streamlit as st
import matplotlib.pyplot as plt

from database import get_connection
from ml_prediction import (
    get_recent_consistency,
    get_last_five_days,
    predict_habit_completion
)


def dashboard():

    # =====================================================
    # CSS
    # =====================================================

    st.markdown("""
    <style>

    .stApp {
        background: #080918;
        color: white;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 30px;
        padding-bottom: 40px;
    }

    /* HEADER */

    .dashboard-header {
        text-align: center;
        margin-bottom: 28px;
    }

    .dashboard-icon {
        width: 50px;
        height: 50px;
        margin: auto;
        border-radius: 13px;
        background: linear-gradient(135deg, #48206d, #873ed0);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 25px;
    }

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        margin-top: 12px;
        color: #ffffff;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #aaa7d5;
        margin-top: 5px;
    }

    /* STAT CARDS */

    .stat-card {
        background: linear-gradient(145deg, #121326, #0d0e1d);
        border: 1px solid #34265b;
        border-radius: 13px;
        padding: 19px;
        min-height: 105px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }

    .stat-content {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        min-width: 50px;
        border-radius: 50%;
        background: #402064;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
    }

    .stat-label {
        color: #aaa7d5;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .stat-value {
        color: white;
        font-size: 27px;
        font-weight: 700;
    }

    .green {
        color: #52d681;
    }

    .orange {
        color: #ff9d20;
    }

    .purple {
        color: #b16aff;
    }

    /* SECTION */

    .section-card {
        background: linear-gradient(145deg, #121326, #0d0e1d);
        border: 1px solid #34265b;
        border-radius: 13px;
        padding: 22px;
        margin-top: 20px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: white;
        margin-bottom: 12px;
    }

    /* PROGRESS */

    .progress-text {
        color: #aaa7d5;
        font-size: 15px;
        margin-bottom: 10px;
    }

    .progress-number {
        color: #a967ff;
        font-weight: 700;
    }

    .custom-progress {
        width: 100%;
        height: 15px;
        background: #22233b;
        border-radius: 15px;
        overflow: hidden;
    }

    .custom-progress-fill {
        height: 100%;
        background: linear-gradient(
            90deg,
            #7025c5,
            #a94cff
        );
        border-radius: 15px;
    }

    .progress-percent {
        text-align: right;
        color: #a967ff;
        font-size: 14px;
        font-weight: bold;
        margin-top: 5px;
    }

    /* HABIT PERFORMANCE */

    .habit-row {
        background: #17182d;
        border: 1px solid #252641;
        border-radius: 9px;
        padding: 9px 12px;
        margin-bottom: 7px;
        display: flex;
        align-items: center;
    }

    .habit-left {
        width: 37%;
        display: flex;
        align-items: center;
    }

    .habit-icon {
        width: 34px;
        height: 34px;
        min-width: 34px;
        border-radius: 50%;
        background: #7034a9;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 9px;
        font-size: 16px;
    }

    .habit-name {
        color: white;
        font-size: 14px;
        font-weight: 600;
    }

    .habit-history {
        width: 43%;
    }

    .history-title {
        text-align: center;
        color: #8e8ba9;
        font-size: 12px;
    }

    .history {
        display: flex;
        justify-content: center;
        gap: 7px;
        margin-top: 5px;
    }

    .history-circle {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: bold;
    }

    .completed-circle {
        border: 2px solid #4ade80;
        color: #4ade80;
    }

    .missed-circle {
        border: 2px solid #ff5b61;
        color: #ff5b61;
    }

    .consistency {
        width: 20%;
    }

    .consistency-title {
        text-align: center;
        color: #8e8ba9;
        font-size: 12px;
    }

    .consistency-value {
        text-align: center;
        color: white;
        font-size: 16px;
        font-weight: 700;
        margin-top: 3px;
    }

    /* AI */

    .ai-box {
        background: linear-gradient(145deg, #121326, #0d0e1d);
        border: 1px solid #34265b;
        border-radius: 13px;
        padding: 22px;
        margin-top: 20px;
    }

    .ai-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
    }

    .ai-description {
        color: #aaa7d5;
        font-size: 14px;
        margin-top: 7px;
    }

    /* BUTTON */

    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton > button {
        background: linear-gradient(
            135deg,
            #7025c5,
            #8f3de0
        ) !important;

        color: white !important;
        border: none !important;
        border-radius: 8px !important;

        padding: 7px 18px !important;
        min-height: 38px !important;

        width: auto !important;

        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #8438dc,
            #a451ef
        ) !important;
    }

    /* SELECTBOX */

    div[data-baseweb="select"] > div {
        background: #111226 !important;
        border: 1px solid #34265b !important;
        border-radius: 8px !important;
    }

    /* AI RESULT */

    .prediction-result {
        background: #17182d;
        border: 1px solid #34265b;
        border-radius: 10px;
        padding: 18px;
        margin-top: 15px;
        text-align: center;
    }

    .prediction-label {
        color: #aaa7d5;
        font-size: 14px;
    }

    .prediction-value {
        color: #ad69ff;
        font-size: 34px;
        font-weight: 700;
        margin-top: 5px;
    }

    .dashboard-footer {
        text-align: center;
        color: #686685;
        margin-top: 28px;
        font-size: 12px;
    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # HEADER
    # =====================================================

    st.html("""
    <div class="dashboard-header">

        <div class="dashboard-icon">
            📊
        </div>

        <div class="dashboard-title">
            Progress Dashboard
        </div>

        <div class="dashboard-subtitle">
            Track your habit performance and see your progress.
        </div>

    </div>
    """)


    # =====================================================
    # LOGIN CHECK
    # =====================================================

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return


    # =====================================================
    # GET HABITS
    # =====================================================

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, habit_name, category
            FROM habits
            WHERE user_id = %s
            ORDER BY id
        """, (user_id,))

        habits = cursor.fetchall()

    except Exception as e:

        st.error(f"Unable to load habits: {e}")
        return

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


    # =====================================================
    # COMPLETED TODAY
    # =====================================================

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM progress p
            JOIN habits h
                ON p.habit_id = h.id
            WHERE h.user_id = %s
              AND p.completed_date = CURRENT_DATE
              AND p.completed = 1
        """, (user_id,))

        completed_today = cursor.fetchone()[0]

    except Exception as e:

        st.error(
            f"Unable to load today's progress: {e}"
        )
        return

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


    # =====================================================
    # CALCULATIONS
    # =====================================================

    total_habits = len(habits)

    pending_today = max(
        total_habits - completed_today,
        0
    )

    if total_habits > 0:

        progress_percent = round(
            (completed_today / total_habits) * 100,
            1
        )

    else:

        progress_percent = 0


    # =====================================================
    # STAT CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-content">

                <div class="stat-icon">
                    📋
                </div>

                <div>

                    <div class="stat-label">
                        Total Habits
                    </div>

                    <div class="stat-value">
                        {total_habits}
                    </div>

                </div>

            </div>

        </div>
        """)


    with col2:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-content">

                <div class="stat-icon">
                    ✓
                </div>

                <div>

                    <div class="stat-label">
                        Completed Today
                    </div>

                    <div class="stat-value green">
                        {completed_today}
                    </div>

                </div>

            </div>

        </div>
        """)


    with col3:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-content">

                <div class="stat-icon">
                    ⏳
                </div>

                <div>

                    <div class="stat-label">
                        Pending
                    </div>

                    <div class="stat-value orange">
                        {pending_today}
                    </div>

                </div>

            </div>

        </div>
        """)


    with col4:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-content">

                <div class="stat-icon">
                    🎯
                </div>

                <div>

                    <div class="stat-label">
                        Today's Progress
                    </div>

                    <div class="stat-value purple">
                        {progress_percent}%
                    </div>

                </div>

            </div>

        </div>
        """)


    # =====================================================
    # DAILY PROGRESS
    # =====================================================

    st.html(f"""
    <div class="section-card">

        <div class="section-title">
            🎯 Daily Progress
        </div>

        <div class="progress-text">

            <span class="progress-number">
                {completed_today}
            </span>

            of {total_habits}
            habits completed today

        </div>

        <div class="custom-progress">

            <div
                class="custom-progress-fill"
                style="width:{progress_percent}%;">
            </div>

        </div>

        <div class="progress-percent">
            {progress_percent}%
        </div>

    </div>
    """)


    # =====================================================
    # TWO COLUMNS
    # =====================================================

    left_col, right_col = st.columns(
        [0.9, 1.4],
        gap="medium"
    )


    # =====================================================
    # TODAY'S COMPLETION
    # =====================================================

    with left_col:

        st.html("""
        <div class="section-card">

            <div class="section-title">
                📈 Today's Completion
            </div>

        </div>
        """)


        if total_habits == 0:

            st.info(
                "No habits added yet."
            )

        else:

            fig, ax = plt.subplots(
                figsize=(3.4, 2.5)
            )

            values = [
                completed_today,
                pending_today
            ]

            if completed_today == 0:

                values = [
                    0.0001,
                    pending_today
                ]

            elif pending_today == 0:

                values = [
                    completed_today,
                    0.0001
                ]


            ax.pie(
                values,
                startangle=90,
                counterclock=False,
                colors=[
                    "#4ade80",
                    "#ff9418"
                ],
                wedgeprops={
                    "width": 0.32,
                    "edgecolor": "#080918"
                }
            )

            ax.text(
                0,
                0,
                f"{progress_percent:.0f}%",
                ha="center",
                va="center",
                fontsize=19,
                fontweight="bold",
                color="white"
            )

            ax.axis("equal")

            fig.patch.set_alpha(0)

            st.pyplot(
                fig,
                use_container_width=False
            )

            plt.close(fig)


            # =================================================
            # FIXED: NO RAW HTML
            # =================================================

            st.html(f"""
            <div style="
                text-align:center;
                color:#aaa7d5;
                font-size:14px;
                margin-top:-5px;
            ">

                🟠 Pending:
                <span style="
                    color:#ff9418;
                    font-weight:700;
                ">
                    {pending_today}
                </span>

                <span style="
                    display:inline-block;
                    width:20px;
                "></span>

                🟢 Completed:
                <span style="
                    color:#4ade80;
                    font-weight:700;
                ">
                    {completed_today}
                </span>

            </div>

            <div style="
                text-align:center;
                color:#aaa7d5;
                margin-top:18px;
                font-size:14px;
            ">

                💪 Keep going!
                Every small step counts.

            </div>
            """)


    # =====================================================
    # HABIT PERFORMANCE
    # =====================================================

    with right_col:

        st.html("""
        <div class="section-card">

            <div class="section-title">
                📝 Habit Performance
            </div>

        </div>
        """)


        if not habits:

            st.info(
                "No habits found."
            )

        else:

            for habit_id, habit_name, category in habits:

                try:

                    consistency = get_recent_consistency(
                        habit_id
                    )

                    history = get_last_five_days(
                        habit_id
                    )

                except Exception:

                    consistency = 0
                    history = []


                symbols = [
                    symbol
                    for _, symbol in history
                ]


                while len(symbols) < 5:

                    symbols.insert(
                        0,
                        "❌"
                    )


                symbols = symbols[-5:]


                icons = {
                    "Study": "📖",
                    "Education": "📖",
                    "Health": "💧",
                    "Fitness": "🏃",
                    "Personal": "📋",
                    "Other": "📋"
                }


                icon = icons.get(
                    category,
                    "📋"
                )


                history_html = ""


                for symbol in symbols:

                    if symbol == "✅":

                        history_html += """
                        <div class="
                            history-circle
                            completed-circle
                        ">
                            ✓
                        </div>
                        """

                    else:

                        history_html += """
                        <div class="
                            history-circle
                            missed-circle
                        ">
                            ×
                        </div>
                        """


                st.html(f"""
                <div class="habit-row">

                    <div class="habit-left">

                        <div class="habit-icon">
                            {icon}
                        </div>

                        <div class="habit-name">
                            {habit_name}
                        </div>

                    </div>


                    <div class="habit-history">

                        <div class="history-title">
                            Recent (Last 5 Days)
                        </div>

                        <div class="history">
                            {history_html}
                        </div>

                    </div>


                    <div class="consistency">

                        <div class="consistency-title">
                            Consistency
                        </div>

                        <div class="consistency-value">
                            {consistency}%
                        </div>

                    </div>

                </div>
                """)


    # =====================================================
    # AI PREDICTION
    # =====================================================

    st.html("""
    <div class="ai-box">

        <div class="ai-title">
            🤖 AI Habit Prediction
        </div>

        <div class="ai-description">
            Select a habit to predict the probability
            of completing it next.
        </div>

    </div>
    """)


    if habits:

        habit_options = {
            habit_name: habit_id
            for habit_id, habit_name, category
            in habits
        }


        select_col, button_col = st.columns(
            [2.5, 1]
        )


        with select_col:

            selected_habit = st.selectbox(
                "Select Habit",
                list(habit_options.keys()),
                label_visibility="collapsed"
            )


        with button_col:

            predict_button = st.button(
                "🔮 Predict"
            )


        if predict_button:

            selected_id = habit_options[
                selected_habit
            ]


            try:

                prediction, error = (
                    predict_habit_completion(
                        selected_id
                    )
                )


                if error:

                    st.warning(error)

                else:

                    st.html(f"""
                    <div class="prediction-result">

                        <div class="prediction-label">

                            Predicted completion
                            probability for
                            <b>{selected_habit}</b>

                        </div>

                        <div class="prediction-value">
                            {prediction}%
                        </div>

                    </div>
                    """)


            except Exception as e:

                st.error(
                    f"Prediction error: {e}"
                )


    # =====================================================
    # FOOTER
    # =====================================================

    st.html("""
    <div class="dashboard-footer">

        AI Smart Habit Tracker
        • Stay consistent, stay productive 💜

    </div>
    """)