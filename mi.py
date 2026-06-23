import customtkinter as ctk
from api import get_motivation

class GamerTaskApp(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.user = user  # Diccionario con datos del usuario
        
        self.geometry("800x600")
        self.title("GamerTask Dashboard")

        # Layout: Sidebar para navegación
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Área principal donde cambiará el contenido
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_sidebar()
        self.show_dashboard()

    def setup_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Menú", font=("Arial", 16, "bold")).pack(pady=10)
        
        buttons = [
            ("Inicio", self.show_dashboard),
            ("Materias", self.show_materias),
            ("Tareas", self.show_tareas),
            ("Exámenes", self.show_examenes),
            ("Pomodoro", self.show_pomodoro),
            ("Estadísticas", self.show_estadisticas)
        ]
        
        for text, command in buttons:
            ctk.CTkButton(self.sidebar, text=text, command=command).pack(pady=5, padx=10)

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text=f"Bienvenido {self.user['username']} 🎮", font=("Arial", 24)).pack(pady=20)
        ctk.CTkLabel(self.main_area, text=f"XP: {self.user['xp']} | Nivel: {self.user['level']}").pack(pady=10)
        
        self.motivation_label = ctk.CTkLabel(self.main_area, text="Pulsa el botón para motivarte")
        self.motivation_label.pack(pady=20)
        ctk.CTkButton(self.main_area, text="Frase motivacional", command=self.load_motivation).pack()

    def load_motivation(self):
        msg = get_motivation()
        self.motivation_label.configure(text=msg)

    def show_materias(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Gestión de Materias", font=("Arial", 20)).pack(pady=20)
        # Aquí puedes añadir un entry para añadir nuevas materias
        ctk.CTkEntry(self.main_area, placeholder_text="Nombre de la materia...").pack(pady=10)
        ctk.CTkButton(self.main_area, text="Guardar Materia").pack()

    def show_tareas(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Lista de Tareas").pack(pady=20)
        # Aquí implementarías una lista (ScrollableFrame)
        
    def show_examenes(self): pass
    def show_pomodoro(self): pass
    def show_estadisticas(self): pass

# Simulación de usuario
user_data = {"username": "Player1", "xp": 150, "level": 2}

if __name__ == "__main__":
    app = GamerTaskApp(user_data)
    app.mainloop()