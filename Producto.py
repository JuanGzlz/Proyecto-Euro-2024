class Producto:

    def __init__(self, nombre, ventas, precio, stock, adicional):
        self.nombre = nombre
        self.ventas = ventas
        self.precio = precio # * 1.16
        self.stock = stock
        self.adicional = adicional
        self.cantidad_gastada = 0

    def ventas_stock(self, cantidad):
        self.stock -= cantidad
        self.ventas += cantidad

    # def dinero_gastado(self):
    #     self.cantidad_gastada = self.ventas * self.precio

    def show(self):
        return f"""
INFORMACIÓN DEL PRODUCTO
========================
{self.nombre}
CONTENIDO: {self.adicional}
PRECIO: {self.precio}
CANTIDAD RESTANTE: {self.stock}
CANTIDAD VENDIDA: {self.ventas}
"""