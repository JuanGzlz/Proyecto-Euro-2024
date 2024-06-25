from Cliente import Cliente
from Equipo import Equipo
from Estadio import Estadio
from Partido import Partido
from Producto import Producto
from Restaurante import Restaurante

import datetime
import pickle
# import matplotlib.pyplot as grafica

class App:
    def __init__(self):
        self.estadios = []
        self.partidos = []
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
                i = 0
                for partido in self.partidos:
                    i += 1
                    print(f"----------- {i} -----------")
                    print(partido.show())
            
            elif opcion == "2":
                eleccion_pais = input("Ingrese un país de la Eurocopa (en inglés): ").lower()
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_pais in partido.local.nombre.lower() or eleccion_pais in partido.visitante.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"----------- {i} -----------")
                        print(partido.show())
                if contador == 0:
                    print("El país ingresado no fue conseguido")

            elif opcion == "3":
                eleccion_estadio = input("Ingrese un estadio de la Eurocopa: ").lower()
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_estadio in partido.id_estadio.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"----------- {i} -----------")
                        print(partido.show())
                if contador == 0:
                    print("El estadio ingresado no fue conseguido")
            
            elif opcion == "4":
                eleccion_fecha = input("Ingrese la fecha que desea ver un partido de la Eurocopa (AAAA-DD-MM): ")
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_fecha in partido.fecha:
                        contador = 1
                        i += 1
                        print(f"----------- {i} -----------")
                        print(partido.show())
                if contador == 0:
                    print("No hay partidos en la fecha ingresada")

            else:
                break

    def inicio_sesion(self):
        print(f"""
Bienvenido/a al registro de su persona para obtener su entrada
""")
        
        nombre = input("Ingrese su primer nombre: ").capitalize()
        while nombre == "" or not nombre.isalpha():
            print("Ingreso inválido...")
            nombre = input("Ingrese su nombre completo: ")

        apellido = input("Ingrese su primer apellido: ").capitalize()
        while apellido == "" or not apellido.isalpha():
            print("Ingreso inválido...")
            apellido = input("Ingrese su nombre completo: ")

        nombre_completo = nombre + " " + apellido

        dni = input("Ingrese su DNI: ")
        while len(dni) == 0 or not dni.isnumeric():
            print("Ingreso inválido...")
            dni = input("Ingrese su DNI: ")

        edad = input("Ingrese sus años de edad: ")
        while edad <= 0 or edad > 100 or not edad.isnumeric():
            print("Ingreso inválido...")
            edad = input("Ingrese sus años de edad: ")

        cliente = Cliente(nombre_completo, dni, edad)

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
                pass
            elif opcion == "3":
                pass
            elif opcion == "4":
                pass
            elif opcion == "5":
                pass
            elif opcion == "6":
                pass