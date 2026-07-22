"""search.py - Search recipes by keyword and/or category."""

import streamlit as st
from services.recipe_service import search_recipes
from services.category_service import get_all_categories, get_category_name


def show_search():
    st.title("🔍 Search Recipes")
    user = st.session_state["user"]

    categories = get_all_categories()
    cat_names = ["All Categories"] + [c["name"] for c in categories]
    cat_ids = [None] + [c["id"] for c in categories]

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Search by title, ingredient, or description")
    with col2:
        cat_choice = st.selectbox("Category", cat_names)

    category_id = cat_ids[cat_names.index(cat_choice)]
    results = search_recipes(query=query, category_id=category_id, user_id=user["id"])

    st.markdown(f"**{len(results)} result(s) found**")

    for recipe in results:
        with st.container(border=True):
            cols = st.columns([1, 4])
            with cols[0]:
                if recipe["image_path"]:
                    st.image(recipe["image_path"], use_container_width=True)
                else:
                    st.markdown("🍽️")
            with cols[1]:
                st.markdown(f"**{recipe['title']}**")
                st.caption(get_category_name(recipe["category_id"]))
                if recipe["description"]:
                    st.write(recipe["description"])
                if st.button("View Recipe", key=f"search_view_{recipe['id']}"):
                    st.session_state["page"] = "recipes"
                    st.session_state["viewing_recipe_id"] = recipe["id"]
                    st.rerun()
