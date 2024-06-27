from Cliente import Cliente
from Equipo import Equipo
from Estadio import Estadio
from Partido import Partido
from Producto import Producto
from Restaurante import Restaurante
from Entrada import Entrada
from Vip import Vip
from General import General

import datetime
import pickle
import random
# import matplotlib.pyplot as graficaa

class App:
    def __init__(self):
        self.estadios = []
        self.partidos = []
        self.entradas = []
        self.equipos = []
        self.clientes = []
        self.restaurantes = []
        self.productos = []

    """Función para registrar los datos del .json a objetos"""
    def register_data(self, teams, stadiums, matches):

        """Registrar los datos del equipo en el sistema"""
        for equipo in teams:
            """Crear el objeto Equipo y asignar sus atributos"""
            equipo = Equipo(equipo["id"], equipo["code"], equipo["name"], equipo["group"])
            self.equipos.append(equipo)

        """Registrar los datos del estadio en el sistema"""
        for estadio in stadiums:
            """Transformar los parámetros que sean listas en objetos"""
            lista_restaurantes = []
            for restaurante in estadio["restaurants"]:
                lista_productos = []
                for producto in restaurante["products"]:
                    producto = Producto(producto["name"], producto["quantity"], producto["price"], producto["stock"], producto["adicional"], )
                    self.productos.append(producto)
                    lista_productos.append(producto)
                restaurante = Restaurante(restaurante["name"], lista_productos)
                self.restaurantes.append(restaurante)
                lista_restaurantes.append(restaurante)

            """Crear el objeto Estadio y asignar sus atributos"""
            estadio = Estadio(estadio["id"], estadio["name"], estadio["city"], estadio["capacity"], lista_restaurantes)
            self.estadios.append(estadio)

        """Registrar los datos del partido en el sistema"""
        for partido in matches:
            """Transformar los parámetros que sean listas en objetos"""
            for equipo in self.equipos:
                if partido["home"]["id"] == equipo.id:
                    equipo_local = equipo
                elif partido["away"]["id"] == equipo.id:
                    equipo_visitante = equipo

            for estadio in self.estadios:
                if partido["stadium_id"] == estadio.id:
                    estadio_partido = estadio
            
            """Crear el objeto Partido y asignar sus atributos"""
            partido = Partido(partido["id"], partido["number"], equipo_local, equipo_visitante, partido["date"], partido["group"], estadio_partido)
            self.partidos.append(partido)

    def busqueda_partidos(self):
        print(f"""
Bienvenido/a a la búsqueda de partidos de la Eurocopa 2024
""")
        while True:
            print("""Seleccione un filtro...
        1. Ver todos los partidos disponibles
        2. Búsqueda de los partidos de un país
        3. Búsqueda de los partidos en un estadio específico
        4. Búsqueda de los partidos en una fecha determinada
        5. Volver al menú inicial
        """)
                
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,6):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                for i, partido in enumerate(self.partidos):
                    print(f"------------- {i+1} -------------")
                    print(partido.show())
            
            elif opcion == "2":
                eleccion_pais = input("Ingrese el nombre o código FIFA de un país (en inglés): ").lower()
                contador = 0
                for i, partido in enumerate(self.partidos):
                    if eleccion_pais in partido.local.nombre.lower() or eleccion_pais in partido.visitante.nombre.lower():
                        contador = 1
                        print(f"------------- {i+1} -------------")
                        print(partido.show())
                if contador == 0:
                    print("El país ingresado no fue conseguido")

            elif opcion == "3":
                eleccion_estadio = input("Ingrese un estadio de la Eurocopa: ").lower()
                contador = 0
                for i, partido in enumerate(self.partidos):
                    if eleccion_estadio in partido.id_estadio.nombre.lower():
                        contador = 1
                        print(f"------------- {i+1} -------------")
                        print(partido.show())
                if contador == 0:
                    print("El estadio ingresado no fue conseguido")
            
            elif opcion == "4":
                eleccion_fecha = input("Ingrese la fecha que desea ver un partido (AAAA-MM-DD): ")
                contador = 0
                for i, partido in enumerate(self.partidos):
                    if eleccion_fecha in partido.fecha:
                        contador = 1
                        print(f"------------- {i+1} -------------")
                        print(partido.show())
                if contador == 0:
                    print("No hay partidos en la fecha ingresada")

            else:
                break

    def registro_cliente(self):
        print(f"""
Bienvenido/a al registro OFICIAL de su persona en el sistema de la Eurocopa 2024...
""")
        
        nombre = input("Ingrese su primer nombre: ").capitalize().strip()
        while nombre == "" or not nombre.isalpha():
            print("Ingreso inválido...")
            nombre = input("Ingrese su primer nombre: ").capitalize().strip()

        apellido = input("Ingrese su primer apellido: ").capitalize().strip()
        while apellido == "" or not apellido.isalpha():
            print("Ingreso inválido...")
            apellido = input("Ingrese su primer apellido: ").capitalize().strip()

        nombre_completo = nombre + " " + apellido

        dni = input("Ingrese su cédula/DNI: ").strip()
        while len(dni) == 0 or not dni.isnumeric():
            print("Ingreso inválido...")
            dni = input("Ingrese su cédula/DNI: ").strip()

        while True:
            try:
                edad = int(input("Ingrese sus años de edad: "))
                if edad > 0 and edad < 100:
                    break
                else:
                    print("Ingreso inválido, coloque una edad real...")
            except ValueError:
                print("Ingreso inválido...")

        print("""
¡El cliente ha sido registrado exitosamente!
""")
        cliente = Cliente(nombre_completo, dni, edad)
        cliente.descuentos()
    
        return cliente

    def seleccion_partido(self, partidos_disponibles):
        print("""
PARTIDOS DISPONIBLES
""")
        for i, partido in enumerate(partidos_disponibles):
            print(f"------------- {i+1} -------------")
            print(partido.show())
            print(f"/////////////////////////////////")

        opcion = input("Ingrese el número de la opción que desea elegir: ")
        while not opcion.isnumeric() or int(opcion) not in range(1, len(partidos_disponibles)):
            print("Ingreso inválido...")
            opcion = input("Ingrese el número de la opción que desea elegir: ")
        
        print(f"""
PARTIDO SELECCIONADO: {partidos_disponibles[opcion - 1].local.nombre} VS. {partidos_disponibles[opcion - 1].visitante.nombre}
""")
        return partidos_disponibles[opcion - 1]

    def mapa_disponibilidad(self, juego_selec):
        mapa_estadio = []
        columnas = 10
        limite = juego_selec.estadio.capacidad[0] + juego_selec.estadio.capacidad[1]
        filas = limite // columnas
        lista_abc = []
        abc = "ABCDEFGHIJ"
        for letra1 in abc:
            for letra2 in abc:
                lista_abc.append(letra1 + letra2)

        asientos = []
        for i in range(filas):
            for j in range(1, columnas + 1):
                asientos.append(f"{lista_abc[i]}{j}")

        asientos_disponibles = []
        for asiento in asientos:
            if asiento not in juego_selec.asientos_tomados:
                asientos_disponibles.append(asiento)

        for i in lista_abc[:filas]:
            fila = []
            for j in range(1, columnas + 1):
                asiento1 = f"{i}{j}"
                if asiento1 in juego_selec.asientos_tomados:
                    fila.append(f"|   X  ")
                else:
                    fila.append(f"|  {asiento1} ")
            fila.append("|")
            mapa_estadio.append("".join(fila))
        
        seccion_actual = None
        for fila1 in mapa_estadio:
            seccion = fila1.split("|")[1].strip()[0]
            if seccion != seccion_actual:
                seccion_actual = seccion
                if seccion_actual != "A":
                    print("-" * len(fila1))
                print(f"""

============================== ZONA: '{seccion_actual}' ===============================
""")
            print("-" * len(fila1))
            print(fila1)
        print("-" * len(mapa_estadio[-1]))

        asiento_elegido = input("Ingrese el asiento desde donde desee ver el partido (Ej: AA1): ")
        while asiento_elegido not in asientos_disponibles:
            print("El asiento ingresado NO existe o está OCUPADO...")

        print(f"""
ASIENTO SELECCIONADO: {asiento_elegido}
""")
        return asiento_elegido

    def compra_entrada(self):
        ans = input("""
¿Se encuentra registrado? [s/n]: """)
        while ans not in ["s", "n"]:
            print("Ingreso inválido...")
            ans = input("¿Se encuentra registrado? [s/n]: ")
        
        if ans == "s":
            dni = input("Ingrese su cédula/DNI: ")
            while len(dni) == 0 or not dni.isnumeric():
                print("Ingreso inválido...")
                dni = input("Ingrese su cédula/DNI: ")
            
            if self.binary_search(self.clientes, 0, len(self.clientes) - 1, dni, lambda x: x.dni) == -1:
                print("¡El cliente no se encuentra registrado! Su DNI no se encontró...")
                self.compra_entrada()
            
            ind = self.binary_search(self.clientes, 0, len(self.clientes) - 1, dni, lambda x: x.dni)
            cliente = self.clientes[ind]
            
        else:
            cliente = self.registro_cliente()

        partidos_disponibles = []
        for partido in self.partidos:
            if partido.entradas_general > 0 or partido.entradas_vip > 0:
                partidos_disponibles.append(partido)
        
        juego_selec = self.seleccion_partido(partidos_disponibles)


        # if cliente.descuento_entrada():
        #     print("¡Por su DNI, ha sido beneficiado con un 50% de descuento en la compra de entradas!")

        print("""
ENTRADAS DISPONIBLES
--------------------
""")


    def binary_search(self, list, min, max, x, key = lambda x: x):
        if len(list) != 0:
            mid = len(list) // 2
            if key(list[mid]) == x:
                return mid
            elif key(list[mid]) > x:
                return self.binary_search(list, min, mid - 1, x, key)
            elif key(list[mid]) < x:
                return self.binary_search(list, min + 1, max, x, key)
        else:
            return -1

    def menu(self, teams, stadiums, matches):
        self.register_data(teams, stadiums, matches)
        print(f"""
--- BIENVENIDO/A A LA EUROCOPA 2024 ---
""")
        while True:
            print("""Ingrese una opción...
        1. Búsqueda de partidos
        2. Compra de entradas
        3. Confirmación de asistencia
        4. Acerca de los restaurantes
        5. Revisión de estadísticas
        6. Salir
        """)
                
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,7):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                self.busqueda_partidos()
            elif opcion == "2":
                self.compra_entrada()
            elif opcion == "3":
                pass
            elif opcion == "4":
                pass
            elif opcion == "5":
                pass
            elif opcion == "6":
                pass