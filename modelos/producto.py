class Producto:
    def __init__(self, id_producto, nombre, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = float(precio)

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            id_producto=data["id_producto"],
            nombre=data["nombre"],
            precio=data["precio"]
        )