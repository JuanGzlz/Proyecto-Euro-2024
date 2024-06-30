from Entrada import Entrada

class Vip(Entrada):

    def __init__(self, id, partido, estadio, asiento):
        super().__init__(id, partido, estadio, asiento)
        self.precio = 75

    def precio_real(self):
        self.subtotal = self.precio
        if self.descuento:
            self.cantidad_descuento = self.subtotal * 0.5
        self.total = self.subtotal - self.cantidad_descuento + (self.subtotal * self.impuestos)

    def show(self):
        return f"""
INFO. ENTRADA V.I.P
====================
{super().show()}"""