class Restaurante:

    def __init__(self, nombre, estadio):
        self.nombre = nombre
        self.estadio = estadio
        self.productos = []

    def show(self):
        print(f"""
INFORMACIÓN DEL RESTAURANTE
===========================
{self.nombre}
ESTADIO: {self.estadio}
===========================
PRODUCTOS: """)
        for i, producto in enumerate(self.productos):
            print(f"""
------------- {i+1} -------------""")
            producto.show()