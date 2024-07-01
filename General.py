from Entrada import Entrada

class General(Entrada):

    def __init__(self, id, partido, estadio, asiento):
        super().__init__(id, partido, estadio, asiento)
        self.precio = 35

# Calcular el total a pagar por la entrada General, tomando en cuenta el descuento
    def precio_real(self):
        self.subtotal = self.precio
        if self.descuento:
            self.cantidad_descuento = self.subtotal * 0.5
        self.total = self.subtotal - self.cantidad_descuento + (self.subtotal * self.impuestos)

# Muestra la información de una entrada General
    def show(self):
        return f"""
INFO. ENTRADA GENERAL
=====================
{super().show()}"""