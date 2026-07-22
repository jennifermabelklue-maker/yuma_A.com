"""sidebar.py - Left navigation shown to logged-in users."""

import os
import streamlit as st

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

PAGES = {
    "🏠 Dashboard": "dashboard",
    "📖 My Recipes": "recipes",
    "➕ Add Recipe": "add_recipe",
    "🔍 Search": "search",
    "🗂️ Categories": "categories",
    "❤️ Favorites": "favorites",
    "🎲 Random Recipe": "random_recipe",
    "👤 Profile": "profile",
    "⚙️ Settings": "settings",
}


def show_sidebar():
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        else:
            st.markdown("## 🍳 Recipe Time")

        user = st.session_state.get("user")
        if user:
            st.markdown(f"**Welcome, {user['username']}!**")

        st.markdown("---")

        current_page = st.session_state.get("page", "dashboard")
        for label, page_key in PAGES.items():
            if st.button(label, use_container_width=True,
                         type="primary" if current_page == page_key else "secondary"):
                st.session_state["page"] = page_key
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.pop("user", None)
            st.session_state["page"] = "dashboard"
            st.rerun()
