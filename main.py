import customtkinter as ctk
from au import login, register
from dashboard import open_dashboard
from estilo import *

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("400x500")
app.title("GamerTask Login")

title = ctk.CTkLabel(app, text="🎮 GAMERTASK", font=("Arial", 24, "bold"))
title.pack(pady=20)

username_entry = ctk.CTkEntry(app, placeholder_text="Usuario")
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Contraseña", show="*")
password_entry.pack(pady=10)

label_msg = ctk.CTkLabel(app, text="")
label_msg.pack()

def do_login():
    user = username_entry.get()
    pwd = password_entry.get()

    ok, data = login(user, pwd)

    if ok:
        app.destroy()
        open_dashboard(data)
    else:
        label_msg.configure(text="Login incorrecto ❌")

def do_register():
    user = username_entry.get()
    pwd = password_entry.get()

    ok, msg = register(user, pwd)
    label_msg.configure(text=msg)

btn_login = ctk.CTkButton(app, text="Ingresar", command=do_login)
btn_login.pack(pady=10)

btn_register = ctk.CTkButton(app, text="Registrar", command=do_register)
btn_register.pack(pady=10)

app.mainloop()