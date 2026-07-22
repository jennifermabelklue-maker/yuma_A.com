"""categories.py - Manage categories and browse recipes grouped by category."""

import streamlit as st
from services.category_service import get_all_categories, add_category, delete_category
from services.recipe_service import search_recipes


def show_categories():
    st.title("🗂️ Categories")
    user = st.session_state["user"]

    with st.form("new_category_form"):
        name = st.text_input("New category name")
        if st.form_submit_button("Add Category"):
            success, msg = add_category(name)
            st.success(msg) if success else st.error(msg)
            if success:
                st.rerun()

    st.markdown("---")

    categories = get_all_categories()
    if not categories:
        st.info("No categories yet. Add one above.")
        return

    for cat in categories:
        recipes_in_cat = search_recipes(category_id=cat["id"], user_id=user["id"])
        with st.expander(f"{cat['name']} ({len(recipes_in_cat)} recipes)"):
            if recipes_in_cat:
                for r in recipes_in_cat:
                    st.write(f"• {r['title']}")
            else:
                st.caption("No recipes in this category yet.")

            if st.button("Delete Category", key=f"del_cat_{cat['id']}"):
                delete_category(cat["id"])
                st.rerun()
