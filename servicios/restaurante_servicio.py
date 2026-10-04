from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.ruta_usuarios = "datos/usuarios.json"
        self.ruta_productos = "datos/productos.json"
        self.ruta_ventas = "datos/ventas.json"

    # --- USUARIOS ---
    def obtener_usuarios(self):
        datos = ArchivoServicio.cargar_json(self.ruta_usuarios)
        return [Usuario.from_dict(u) for u in datos]

    def obtener_usuario_por_id(self, id_usuario):
        for u in self.obtener_usuarios():
            if u.id_usuario == id_usuario:
                return u
        return None

    def autenticar(self, usuario, contrasena):
        for u in self.obtener_usuarios():
            if u.usuario == usuario and u.contrasena == contrasena:
                return u
        return None

    def registrar_usuario(self, usuario_obj):
        usuarios = self.obtener_usuarios()
        if any(u.id_usuario == usuario_obj.id_usuario for u in usuarios):
            raise ValueError("El ID de usuario ya existe.")
        usuarios.append(usuario_obj)
        self._guardar_usuarios(usuarios)

    def actualizar_usuario(self, usuario_obj):
        usuarios = self.obtener_usuarios()
        for i, u in enumerate(usuarios):
            if u.id_usuario == usuario_obj.id_usuario:
                usuarios[i] = usuario_obj
                self._guardar_usuarios(usuarios)
                return True
        return False

    def eliminar_usuario(self, id_usuario, usuario_actual_id):
        if id_usuario == usuario_actual_id:
            raise ValueError("No puede eliminar la cuenta con la que está autenticado.")
        
        usuarios = self.obtener_usuarios()
        nuevos_usuarios = [u for u in usuarios if u.id_usuario != id_usuario]
        self._guardar_usuarios(nuevos_usuarios)

    def _guardar_usuarios(self, usuarios):
        data = [u.to_dict() for u in usuarios]
        ArchivoServicio.guardar_json(self.ruta_usuarios, data)

    # --- PRODUCTOS ---
    def obtener_productos(self):
        datos = ArchivoServicio.cargar_json(self.ruta_productos)
        return [Producto.from_dict(p) for p in datos]