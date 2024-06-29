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
import matplotlib.pyplot as grafica
import numpy as np

class App:
    def __init__(self):
        self.estadios = []
        self.partidos = []
        self.entradas = []
        self.tipo_entradas = {"General": [], "Vip": []}
        self.entradas_verificadas = []
        self.equipos = []
        self.clientes = []
        self.restaurantes = []
        self.productos = []
        self.bebidas = []
        self.comidas = []

    def binary_search(self, lista_arg, min, max, x, key = lambda x: x):
        if max >= min:
            mid = (max + min) // 2
            if key(lista_arg[mid]) == x:
                return mid
            elif key(lista_arg[mid]) > x:
                return self.binary_search(lista_arg, min, mid - 1, x, key)
            else:
                return self.binary_search(lista_arg, mid + 1, max, x, key)
        else:
            return -1

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
                    producto = Producto(producto["name"], producto["quantity"], producto["price"], producto["stock"], producto["adicional"])
                    self.productos.append(producto)
                    lista_productos.append(producto)
                    
                restaurante = Restaurante(restaurante["name"], lista_productos)
                self.restaurantes.append(restaurante)
                lista_restaurantes.append(restaurante)

            """Crear el objeto Estadio y asignar sus atributos"""
            estadio = Estadio(estadio["id"], estadio["name"], estadio["city"], estadio["capacity"], lista_restaurantes)
            self.estadios.append(estadio)

        """Clasificar los productos en Bebidas y Comidas"""
        for producto1 in self.productos:
            if producto1.adicional == "alcoholic" or producto1.adicional == "non-alcoholic":
                self.bebidas.append(producto1)
            else:
                self.comidas.append(producto1)

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
                    print(f"------------- {i} -------------")
                    print(partido.show())
            
            elif opcion == "2":
                eleccion_pais = input("Ingrese el nombre o código FIFA de un país (en inglés): ").lower()
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_pais in partido.local.nombre.lower() or eleccion_pais in partido.visitante.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"------------- {i} -------------")
                        print(partido.show())
                if contador == 0:
                    print("El país ingresado no fue conseguido")

            elif opcion == "3":
                eleccion_estadio = input("Ingrese un estadio de la Eurocopa: ").lower()
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_estadio in partido.estadio.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"------------- {i} -------------")
                        print(partido.show())
                if contador == 0:
                    print("El estadio ingresado no fue conseguido")
            
            elif opcion == "4":
                eleccion_fecha = input("Ingrese la fecha que desea ver un partido (AAAA-MM-DD): ")
                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_fecha in partido.fecha:
                        contador = 1
                        i += 1
                        print(f"------------- {i} -------------")
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

        while True:
            try:
                dni = input("Ingrese su cédula/DNI: ").strip()
                if len(dni) == 0 or not dni.isnumeric():
                    raise Exception
                j = self.binary_search(self.clientes, 0, len(self.clientes) - 1, dni, lambda x: x.cedula)
                if j != -1:
                    print("La cédula/DNI ya se encuentra registrada...")
                    raise Exception
                break
            except:
                print("Ingreso inválido...")

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

    def seleccion_partido(self):
        partidos_disponibles = []
        for partido in self.partidos:
            if partido.entradas_general > 0 or partido.entradas_vip > 0:
                partidos_disponibles.append(partido)

        print("""Bienvenido/a a la selección del partido que desea ver de la Eurocopa 2024...

PARTIDOS DISPONIBLES:
""")
        for i, partido in enumerate(partidos_disponibles):
            print(f"""
------------- {i+1} -------------""")
            print(partido.show())

        opcion = input("""
////////////////////////////////      
Ingrese el número colocado encima de la información del partido que desea ver: """)
        while not opcion.isnumeric() or int(opcion) not in range(1, len(partidos_disponibles) + 1):
            print("Ingreso inválido...")
            opcion = input("""
////////////////////////////////      
Ingrese el número colocado encima de la información del partido que desea ver: """)
        
        print(f"""PARTIDO SELECCIONADO: {partidos_disponibles[int(opcion) - 1].local.nombre} VS. {partidos_disponibles[int(opcion) - 1].visitante.nombre}
////////////////////////////////
""")
        return partidos_disponibles[int(opcion) - 1]

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
            asientos_fila = [asiento.strip() for asiento in fila1.split("|") if asiento.strip() and asiento.strip() != "X"]
            if asientos_fila:
                seccion = asientos_fila[0][0]
            else:
                seccion = seccion_actual
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

        asiento_elegido = input("""
////////////////////////////////
Ingrese el asiento desde donde desee ver el partido (Ej: AA1): """).upper().strip()
        while asiento_elegido not in asientos_disponibles:
            print("El asiento ingresado NO existe o está OCUPADO...")
            asiento_elegido = input("""
////////////////////////////////
Ingrese el asiento desde donde desee ver el partido (Ej: AA1): """).upper().strip()

        print(f"""ASIENTO SELECCIONADO: {asiento_elegido}
////////////////////////////////
""")
        return asiento_elegido

    def crear_entrada(self, cliente, juego_selec, tipo_entrada):

        id_entradas = self.tipo_entradas["General"] + self.tipo_entradas["Vip"]
        while True:
            entrada_id = random.randint(1000000000, 9999999999)
            if entrada_id not in id_entradas:
                break
        
        asiento_selec = self.mapa_disponibilidad(juego_selec)

        if tipo_entrada == "General":
            entrada = General(entrada_id, juego_selec, juego_selec.estadio, asiento_selec)
            entrada.descuento = cliente.descuento_entrada
            return entrada
        
        if tipo_entrada == "Vip":
            entrada = Vip(entrada_id, juego_selec, juego_selec.estadio, asiento_selec)
            entrada.descuento = cliente.descuento_entrada
            return entrada

    def compra_entrada(self):
        ans = input("""
¿Se encuentra registrado? [s/n]: """)
        while ans not in ["s", "n"]:
            print("Ingreso inválido...")
            ans = input("¿Se encuentra registrado? [s/n]: ")
        
        if ans == "s":
            while True:
                try:
                    dni = input("Ingrese su cédula/DNI: ")
                    if len(dni) == 0 or not dni.isnumeric():
                        raise Exception
                    if self.binary_search(self.clientes, 0, len(self.clientes) - 1, dni, lambda x: x.cedula) == -1:
                        print("¡El cliente no se encuentra registrado! Su DNI no se encontró...")
                        ans1 = input("""
¿Quiere intentarlo de nuevo? [s/n]: """)
                        while ans1 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans1 = input("¿Quiere intentarlo de nuevo? [s/n]: ")
                        if ans1 == "s":
                            continue
                        else:
                            return
                    break
                except:
                    print("Ingreso inválido...")
                    ans1 = input("""
¿Quiere intentarlo de nuevo? [s/n]: """)
                    while ans1 not in ["s", "n"]:
                        print("Ingreso inválido...")
                        ans1 = input("¿Quiere intentarlo de nuevo? [s/n]: ")
                    if ans1 == "s":
                        continue
                    else:
                        return
            
            ind = self.binary_search(self.clientes, 0, len(self.clientes) - 1, dni, lambda x: x.cedula)
            cliente = self.clientes[ind]
            juego_selec = self.seleccion_partido()
            
        else:
            cliente = self.registro_cliente()
            juego_selec = self.seleccion_partido()


        if cliente.descuento_entrada:
            print("""¡Por su DNI, ha sido beneficiado con un 50(%) de descuento en la compra de entradas!
""")

        print("""ENTRADAS DISPONIBLES:
---------------------""")
        if juego_selec.entradas_general > 0 and juego_selec.entradas_vip > 0:
            print("""¡Todavía quedan ambos tipos de entrada! Seleccione uno...
        1. Entradas General (35$)
        2. Entradas VIP (75$)
""")
            opcion = input("Ingrese el número de opción de la entrada que desea comprar: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,3):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de opción de la entrada que desea comprar: ")
        
        elif juego_selec.entradas_general > 0:
            print("""¡Sólo quedan entradas de tipo General!
""")
            opcion = "1"
        
        elif juego_selec.entradas_vip > 0:
            print("""¡Sólo quedan entradas de tipo VIP!
""")
            opcion = "2"

        if opcion == "1":
            while True:
                entrada = self.crear_entrada(cliente, juego_selec, "General")
                entrada.precio_real()
                print(entrada.show())

                opcion1 = input("""
¿Quiere confirmar su compra? [s/n]: """)
                while opcion1 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    opcion1 = input("""
¿Quiere confirmar su compra? [s/n]: """)
                    
                if opcion1 == "s":
                    cliente.entradas_compradas.append(entrada)
                    self.entradas.append(entrada)
                    juego_selec.asientos_tomados.append(entrada.asiento)
                    self.tipo_entradas["General"].append(entrada.id)
                    juego_selec.entradas_general -= 1
                    print("¡Su compra ha sido EXITOSA!")
                else:
                    print("Compra cancelada...")
                    break
                
                if juego_selec.entradas_general == 0:
                    print("NO quedan entradas de tipo General...")
                    break

                opcion2 = input("""
¿Desearía comprar una entrada más? [s/n]: """)
                while opcion2 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    opcion2 = input("""
¿Desearía comprar una entrada más? [s/n]: """)
                    
                if opcion2 == "n":
                    print("""¡Gracias por haber comprado en EUROCOPA 2024!
""")
                    break

        else:
            while True:
                entrada = self.crear_entrada(cliente, juego_selec, "Vip")
                entrada.precio_real()
                print(entrada.show())

                opcion1 = input("""
¿Quiere confirmar su compra? [s/n]: """)
                while opcion1 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    opcion1 = input("""
¿Quiere confirmar su compra? [s/n]: """)
                    
                if opcion1 == "s":
                    cliente.entradas_compradas.append(entrada)
                    self.entradas.append(entrada)
                    juego_selec.asientos_tomados.append(entrada.asiento)
                    self.tipo_entradas["Vip"].append(entrada.id)
                    juego_selec.entradas_vip -= 1
                    print("¡Su compra ha sido EXITOSA!")
                else:
                    print("Compra cancelada...")
                    break
                
                if juego_selec.entradas_vip == 0:
                    print("NO quedan entradas de tipo VIP...")
                    break

                opcion2 = input("""
¿Desearía comprar una entrada más? [s/n]: """)
                while opcion2 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    opcion2 = input("""
¿Desearía comprar una entrada más? [s/n]: """)
                    
                if opcion2 == "n":
                    print("""¡Gracias por haber comprado en EUROCOPA 2024!
""")
                    break
        
        if len(cliente.entradas_compradas) > 0:
            cliente.gasto_entradas()
            i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cliente.cedula, lambda x: x.cedula)
            if i == -1:
                self.clientes.append(cliente)
            print(f"""
////////////////////////////////
ENTRADAS COMPRADAS: {len(cliente.entradas_compradas)}
MONTO FINAL: {cliente.cant_entradas}$
////////////////////////////////
""")

    def confirmacion_asistencia(self):
        while True:
            try:
                id_entrada = int(input("Ingrese el ID de la entrada para verificarla y confirmar su asistencia: "))
                if len(str(id_entrada)) == 10:
                    break
                else:
                    print("Ingreso inválido...")
            except ValueError:
                print("Ingreso inválido...")

        entradas_totales = self.tipo_entradas["General"] + self.tipo_entradas["Vip"]

        entradas_usadas = []
        for entrada1 in entradas_totales:
            entradas_usadas.append(entrada1)

        if id_entrada in entradas_totales:
            if id_entrada not in self.entradas_verificadas:
                self.entradas_verificadas.append(id_entrada)
                print("""
////////////////////////////////
¡Su entrada ha sido VERIFICADA exitosamente!""")
                i = self.binary_search(self.entradas, 0, len(self.entradas) - 1, id_entrada, lambda x: x.id)
                entrada = self.entradas[i]
                print(entrada.show())
                print("""¡Su asistencia ha sido CONFIRMADA exitosamente!
////////////////////////////////""")
                
                j = self.binary_search(self.partidos, 0, len(self.entradas) - 1, entrada.partido.id, lambda x: x.id)
                partido = self.partidos[j]
                partido.asistencia_confirmada += 1
            else:
                print("""
La entrada ya fue verificada...
""")
        else:
            print("""
El ID de la entrada ingresada no existe...
""")

    def info_restaurantes(self):
        print(f"""
Bienvenido/a a los restaurantes de la Eurocopa 2024
""")
        while True:
            print("""Seleccione lo que quiera hacer...
        1. Buscar productos
        2. Comprar productos
        3. Volver al menú inicial
        """)
                
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,6):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                pass

            elif opcion == "2":
                pass

            else:
                break

    def busqueda_productos():
        while True:
            print("""Seleccione un filtro...
        1. Ver todos los partidos disponibles
        2. Búsqueda de los partidos de un país
        3. Búsqueda de los partidos en un estadio específico
        4. Búsqueda de los partidos en una fecha determinada
        5. Volver al menú inicial
        """)

    def menu(self, teams, stadiums, matches):
        self.register_data(teams, stadiums, matches)
        print(f"""
--- BIENVENIDO/A A LA EUROCOPA 2024 ---""")
        while True:
            print("""
MENÚ PRINCIPAL:
Ingrese una opción...
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
                print(f"""
{'~' * 100}""")
                self.busqueda_partidos()
                print(f"{'~' * 100}")
            elif opcion == "2":
                print(f"""
{'~' * 100}""")
                self.compra_entrada()
                print(f"{'~' * 100}")
            elif opcion == "3":
                print(f"""
{'~' * 100}""")
                self.confirmacion_asistencia()
                print(f"{'~' * 100}")
            elif opcion == "4":
                print(f"""
{'~' * 100}""")
                pass
                print(f"{'~' * 100}")
            elif opcion == "5":
                print(f"""
{'~' * 100}""")
                pass
                print(f"{'~' * 100}")
            else:
                print("""
Cerrando sesión...
Vuelva por más novedades del torneo internacional más competitivo...
¡LA EUROCOPA 2024!
""")
                break

            ans = input("""
¿Desea continuar? [s/n]: """)
            while ans not in ["s", "n"]:
                print("Ingreso inválido")
                ans = input("""
¿Desea continuar? [s/n]: """)

            if ans == "n":
                print("""
Cerrando sesión...
Vuelva por más novedades del torneo internacional más competitivo...
¡LA EUROCOPA 2024!
""")
                break