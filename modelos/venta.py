class Venta:
    def __init__(self, id_venta, cliente, productos, total):
        self.id_venta = id_venta
        self.cliente = cliente
        self.productos = productos
        self.total = float(total)

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "cliente": self.cliente,
            "productos": self.productos,
            "total": self.total
        }

    @staticmethod
    def from_dict(data):
        return Venta(
            id_venta=data["id_venta"],
            cliente=data["cliente"],
            productos=data["productos"],
            total=data["total"]
        )