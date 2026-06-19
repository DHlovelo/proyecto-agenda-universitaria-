import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import load_users, save_users, find_user
class Usuario:
    def __init__(self, username, password, xp=0, level=1):
        self.username = username
        self.password = password
        self.xp = xp
        self.level = level

def register(username, password):
    users = load_users()

    if find_user(username):
        return False, "Usuario ya existe"
    nuevo_usuario = Usuario(username, password)
    users.append(nuevo_usuario.__dict__)
    save_users(users)
    return True, "Usuario creado"

def login(username, password):
    user = find_user(username)

    
    if user and user.get("password") == password:
        return True, user
    return False, None