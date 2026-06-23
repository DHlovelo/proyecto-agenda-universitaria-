import customtkinter as ctk
import json
import os
from api import get_motivation
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

# Configuración global
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UFlowA(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.data_file = "users.json"
        self.user = self.load_user_data(user)
        
        self.geometry("950x700")
        self.title("UFlowA - Agenda Universitaria")
        self.minsize(900, 650)

        # Paleta de colores juvenil y moderna (Estilo Tailwind)
        self.theme_colors = {
            "Inicio": {"main": "#3B82F6", "hover": "#2563EB"},        # Azul vibrante
            "Materias": {"main": "#8B5CF6", "hover": "#7C3AED"},      # Morado amatista
            "Tareas": {"main": "#10B981", "hover": "#059669"},        # Verde menta
            "Exámenes": {"main": "#F43F5E", "hover": "#E11D48"},      # Rojo coral/rosa
            "Pomodoro": {"main": "#F97316", "hover": "#EA580C"},      # Naranja cálido
            "Estadísticas": {"main": "#06B6D4", "hover": "#0891B2"},  # Cyan / Celeste
            "Perfil": {"main": "#6366F1", "hover": "#4F46E5"}         # Índigo
        }

        # Variables de Pomodoro
        self.pomodoro_time_left = 25 * 60
        self.pomodoro_running = False
        self.pomodoro_mode = "Trabajo"

        # Diseño principal
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.setup_sidebar()
        self.show_dashboard()

    def load_user_data(self, default_user):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"username": data[0], "materias": [], "tema": "System", "frase_personalizada": ""}
                return data
        return default_user

    def save_user_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.user, f)

    def setup_sidebar(self):
        ctk.CTkLabel(
            self.sidebar, 
            text="UFlowA", 
            font=("Segoe UI", 32, "bold"), 
            text_color=self.theme_colors["Inicio"]["main"]
        ).pack(pady=(40, 40))
        
        buttons = [
            ("Inicio", "🏠", self.show_dashboard, "Inicio"),
            ("Materias", "📚", self.show_materias, "Materias"),
            ("Tareas", "📝", self.show_tareas, "Tareas"),
            ("Exámenes", "📖", self.show_examenes, "Exámenes"),
            ("Pomodoro", "⏱️", self.show_pomodoro, "Pomodoro"),
            ("Estadísticas", "📊", self.show_estadisticas, "Estadísticas"),
            ("Perfil", "👤", self.show_usuario, "Perfil")
        ]
        
        for text, icon, command, key in buttons:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=f"{icon}   {text}", 
                command=command,
                fg_color="transparent",
                text_color=self.theme_colors[key]["main"],
                hover_color=("#E2E8F0", "#1E293B"),
                anchor="w",
                font=("Segoe UI", 16, "bold"),
                height=45,
                corner_radius=10
            )
            btn.pack(pady=5, padx=15, fill="x")

        self.sidebar_bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_bottom.pack(side="bottom", fill="x", pady=20)

        ctk.CTkLabel(self.sidebar_bottom, text="Modo Visual", font=("Segoe UI", 12)).pack(pady=(0, 5))
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar_bottom, 
            values=["Sistema", "Claro", "Oscuro"], 
            command=self.cambiar_tema,
            font=("Segoe UI", 12),
            fg_color=self.theme_colors["Perfil"]["main"],
            button_color=self.theme_colors["Perfil"]["hover"],
            button_hover_color=self.theme_colors["Perfil"]["main"]
        )
        self.theme_menu.pack(pady=5, padx=20)

        tema_actual = self.user.get("tema", "Sistema")
        self.theme_menu.set(tema_actual)
        self.cambiar_tema(tema_actual)

    def cambiar_tema(self, modo):
        if modo == "Claro": ctk.set_appearance_mode("Light")
        elif modo == "Oscuro": ctk.set_appearance_mode("Dark")
        else: ctk.set_appearance_mode("System")
        
        self.user["tema"] = modo
        self.save_user_data()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ================= PERFIL =================
    def show_usuario(self):
        self.clear_main_area()
        color = self.theme_colors["Perfil"]["main"]
        hover = self.theme_colors["Perfil"]["hover"]

        ctk.CTkLabel(self.main_area, text="Configuración de Perfil", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 30), anchor="w")
        
        card = ctk.CTkFrame(self.main_area, corner_radius=15)
        card.pack(fill="x", pady=10)

        ctk.CTkLabel(card, text="Nombre del Estudiante", font=("Segoe UI", 14, "bold")).pack(pady=(20, 5), padx=20, anchor="w")
        entry = ctk.CTkEntry(card, placeholder_text=self.user['username'], width=300, height=45, corner_radius=10)
        entry.pack(pady=5, padx=20, anchor="w")
        
        def guardar():
            nuevo_nombre = entry.get()
            if nuevo_nombre:
                self.user['username'] = nuevo_nombre
                self.save_user_data()
                self.show_dashboard()
        
        ctk.CTkButton(card, text="Guardar Cambios", command=guardar, height=45, corner_radius=10, fg_color=color, hover_color=hover, font=("Segoe UI", 14, "bold")).pack(pady=20, padx=20, anchor="w")

    # ================= INICIO =================
    def show_dashboard(self):
        self.clear_main_area()
        color = self.theme_colors["Inicio"]["main"]
        hover = self.theme_colors["Inicio"]["hover"]
        
        header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 30))
        
        ctk.CTkLabel(header_frame, text=f"¡Hola, {self.user['username']}! 👋", font=("Segoe UI", 36, "bold"), text_color=color).pack(side="left")

        mot_card = ctk.CTkFrame(self.main_area, corner_radius=15)
        mot_card.pack(fill="x", pady=10)
        
        # Frase actual (si no hay ninguna, pone una por defecto)
        frase_guardada = self.user.get("frase_personalizada", "Tu energía define tu día. ¡Tú puedes con todo!")

        self.motivation_label = ctk.CTkLabel(
            mot_card, 
            text=f'"{frase_guardada}"', 
            font=("Segoe UI", 20, "italic"),
            wraplength=700,
            text_color=color
        )
        self.motivation_label.pack(pady=(30, 20), padx=20)

        # Controles para editar la frase
        input_frame = ctk.CTkFrame(mot_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=(0, 15))

        self.frase_entry = ctk.CTkEntry(input_frame, placeholder_text="Escribe tu propia frase motivacional...", height=40, corner_radius=8)
        self.frase_entry.pack(side="left", expand=True, fill="x", padx=(0, 15))

        def guardar_frase_propia():
            nueva_frase = self.frase_entry.get().strip()
            if nueva_frase:
                self.user["frase_personalizada"] = nueva_frase
                self.save_user_data()
                self.motivation_label.configure(text=f'"{nueva_frase}"')
                self.frase_entry.delete(0, "end")

        ctk.CTkButton(input_frame, text="Guardar mi frase", command=guardar_frase_propia, fg_color=color, hover_color=hover, height=40, corner_radius=8, font=("Segoe UI", 13, "bold")).pack(side="left")
        
        # Botón para pedir a la API
        ctk.CTkButton(mot_card, text="✨ Sorpréndeme (Inspiración aleatoria)", command=self.load_motivation, fg_color="transparent", border_width=2, border_color=color, text_color=color, hover_color=("#E2E8F0", "#1E293B"), height=40, corner_radius=8, font=("Segoe UI", 13, "bold")).pack(pady=(5, 30))

    def load_motivation(self):
        msg = get_motivation()
        self.motivation_label.configure(text=f'"{msg}"')
        self.user["frase_personalizada"] = msg
        self.save_user_data()

    # ================= MATERIAS =================
    def show_materias(self):
        self.clear_main_area()
        color = self.theme_colors["Materias"]["main"]
        hover = self.theme_colors["Materias"]["hover"]

        ctk.CTkLabel(self.main_area, text="📚 Materias Académicas", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 20), anchor="w")

        input_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)

        if "materias" not in self.user:
            self.user["materias"] = []

        materia_entry = ctk.CTkEntry(input_frame, placeholder_text="Añadir nueva materia...", width=350, height=45, corner_radius=10)
        materia_entry.pack(side="left", padx=(0, 15))

        def agregar_materia():
            nombre = materia_entry.get().strip()
            if nombre:
                self.user["materias"].append(nombre)
                self.save_user_data()
                materia_entry.delete(0, "end")
                actualizar_lista()

        ctk.CTkButton(input_frame, text="Agregar Materia", command=agregar_materia, height=45, corner_radius=10, fg_color=color, hover_color=hover, font=("Segoe UI", 14, "bold")).pack(side="left")

        self.lista_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, pady=20)

        def actualizar_lista():
            for widget in self.lista_frame.winfo_children():
                widget.destroy()

            if len(self.user["materias"]) == 0:
                ctk.CTkLabel(self.lista_frame, text="No hay materias registradas aún. ¡Empieza agregando una!", text_color="gray", font=("Segoe UI", 14)).pack(pady=20)
                return

            for materia in self.user["materias"]:
                fila = ctk.CTkFrame(self.lista_frame, corner_radius=12)
                fila.pack(fill="x", pady=8)

                ctk.CTkLabel(fila, text=materia, font=("Segoe UI", 16, "bold")).pack(side="left", padx=25, pady=20)

                def eliminar(m=materia):
                    self.user["materias"].remove(m)
                    self.save_user_data()
                    actualizar_lista()

                ctk.CTkButton(fila, text="Eliminar", fg_color="#ef4444", hover_color="#dc2626", corner_radius=8, width=90, height=35, command=eliminar).pack(side="right", padx=20)

        actualizar_lista()

    # ================= TAREAS =================
    def show_tareas(self):
        self.clear_main_area()
        color = self.theme_colors["Tareas"]["main"]
        hover = self.theme_colors["Tareas"]["hover"]

        ctk.CTkLabel(self.main_area, text="📝 Agenda de Tareas", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 20), anchor="w")

        if "tareas" not in self.user: self.user["tareas"] = []

        if not self.user.get("materias"):
            ctk.CTkLabel(self.main_area, text="⚠️ Por favor, registra al menos una materia antes de crear tareas.", text_color="gray", font=("Segoe UI", 14)).pack(pady=20, anchor="w")
            return

        form_card = ctk.CTkFrame(self.main_area, corner_radius=15)
        form_card.pack(fill="x", pady=10)

        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(20, 10))
        materia_var = tk.StringVar(value=self.user["materias"][0])
        ctk.CTkOptionMenu(row1, values=self.user["materias"], variable=materia_var, width=180, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left", padx=(0, 10))
        tarea_entry = ctk.CTkEntry(row1, placeholder_text="Nombre de la tarea", height=35)
        tarea_entry.pack(side="left", expand=True, fill="x")

        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 10))
        desc_entry = ctk.CTkEntry(row2, placeholder_text="Descripción o detalles de la tarea...", height=35)
        desc_entry.pack(fill="x", expand=True)

        row3 = ctk.CTkFrame(form_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(row3, text="Fecha límite:", font=("Segoe UI", 13, "bold")).pack(side="left", padx=(0, 10))
        
        fecha_entry = DateEntry(row3, width=12, background=color, foreground='white', borderwidth=0, date_pattern='dd/mm/yyyy', font=("Segoe UI", 12))
        fecha_entry.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(row3, text="Hora:", font=("Segoe UI", 13, "bold")).pack(side="left", padx=(0, 5))
        horas = [f"{i:02d}" for i in range(24)]
        minutos = ["00", "15", "30", "45", "59"]
        
        hora_var = tk.StringVar(value="23")
        ctk.CTkOptionMenu(row3, values=horas, variable=hora_var, width=70, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left")
        ctk.CTkLabel(row3, text=":", font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
        min_var = tk.StringVar(value="59")
        ctk.CTkOptionMenu(row3, values=minutos, variable=min_var, width=70, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left", padx=(0, 20))

        prioridad_var = tk.StringVar(value="Normal")
        ctk.CTkOptionMenu(row3, values=["Alta", "Normal", "Baja"], variable=prioridad_var, width=110, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left", padx=(0, 10))

        def agregar_tarea():
            nombre = tarea_entry.get().strip()
            if not nombre: return
            nueva_tarea = {
                "nombre": nombre, "descripcion": desc_entry.get().strip(),
                "materia": materia_var.get(), "fecha": fecha_entry.get(), 
                "hora": f"{hora_var.get()}:{min_var.get()}", "prioridad": prioridad_var.get(), "hecha": False
            }
            self.user["tareas"].append(nueva_tarea)
            self.save_user_data()
            tarea_entry.delete(0, "end")
            desc_entry.delete(0, "end")
            actualizar_lista()

        ctk.CTkButton(row3, text="Crear Tarea", command=agregar_tarea, fg_color=color, hover_color=hover, font=("Segoe UI", 14, "bold"), corner_radius=10).pack(side="right")

        self.lista_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, pady=10)

        def actualizar_lista():
            for widget in self.lista_frame.winfo_children(): widget.destroy()
            if len(self.user["tareas"]) == 0:
                ctk.CTkLabel(self.lista_frame, text="¡Estás al día! No tienes tareas pendientes.", text_color="gray", font=("Segoe UI", 14)).pack(pady=20)
                return

            for tarea in self.user["tareas"]:
                fila = ctk.CTkFrame(self.lista_frame, corner_radius=12)
                fila.pack(fill="x", pady=6)

                color_estado = "gray" if tarea["hecha"] else color
                tachado = "overstrike" if tarea["hecha"] else "normal"
                
                info_frame = ctk.CTkFrame(fila, fg_color="transparent")
                info_frame.pack(side="left", padx=20, pady=10, fill="x", expand=True)

                ctk.CTkLabel(info_frame, text=tarea['nombre'], font=("Segoe UI", 18, "bold", tachado), text_color=color_estado).pack(anchor="w")
                detalles = f"{tarea['materia']}  •  Entrega: {tarea['fecha']} a las {tarea.get('hora', '23:59')}  •  Prioridad: {tarea['prioridad']}"
                ctk.CTkLabel(info_frame, text=detalles, font=("Segoe UI", 13), text_color="gray").pack(anchor="w")
                
                if tarea.get("descripcion", ""):
                    ctk.CTkLabel(info_frame, text=f"Detalles: {tarea['descripcion']}", font=("Segoe UI", 13, "italic")).pack(anchor="w", pady=(2,0))

                def marcar(t=tarea):
                    t["hecha"] = not t["hecha"]
                    self.save_user_data()
                    actualizar_lista()

                def eliminar(t=tarea):
                    self.user["tareas"].remove(t)
                    self.save_user_data()
                    actualizar_lista()

                btn_text = "Deshacer" if tarea["hecha"] else "Completar"
                ctk.CTkButton(fila, text=btn_text, width=100, corner_radius=8, fg_color=color if not tarea["hecha"] else "gray", hover_color=hover if not tarea["hecha"] else "darkgray", command=marcar).pack(side="right", padx=(0, 20))
                ctk.CTkButton(fila, text="X", width=40, corner_radius=8, fg_color="transparent", text_color="#ef4444", hover_color="#fee2e2", command=eliminar).pack(side="right", padx=(0, 10))

        actualizar_lista()

    # ================= EXÁMENES =================
    def show_examenes(self):
        self.clear_main_area()
        color = self.theme_colors["Exámenes"]["main"]
        hover = self.theme_colors["Exámenes"]["hover"]

        ctk.CTkLabel(self.main_area, text="📖 Control de Exámenes", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 20), anchor="w")

        if "examenes" not in self.user: self.user["examenes"] = []

        if not self.user.get("materias"):
            ctk.CTkLabel(self.main_area, text="⚠️ Por favor, registra al menos una materia antes de agendar exámenes.", text_color="gray", font=("Segoe UI", 14)).pack(pady=20, anchor="w")
            return

        form_card = ctk.CTkFrame(self.main_area, corner_radius=15)
        form_card.pack(fill="x", pady=10)

        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(20, 10))
        materia_var = tk.StringVar(value=self.user["materias"][0])
        ctk.CTkOptionMenu(row1, values=self.user["materias"], variable=materia_var, width=180, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left", padx=(0, 10))
        examen_entry = ctk.CTkEntry(row1, placeholder_text="Tema o título del examen", height=35)
        examen_entry.pack(side="left", fill="x", expand=True)

        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 10))
        desc_entry = ctk.CTkEntry(row2, placeholder_text="Temario, aula, requerimientos o detalles extra...", height=35)
        desc_entry.pack(fill="x", expand=True)

        row3 = ctk.CTkFrame(form_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(row3, text="Fecha:", font=("Segoe UI", 13, "bold")).pack(side="left", padx=(0, 10))
        fecha_entry = DateEntry(row3, width=12, background=color, foreground='white', borderwidth=0, date_pattern='dd/mm/yyyy', font=("Segoe UI", 12))
        fecha_entry.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(row3, text="Hora:", font=("Segoe UI", 13, "bold")).pack(side="left", padx=(0, 5))
        horas = [f"{i:02d}" for i in range(24)]
        minutos = ["00", "15", "30", "45"]
        
        hora_var = tk.StringVar(value="08")
        ctk.CTkOptionMenu(row3, values=horas, variable=hora_var, width=70, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left")
        ctk.CTkLabel(row3, text=":", font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
        min_var = tk.StringVar(value="00")
        ctk.CTkOptionMenu(row3, values=minutos, variable=min_var, width=70, fg_color=color, button_color=hover, button_hover_color=color).pack(side="left", padx=(0, 15))

        def agregar_examen():
            nombre = examen_entry.get().strip()
            if not nombre: return
            nuevo_examen = {
                "nombre": nombre, "descripcion": desc_entry.get().strip(),
                "materia": materia_var.get(), "fecha": fecha_entry.get(), 
                "hora": f"{hora_var.get()}:{min_var.get()}", "realizado": False, "nota": ""
            }
            self.user["examenes"].append(nuevo_examen)
            self.save_user_data()
            examen_entry.delete(0, "end")
            desc_entry.delete(0, "end")
            actualizar_lista()

        ctk.CTkButton(row3, text="Agendar Examen", command=agregar_examen, fg_color=color, hover_color=hover, font=("Segoe UI", 14, "bold"), corner_radius=10).pack(side="right")

        self.lista_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, pady=10)

        def actualizar_lista():
            for widget in self.lista_frame.winfo_children(): widget.destroy()
            if len(self.user["examenes"]) == 0:
                ctk.CTkLabel(self.lista_frame, text="No tienes exámenes programados en puerta.", text_color="gray", font=("Segoe UI", 14)).pack(pady=20)
                return

            for examen in self.user["examenes"]:
                fila = ctk.CTkFrame(self.lista_frame, corner_radius=12)
                fila.pack(fill="x", pady=6)

                info_frame = ctk.CTkFrame(fila, fg_color="transparent")
                info_frame.pack(side="left", padx=20, pady=10, fill="x", expand=True)

                titulo = f"{examen['nombre']} - Calificación: {examen.get('nota', 'Pendiente')}" if examen["realizado"] else examen['nombre']
                ctk.CTkLabel(info_frame, text=titulo, font=("Segoe UI", 18, "bold"), text_color=color).pack(anchor="w")
                
                detalles = f"{examen['materia']}  •  Fecha: {examen['fecha']} a las {examen.get('hora', '08:00')}"
                ctk.CTkLabel(info_frame, text=detalles, font=("Segoe UI", 13), text_color="gray").pack(anchor="w")
                
                desc_str = examen.get("descripcion", examen.get("notas", ""))
                if desc_str:
                    ctk.CTkLabel(info_frame, text=f"Detalles: {desc_str}", font=("Segoe UI", 13, "italic")).pack(anchor="w", pady=(2,0))

                def registrar_resultado(e=examen):
                    dialog = ctk.CTkInputDialog(text="Ingresa la calificación obtenida:", title="Resultado del Examen")
                    nota_input = dialog.get_input()
                    if nota_input is not None:
                        e["realizado"] = True
                        e["nota"] = nota_input
                        self.save_user_data()
                        actualizar_lista()

                def eliminar(e=examen):
                    self.user["examenes"].remove(e)
                    self.save_user_data()
                    actualizar_lista()

                if not examen["realizado"]:
                    ctk.CTkButton(fila, text="Calificar", width=100, corner_radius=8, fg_color=color, hover_color=hover, command=registrar_resultado).pack(side="right", padx=(0, 20))
                else:
                    ctk.CTkLabel(fila, text="Finalizado ✅", text_color="#10b981", font=("Segoe UI", 14, "bold")).pack(side="right", padx=(0, 20))
                
                ctk.CTkButton(fila, text="X", width=40, corner_radius=8, fg_color="transparent", text_color="#ef4444", hover_color="#fee2e2", command=eliminar).pack(side="right", padx=(0, 10))

        actualizar_lista()

    # ================= POMODORO =================
    def show_pomodoro(self):
        self.clear_main_area()
        color = self.theme_colors["Pomodoro"]["main"]
        hover = self.theme_colors["Pomodoro"]["hover"]
        verde = self.theme_colors["Tareas"]["main"]

        ctk.CTkLabel(self.main_area, text="⏱️ Técnica Pomodoro", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 5), anchor="w")
        ctk.CTkLabel(self.main_area, text="Optimiza tu tiempo de estudio alternando bloques de enfoque y descansos.", text_color="gray", font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 30))

        timer_card = ctk.CTkFrame(self.main_area, corner_radius=20)
        timer_card.pack(pady=20, padx=50, fill="x")

        self.lbl_modo = ctk.CTkLabel(timer_card, text=f"Modo: {self.pomodoro_mode}", font=("Segoe UI", 20, "bold"), text_color=color)
        self.lbl_modo.pack(pady=(40, 5))

        self.lbl_timer = ctk.CTkLabel(timer_card, text=self.format_time(self.pomodoro_time_left), font=("Consolas", 80, "bold"))
        self.lbl_timer.pack(pady=10)

        btn_frame = ctk.CTkFrame(timer_card, fg_color="transparent")
        btn_frame.pack(pady=(10, 40))

        texto_btn = "Pausar" if self.pomodoro_running else "Iniciar Sesión"
        self.btn_start = ctk.CTkButton(btn_frame, text=texto_btn, font=("Segoe UI", 16, "bold"), width=140, height=45, corner_radius=10, fg_color=color, hover_color=hover, command=self.toggle_pomodoro)
        self.btn_start.pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="Reiniciar", fg_color="gray", hover_color="darkgray", font=("Segoe UI", 16, "bold"), width=140, height=45, corner_radius=10, command=self.reset_pomodoro).pack(side="left", padx=15)

        modo_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        modo_frame.pack(pady=20)

        ctk.CTkButton(modo_frame, text="Enfoque (25m)", fg_color=color, hover_color=hover, width=160, height=45, corner_radius=10, font=("Segoe UI", 14, "bold"),
                      command=lambda: self.set_pomodoro_mode("Trabajo", 25)).pack(side="left", padx=15)
        ctk.CTkButton(modo_frame, text="Descanso Corto (5m)", fg_color=verde, hover_color="#059669", width=160, height=45, corner_radius=10, font=("Segoe UI", 14, "bold"),
                      command=lambda: self.set_pomodoro_mode("Descanso", 5)).pack(side="left", padx=15)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def toggle_pomodoro(self):
        self.pomodoro_running = not self.pomodoro_running
        if self.pomodoro_running:
            self.btn_start.configure(text="Pausar")
            self.update_timer()
        else:
            self.btn_start.configure(text="Reanudar")

    def reset_pomodoro(self):
        self.pomodoro_running = False
        if hasattr(self, 'btn_start') and self.btn_start.winfo_exists():
            self.btn_start.configure(text="Iniciar Sesión")
        self.pomodoro_time_left = 25 * 60 if self.pomodoro_mode == "Trabajo" else 5 * 60
        if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
            self.lbl_timer.configure(text=self.format_time(self.pomodoro_time_left))

    def set_pomodoro_mode(self, mode, mins):
        self.pomodoro_running = False
        self.pomodoro_mode = mode
        self.pomodoro_time_left = mins * 60
        if hasattr(self, 'lbl_modo') and self.lbl_modo.winfo_exists():
            self.lbl_modo.configure(text=f"Modo: {self.pomodoro_mode}")
        if hasattr(self, 'btn_start') and self.btn_start.winfo_exists():
            self.btn_start.configure(text="Iniciar Sesión")
        if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
            self.lbl_timer.configure(text=self.format_time(self.pomodoro_time_left))

    def update_timer(self):
        if not self.pomodoro_running: return
        if self.pomodoro_time_left > 0:
            self.pomodoro_time_left -= 1
            if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
                self.lbl_timer.configure(text=self.format_time(self.pomodoro_time_left))
            self.after(1000, self.update_timer)
        else:
            self.pomodoro_running = False
            if hasattr(self, 'btn_start') and self.btn_start.winfo_exists():
                self.btn_start.configure(text="Iniciar Sesión")
            if self.pomodoro_mode == "Trabajo":
                messagebox.showinfo("¡Bloque Completado!", "Has completado un bloque de estudio. ¡Es hora de un descanso!")
            else:
                messagebox.showinfo("¡Descanso Terminado!", "Descanso finalizado. Prepárate para el próximo bloque.")

    # ================= ESTADÍSTICAS =================
    def show_estadisticas(self):
        self.clear_main_area()
        color = self.theme_colors["Estadísticas"]["main"]
        color_tareas = self.theme_colors["Tareas"]["main"]
        color_examenes = self.theme_colors["Exámenes"]["main"]

        ctk.CTkLabel(self.main_area, text="📊 Rendimiento Académico", font=("Segoe UI", 30, "bold"), text_color=color).pack(pady=(10, 20), anchor="w")

        stats_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, pady=10)

        tareas = self.user.get("tareas", [])
        tot_tar = len(tareas)
        comp_tar = sum(1 for t in tareas if t.get("hecha", False))
        pend_tar = tot_tar - comp_tar
        prog_tar = comp_tar / tot_tar if tot_tar > 0 else 0.0

        tareas_card = ctk.CTkFrame(stats_frame, corner_radius=15)
        tareas_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(tareas_card, text="Productividad de Tareas", font=("Segoe UI", 20, "bold"), text_color=color_tareas).pack(pady=(25, 5), padx=25, anchor="w")
        ctk.CTkLabel(tareas_card, text=f"Completadas: {comp_tar}   |   Pendientes: {pend_tar}   |   Total Registradas: {tot_tar}", font=("Segoe UI", 15), text_color="gray").pack(padx=25, anchor="w")
        
        bar_tar = ctk.CTkProgressBar(tareas_card, height=18, corner_radius=10, progress_color=color_tareas)
        bar_tar.pack(pady=(20, 25), padx=25, fill="x")
        bar_tar.set(prog_tar)

        examenes = self.user.get("examenes", [])
        tot_ex = len(examenes)
        comp_ex = sum(1 for e in examenes if e.get("realizado", False))
        pend_ex = tot_ex - comp_ex
        prog_ex = comp_ex / tot_ex if tot_ex > 0 else 0.0

        examenes_card = ctk.CTkFrame(stats_frame, corner_radius=15)
        examenes_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(examenes_card, text="Avance de Evaluaciones", font=("Segoe UI", 20, "bold"), text_color=color_examenes).pack(pady=(25, 5), padx=25, anchor="w")
        ctk.CTkLabel(examenes_card, text=f"Realizados: {comp_ex}   |   Pendientes: {pend_ex}   |   Total Registrados: {tot_ex}", font=("Segoe UI", 15), text_color="gray").pack(padx=25, anchor="w")
        
        bar_ex = ctk.CTkProgressBar(examenes_card, height=18, corner_radius=10, progress_color=color_examenes)
        bar_ex.pack(pady=(20, 25), padx=25, fill="x")
        bar_ex.set(prog_ex)


if __name__ == "__main__":
    default_data = {
        "username": "Estudiante",
        "materias": [],
        "tema": "System",
        "frase_personalizada": ""
    }
    app = UFlowA(default_data)
    app.mainloop()