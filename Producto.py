class Producto:

    def __init__(self, nombre, ventas, precio, stock, adicional, restaurante, estadio):
        self.nombre = nombre
        self.ventas = ventas
        self.precio = float(precio) * 1.16
        self.stock = int(stock)
        self.adicional = adicional
        self.restaurante = restaurante
        self.estadio = estadio
        self.cantidad_gastada = 0

    def ventas_stock(self, cantidad):
        self.stock -= cantidad
        self.ventas += cantidad

    def dinero_gastado(self):
        self.cantidad_gastada = self.ventas * self.precio

    def show(self):
        return f"""
INFORMACIÓN DEL PRODUCTO
========================
{self.nombre}
CONTENIDO: {self.adicional}
PRECIO (IVA incluido): {self.precio}
CANTIDAD RESTANTE: {self.stock}
CANTIDAD VENDIDA: {self.ventas}
CAPITAL RECOGIDO: {self.cantidad_gastada}
========================
REST.: {self.restaurante}
ESTADIO: {self.estadio}"""