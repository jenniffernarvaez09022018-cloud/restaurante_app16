import os
import tkinter as tk
from tkinter import ttk, messagebox
from modelos.usuario import Usuario

class MainView(tk.Tk):
    def __init__(self, servicio, usuario_actual):
        super().__init__()
        self.servicio = servicio
        self.usuario_actual = usuario_actual

        self.title(f"Restaurante App - Bienvenido {usuario_actual.nombre} ({usuario_actual.rol})")
        self.geometry("850x600")

        self.crear_interfaz()
        self.configurar_eventos()

    def crear_interfaz(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", padx=10, pady=5)

        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_gif = os.path.normpath(os.path.join(dir_actual, "..", "assets", "logo.gif"))

        if os.path.exists(ruta_gif):
            try:
                # Reducimos la imagen dividiendo sus dimensiones por 8 para que quede como un icono pequeño arriba
                self.logo_img = tk.PhotoImage(file=ruta_gif).subsample(8, 8)
                self.iconphoto(False, self.logo_img)
                lbl_logo = ttk.Label(frame_top, image=self.logo_img)
                lbl_logo.pack(side="left", padx=5)
            except Exception as e:
                print(f"Error imagen main: {e}")

        ttk.Label(frame_top, text=f"Usuario Activo: {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}", font=("Helvetica", 10, "bold")).pack(side="right", padx=5)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        frame_usuarios = ttk.Frame(notebook)
        notebook.add(frame_usuarios, text="Gestión de Usuarios")

        if self.usuario_actual.rol != "Administrador":
            ttk.Label(frame_usuarios, text="Acceso restringido solo para Administradores.", font=("Helvetica", 12)).pack(pady=50)
        else:
            self.construir_modulo_usuarios(frame_usuarios)

        frame_productos = ttk.Frame(notebook)
        notebook.add(frame_productos, text="Productos")
        self.construir_modulo_productos(frame_productos)

    def construir_modulo_usuarios(self, parent):
        frame_form = ttk.LabelFrame(parent, text=" Formulario de Usuario ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.txt_id = ttk.Entry(frame_form)
        self.txt_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.txt_nombre = ttk.Entry(frame_form)
        self.txt_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Usuario:").grid(row=1, column=0, padx=5, pady=5)
        self.txt_usuario = ttk.Entry(frame_form)
        self.txt_usuario.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Rol:").grid(row=1, column=2, padx=5, pady=5)
        self.cmb_rol = ttk.Combobox(frame_form, values=["Administrador", "Empleado", "Cliente"], state="readonly")
        self.cmb_rol.set("Cliente")
        self.cmb_rol.grid(row=1, column=3, padx=5, pady=5)

        frame_botones = ttk.Frame(parent)
        frame_botones.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_botones, text="Registrar", command=self.btn_registrar_click).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Actualizar", command=self.btn_actualizar_click).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.btn_eliminar_click).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Limpiar (Esc)", command=self.limpiar_formulario).pack(side="left", padx=5)

        self.tabla = ttk.Treeview(parent, columns=("ID", "Nombre", "Usuario", "Rol"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Usuario", text="Usuario")
        self.tabla.heading("Rol", text="Rol")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.cargar_tabla_usuarios()

    def configurar_eventos(self):
        if self.usuario_actual.rol == "Administrador":
            self.tabla.bind("<<TreeviewSelect>>", self.on_treeview_select)
            self.cmb_rol.bind("<<ComboboxSelected>>", self.on_combobox_selected)
            self.bind_all("<Return>", self.on_key_return)
            self.bind_all("<Escape>", self.on_key_escape)

    def on_treeview_select(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        
        item = self.tabla.item(seleccion[0])
        id_usuario = item["values"][0]

        usuario = self.servicio.obtener_usuario_por_id(str(id_usuario))
        if usuario:
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, usuario.id_usuario)
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, usuario.nombre)
            self.txt_usuario.delete(0, tk.END)
            self.txt_usuario.insert(0, usuario.usuario)
            self.cmb_rol.set(usuario.rol)

    def on_combobox_selected(self, event):
        print(f"Cambio de rol en Combobox a: {self.cmb_rol.get()}")

    def on_key_return(self, event):
        self.btn_registrar_click()

    def on_key_escape(self, event):
        self.limpiar_formulario()

    def btn_registrar_click(self):
        try:
            if not self.txt_id.get() or not self.txt_usuario.get():
                messagebox.showwarning("Atención", "Por favor llene los campos requeridos.")
                return

            nuevo_u = Usuario(
                id_usuario=self.txt_id.get(),
                nombre=self.txt_nombre.get(),
                usuario=self.txt_usuario.get(),
                contrasena="1234",
                rol=self.cmb_rol.get()
            )
            self.servicio.registrar_usuario(nuevo_u)
            self.cargar_tabla_usuarios()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def btn_actualizar_click(self):
        try:
            u_mod = Usuario(
                id_usuario=self.txt_id.get(),
                nombre=self.txt_nombre.get(),
                usuario=self.txt_usuario.get(),
                contrasena="1234",
                rol=self.cmb_rol.get()
            )
            if self.servicio.actualizar_usuario(u_mod):
                self.cargar_tabla_usuarios()
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            else:
                messagebox.showwarning("Atención", "No se encontró el usuario para actualizar.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def btn_eliminar_click(self):
        id_u = self.txt_id.get()
        if not id_u:
            messagebox.showwarning("Atención", "Seleccione un usuario de la lista.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario {id_u}?"):
            try:
                self.servicio.eliminar_usuario(id_u, self.usuario_actual.id_usuario)
                self.cargar_tabla_usuarios()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", "Usuario eliminado.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_usuario.delete(0, tk.END)
        self.cmb_rol.set("Cliente")
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())

    def cargar_tabla_usuarios(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for u in self.servicio.obtener_usuarios():
            self.tabla.insert("", "end", values=(u.id_usuario, u.nombre, u.usuario, u.rol))

    def construir_modulo_productos(self, parent):
        tabla_p = ttk.Treeview(parent, columns=("ID", "Nombre", "Precio"), show="headings")
        tabla_p.heading("ID", text="ID Producto")
        tabla_p.heading("Nombre", text="Nombre")
        tabla_p.heading("Precio", text="Precio")
        tabla_p.pack(fill="both", expand=True, padx=10, pady=10)

        for p in self.servicio.obtener_productos():
            tabla_p.insert("", "end", values=(p.id_producto, p.nombre, f"${p.precio:.2f}"))