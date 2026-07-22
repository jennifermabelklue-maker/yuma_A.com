"""recipes.py - Browse, view, edit, and delete your own recipes."""

import streamlit as st
from services.recipe_service import (
    get_all_recipes, delete_recipe, update_recipe, is_favorite, toggle_favorite
)
from services.category_service import get_all_categories, get_category_name


def show_recipes():
    st.title("📖 My Recipes")
    user = st.session_state["user"]

    recipes = get_all_recipes(user_id=user["id"])
    if not recipes:
        st.info("No recipes yet. Add your first one from **Add Recipe**!")
        return

    selected_id = st.session_state.get("viewing_recipe_id")

    if selected_id:
        _show_recipe_detail(selected_id, user["id"])
        return

    for recipe in recipes:
        with st.container(border=True):
            cols = st.columns([1, 3, 1])
            with cols[0]:
                if recipe["image_path"]:
                    st.image(recipe["image_path"], use_container_width=True)
                else:
                    st.markdown("### 🍽️")
            with cols[1]:
                st.markdown(f"**{recipe['title']}**")
                st.caption(get_category_name(recipe["category_id"]))
            with cols[2]:
                if st.button("View", key=f"view_{recipe['id']}", use_container_width=True):
                    st.session_state["viewing_recipe_id"] = recipe["id"]
                    st.rerun()


def _show_recipe_detail(recipe_id, user_id):
    from services.recipe_service import get_recipe

    recipe = get_recipe(recipe_id)
    if not recipe:
        st.error("Recipe not found.")
        st.session_state["viewing_recipe_id"] = None
        return

    if st.button("← Back to list"):
        st.session_state["viewing_recipe_id"] = None
        st.rerun()

    st.header(recipe["title"])
    if recipe["image_path"]:
        st.image(recipe["image_path"], use_container_width=True)

    st.caption(f"{get_category_name(recipe['category_id'])} · "
               f"Prep {recipe['prep_time']}m · Cook {recipe['cook_time']}m · "
               f"Serves {recipe['servings']}")

    if recipe["description"]:
        st.write(recipe["description"])

    fav = is_favorite(user_id, recipe_id)
    if st.button("💔 Remove Favorite" if fav else "❤️ Add to Favorites"):
        toggle_favorite(user_id, recipe_id)
        st.rerun()

    st.subheader("Ingredients")
    st.markdown("\n".join(f"- {line}" for line in recipe["ingredients"].split("\n") if line.strip()))

    st.subheader("Instructions")
    st.write(recipe["instructions"])

    if recipe["user_id"] == user_id:
        st.markdown("---")
        with st.expander("✏️ Edit Recipe"):
            _edit_form(recipe)
        if st.button("🗑️ Delete Recipe", type="primary"):
            delete_recipe(recipe_id)
            st.session_state["viewing_recipe_id"] = None
            st.success("Recipe deleted.")
            st.rerun()


def _edit_form(recipe):
    categories = get_all_categories()
    cat_names = ["Uncategorized"] + [c["name"] for c in categories]
    cat_ids = [None] + [c["id"] for c in categories]
    current_index = cat_ids.index(recipe["category_id"]) if recipe["category_id"] in cat_ids else 0

    with st.form(f"edit_{recipe['id']}"):
        title = st.text_input("Title", value=recipe["title"])
        description = st.text_area("Description", value=recipe["description"] or "")
        ingredients = st.text_area("Ingredients (one per line)", value=recipe["ingredients"])
        instructions = st.text_area("Instructions", value=recipe["instructions"])
        category_choice = st.selectbox("Category", cat_names, index=current_index)
        col1, col2, col3 = st.columns(3)
        prep_time = col1.number_input("Prep time (min)", min_value=0, value=recipe["prep_time"])
        cook_time = col2.number_input("Cook time (min)", min_value=0, value=recipe["cook_time"])
        servings = col3.number_input("Servings", min_value=1, value=recipe["servings"])

        if st.form_submit_button("Save Changes"):
            category_id = cat_ids[cat_names.index(category_choice)]
            update_recipe(
                recipe["id"],
                title=title, description=description, ingredients=ingredients,
                instructions=instructions, category_id=category_id,
                prep_time=prep_time, cook_time=cook_time, servings=servings,
            )
            st.success("Recipe updated!")
            st.rerun()
