"""favorites.py - Shows the user's favorited recipes."""

import streamlit as st
from services.recipe_service import get_favorite_recipes, toggle_favorite
from services.category_service import get_category_name


def show_favorites():
    st.title("❤️ Favorite Recipes")
    user = st.session_state["user"]

    favorites = get_favorite_recipes(user["id"])
    if not favorites:
        st.info("You haven't favorited any recipes yet. Browse recipes and tap ❤️ to save them here.")
        return

    for recipe in favorites:
        with st.container(border=True):
            cols = st.columns([1, 3, 1])
            with cols[0]:
                if recipe["image_path"]:
                    st.image(recipe["image_path"], use_container_width=True)
                else:
                    st.markdown("🍽️")
            with cols[1]:
                st.markdown(f"**{recipe['title']}**")
                st.caption(get_category_name(recipe["category_id"]))
            with cols[2]:
                if st.button("💔 Remove", key=f"unfav_{recipe['id']}", use_container_width=True):
                    toggle_favorite(user["id"], recipe["id"])
                    st.rerun()
                if st.button("View", key=f"fav_view_{recipe['id']}", use_container_width=True):
                    st.session_state["page"] = "recipes"
                    st.session_state["viewing_recipe_id"] = recipe["id"]
                    st.rerun()
