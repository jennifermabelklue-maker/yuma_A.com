"""dashboard.py - Landing page after login: quick stats + recent recipes."""

import streamlit as st
from services.recipe_service import get_all_recipes, get_favorite_recipes
from services.category_service import get_category_name


def show_dashboard():
    user = st.session_state["user"]
    st.title(f"🍳 Welcome back, {user['username']}!")

    my_recipes = get_all_recipes(user_id=user["id"])
    favorites = get_favorite_recipes(user["id"])

    col1, col2, col3 = st.columns(3)
    col1.metric("My Recipes", len(my_recipes))
    col2.metric("Favorites", len(favorites))
    col3.metric("Total Cook Time (min)", sum(r["cook_time"] or 0 for r in my_recipes))

    st.markdown("---")
    st.subheader("📌 Your Most Recent Recipes")

    if not my_recipes:
        st.info("You haven't added any recipes yet. Head to **Add Recipe** to create your first one!")
        return

    for recipe in my_recipes[:5]:
        with st.container(border=True):
            cols = st.columns([1, 4])
            with cols[0]:
                if recipe["image_path"]:
                    st.image(recipe["image_path"], use_container_width=True)
                else:
                    st.markdown("🍽️")
            with cols[1]:
                st.markdown(f"**{recipe['title']}**")
                st.caption(f"{get_category_name(recipe['category_id'])} · "
                           f"Prep {recipe['prep_time']}m · Cook {recipe['cook_time']}m")
                if recipe["description"]:
                    st.write(recipe["description"])
