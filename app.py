import streamlit as st

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="AI Smart Habit Tracker",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database import create_tables
from login import register, login
from add_habit import add_habit
from view_habits import view_habits
from dashboard import dashboard
from daily_checkin import daily_checkin
from ai_helper import ai_assistant
from analytics import analytics
from streak import show_streaks
from remember_login import get_saved_user, clear_saved_user


# =====================================================
# DATABASE
# =====================================================

try:
    create_tables()
except Exception as e:
    st.error("Database connection failed.")
    st.caption(str(e))
    st.stop()


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "logged_in": False,
    "user_id": None,
    "name": "",
    "page": "Home",
    "dark_mode": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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
                "SELECT id, name FROM users WHERE id = %s",
                (saved_user_id,),
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
# THEME
# =====================================================

st.sidebar.markdown("## 🎨 Theme")

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode,
)


if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp { background:#121016 !important; }
        [data-testid="stSidebar"] { background:#18151d !important; }
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp h5, .stApp h6, .stApp label { color:#f4f0f7 !important; }
        .stat-card, .habit-card, .message-card {
            background:#211b2c !important;
            border-color:#3b304d !important;
        }
        .stat-value, .habit-name { color:#f4f0f7 !important; }
        .progress-card, .prediction-card {
            background:#251e31 !important;
            border-color:#4a3b60 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# LOGGED OUT
# =====================================================

if not st.session_state.logged_in:
    st.markdown(
        """
        <div style="
            background:linear-gradient(135deg,#6d42d8,#9b6cff);
            padding:30px;
            border-radius:26px;
            color:white;
            margin-bottom:20px;">
            <h1 style="color:white;margin:0;">📱 AI Smart Habit Tracker</h1>
            <p style="color:white;margin:6px 0 0;">
                Build better habits and improve your daily routine with AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    option = st.radio(
        "Choose an option",
        ["🔐 Login", "📝 Register"],
        horizontal=True,
    )

    if option == "🔐 Login":
        login()
    else:
        register()

    st.stop()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown(f"### 👋 Hi, {st.session_state.name}")

pages = {
    "🏠 Home": "Home",
    "➕ Add Habit": "Add Habit",
    "📋 My Habits": "My Habits",
    "📅 Daily Check-in": "Check-in",
    "📊 Analytics": "Analytics",
    "🔥 Streaks": "Streaks",
    "🤖 AI Coach": "AI",
}

current_label = next(
    (label for label, page in pages.items() if page == st.session_state.page),
    "🏠 Home",
)

selected_label = st.sidebar.radio(
    "Navigation",
    list(pages.keys()),
    index=list(pages.keys()).index(current_label),
)

new_page = pages[selected_label]

if new_page != st.session_state.page:
    st.session_state.page = new_page
    st.rerun()


st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    clear_saved_user()
    st.session_state.clear()
    st.rerun()


# =====================================================
# PAGES
# =====================================================

if st.session_state.page == "Home":
    dashboard()

elif st.session_state.page == "Add Habit":
    st.title("➕ Add Habit")
    add_habit()

elif st.session_state.page == "My Habits":
    st.title("📋 My Habits")
    view_habits()

elif st.session_state.page == "Check-in":
    st.title("📅 Daily Check-in")
    daily_checkin()

elif st.session_state.page == "Analytics":
    analytics()

elif st.session_state.page == "Streaks":
    show_streaks()

elif st.session_state.page == "AI":
    ai_assistant()
