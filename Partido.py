class Partido:

    def __init__(self, id, numero, local, visitante, fecha, grupo, id_estadio):
        self.id = id
        self.numero = numero
        self.local = local
        self.visitante = visitante
        self.fecha = fecha
        self.grupo = grupo
        self.id_estadio = id_estadio

    """Mostrar los datos completos del partido"""

    def show(self):
        return f"""
INFORMACIÓN DEL PARTIDO
=======================
ID: {self.id}
NUMERO: {self.numero}
EQUIPO LOCAL: {self.local.nombre}
EQUIPO VISITANTE: {self.visitante.nombre}
FECHA: {self.fecha}
GRUPO: {self.grupo}
ESTADIO: {self.id_estadio.nombre}
"""