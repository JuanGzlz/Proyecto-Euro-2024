class Estadio:

    def __init__(self, id, nombre, ciudad, capacidad, restaurantes):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.capacidad = capacidad
        self.restaurantes = restaurantes

    """Mostrar los datos completos del estadio"""

    def show(self):
        print(f"""
INFORMACIÓN DEL ESTADIO
=======================
ID: {self.id}
NOMBRE: {self.nombre}
CIUDAD: {self.ciudad}
CAPACIDAD: {self.capacidad[0] + self.capacidad[1]}
=======================
RESTAURANTES: """)
        for i, restaurante in enumerate(self.restaurantes):
            print(f"----------- {i+1} -----------")
            restaurante.show()

