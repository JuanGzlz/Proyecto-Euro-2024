class Partido:

    def __init__(self, id, numero, local, visitante, fecha, grupo, estadio):
        self.id = id
        self.numero = numero
        self.local = local
        self.visitante = visitante
        self.fecha = fecha
        self.grupo = grupo
        self.estadio = estadio
        self.entradas_general = estadio.capacidad[0]
        self.entradas_vip = estadio.capacidad[1]
        self.asientos_tomados = []
        self.asistencia_confirmada = 0

    """Mostrar los datos completos del partido"""

    def show(self):
        return f"""
INFORMACIÓN DEL PARTIDO Nº {self.numero}
=============================
ID: {self.id}
(LOC.) {self.local.nombre} VS. {self.visitante.nombre} (VIS.)
FECHA: {self.fecha}
GRUPO: {self.grupo}
ESTADIO: {self.estadio.nombre}
CAPACIDAD: {self.estadio.capacidad[0] + self.estadio.capacidad[1]} personas
ENTRADAS DISPONIBLES: {self.entradas_general + self.entradas_vip}
ENTRADAS VENDIDAS: {len(self.asientos_tomados)}
CONFIRMADOS: {self.asistencia_confirmada}
"""