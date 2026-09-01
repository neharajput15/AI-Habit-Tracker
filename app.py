import streamlit as st

from database import create_tables
from login import login
from register import register
from add_habit import add_habit
from view_habits import view_habits
from dashboard import dashboard
from daily_checkin import daily_checkin
from ai_helper import ai_assistant
from streak import show_streaks
from mobile_home import mobile_home


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Smart Habit Tracker",
    page_icon="💜",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

create_tables()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "name" not in st.session_state:
    st.session_state.name = ""

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    st.title("💜 AI Smart Habit Tracker")

    st.write(
        "Build better habits. Track your progress. "
        "Become consistent."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    with login_tab:
        login()

    with register_tab:
        register()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💜 Habit Tracker")

    st.write(
        f"Welcome, {st.session_state.name}"
    )

    st.divider()

    st.subheader("Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("➕ Add Habit", use_container_width=True):
        st.session_state.page = "Add Habit"
        st.rerun()

    if st.button("📝 My Habits", use_container_width=True):
        st.session_state.page = "My Habits"
        st.rerun()

    if st.button("📊 Progress", use_container_width=True):
        st.session_state.page = "Progress"
        st.rerun()

    if st.button("✅ Daily Check-in", use_container_width=True):
        st.session_state.page = "Daily Check-in"
        st.rerun()

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.session_state.page = "AI Assistant"
        st.rerun()

    if st.button("🔥 Streaks", use_container_width=True):
        st.session_state.page = "Streaks"
        st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.name = ""
        st.session_state.page = "Home"

        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Home":

    mobile_home()


elif st.session_state.page == "Add Habit":

    st.header("➕ Add Habit")
    add_habit()


elif st.session_state.page == "My Habits":

    st.header("📝 My Habits")
    view_habits()


elif st.session_state.page == "Progress":

    st.header("📊 Progress")
    dashboard()


elif st.session_state.page == "Daily Check-in":

    st.header("✅ Daily Check-in")
    daily_checkin()


elif st.session_state.page == "AI Assistant":

    st.header("🤖 AI Assistant")
    ai_assistant()


elif st.session_state.page == "Streaks":

    st.header("🔥 Streaks")
    show_streaks()