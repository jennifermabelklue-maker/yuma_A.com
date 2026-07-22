"""add_recipe.py - Form to create a new recipe."""

import streamlit as st  # type: ignore[reportMissingImports]
from services.recipe_service import add_recipe, save_uploaded_image
from services.category_service import get_all_categories, add_category


def show_add_recipe():
    st.title("➕ Add a New Recipe")
    user = st.session_state["user"]

    categories = get_all_categories()
    cat_names = ["Uncategorized"] + [c["name"] for c in categories]
    cat_ids = [None] + [c["id"] for c in categories]

    with st.expander("Need a new category?"):
        new_cat = st.text_input("New category name", key="new_cat_input")
        if st.button("Add Category"):
            success, msg = add_category(new_cat)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    with st.form("add_recipe_form", clear_on_submit=True):
        title = st.text_input("Recipe Title *")
        description = st.text_area("Short Description")
        image = st.file_uploader("Recipe Photo (optional)", type=["png", "jpg", "jpeg"])
        ingredients = st.text_area("Ingredients * (one per line)",
                                    placeholder="2 cups flour\n1 tsp salt\n...")
        instructions = st.text_area("Instructions *",
                                     placeholder="1. Preheat oven...\n2. Mix...")
        category_choice = st.selectbox("Category", cat_names)

        col1, col2, col3 = st.columns(3)
        prep_time = col1.number_input("Prep time (min)", min_value=0, value=10)
        cook_time = col2.number_input("Cook time (min)", min_value=0, value=20)
        servings = col3.number_input("Servings", min_value=1, value=4)

        submitted = st.form_submit_button("Save Recipe", use_container_width=True)

        if submitted:
            if not title.strip() or not ingredients.strip() or not instructions.strip():
                st.error("Title, ingredients, and instructions are required.")
            else:
                category_id = cat_ids[cat_names.index(category_choice)]
                image_path = save_uploaded_image(image) if image else None
                add_recipe(
                    user_id=user["id"], title=title.strip(), description=description.strip(),
                    ingredients=ingredients.strip(), instructions=instructions.strip(),
                    category_id=category_id, prep_time=prep_time, cook_time=cook_time,
                    servings=servings, image_path=image_path,
                )
                st.success(f"'{title}' was added to your recipe book! 🎉")
