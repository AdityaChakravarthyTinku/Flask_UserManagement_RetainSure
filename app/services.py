from .db import fetch_one, fetch_all, execute_query
from .utils import hash_password, verify_password

def get_all_users_service():
    users = fetch_all("SELECT id, name, email FROM users")
    return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]

def get_user_service(user_id: int):
    return fetch_one("SELECT id, name, email FROM users WHERE id = ?", (user_id,))

def user_exists_by_email(email: str) -> bool:
    user = fetch_one("SELECT id FROM users WHERE email = ?", (email,))
    return user is not None


def create_user_service(name: str, email: str, password: str):
    hashed_password = hash_password(password)
    return execute_query(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password)
    )

def update_user_service(user_id: int, name: str, email: str):
    return execute_query(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, user_id)
    )

def delete_user_service(user_id: int):
    return execute_query("DELETE FROM users WHERE id = ?", (user_id,))

def search_users_service(name: str):
    users = fetch_all("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
    return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]

def login_user_service(email: str, password: str):
    user = fetch_one("SELECT id, name, password FROM users WHERE email = ?", (email,))
    if user and verify_password(user[2], password):
        return {"status": "success", "user_id": user[0], "User_name": f"Welcome {user[1]}", "email": f"You are logged in with {email}"}
    return {"status": "failed"}