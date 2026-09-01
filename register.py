import streamlit as st
from database import get_connection


def register():

    st.subheader("📝 Create Account")

    name = st.text_input(
        "Full Name",
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
        key="register_confirm"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        if not name or not email or not password:

            st.warning(
                "Please fill in all fields."
            )
            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            if cursor.fetchone():

                st.error(
                    "An account with this email already exists."
                )
                return

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, password)
            )

            conn.commit()

            st.success(
                "✅ Account created successfully!"
            )

            st.info(
                "Go to the Login tab to login."
            )

        except Exception as e:

            conn.rollback()

            st.error(
                f"Registration error: {e}"
            )

        finally:

            cursor.close()
            conn.close()