"""recipe_service.py - CRUD and query helpers for recipes and favorites."""

import os
import random
import uuid
from services.db import get_connection

IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "uploads")
os.makedirs(IMAGE_DIR, exist_ok=True)


def save_uploaded_image(uploaded_file):
    """Save a Streamlit UploadedFile to disk and return its relative path."""
    if uploaded_file is None:
        return None
    ext = os.path.splitext(uploaded_file.name)[1] or ".png"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(IMAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath


def add_recipe(user_id, title, description, ingredients, instructions,
                category_id, prep_time, cook_time, servings, image_path=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO recipes
        (user_id, title, description, ingredients, instructions,
         category_id, prep_time, cook_time, servings, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, ingredients, instructions,
          category_id, prep_time, cook_time, servings, image_path))
    conn.commit()
    conn.close()


def update_recipe(recipe_id, **fields):
    if not fields:
        return
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [recipe_id]
    cur.execute(f"UPDATE recipes SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_recipe(recipe_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()


def get_recipe(recipe_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_recipes(user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    else:
        cur.execute("SELECT * FROM recipes ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_recipes(query="", category_id=None, user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if user_id:
        sql += " AND user_id = ?"
        params.append(user_id)
    if query:
        sql += " AND (title LIKE ? OR ingredients LIKE ? OR description LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like, like])
    if category_id:
        sql += " AND category_id = ?"
        params.append(category_id)

    sql += " ORDER BY created_at DESC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_random_recipe(user_id=None):
    recipes = get_all_recipes(user_id=user_id)
    if not recipes:
        return None
    return random.choice(recipes)


# ---- Favorites ----

def toggle_favorite(user_id, recipe_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM favorites WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
    existing = cur.fetchone()
    if existing:
        cur.execute("DELETE FROM favorites WHERE id = ?", (existing["id"],))
        conn.commit()
        conn.close()
        return False  # now un-favorited
    else:
        cur.execute("INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
        conn.commit()
        conn.close()
        return True  # now favorited


def is_favorite(user_id, recipe_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM favorites WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
    row = cur.fetchone()
    conn.close()
    return row is not None


def get_favorite_recipes(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.* FROM recipes r
        JOIN favorites f ON r.id = f.recipe_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
