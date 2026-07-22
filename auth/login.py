"""login.py - Login form rendered when no user is signed in."""

import streamlit as st
from auth.auth_service import login_user


def show_login():
    st.markdown("## 🔑 Log In to Recipe Time")

    with st.form("login_form", clear_on_submit=False):
        identifier = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In", use_container_width=True)

        if submitted:
            success, result = login_user(identifier, password)
            if success:
                st.session_state["user"] = result
                st.success(f"Welcome back, {get_username(result)}! 🎉")
                st.rerun()
            else:
                st.error(result)

    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Don't have an account yet?")
    with col2:
        if st.button("Register", use_container_width=True):
            st.session_state["auth_view"] = "register"
            st.rerun()

def get_username(result):
    return result.username
