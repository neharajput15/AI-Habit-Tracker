import streamlit as st

# =====================================================
# REMEMBER LOGIN USING SESSION STATE
# (Works with Streamlit Cloud + Neon)
# =====================================================

def save_user(user_id):
    st.session_state["saved_user_id"] = user_id


def get_saved_user():
    return st.session_state.get("saved_user_id")


def clear_saved_user():
    if "saved_user_id" in st.session_state:
        del st.session_state["saved_user_id"]