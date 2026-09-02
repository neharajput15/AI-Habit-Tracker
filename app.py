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
from theme import apply_theme


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

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

apply_theme()
# ============================================================
# THEME COLORS
# ============================================================

if st.session_state.dark_mode:

    # DARK MODE
    background = "#080918"
    card_background = "#121326"
    text_color = "#FFFFFF"
    secondary_text = "#AAA7D5"
    border_color = "#34265B"
    sidebar_background = "#0D0E1D"

    button_color = "#7025C5"
    button_hover = "#8438DC"

else:

    # LIGHT MODE
    background = "#FAF9FC"
    card_background = "#FFFFFF"
    text_color = "#25212B"
    secondary_text = "#716A7A"
    border_color = "#E8E1F0"
    sidebar_background = "#F3F0F6"

    button_color = "#7C4D9E"
    button_hover = "#6B408A"


# ============================================================
# GLOBAL THEME CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       MAIN APP
       ====================================================== */

    .stApp {{
        background: {background};
        color: {text_color};
    }}

    .main {{
        background: {background};
    }}

    .block-container {{
        padding-top: 30px;
        padding-bottom: 40px;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {{
        background: {sidebar_background};
        border-right: 1px solid {border_color};
    }}

    [data-testid="stSidebar"] * {{
        color: {text_color};
    }}


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
    }}

    p {{
        color: {text_color};
    }}


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {{
        background: {button_color} !important;
        color: #FFFFFF !important;

        border: none !important;
        border-radius: 8px !important;

        font-weight: 600 !important;

        min-height: 38px !important;

        transition: 0.2s ease;
    }}

    .stButton > button:hover {{
        background: {button_hover} !important;
        color: #FFFFFF !important;
    }}


    /* ======================================================
       INPUT BOXES
       ====================================================== */

    input,
    textarea {{
        background: {card_background} !important;
        color: {text_color} !important;

        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: {secondary_text} !important;
    }}


    /* ======================================================
       SELECT BOX
       ====================================================== */

    div[data-baseweb="select"] > div {{
        background: {card_background} !important;
        color: {text_color} !important;

        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {{
        color: {secondary_text} !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {button_color} !important;
    }}


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {{
        border-color: {border_color} !important;
    }}


    /* ======================================================
       CHECKBOX
       ====================================================== */

    [data-testid="stCheckbox"] label {{
        color: {text_color} !important;
    }}


    /* ======================================================
       RADIO
       ====================================================== */

    [data-testid="stRadio"] label {{
        color: {text_color} !important;
    }}


    /* ======================================================
       TOGGLE
       ====================================================== */

    [data-testid="stToggle"] label {{
        color: {text_color} !important;
        font-weight: 600;
    }}


    /* ======================================================
       SUCCESS / WARNING / ERROR
       ====================================================== */

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}


    </style>
    """,
    unsafe_allow_html=True
)


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


    # ========================================================
    # LIGHT / DARK MODE
    # ========================================================

    if st.session_state.dark_mode:

        theme_text = "🌙 Dark Mode"

    else:

        theme_text = "☀️ Light Mode"


    theme_changed = st.toggle(
        theme_text,
        value=st.session_state.dark_mode
    )


    if theme_changed != st.session_state.dark_mode:

        st.session_state.dark_mode = theme_changed

        st.rerun()


    st.divider()


    # ========================================================
    # NAVIGATION
    # ========================================================

    st.subheader("Navigation")


    if st.button(
        "🏠 Home",
        use_container_width=True
    ):

        st.session_state.page = "Home"
        st.rerun()


    if st.button(
        "➕ Add Habit",
        use_container_width=True
    ):

        st.session_state.page = "Add Habit"
        st.rerun()


    if st.button(
        "📝 My Habits",
        use_container_width=True
    ):

        st.session_state.page = "My Habits"
        st.rerun()


    if st.button(
        "📊 Progress",
        use_container_width=True
    ):

        st.session_state.page = "Progress"
        st.rerun()


    if st.button(
        "✅ Daily Check-in",
        use_container_width=True
    ):

        st.session_state.page = "Daily Check-in"
        st.rerun()


    if st.button(
        "🤖 AI Assistant",
        use_container_width=True
    ):

        st.session_state.page = "AI Assistant"
        st.rerun()


    if st.button(
        "🔥 Streaks",
        use_container_width=True
    ):

        st.session_state.page = "Streaks"
        st.rerun()


    st.divider()


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

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
