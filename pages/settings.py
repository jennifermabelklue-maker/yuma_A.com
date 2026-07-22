"""settings.py - Account settings, primarily password changes."""

import streamlit as st
from auth.auth_service import update_password, login_user


def show_settings():
    st.title("⚙️ Settings")
    user = st.session_state["user"]

    st.subheader("Change Password")
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Update Password")

        if submitted:
            ok, _ = login_user(user["username"], current_password)
            if not ok:
                st.error("Current password is incorrect.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            else:
                success, msg = update_password(user["id"], new_password)
                st.success(msg) if success else st.error(msg)

    st.markdown("---")
    st.subheader("About")
    st.write(
        "Recipe Time is built entirely on free, open-source tools: "
        "Streamlit for the interface and SQLite for local storage. "
        "No paid services, subscriptions, or external APIs are required to run it."
    )
