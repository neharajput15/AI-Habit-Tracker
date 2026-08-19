import streamlit as st
import sqlite3

from database import create_tables
from login import register, login
from add_habit import add_habit
from view_habits import view_habits
from dashboard import dashboard
from daily_checkin import daily_checkin
from ai_helper import ai_assistant
from analytics import analytics
from streak import show_streaks
from mobile_home import mobile_home

from remember_login import (
    get_saved_user,
    clear_saved_user
)


# =====================================================
# DATABASE
# =====================================================

create_tables()


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="AI Smart Habit Tracker",
    page_icon="📱",
    layout="centered"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "name" not in st.session_state:
    st.session_state.name = ""

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# =====================================================
# AUTO LOGIN
# =====================================================

if not st.session_state.logged_in:

    saved_user_id = get_saved_user()

    if saved_user_id is not None:

        conn = sqlite3.connect(
            "habit_tracker.db"
        )

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT id, name
                FROM users
                WHERE id = ?
                """,
                (saved_user_id,)
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.name = user[1]
                st.session_state.page = "Home"

        except Exception:

            clear_saved_user()

        finally:

            conn.close()


# =====================================================
# THEME
# =====================================================

st.sidebar.markdown("## 🎨 Theme")

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)


# =====================================================
# DARK MODE
# =====================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #121212 !important;
            color: #ffffff !important;
        }

        .stApp p,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        .stApp label {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] {
            background-color: #181818 !important;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        input,
        textarea {
            background-color: #242424 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
        }

        .stButton > button {
            background-color: #242424 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
            border-radius: 12px !important;
        }

        .stButton > button:hover {
            background-color: #333333 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# LIGHT MODE
# =====================================================

else:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #ffffff !important;
            color: #222222 !important;
        }

        .stApp p,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        .stApp label {
            color: #222222 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #f5f5f5 !important;
        }

        [data-testid="stSidebar"] * {
            color: #222222 !important;
        }

        input,
        textarea {
            background-color: #ffffff !important;
            color: #222222 !important;
            border: 1px solid #cccccc !important;
        }

        .stButton > button {
            background-color: #ffffff !important;
            color: #222222 !important;
            border: 1px solid #cccccc !important;
            border-radius: 12px !important;
        }

        .stButton > button:hover {
            background-color: #eeeeee !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# NOT LOGGED IN
# =====================================================

if not st.session_state.logged_in:

    st.title("📱 AI Smart Habit Tracker")

    st.write(
        "Build better habits and improve your daily routine with AI. 🌱"
    )

    st.divider()

    option = st.radio(
        "Choose an option",
        ["🔐 Login", "📝 Register"],
        horizontal=True
    )

    if option == "🔐 Login":

        login()

    else:

        register()


# =====================================================
# LOGGED IN
# =====================================================

else:

    # =================================================
    # HOME
    # =================================================

    if st.session_state.page == "Home":

        mobile_home()

        st.divider()

        st.subheader(
            "What do you want to do? 🎯"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "➕ Add Habit",
                use_container_width=True
            ):

                st.session_state.page = "Add Habit"
                st.rerun()

        with col2:

            if st.button(
                "📋 My Habits",
                use_container_width=True
            ):

                st.session_state.page = "My Habits"
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📊 Progress",
                use_container_width=True
            ):

                st.session_state.page = "Progress"
                st.rerun()

        with col2:

            if st.button(
                "🤖 AI Coach",
                use_container_width=True
            ):

                st.session_state.page = "AI"
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🔥 Streaks",
                use_container_width=True
            ):

                st.session_state.page = "Streaks"
                st.rerun()

        with col2:

            if st.button(
                "📅 Daily Check-in",
                use_container_width=True
            ):

                st.session_state.page = "Check-in"
                st.rerun()

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            clear_saved_user()

            st.session_state.clear()

            st.rerun()


    # =================================================
    # ADD HABIT
    # =================================================

    elif st.session_state.page == "Add Habit":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        add_habit()


    # =================================================
    # MY HABITS
    # =================================================

    elif st.session_state.page == "My Habits":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        view_habits()


    # =================================================
    # PROGRESS
    # =================================================

    elif st.session_state.page == "Progress":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        dashboard()

        st.divider()

        analytics()


    # =================================================
    # AI COACH
    # =================================================

    elif st.session_state.page == "AI":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        ai_assistant()


    # =================================================
    # STREAKS
    # =================================================

    elif st.session_state.page == "Streaks":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        show_streaks()


    # =================================================
    # DAILY CHECK-IN
    # =================================================

    elif st.session_state.page == "Check-in":

        if st.button("⬅️ Back to Home"):

            st.session_state.page = "Home"
            st.rerun()

        daily_checkin()