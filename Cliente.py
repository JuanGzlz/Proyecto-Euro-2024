from General import General
from Vip import Vip

class Cliente:

    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.descuento_entrada = False
        self.descuento_rest = False

    """Determinar si la cédula es un número vampiro para reconocer el descuento, debiendo aplicar permutaciones"""
    def permutacion(self, cedula):
        """Genera una lista con las permutaciones de los digitos de la cédula"""
        
        if len(cedula) == 1:
            return [cedula]
        
        permutaciones = []
        for i in range(len(cedula)):
            for j in self.permutacion(cedula[:i] + cedula[i+1:]):
                permutaciones.append(cedula[i] + j)
        return permutaciones
    
    def num_vampiro(self):
        """Determinar si la cédula es un número vampiro"""

        if len(self.cedula) % 2 != 0:
            return False

        permutaciones = self.permutacion(self.cedula)

        posibles_colmillos = []
        for p in permutaciones:
            mitad = len(p) // 2
            colmillo1 = p[:mitad]
            colmillo2 = p[mitad:]
            if not (colmillo1[-1] == "0" and colmillo2[-1] == "0"):
                posibles_colmillos.append(p)

        for p in posibles_colmillos:
            mitad = len(p) // 2
            a = int(p[:mitad])
            b = int(p[mitad:])
            if a * b == int(self.cedula):
                return True
        return False
    
    def num_perfecto(self):
        """Determinar si la cédula es un número perfecto"""

        suma = 0
        for i in range(1, int(self.cedula)):
            if int(self.cedula) % i == 0:
                suma += i
        if suma == int(self.cedula):
            return True
        return False
    
    def descuentos(self):
        if self.num_vampiro():
            self.descuento_entrada = True
            print("""
Usted ha obtenido el beneficio de un 50% de descuento en la compra de entradas
""")
        if self.num_perfecto():
            self.descuento_rest = True
            print("""
Usted ha obtenido el beneficio de un 15% de descuento en la compra de productos
""")

    # def entradas_compradas():
    #     vip_entradas = 0
    #     general_entradas = 0
    #     for entrada in self.entradas:


    """Mostrar los datos completos del cliente"""
    def show(self):
        return f"""
INFORMACIÓN DEL CLIENTE
=======================
NOMBRE: {self.nombre}
CÉDULA: {self.cedula}
EDAD: {self.edad} """
# PARTIDO QUE DESEA IR: {self.partido}
# TIPO DE ENTRADA: {self.entrada}