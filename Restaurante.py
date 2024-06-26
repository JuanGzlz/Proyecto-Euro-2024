class Restaurante:

    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []

    def show(self):
        print(f"""
INFORMACIÓN DEL RESTAURANTE
===========================
NOMBRE: {self.nombre}
===========================
PRODUCTOS: """)
        for i, producto in enumerate(self.productos):
            print(f"----------- {i+1} -----------")
            producto.show()