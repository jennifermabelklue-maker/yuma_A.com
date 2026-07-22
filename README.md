# 🍳 Recipe Time

A personal recipe manager built entirely with **free, open-source tools**:

- **Streamlit** — the web UI (free, open source)
- **SQLite** — local file-based database, built into Python (no paid database service)
- **hashlib** (Python standard library) — password hashing for accounts

No paid APIs, no cloud database subscriptions, no hosting costs required to
run it locally.

## Features
- Account registration & login (locally hashed passwords)
- Add / edit / delete your own recipes, with optional photo upload
- Browse by category, full-text search across title/ingredients/description
- Favorites list
- "Surprise me" random recipe picker
- Profile & settings (password change)

## Setup

```bash
cd Recipe_Time
pip install -r requirements.txt
streamlit run app.py
```

The app creates `data/recipe_time.db` automatically on first run and seeds
a few starter categories and sample recipes under a demo account
(`demo` / `demo1234`) so the app isn't empty when you first open it.

## Project Structure

```
Recipe_Time/
├── app.py              # Entry point, auth gate + page routing
├── sidebar.py           # Navigation sidebar
├── auth/                 # Login, register, password hashing
├── pages/                 # One file per screen (dashboard, recipes, etc.)
├── services/               # Data layer: SQLite access, recipe/category logic
├── assets/                  # logo.png / banner.png (optional — add your own)
└── data/                     # recipe_time.db lives here (auto-created)
```

## Notes on "free"
- **No paid image storage**: uploaded recipe photos are saved to
  `assets/uploads/` on disk.
- **No paid auth provider**: accounts are stored in SQLite with salted
  SHA-256 password hashes.
- **No external API calls**: everything runs locally / on whatever free
  Streamlit hosting you choose (e.g. Streamlit Community Cloud's free tier).
- `assets/logo.png` and `assets/banner.png` are not included — the app
  falls back to a text header if they're missing. Drop your own free/
  public-domain images in to brand it.
