"""profile.py - Basic account info and stats."""

import streamlit as st
from services.recipe_service import get_all_recipes, get_favorite_recipes


def show_profile():
    st.title("👤 My Profile")
    user = st.session_state["user"]

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### 🧑‍🍳")
    with col2:
        st.markdown(f"**Username:** {user['username']}")
        st.markdown(f"**Email:** {user['email']}")

    st.markdown("---")

    my_recipes = get_all_recipes(user_id=user["id"])
    favorites = get_favorite_recipes(user["id"])

    col1, col2 = st.columns(2)
    col1.metric("Recipes Created", len(my_recipes))
    col2.metric("Favorites Saved", len(favorites))
