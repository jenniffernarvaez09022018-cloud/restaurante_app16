import os
import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Tk):
    def __init__(self, servicio, on_login_success):
        super().__init__()
        self.servicio = servicio
        self.on_login_success = on_login_success

        self.title("Restaurante App - Inicio de Sesión")
        self.geometry("380x480")  # Aumentamos un poco la altura para que todo quepa cómodo
        self.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_gif = os.path.normpath(os.path.join(dir_actual, "..", "assets", "logo.gif"))

        if os.path.exists(ruta_gif):
            try:
                # Reducimos la imagen dividiendo sus dimensiones por 4 (o ajústalo si queda muy grande/pequeña)
                self.logo_img = tk.PhotoImage(file=ruta_gif).subsample(4, 4)
                self.iconphoto(False, self.logo_img)
                lbl_logo = ttk.Label(self, image=self.logo_img)
                lbl_logo.pack(pady=10)
            except Exception as e:
                print(f"Error imagen login: {e}")

        ttk.Label(self, text="Inicio de Sesión", font=("Helvetica", 14, "bold")).pack(pady=5)

        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        ttk.Label(frame, text="Usuario:").pack(anchor="w", pady=(5, 2))
        self.txt_usuario = ttk.Entry(frame, width=30)
        self.txt_usuario.pack(fill="x")

        ttk.Label(frame, text="Contraseña:").pack(anchor="w", pady=(10, 2))
        self.txt_pass = ttk.Entry(frame, show="*", width=30)
        self.txt_pass.pack(fill="x")

        btn_ingresar = ttk.Button(frame, text="Ingresar", command=self.ingresar)
        btn_ingresar.pack(pady=20, fill="x")

        self.bind("<Return>", lambda e: self.ingresar())

    def ingresar(self):
        usr = self.txt_usuario.get()
        pwd = self.txt_pass.get()

        usuario_autenticado = self.servicio.autenticar(usr, pwd)
        if usuario_autenticado:
            self.destroy()
            self.on_login_success(usuario_autenticado)
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")