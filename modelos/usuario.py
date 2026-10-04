class Usuario:
    def __init__(self, id_usuario, nombre, usuario, contrasena, rol="Cliente"):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol  # "Administrador", "Empleado" o "Cliente"

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id_usuario=data["id_usuario"],
            nombre=data["nombre"],
            usuario=data["usuario"],
            contrasena=data["contrasena"],
            rol=data.get("rol", "Cliente")
        )