class Producto:

    def __init__(self, nombre, ventas, precio, estadio, stock, adicional):
        self.nombre = nombre
        self.ventas = ventas
        self.precio = float(precio) * 1.16
        self.estadio = estadio
        self.stock = int(stock)
        self.adicional = adicional
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
ESTADIO: {self.estadio}
CANTIDAD RESTANTE: {self.stock}
CANTIDAD VENDIDA: {self.ventas}
CAPITAL RECOGIDO: {self.cantidad_gastada}"""