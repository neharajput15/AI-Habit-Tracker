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

from remember_login import (
    get_saved_user,
    clear_saved_user
)


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
    st.session_state.dark_mode = False


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
# GLOBAL PURPLE / BLACK THEME
# =====================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(115, 50, 180, 0.18),
                transparent 35%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(80, 30, 130, 0.15),
                transparent 35%
            ),
            #0d0813;
    }


    /* Sidebar */

    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #10091a,
                #170d24
            );

        border-right:
            1px solid #38234b;
    }


    [data-testid="stSidebar"] * {
        color: #eee5f7 !important;
    }


    /* Normal text */

    .stApp p,
    .stApp label {
        color: #e8dff0;
    }


    /* Buttons */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #7135c9,
                #955be8
            ) !important;

        color: white !important;

        border: none !important;

        border-radius: 13px !important;

        font-weight: 700 !important;

        min-height: 45px;
    }


    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #8246dd,
                #a66df5
            ) !important;

        color: white !important;
    }


    /* Select box */

    div[data-baseweb="select"] > div {

        background-color: #181020 !important;

        color: white !important;

        border: 1px solid #51356d !important;

        border-radius: 12px !important;
    }


    /* Progress */

    .stProgress > div > div > div > div {

        background:
            linear-gradient(
                90deg,
                #7135c9,
                #ad7aff
            ) !important;
    }


    /* Hide Streamlit menu */

    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR
# =====================================================

if st.session_state.logged_in:

    with st.sidebar:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:15px 5px 25px 5px;
            ">

                <div style="
                    font-size:38px;
                ">
                    💜
                </div>

                <div style="
                    font-size:20px;
                    font-weight:800;
                    color:white;
                ">
                    AI Habit Tracker
                </div>

                <div style="
                    font-size:12px;
                    color:#a994bd;
                ">
                    Build better habits
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown("---")


        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

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
            "📊  Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "Progress"
            st.rerun()


        if st.button(
            "🤖  AI Coach",
            use_container_width=True
        ):

            st.session_state.page = "AI"
            st.rerun()


        if st.button(
            "🔥  Streaks",
            use_container_width=True
        ):

            st.session_state.page = "Streaks"
            st.rerun()


        if st.button(
            "📅  Daily Check-in",
            use_container_width=True
        ):

            st.session_state.page = "Check-in"
            st.rerun()


        st.markdown("---")


        # -------------------------------------------------
        # USER
        # -------------------------------------------------

        st.markdown(
            f"""
            <div style="
                background:#1b1027;
                border:1px solid #3e2753;
                border-radius:15px;
                padding:14px;
                margin-bottom:15px;
            ">

                <div style="
                    font-size:12px;
                    color:#a995ba;
                ">
                    LOGGED IN AS
                </div>

                <div style="
                    font-size:16px;
                    font-weight:700;
                    color:white;
                    margin-top:4px;
                ">
                    👤 {st.session_state.name}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # DARK MODE
        # -------------------------------------------------

        st.session_state.dark_mode = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.dark_mode
        )


        # -------------------------------------------------
        # LOGOUT
        # -------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            clear_saved_user()

            st.session_state.clear()

            st.rerun()


# =====================================================
# NOT LOGGED IN
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="
            max-width:700px;
            margin:80px auto 0 auto;
            text-align:center;
        ">

            <div style="
                font-size:60px;
            ">
                💜
            </div>

            <h1 style="
                color:white;
                font-size:42px;
                font-weight:900;
            ">
                AI Smart Habit Tracker
            </h1>

            <p style="
                color:#b9a9c7;
                font-size:16px;
            ">
                Build better habits.
                Track your progress.
                Become consistent.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    option = st.radio(
        "Choose an option",
        [
            "🔐 Login",
            "📝 Register"
        ],
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

        st.markdown("---")

        st.subheader(
            "Quick Actions"
        )

        col1, col2, col3 = st.columns(3)


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


        with col3:

            if st.button(
                "📊 Dashboard",
                use_container_width=True
            ):

                st.session_state.page = "Progress"
                st.rerun()


    # =================================================
    # ADD HABIT
    # =================================================

    elif st.session_state.page == "Add Habit":

        add_habit()


    # =================================================
    # MY HABITS
    # =================================================

    elif st.session_state.page == "My Habits":

        view_habits()


    # =================================================
    # DASHBOARD
    # =================================================

    elif st.session_state.page == "Progress":

        dashboard()


    # =================================================
    # AI COACH
    # =================================================

    elif st.session_state.page == "AI":

        ai_assistant()


    # =================================================
    # STREAKS
    # =================================================

    elif st.session_state.page == "Streaks":

        show_streaks()


    # =================================================
    # DAILY CHECK-IN
    # =================================================

    elif st.session_state.page == "Check-in":

        daily_checkin()