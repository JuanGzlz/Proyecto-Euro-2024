class Entrada:

    def __init__(self, id, partido, estadio, asiento):
        self.id = id
        self.partido = partido
        self.estadio = estadio
        self.asiento = asiento
        self.descuento = False
        self.subtotal = 0
        self.cantidad_descuento = 0
        self.impuestos = 0.16
        self.total = 0

    def show(self):
        if self.descuento:
            return f"""
ENTRADA ID: {self.id}
PARTIDO: {self.partido.local.nombre} VS. {self.partido.visitante.nombre}
ESTADIO: {self.estadio.nombre}
ASIENTO: {self.asiento}
DESCUENTO DEL 50%: {self.descuento}
-------------------------
SUBTOTAL: {self.subtotal}$
DESCUENTO: {self.cantidad_descuento}$
IMPUESTOS (16%): {self.subtotal * self.impuestos}$
TOTAL: {self.total}$ 
"""
        else:
            return f"""
ENTRADA ID: {self.id}
PARTIDO: {self.partido.local.nombre} VS. {self.partido.visitante.nombre}
ESTADIO: {self.estadio.nombre}
ASIENTO: {self.asiento}
DESCUENTO DEL 50%: {self.descuento} 
-------------------------
SUBTOTAL: {self.subtotal}$
IMPUESTOS (16%): {self.subtotal * self.impuestos}$ 
TOTAL: {self.total}$ 
"""
