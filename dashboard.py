import customtkinter as ctk
from api import get_motivation

def open_dashboard(user):

    app = ctk.CTk()
    app.geometry("700x500")
    app.title("GamerTask Dashboard")

    title = ctk.CTkLabel(app, text=f"Bienvenido {user['username']} 🎮",
                         font=("Arial", 20))
    title.pack(pady=20)

    xp = ctk.CTkLabel(app, text=f"XP: {user['xp']} | Nivel: {user['level']}")
    xp.pack(pady=10)

    motivation = ctk.CTkLabel(app, text="Cargando motivación...")
    motivation.pack(pady=10)

    def load_motivation():
        msg = get_motivation()
        motivation.configure(text=msg)

    btn = ctk.CTkButton(app, text="Frase motivacional", command=load_motivation)
    btn.pack(pady=10)

    # BOTONES DEL SISTEMA (RAMAS FUTURAS)
    ctk.CTkButton(app, text="📚 Materias").pack(pady=5)
    ctk.CTkButton(app, text="📝 Tareas").pack(pady=5)
    ctk.CTkButton(app, text="📅 Exámenes").pack(pady=5)
    ctk.CTkButton(app, text="⏰ Pomodoro").pack(pady=5)
    ctk.CTkButton(app, text="📊 Estadísticas").pack(pady=5)

    app.mainloop()