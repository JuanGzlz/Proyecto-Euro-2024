class Producto:

    def __init__(self, nombre, quantity, precio, stock, adicional):
        self.nombre = nombre
        self.quantity = quantity
        self.precio = precio
        self.stock = stock
        self.adicional = adicional

    def show(self):
        return f"""
INFORMACIÓN DEL PRODUCTO
========================
NOMBRE: {self.nombre}
CANTIDAD TOTAL: {self.quantity}
PRECIO: {self.precio}
CANTIDAD RESTANTE: {self.stock}
TIPO DE BEBIDA: {self.adicional}
"""