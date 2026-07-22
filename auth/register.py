"""register.py - New account form."""

import streamlit as st
from auth.auth_service import register_user


def show_register():
    st.markdown("## 📝 Create Your Recipe Time Account")

    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

        if submitted:
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(username, email, password)
                if success:
                    st.success(message)
                    st.session_state["auth_view"] = "login"
                    st.rerun()
                else:
                    st.error(message)

    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Already have an account?")
    with col2:
        if st.button("Log In", use_container_width=True):
            st.session_state["auth_view"] = "login"
            st.rerun()
