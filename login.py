import streamlit as st

from database import get_connection
from remember_login import save_user


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

        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if (
            not name.strip()
            or not email.strip()
            or not password
        ):
            st.warning(
                "Please fill all fields."
            )
            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )
            return

        email = email.strip().lower()

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # -----------------------------------------
            # CHECK EXISTING EMAIL
            # -----------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                st.error(
                    "Email already registered. Please login."
                )

                return

            # -----------------------------------------
            # CREATE USER
            # -----------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )
                VALUES (%s, %s, %s)
                """,
                (
                    name.strip(),
                    email,
                    password
                )
            )

            conn.commit()

            st.success(
                "Registration successful! 🎉"
            )

            st.info(
                "Now select Login and enter your email and password."
            )

        except Exception as e:

            if conn:
                conn.rollback()

            st.error(
                f"Registration error: {e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
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

        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not email.strip() or not password:

            st.warning(
                "Please enter email and password."
            )

            return

        email = email.strip().lower()

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # -----------------------------------------
            # CHECK USER
            # -----------------------------------------

            cursor.execute(
                """
                SELECT id, name
                FROM users
                WHERE email = %s
                AND password = %s
                """,
                (
                    email,
                    password
                )
            )

            user = cursor.fetchone()

        except Exception as e:

            st.error(
                f"Login error: {e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        # ---------------------------------------------
        # LOGIN SUCCESS
        # ---------------------------------------------

        if user:

            user_id = user[0]
            name = user[1]

            # Save user for auto-login
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

        # ---------------------------------------------
        # LOGIN FAILED
        # ---------------------------------------------

        else:

            st.error(
                "Invalid email or password."
            )