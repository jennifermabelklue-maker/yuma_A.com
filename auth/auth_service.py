"""
auth_service.py
Handles registration, login, and password hashing.
Uses hashlib (Python standard library) with a per-password salt -
no paid auth provider needed.
"""

import hashlib
import os
import re
from typing import Optional
from services.db import get_connection


def _hash_password(password: str, salt: Optional[str] = None) -> str:
    if salt is None:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${pwd_hash}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, _ = stored_hash.split("$")
    except ValueError:
        return False
    return _hash_password(password, salt) == stored_hash


def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


def register_user(username: str, email: str, password: str):
    """Returns (success: bool, message: str)."""
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return False, "All fields are required."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cur.fetchone():
        conn.close()
        return False, "Username or email already exists."

    pwd_hash = _hash_password(password)
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, pwd_hash),
    )
    conn.commit()
    conn.close()
    return True, "Account created successfully! Please log in."


def login_user(username_or_email: str, password: str):
    """Returns (success: bool, user_dict_or_message)."""
    identifier = username_or_email.strip().lower()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE lower(username) = ? OR lower(email) = ?",
        (identifier, identifier),
    )
    user = cur.fetchone()
    conn.close()

    if not user:
        return False, "No account found with that username/email."
    if not _verify_password(password, user["password_hash"]):
        return False, "Incorrect password."

    return True, {"id": user["id"], "username": user["username"], "email": user["email"]}


def update_password(user_id: int, new_password: str):
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (_hash_password(new_password), user_id),
    )
    conn.commit()
    conn.close()
    return True, "Password updated."
