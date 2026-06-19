import json
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def find_user(username):
    users = load_users()
    for u in users:
        if u["username"] == username:
            return u
    return None