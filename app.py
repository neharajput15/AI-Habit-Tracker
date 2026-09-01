import streamlit as st

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="AI Smart Habit Tracker",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# IMPORTS
# =====================================================

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
    st.session_state.dark_mode = True


# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown(
    """
    <style>

    /* ===============================================
       MAIN APP
    =============================================== */

    .stApp {
        background: #08060b;
        color: white;
    }

    .block-container {
        padding-top: 25px;
        padding-bottom: 40px;
    }


    /* ===============================================
       SIDEBAR
    =============================================== */

    section[data-testid="stSidebar"] {
        background: #0e0a12;
        border-right: 1px solid #2d193b;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }


    /* ===============================================
       SIDEBAR BUTTONS
    =============================================== */

    section[data-testid="stSidebar"] .stButton > button {

        background: #17101f !important;

        color: #ffffff !important;

        border: 1px solid #392047 !important;

        border-radius: 12px !important;

        text-align: left !important;

        min-height: 42px !important;

        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {

        background: #35164c !important;

        border: 1px solid #7438a0 !important;

    }


    /* ===============================================
       GENERAL BUTTON
    =============================================== */

    .stButton > button {

        background: linear-gradient(
            135deg,
            #60259a,
            #833bc3
        ) !important;

        color: white !important;

        border: 1px solid #8e51cf !important;

        border-radius: 12px !important;

        font-weight: 700 !important;

        min-height: 44px !important;
    }

    .stButton > button:hover {

        background: linear-gradient(
            135deg,
            #7130ad,
            #984cdd
        ) !important;

        color: white !important;
    }


    /* ===============================================
       INPUTS
    =============================================== */

    input,
    textarea {

        background-color: #17101f !important;

        color: white !important;

        border: 1px solid #432653 !important;

        border-radius: 10px !important;
    }


    /* ===============================================
       SELECTBOX
    =============================================== */

    div[data-baseweb="select"] > div {

        background-color: #17101f !important;

        color: white !important;

        border: 1px solid #432653 !important;

        border-radius: 10px !important;
    }


    /* ===============================================
       CHECKBOX
    =============================================== */

    label {
        color: #ffffff !important;
    }


    /* ===============================================
       DIVIDER
    =============================================== */

    hr {
        border-color: #34203f !important;
    }


    /* ===============================================
       METRIC
    =============================================== */

    [data-testid="stMetric"] {

        background: #17101f;

        border: 1px solid #432653;

        padding: 15px;

        border-radius: 15px;
    }


    /* ===============================================
       MOBILE
    =============================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 15px;
            padding-right: 15px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# AUTO LOGIN
# =====================================================

saved_user = get_saved_user()

if (
    not st.session_state.logged_in
    and saved_user is not None
):

    try:

        conn = None

        from database import get_connection

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name
            FROM users
            WHERE id = %s
            """,
            (saved_user,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.name = user[1]

    except Exception:

        clear_saved_user()


# =====================================================
# LOGIN / REGISTER
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:50px 20px 30px 20px;
        ">

            <div style="
                font-size:60px;
            ">
                💜
            </div>

            <div style="
                color:white;
                font-size:40px;
                font-weight:900;
            ">
                AI Smart Habit Tracker
            </div>

            <div style="
                color:#b9a9c7;
                font-size:15px;
                margin-top:8px;
            ">
                Build better habits. Track your progress.
                Become consistent.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )


    with login_tab:

        login()


    with register_tab:

        register()


# =====================================================
# LOGGED IN APPLICATION
# =====================================================

else:

    # =================================================
    # SIDEBAR
    # =================================================

    with st.sidebar:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:15px 5px 20px 5px;
            ">

                <div style="
                    font-size:40px;
                ">
                    💜
                </div>

                <div style="
                    color:white;
                    font-size:20px;
                    font-weight:800;
                ">
                    AI Habit Tracker
                </div>

                <div style="
                    color:#9f8cab;
                    font-size:12px;
                ">
                    Build better habits
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.divider()


        # =============================================
        # USER
        # =============================================

        st.markdown(
            f"""
            <div style="
                background:#17101f;
                border:1px solid #392047;
                border-radius:14px;
                padding:12px;
                margin-bottom:15px;
            ">

                <div style="
                    color:#9f8cab;
                    font-size:11px;
                ">
                    LOGGED IN AS
                </div>

                <div style="
                    color:white;
                    font-size:15px;
                    font-weight:700;
                    margin-top:4px;
                ">
                    {st.session_state.name}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # =============================================
        # NAVIGATION
        # =============================================

        st.markdown(
            """
            <div style="
                color:#9f8cab;
                font-size:11px;
                font-weight:700;
                margin-bottom:8px;
            ">
                MENU
            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "🏠  Home",
            use_container_width=True
        ):

            st.session_state.page = "Home"
            st.rerun()


        if st.button(
            "➕  Add Habit",
            use_container_width=True
        ):

            st.session_state.page = "Add Habit"
            st.rerun()


        if st.button(
            "📋  My Habits",
            use_container_width=True
        ):

            st.session_state.page = "My Habits"
            st.rerun()


        if st.button(
            "📊  Progress",
            use_container_width=True
        ):

            st.session_state.page = "Progress"
            st.rerun()


        if st.button(
            "🤖  AI Assistant",
            use_container_width=True
        ):

            st.session_state.page = "AI Assistant"
            st.rerun()


        if st.button(
            "🔥  Streaks",
            use_container_width=True
        ):

            st.session_state.page = "Streaks"
            st.rerun()


        if st.button(
            "✅  Daily Check-in",
            use_container_width=True
        ):

            st.session_state.page = "Daily Check-in"
            st.rerun()


        st.divider()


        # =============================================
        # LOGOUT
        # =============================================

        if st.button(
            "🚪  Logout",
            use_container_width=True
        ):

            clear_saved_user()

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.name = ""
            st.session_state.page = "Home"

            st.rerun()


    # =================================================
    # PAGE ROUTING
    # =================================================

    if st.session_state.page == "Home":

        mobile_home()


    elif st.session_state.page == "Add Habit":

        add_habit()


    elif st.session_state.page == "My Habits":

        view_habits()


    elif st.session_state.page == "Progress":

        dashboard()


    elif st.session_state.page == "AI Assistant":

        ai_assistant()


    elif st.session_state.page == "Streaks":

        show_streaks()


    elif st.session_state.page == "Daily Check-in":

        daily_checkin()