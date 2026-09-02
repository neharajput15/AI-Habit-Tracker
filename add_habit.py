import streamlit as st

from database import get_connection


def add_habit():

    # =====================================================
    # CSS
    # =====================================================

    st.markdown("""
    <style>

    .page-header {
        text-align: center;
        padding: 20px 10px 30px 10px;
    }

    .page-icon {
        font-size: 42px;
    }

    .page-title {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .page-subtitle {
        color: #aaa2b9;
        font-size: 14px;
        margin-top: 8px;
    }

    .form-card {
        background: #111117;
        border: 1px solid #302b3b;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 25px;
    }

    .form-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 20px;
    }

    .info-card {
        background: #18111f;
        border: 1px solid #49315e;
        border-radius: 14px;
        padding: 18px;
        color: #c9bdd8;
        font-size: 13px;
        margin-top: 15px;
    }

    div.stButton > button {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #9333ea
        );
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            90deg,
            #9333ea,
            #a855f7
        );
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # LOGIN CHECK
    # =====================================================

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first.")
        return


    # =====================================================
    # HEADER
    # =====================================================

    st.html("""
    <div class="page-header">

        <div class="page-icon">
            ➕
        </div>

        <div class="page-title">
            Add New Habit
        </div>

        <div class="page-subtitle">
            Create a habit and start building your routine.
        </div>

    </div>
    """)


    # =====================================================
    # FORM
    # =====================================================

    st.html("""
    <div class="form-card">

        <div class="form-title">
            ✨ Habit Details
        </div>

    </div>
    """)


    habit_name = st.text_input(
        "Habit Name",
        placeholder="Example: Study Java"
    )

    category = st.selectbox(
        "Category",
        [
            "Study",
            "Health",
            "Fitness",
            "Personal",
            "Work",
            "Other"
        ]
    )

    target = st.text_input(
        "Target / Goal",
        placeholder="Example: 2 hours"
    )

    frequency = st.selectbox(
        "Frequency",
        [
            "Daily",
            "Weekly",
            "Weekdays",
            "Weekends"
        ]
    )


    st.html("""
    <div class="info-card">
        💡 <b>Tip:</b> Start with a simple and realistic
        target. Small habits are easier to maintain.
    </div>
    """)


    st.write("")


    # =====================================================
    # ADD BUTTON
    # =====================================================

    if st.button(
        "➕ Add Habit",
        use_container_width=True
    ):

        if not habit_name.strip():

            st.error(
                "Please enter a habit name."
            )

            return


        if not target.strip():

            st.error(
                "Please enter a target."
            )

            return


        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO habits
                (
                    user_id,
                    habit_name,
                    category,
                    target,
                    frequency,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    habit_name.strip(),
                    category,
                    target.strip(),
                    frequency,
                    "Pending"
                )
            )

            conn.commit()

            st.success(
                f"🎉 '{habit_name}' added successfully!"
            )

            st.rerun()

        except Exception as e:

            conn.rollback()

            st.error(
                f"Unable to add habit: {e}"
            )

        finally:

            cursor.close()
            conn.close()