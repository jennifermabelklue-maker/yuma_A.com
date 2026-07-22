"""category_service.py - CRUD helpers for recipe categories."""

from services.db import get_connection


def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories ORDER BY name ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_category(name: str):
    name = name.strip()
    if not name:
        return False, "Category name cannot be empty."
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        return True, "Category added."
    except Exception:
        return False, "That category already exists."
    finally:
        conn.close()


def delete_category(category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()


def get_category_name(category_id):
    if not category_id:
        return "Uncategorized"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
    row = cur.fetchone()
    conn.close()
    return row["name"] if row else "Uncategorized"
