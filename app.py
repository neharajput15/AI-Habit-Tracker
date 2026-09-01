import streamlit as st

from database import create_tables

from login import register, login
from add_habit import add_habit
from view_habits import view_habits
from dashboard import dashboard
from daily_checkin import daily_checkin
from ai_helper import ai_assistant
from streak import show_streaks
from mobile_home import mobile_home
from analytics import analytics

from remember_login import (
    get_saved_user,
    clear_saved_user
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Smart Habit Tracker",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# PURPLE + BLACK THEME
# SAME IN BOTH MODES
# =====================================================

st.markdown(
    """
    <style>

    /* ===============================
       MAIN BACKGROUND
    =============================== */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                #24104a 0%,
                #10091f 35%,
                #08060d 75%
            ) !important;

        color: #ffffff !important;
    }


    /* ===============================
       MAIN CONTENT
    =============================== */

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ===============================
       ALL TEXT
    =============================== */

    h1, h2, h3, h4, h5, h6,
    p, span, label, div {
        color: #ffffff;
    }


    /* ===============================
       SIDEBAR
    =============================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0d0915 0%,
                #130b22 100%
            ) !important;

        border-right: 1px solid #30204d;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }


    /* ===============================
       BUTTONS
    =============================== */

    .stButton > button {
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #a855f7
            ) !important;

        color: white !important;

        border: none !important;

        border-radius: 12px !important;

        padding: 0.65rem 1rem !important;

        font-weight: 600 !important;

        transition: 0.2s;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #9333ea,
                #c084fc
            ) !important;

        transform: translateY(-1px);
    }


    /* ===============================
       INPUTS
    =============================== */

    input,
    textarea,
    [data-baseweb="select"] > div {
        background-color: #17121f !important;

        color: white !important;

        border: 1px solid #493568 !important;

        border-radius: 10px !important;
    }


    /* ===============================
       CARDS
    =============================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #171020,
                #21132f
            );

        border: 1px solid #493568;

        border-radius: 16px;

        padding: 18px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.35);
    }


    /* ===============================
       CONTAINERS
    =============================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                #120d1a,
                #1d1129
            ) !important;

        border: 1px solid #493568 !important;

        border-radius: 16px !important;
    }


    /* ===============================
       EXPANDER
    =============================== */

    [data-testid="stExpander"] {
        background: #120d1a !important;

        border: 1px solid #493568 !important;

        border-radius: 14px !important;
    }


    /* ===============================
       PROGRESS BAR
    =============================== */

    [data-testid="stProgress"] > div {
        background-color: #281b38 !important;

        border-radius: 20px;
    }

    [data-testid="stProgress"] > div > div {
        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #c084fc
            ) !important;

        border-radius: 20px;
    }


    /* ===============================
       DIVIDER
    =============================== */

    hr {
        border-color: #332044 !important;
    }


    /* ===============================
       DATAFRAME
    =============================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #493568;
        border-radius: 12px;
        overflow: hidden;
    }


    /* ===============================
       SUCCESS
    =============================== */

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }


    /* ===============================
       TITLE
    =============================== */

    .app-title {
        font-size: 38px;
        font-weight: 800;

        background:
            linear-gradient(
                90deg,
                #c084fc,
                #8b5cf6
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* ===============================
       SMALL TEXT
    =============================== */

    .subtitle {
        color: #aaa0b8 !important;
        font-size: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# DATABASE
# =====================================================

create_tables()


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


# =====================================================
# AUTO LOGIN
# =====================================================

if not st.session_state.logged_in:

    saved_user_id = get_saved_user()

    if saved_user_id is not None:

        conn = None
        cursor = None

        try:

            from database import get_connection

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name
                FROM users
                WHERE id = %s
                """,
                (saved_user_id,)
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.name = user[1]
                st.session_state.page = "Home"

            else:

                clear_saved_user()

        except Exception:

            clear_saved_user()

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


# =====================================================
# LOGIN / REGISTER
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="app-title">💜 AI Smart Habit Tracker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Build better habits. Track your progress. Stay consistent.</div>',
        unsafe_allow_html=True
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

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="app-title">💜 Habit Tracker</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"Welcome, {st.session_state.name} 👋"
    )

    st.divider()

    if st.button("🏠 Home"):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("➕ Add Habit"):
        st.session_state.page = "Add Habit"
        st.rerun()

    if st.button("📋 My Habits"):
        st.session_state.page = "My Habits"
        st.rerun()

    if st.button("📅 Daily Check-in"):
        st.session_state.page = "Check-in"
        st.rerun()

    if st.button("📊 Dashboard"):
        st.session_state.page = "Progress"
        st.rerun()

    if st.button("🤖 AI Coach"):
        st.session_state.page = "AI"
        st.rerun()

    if st.button("🔥 Streaks"):
        st.session_state.page = "Streaks"
        st.rerun()

    st.divider()

    if st.button("🚪 Logout"):

        clear_saved_user()

        st.session_state.clear()

        st.rerun()


# =====================================================
# HOME
# =====================================================

if st.session_state.page == "Home":

    mobile_home()

    st.divider()

    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("➕ Add Habit"):
            st.session_state.page = "Add Habit"
            st.rerun()

    with col2:

        if st.button("📅 Check-in"):
            st.session_state.page = "Check-in"
            st.rerun()

    with col3:

        if st.button("📊 Dashboard"):
            st.session_state.page = "Progress"
            st.rerun()


# =====================================================
# ADD HABIT
# =====================================================

elif st.session_state.page == "Add Habit":

    add_habit()


# =====================================================
# MY HABITS
# =====================================================

elif st.session_state.page == "My Habits":

    view_habits()


# =====================================================
# DASHBOARD
# =====================================================

elif st.session_state.page == "Progress":

    dashboard()

    st.divider()

    analytics()


# =====================================================
# AI
# =====================================================

elif st.session_state.page == "AI":

    ai_assistant()


# =====================================================
# STREAKS
# =====================================================

elif st.session_state.page == "Streaks":

    show_streaks()


# =====================================================
# CHECK-IN
# =====================================================

elif st.session_state.page == "Check-in":

    daily_checkin()