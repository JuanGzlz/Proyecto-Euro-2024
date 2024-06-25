class Equipo:

    def __init__(self, id, codigo, nombre, grupo):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.grupo = grupo

    """Mostrar los datos completos del equipo"""

    def show(self):
        return f"""
INFORMACIÓN DEL EQUIPO
=======================
ID: {self.id}
CÓDIGO FIFA: {self.codigo}
NOMBRE: {self.nombre}
GRUPO: {self.grupo}
"""