"""
starter_recipes.py
Seeds the database with a few starter categories and public-domain-style
sample recipes so a brand-new install isn't empty. Runs once - it checks
before inserting so it never duplicates data.
"""

from services.db import get_connection

STARTER_CATEGORIES = [
    "Breakfast", "Lunch", "Dinner", "Dessert", "Snacks", "Vegetarian", "Drinks"
]

STARTER_RECIPES = [
    {
        "title": "Classic Pancakes",
        "description": "Fluffy homemade pancakes, ready in 20 minutes.",
        "ingredients": "1.5 cups flour\n1 tbsp sugar\n2 tsp baking powder\n"
                        "0.5 tsp salt\n1.25 cups milk\n1 egg\n3 tbsp melted butter",
        "instructions": "1. Whisk dry ingredients together.\n"
                         "2. In a separate bowl, whisk milk, egg, and butter.\n"
                         "3. Combine wet and dry ingredients until just mixed.\n"
                         "4. Pour batter onto a hot greased griddle.\n"
                         "5. Flip when bubbles form on top, cook until golden.",
        "category": "Breakfast",
        "prep_time": 10,
        "cook_time": 10,
        "servings": 4,
    },
    {
        "title": "Simple Tomato Pasta",
        "description": "A quick weeknight pasta with a fresh tomato sauce.",
        "ingredients": "300g pasta\n4 ripe tomatoes, diced\n2 cloves garlic, minced\n"
                        "3 tbsp olive oil\nSalt and pepper\nFresh basil",
        "instructions": "1. Cook pasta according to package instructions.\n"
                         "2. Saute garlic in olive oil until fragrant.\n"
                         "3. Add tomatoes, salt, and pepper; simmer 10 minutes.\n"
                         "4. Toss with drained pasta and fresh basil.",
        "category": "Dinner",
        "prep_time": 10,
        "cook_time": 20,
        "servings": 3,
    },
    {
        "title": "Fruit Smoothie",
        "description": "A refreshing blended fruit drink.",
        "ingredients": "1 banana\n1 cup mixed berries\n1 cup yogurt\n0.5 cup milk\n1 tbsp honey",
        "instructions": "1. Add all ingredients to a blender.\n"
                         "2. Blend until smooth.\n"
                         "3. Pour into a glass and serve chilled.",
        "category": "Drinks",
        "prep_time": 5,
        "cook_time": 0,
        "servings": 2,
    },
]


def seed_starter_data():
    conn = get_connection()
    cur = conn.cursor()

    # Seed categories
    for name in STARTER_CATEGORIES:
        cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
    conn.commit()

    # Only seed sample recipes if the recipes table is completely empty
    cur.execute("SELECT COUNT(*) as c FROM recipes")
    count = cur.fetchone()["c"]

    if count == 0:
        # Create a default "demo" account to own the starter recipes
        cur.execute("SELECT id FROM users WHERE username = 'demo'")
        demo_user = cur.fetchone()
        if not demo_user:
            from auth.auth_service import _hash_password
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                ("demo", "demo@recipetime.local", _hash_password("demo1234")),
            )
            conn.commit()
            cur.execute("SELECT id FROM users WHERE username = 'demo'")
            demo_user = cur.fetchone()

        demo_user_id = demo_user["id"]

        cur.execute("SELECT id, name FROM categories")
        cat_map = {row["name"]: row["id"] for row in cur.fetchall()}

        for r in STARTER_RECIPES:
            cur.execute("""
                INSERT INTO recipes
                (user_id, title, description, ingredients, instructions,
                 category_id, prep_time, cook_time, servings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                demo_user_id, r["title"], r["description"], r["ingredients"],
                r["instructions"], cat_map.get(r["category"]),
                r["prep_time"], r["cook_time"], r["servings"],
            ))
        conn.commit()

    conn.close()
