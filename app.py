"""
app.py
Entry point for Recipe Time.
Run with: streamlit run app.py
100% free stack: Streamlit (UI) + SQLite (storage) - no paid services required.
"""

import streamlit as st

from services.db import init_db
from services.starter_recipes import seed_starter_data

from auth.login import show_login
from auth.register import show_register

from sidebar import show_sidebar
from pages.dashboard import show_dashboard
from pages.recipes import show_recipes
from pages.add_recipe import show_add_recipe
from pages.search import show_search
from pages.categories import show_categories
from pages.favorites import show_favorites
from pages.random_recipe import show_random_recipe
from pages.settings import show_settings
from pages.profile import show_profile

st.set_page_config(
    page_title="Recipe Time",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def _bootstrap_database():
    """Runs once per server process: create tables + seed starter data."""
    init_db()
    seed_starter_data()
    return True


_bootstrap_database()

# ---- Session defaults ----
if "user" not in st.session_state:
    st.session_state["user"] = None
if "auth_view" not in st.session_state:
    st.session_state["auth_view"] = "login"
if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

PAGE_ROUTES = {
    "dashboard": show_dashboard,
    "recipes": show_recipes,
    "add_recipe": show_add_recipe,
    "search": show_search,
    "categories": show_categories,
    "favorites": show_favorites,
    "random_recipe": show_random_recipe,
    "settings": show_settings,
    "profile": show_profile,
}


def main():
    if not st.session_state["user"]:
        st.markdown(
            "<h1 style='text-align:center;'>🍳 Recipe Time</h1>"
            "<p style='text-align:center;color:gray;'>Your free, personal recipe box</p>",
            unsafe_allow_html=True,
        )
        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.session_state["auth_view"] == "login":
                show_login()
            else:
                show_register()
        return

    show_sidebar()
    page_key = st.session_state.get("page", "dashboard")
    render = PAGE_ROUTES.get(page_key, show_dashboard)
    render()


if __name__ == "__main__":
    main()
