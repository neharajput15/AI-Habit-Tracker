import streamlit as st
import sqlite3

from remember_login import save_user


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect("habit_tracker.db")


# =====================================================
# REGISTER
# =====================================================

def register():

    st.header("📝 Create Account")

    name = st.text_input(
        "Name",
        key="register_name"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button(
        "📝 Register",
        use_container_width=True
    ):

        if not name or not email or not password:
            st.warning("Please fill all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password)
            )

            conn.commit()

            st.success(
                "Registration successful! Please login. 🎉"
            )

        except sqlite3.IntegrityError:

            st.error(
                "Email already registered."
            )

        except Exception as e:

            st.error(
                f"Registration error: {e}"
            )

        finally:

            conn.close()


# =====================================================
# LOGIN
# =====================================================

def login():

    st.header("🔐 User Login")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        if not email or not password:
            st.warning(
                "Please enter email and password."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name
            FROM users
            WHERE email = ?
            AND password = ?
            """,
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            user_id = user[0]
            name = user[1]

            # Save login permanently
            save_user(user_id)

            # Streamlit session
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.name = name
            st.session_state.page = "Home"

            st.success(
                f"Welcome back, {name}! 🎉"
            )

            st.rerun()

        else:

            st.error(
                "Invalid email or password."
            )