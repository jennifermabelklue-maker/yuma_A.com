"""random_recipe.py - Picks a random recipe from the user's collection."""

import streamlit as st
from services.recipe_service import get_random_recipe, is_favorite, toggle_favorite
from services.category_service import get_category_name


def show_random_recipe():
    st.title("🎲 Feeling Indecisive?")
    st.write("Let us pick a recipe for you!")
    user = st.session_state["user"]

    if st.button("🎲 Surprise Me!", use_container_width=True):
        st.session_state["random_recipe"] = get_random_recipe(user_id=user["id"])

    recipe = st.session_state.get("random_recipe")

    if recipe is None:
        st.info("Click the button above to get a random recipe suggestion.")
        return

    with st.container(border=True):
        if recipe["image_path"]:
            st.image(recipe["image_path"], use_container_width=True)
        st.header(recipe["title"])
        st.caption(f"{get_category_name(recipe['category_id'])} · "
                   f"Prep {recipe['prep_time']}m · Cook {recipe['cook_time']}m")
        if recipe["description"]:
            st.write(recipe["description"])

        fav = is_favorite(user["id"], recipe["id"])
        if st.button("💔 Remove Favorite" if fav else "❤️ Add to Favorites"):
            toggle_favorite(user["id"], recipe["id"])
            st.rerun()

        st.subheader("Ingredients")
        st.markdown("\n".join(f"- {line}" for line in recipe["ingredients"].split("\n") if line.strip()))

        st.subheader("Instructions")
        st.write(recipe["instructions"])
