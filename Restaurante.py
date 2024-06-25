class Restaurante:

    def __init__(self, nombre, productos):
        self.nombre = nombre
        self.productos = []

    def show(self):
        return f"""
INFORMACIÓN DEL RESTAURANTE
===========================
NOMBRE: {self.nombre}

PRODUCTOS DISPONIBLES
===========================
NOMBRE: {self.productos}
PRECIO

#
#
#
#
"""