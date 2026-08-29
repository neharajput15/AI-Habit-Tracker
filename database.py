import psycopg2
import streamlit as st


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():

    return psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )


# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # =================================================
        # USERS
        # =================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        # =================================================
        # HABITS
        # =================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                habit_name TEXT NOT NULL,
                category TEXT,
                target TEXT,
                status TEXT DEFAULT 'Pending',

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
            )
            """
        )

        # =================================================
        # PROGRESS
        # =================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                id SERIAL PRIMARY KEY,
                habit_id INTEGER NOT NULL,
                completed_date TEXT NOT NULL,
                completed INTEGER DEFAULT 0,

                FOREIGN KEY (habit_id)
                REFERENCES habits(id)
                ON DELETE CASCADE
            )
            """
        )

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        cursor.close()
        conn.close()


# =====================================================
# INITIALIZE DATABASE
# =====================================================

create_tables()