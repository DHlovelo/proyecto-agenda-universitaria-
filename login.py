import customtkinter as ctk

def pedir_usuario():
    # Creamos una ventana temporal de login
    login_window = ctk.CTk()
    login_window.geometry("300x200")
    login_window.title("Login GamerTask")

    user_info = {"username": None}

    def guardar():
        if entry.get():
            user_info["username"] = entry.get()
            login_window.destroy() # Cierra el login

    ctk.CTkLabel(login_window, text="Nombre de Usuario:").pack(pady=20)
    entry = ctk.CTkEntry(login_window)
    entry.pack(pady=10)
    
    ctk.CTkButton(login_window, text="Entrar", command=guardar).pack(pady=10)
    
    login_window.mainloop()
    return user_info["username"]