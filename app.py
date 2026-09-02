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
    page_icon="🌱",
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
    st.session_state.dark_mode = False


# ============================================================
# THEME COLORS
# ============================================================

if st.session_state.dark_mode:

    # -------------------------
    # DARK MODE
    # -------------------------

    background = "#071817"
    card_background = "#102321"
    text_color = "#FFFFFF"
    secondary_text = "#A8C7C3"
    border_color = "#28504B"
    sidebar_background = "#0B1E1C"

    button_color = "#1FA39A"
    button_hover = "#178B83"

else:

    # -------------------------
    # LIGHT MODE
    # -------------------------

    background = "#F6FBFA"
    card_background = "#FFFFFF"
    text_color = "#202827"
    secondary_text = "#687875"
    border_color = "#D8E9E6"
    sidebar_background = "#EEF7F5"

    button_color = "#1FA39A"
    button_hover = "#178B83"


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
        background-color: {background};
        color: {text_color};
    }}

    .main {{
        background-color: {background};
    }}

    .block-container {{
        padding-top: 30px;
        padding-bottom: 40px;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {{
        background-color: {sidebar_background};
        border-right: 1px solid {border_color};
    }}

    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {{
        color: {text_color} !important;
    }}

    p {{
        color: {text_color};
    }}


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {{
        background-color: {button_color} !important;
        color: #FFFFFF !important;

        border: none !important;
        border-radius: 10px !important;

        font-weight: 600 !important;

        min-height: 40px !important;

        transition: 0.2s ease;
    }}

    .stButton > button:hover {{
        background-color: {button_hover} !important;
        color: #FFFFFF !important;
    }}


    /* ======================================================
       INPUT BOXES
       ====================================================== */

    input,
    textarea {{
        background-color: {card_background} !important;
        color: {text_color} !important;

        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: {secondary_text} !important;
    }}


    /* ======================================================
       SELECT BOX
       ====================================================== */

    div[data-baseweb="select"] > div {{
        background-color: {card_background} !important;
        color: {text_color} !important;

        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
    }}


    /* ======================================================
       SELECT BOX TEXT
       ====================================================== */

    div[data-baseweb="select"] span {{
        color: {text_color} !important;
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
        font-weight: 600 !important;
    }}


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="stMetric"] {{
        background-color: {card_background};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 15px;
    }}


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {{
        background-color: {card_background};
        border: 1px solid {border_color};
        border-radius: 14px;
    }}


    /* ======================================================
       ALERT BOXES
       ====================================================== */

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}


    /* ======================================================
       PROGRESS BAR
       ====================================================== */

    div[data-testid="stProgressBar"] > div > div {{
        background-color: {button_color};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    st.title("🌱 AI Smart Habit Tracker")

    st.write(
        "Build better habits. Track your progress. "
        "Become consistent."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
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

    st.title("🌱 Habit Tracker")

    st.write(
        f"Welcome, {st.session_state.name} 👋"
    )

    st.divider()


    # ========================================================
    # THEME
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


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    mobile_home()


# ============================================================
# ADD HABIT
# ============================================================

elif st.session_state.page == "Add Habit":

    st.header("➕ Add Habit")

    add_habit()


# ============================================================
# MY HABITS
# ============================================================

elif st.session_state.page == "My Habits":

    st.header("📝 My Habits")

    view_habits()


# ============================================================
# PROGRESS
# ============================================================

elif st.session_state.page == "Progress":

    st.header("📊 Progress")

    dashboard()


# ============================================================
# DAILY CHECK-IN
# ============================================================

elif st.session_state.page == "Daily Check-in":

    st.header("✅ Daily Check-in")

    daily_checkin()


# ============================================================
# AI ASSISTANT
# ============================================================

elif st.session_state.page == "AI Assistant":

    st.header("🤖 AI Assistant")

    ai_assistant()


# ============================================================
# STREAKS
# ============================================================

elif st.session_state.page == "Streaks":

    st.header("🔥 Streaks")

    show_streaks()