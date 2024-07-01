from Cliente import Cliente
from Equipo import Equipo
from Estadio import Estadio
from Partido import Partido
from Producto import Producto
from Restaurante import Restaurante
from Entrada import Entrada
from Vip import Vip
from General import General

from datetime import datetime
import pickle
import random
import matplotlib.pyplot as grafica
from tabulate import tabulate
import numpy as np

# Crear la clase App para guardar todos los datos bajados en el main
class App:
    def __init__(self):
# Inicializar los datos
        self.estadios = []
        self.partidos = []
        self.entradas = []
        self.tipo_entradas = {"General": [], "Vip": []}
        self.entradas_verificadas = []
        self.equipos = []
        self.clientes = []
        self.bebidas = []
        self.comidas = []

# Buscar dentro de una lista con un algoritmo de búsqueda predeterminado
    def binary_search(self, lista_arg, min, max, x, key = lambda x: x):
# Divide en dos la lista, para luego ir reduciendo por la mitad hasta hallar un valor paralelo al buscado
# Lo hace dependiendo de si es menor, mayor o igual a la mitad
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

# Ordenar una lista con un algoritmo de ordenamiento predeterminado
    def merge_sort(self, lista_orden, key = lambda x: x):
# Divide en dos la lista, y ordena cada tramo para luego unirlas y ordenarlas un solo conjunto
# Hace uso de dos parámetros, una lista y la propia función que ordena
        if len(lista_orden) > 1:
            mid = len(lista_orden) // 2
            left = lista_orden[:mid]
            right = lista_orden[mid:]
            self.merge_sort(left, key)
            self.merge_sort(right, key)
            i = j = k = 0

            while i < len(left) and j < len(right):
                if key(left[i]) <= key(right[j]):
                  lista_orden[k] = left[i]
                  i += 1
                else:
                    lista_orden[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                lista_orden[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                lista_orden[k] = right[j]
                j += 1
                k += 1

# Función para registrar los datos del .json a objetos
    def register_data(self, teams, stadiums, matches):

# Registrar los datos del equipo en el sistema y asignar sus atributos
        for equipo in teams:
            equipo = Equipo(equipo["id"], equipo["code"], equipo["name"], equipo["group"])
            self.equipos.append(equipo)

 # Registrar los datos del estadio en el sistema y asignar sus atributos
        for estadio in stadiums:
            estadioinfo = Estadio(estadio["id"], estadio["name"], estadio["city"], estadio["capacity"])

# Registrar los datos del restaurante dentro de estadio en el sistema y asignar sus atributos
            for restaurante in estadio["restaurants"]:
                restauranteinfo = Restaurante(restaurante["name"], estadio["name"])
                estadioinfo.restaurantes.append(restauranteinfo)
# Registrar los datos del producto dentro de restaurante en el sistema y asignar sus atributos
                for producto in restaurante["products"]:
                    productoinfo = Producto(producto["name"], producto["quantity"], producto["price"], producto["stock"], producto["adicional"], restaurante["name"], estadio["name"])
                    restauranteinfo.productos.append(productoinfo)

            self.estadios.append(estadioinfo)

# Clasificar los productos en Bebidas y Comidas sólo para la búsqueda
        for estadio1 in self.estadios:
                for restaurante1 in estadio1.restaurantes:
                    for producto1 in restaurante1.productos:
                        if producto1.adicional == "alcoholic" or producto1.adicional == "non-alcoholic":
                            self.bebidas.append(producto1)
                        else:
                            self.comidas.append(producto1)

# Registrar los datos del partido en el sistema y asignar sus atributos
        for partido in matches:
# Transformar los parámetros que sean listas en objetos
            for equipo in self.equipos:
                if partido["home"]["id"] == equipo.id:
                    equipo_local = equipo
                elif partido["away"]["id"] == equipo.id:
                    equipo_visitante = equipo

            for estadio in self.estadios:
                if partido["stadium_id"] == estadio.id:
                    estadio_partido = estadio

            partido = Partido(partido["id"], partido["number"], equipo_local, equipo_visitante, partido["date"], partido["group"], estadio_partido)
            self.partidos.append(partido)

# Función para buscar partidos según ciertos filtros, únicamente comparando con los atributos de los objetos ya creados
    def busqueda_partidos(self):
        print(f"""
Bienvenido/a a la búsqueda de partidos de la Eurocopa 2024""")
        while True:
            print("""
Seleccione un filtro...
        1. Ver todos los partidos disponibles
        2. Búsqueda de los partidos de un país
        3. Búsqueda de los partidos en un estadio específico
        4. Búsqueda de los partidos en una fecha determinada
        5. Volver al menú inicial
        """)

# Este tipo de validaciones se usará recurrentemente a lo largo del código
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,6):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                i = 0
                for partido in self.partidos:
                    i += 1
                    print(f"""
------------- {i} -------------""")
                    print(partido.show())

# Validación para seguir en la función con las mismas opciones o hacer un Break y volver al inicio
                ans1 = input("""
¿Quiere seguir buscando partidos? [s/n]: """)
                while ans1 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans1 = input("¿Quiere seguir buscando partidos? [s/n]: ")
                if ans1 == "s":
                    continue
                else:
                    return
            
            elif opcion == "2":
                eleccion_pais = input("Ingrese el nombre o código FIFA de un país (en inglés): ").lower()
                while eleccion_pais == "" or not eleccion_pais.isalpha():
                    print("Ingreso inválido...")
                    eleccion_pais = input("Ingrese el nombre o código FIFA de un país (en inglés): ").lower()

                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_pais in partido.local.nombre.lower() or eleccion_pais in partido.visitante.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"""
------------- {i} -------------""")
                        print(partido.show())

                if contador == 0:
                    print("El país ingresado no fue conseguido...")

                ans2 = input("""
¿Quiere seguir buscando partidos? [s/n]: """)
                while ans2 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans1 = input("¿Quiere seguir buscando partidos? [s/n]: ")
                if ans2 == "s":
                    continue
                else:
                    return

            elif opcion == "3":
                eleccion_estadio = input("Ingrese un estadio de la Eurocopa 2024: ").lower()
                while eleccion_estadio == "" or not eleccion_estadio.isalpha():
                    print("Ingreso inválido...")
                    eleccion_estadio = input("Ingrese un estadio de la Eurocopa 2024: ").lower()

                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_estadio in partido.estadio.nombre.lower():
                        contador = 1
                        i += 1
                        print(f"""
------------- {i} -------------""")
                        print(partido.show())

                if contador == 0:
                    print("El estadio ingresado no fue conseguido...")
        
                ans3 = input("""
¿Quiere seguir buscando partidos? [s/n]: """)
                while ans3 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans1 = input("¿Quiere seguir buscando partidos? [s/n]: ")
                if ans3 == "s":
                    continue
                else:
                    return
            
            elif opcion == "4":
                while True:
                    eleccion_fecha = input("Ingrese la fecha que desea ver un partido (AAAA-MM-DD): ")
                    try:
                        if datetime.strptime(eleccion_fecha, "%Y-%m-%d"):
                            break
                        else:
                            raise Exception
                    except ValueError:
                        print("Ingreso inválido. Por favor, ingrese la fecha en el formato AAAA-MM-DD...")

                contador = 0
                i = 0
                for partido in self.partidos:
                    if eleccion_fecha in partido.fecha:
                        contador = 1
                        i += 1
                        print(f"""
------------- {i} -------------""")
                        print(partido.show())

                if contador == 0:
                    print("En la fecha ingresada no hay partidos...")

                ans4 = input("""
¿Quiere seguir buscando partidos? [s/n]: """)
                while ans4 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans4 = input("¿Quiere seguir buscando partidos? [s/n]: ")
                if ans4 == "s":
                    continue
                else:
                    return

            else:
                break

# Función que pide información a la persona que está en el sistema para crear el objeto Cliente y guardar nuevos atributos
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

# Función que imprime los partidos disponibles para elegir uno y luego comprar las entradas del mismo
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

# Función que imprime un mapa para visualizar los asientos y elegir la zona donde ver el partido seleccionado
# El mapa es creado con letras y números que dependen de la capacidad que la misma función calcula
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

# Crear una entrada con un ID aleatorio y validar que no se repita. Este servirá para verificar la asistencia al partido
# Se verifica el tipo de entrada y aplica descuentos dependiendo de si los tiene
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
            entrada = Vip(entrada_id, juego_selec, juego_selec.estadio, asiento_selec,)
            entrada.descuento = cliente.descuento_entrada
            return entrada

# Función que contiene toda la compra de la entrada y las demás funciones que validan esta
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
# Reconoce el error y permite intentarlo de nuevo
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

# Permite la confirmación de la compra para evitar gastos directos
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

# Valida la compra potencial de otra entrada
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
# Se guarda la entrada, y se hacen todos los cálculos respecto a las entradas vendidas y evitar la repetición del asiento
            cliente.gasto_entradas()
            self.merge_sort(self.clientes, lambda x: x.cedula)
            i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cliente.cedula, lambda x: x.cedula)
            if i == -1:
                self.clientes.append(cliente)
            print(f"""
////////////////////////////////
ENTRADAS COMPRADAS: {len(cliente.entradas_compradas)}
MONTO FINAL: {cliente.cant_entradas}$
////////////////////////////////
""")

# Función que verifica si una entrada es real o si ya fue usada
    def confirmacion_asistencia(self):
        while True:
            while True:
                try:
                    id_entrada = int(input("""
Ingrese el ID de la entrada para verificarla y confirmar su asistencia: """))
                    if len(str(id_entrada)) == 10:
                        break
                    else:
                        print("Ingreso inválido. El ID debe poseer 10 dígitos...")
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
                    break
                else:
                    print("""La entrada ya fue verificada...
""")
                    break
            else:
                print("""El ID de la entrada ingresada no existe...""")
                ans = input("""
¿Quiere intentarlo de nuevo? [s/n]: """)
                while ans not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans = input("¿Quiere intentarlo de nuevo? [s/n]: ")
                if ans == "s":
                    continue
                else:
                    return

# Función que sirve como un menú sobre los restaurantes para evitar el exceso de información en una parte
    def info_restaurantes(self):
        print(f"""
Bienvenido/a a los restaurantes de la Eurocopa 2024""")
        while True:
            print("""
Seleccione lo que quiera hacer...
        1. Buscar productos
        2. Comprar productos
        3. Volver al menú inicial
        """)
                
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,4):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                print(f"""
{'~' * 100}""")
                self.busqueda_productos()
                print(f"{'~' * 100}")

            elif opcion == "2":
                print(f"""
{'~' * 100}""")
                self.compra_productos()
                print(f"{'~' * 100}")
                self.salvar_archivos()

            else:
                break

# Función para buscar productos según ciertos filtros, únicamente comparando con los atributos de los objetos que ya fueron bajados de la API
    def busqueda_productos(self):
        print(f"""
Bienvenido/a a la búsqueda de productos de la Eurocopa 2024""")
        while True:
            print("""
Seleccione un filtro...
        1. Ver todos los productos disponibles
        2. Búsqueda de los productos por nombre
        3. Búsqueda de los productos por tipo (Bebida/Comida)
        4. Búsqueda de los productos por rango de precio
        5. Volver al menú anterior
        """)
            
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,6):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                i = 0
                print("""///////////////////
TODAL DE PRODUCTOS
///////////////////
""")
                for estadio in self.estadios:
                    for restaurante in estadio.restaurantes:
                        for producto in restaurante.productos:

                            i += 1
                            print(f"""
------------- {i} -------------""")
                            print(producto.show())
                ans1 = input("""
¿Quiere seguir buscando productos? [s/n]: """)
                while ans1 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans1 = input("¿Quiere seguir buscando productos? [s/n]: ")
                if ans1 == "s":
                    continue
                else:
                    return
            
            elif opcion == "2":
                eleccion_prod = input("Ingrese el nombre del producto que desea buscar: ").lower()
                while eleccion_prod == "" or not eleccion_prod.isalpha():
                    print("Ingreso inválido...")
                    eleccion_prod = input("Ingrese el nombre del producto que desea buscar: ").lower()

                contador = 0
                i = 0
                for estadio in self.estadios:
                    for restaurante in estadio.restaurantes:
                        for producto1 in restaurante.productos:
                            if eleccion_prod in producto1.nombre.lower() or eleccion_prod in producto1.nombre.lower():
                                contador = 1
                                i += 1
                                print(f"""
------------- {i} -------------""")
                                print(producto1.show())
                if contador == 0:
                    print("El producto ingresado no fue conseguido...")

                ans2 = input("""
¿Quiere seguir buscando productos? [s/n]: """)
                while ans2 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans2 = input("¿Quiere seguir buscando productos? [s/n]: ")
                if ans2 == "s":
                    continue
                else:
                    return

            elif opcion == "3":
                opc = input("¿Qué tipo de productos está buscando, bebidas o comidas? [b/c]: ")
                while opc not in ["b", "c"]:
                    print("Ingreso inválido...")
                    opc = input("¿Qué tipo de productos está buscando, bebidas o comidas? [b/c]: ")     

                if opc == "b":
                    i = 0
                    print("""///////////////////
TOTAL DE BEBIDAS
///////////////////
""")
                    for estadio in self.estadios:
                        for restaurante in estadio.restaurantes:
                            for producto2 in restaurante.productos:
                                if producto2 in self.bebidas:
                                    i += 1
                                    print(f"""
------------- {i} -------------""")
                                    print(producto2.show())
                    ans3 = input("""
¿Quiere seguir buscando productos? [s/n]: """)
                    while ans3 not in ["s", "n"]:
                        print("Ingreso inválido...")
                        ans3 = input("¿Quiere seguir buscando productos? [s/n]: ")
                    if ans3 == "s":
                        continue
                    else:
                        return
                
                else:
                    i = 0
                    print("""///////////////////
TOTAL DE COMIDAS
///////////////////
""")
                    for estadio in self.estadios:
                        for restaurante in estadio.restaurantes:
                            for producto3 in restaurante.productos:
                                if producto3 in self.comidas:
                                    i += 1
                                    print(f"""
------------- {i} -------------""")
                                    print(producto3.show())
                    ans4 = input("""
¿Quiere seguir buscando productos? [s/n]: """)
                    while ans4 not in ["s", "n"]:
                        print("Ingreso inválido...")
                        ans4 = input("¿Quiere seguir buscando productos? [s/n]: ")
                    if ans4 == "s":
                        continue
                    else:
                        return
            
            elif opcion == "4":
                while True:
                    print("""
Buscar según el precio (IVA incluido):
        1. Igual a...
        2. Menor a...
        3. Mayor a...
        4. Entre...
        5. Volver a los filtros de búsqueda
        """)
                    opcion1 = input("Ingrese el número de la opción que desea elegir: ")
                    while not opcion1.isnumeric() or int(opcion1) not in range(1,6):
                        print("Ingreso inválido...")
                        opcion1 = input("Ingrese el número de la opción que desea elegir: ")


                    if opcion1 == "1":
                        while True:
                            try:
                                precio = float(input("Ingrese el precio de cualquier producto: "))
                                if precio <= 0:
                                    raise Exception
                                break
                            except ValueError:
                                print("Ingreso inválido...")

                        i = 0
                        contador = 0
                        for estadio in self.estadios:
                            for restaurante in estadio.restaurantes:
                                for producto4 in restaurante.productos:
                                    if precio == producto4.precio:
                                        contador = 1
                                        i += 1
                                        print(f"""
------------- {i} -------------""")
                                        print(producto4.show())
                        if contador == 0:
                            print("Ningún producto posee el precio ingresado...")

                        ans5 = input("""
¿Quiere seguir buscando productos según el precio? [s/n]: """)
                        while ans5 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans5 = input("¿Quiere seguir buscando productos según el precio? [s/n]: ")
                        if ans5 == "s":
                            continue
                        else:
                            return
                        
                    elif opcion1 == "2":
                        while True:
                            try:
                                precio1 = float(input("Ingrese un precio para mostrar todos los productos menores a este: "))
                                if precio1 <= 0:
                                    raise Exception
                                break
                            except ValueError:
                                print("Ingreso inválido...")

                        i = 0
                        contador = 0
                        for estadio in self.estadios:
                            for restaurante in estadio.restaurantes:
                                for producto5 in restaurante.productos:
                                    if precio1 >= producto5.precio:
                                        contador = 1
                                        i += 1
                                        print(f"""
------------- {i} -------------""")
                                        print(producto5.show())
                        if contador == 0:
                            print("No hay productos por debajo del precio ingresado...")

                        ans6 = input("""
¿Quiere seguir buscando productos según el precio? [s/n]: """)
                        while ans6 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans6 = input("¿Quiere seguir buscando productos según el precio? [s/n]: ")
                        if ans6 == "s":
                            continue
                        else:
                            return

                    elif opcion1 == "3":
                        while True:
                            try:
                                precio2 = float(input("Ingrese un precio para mostrar todos los productos mayores a este: "))
                                if precio2 <= 0:
                                    raise Exception
                                break
                            except ValueError:
                                print("Ingreso inválido...")

                        i = 0
                        contador = 0
                        for estadio in self.estadios:
                            for restaurante in estadio.restaurantes:
                                for producto6 in restaurante.productos:
                                    if precio2 <= producto6.precio:
                                        contador = 1
                                        i += 1
                                        print(f"""
------------- {i} -------------""")
                                        print(producto6.show())
                        if contador == 0:
                            print("No hay productos por encima del precio ingresado...")

                        ans7 = input("""
¿Quiere seguir buscando productos según el precio? [s/n]: """)
                        while ans7 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans7 = input("¿Quiere seguir buscando productos según el precio? [s/n]: ")
                        if ans7 == "s":
                            continue
                        else:
                            return

                    elif opcion1 == "4":
                        while True:
                            try:
                                precio3 = float(input("Ingrese un precio como el límite menor: "))
                                precio4 = float(input("Ingrese un precio como el límite mayor: "))
                                if precio3 <= 0 or precio4 <= 0 or precio3 >= precio4:
                                    raise Exception
                                break
                            except ValueError:
                                print("Ingreso inválido. Considere que el primer precio sea menor al segundo...")
                        i = 0
                        contador = 0
                        for estadio in self.estadios:
                            for restaurante in estadio.restaurantes:
                                for producto7 in restaurante.productos:
                                    if producto7.precio >= precio3 and producto7.precio <= precio4:
                                        contador = 1
                                        i += 1
                                        print(f"""
------------- {i} -------------""")
                                        print(producto7.show())
                        if contador == 0:
                            print("No hay productos entre los rangos ingresados...")

                        ans8 = input("""
¿Quiere seguir buscando productos según el precio? [s/n]: """)
                        while ans8 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans8 = input("¿Quiere seguir buscando productos según el precio? [s/n]: ")
                        if ans8 == "s":
                            continue
                        else:
                            return
                        
                    else:
                        break
            else:
                break

# Función que contiene toda la compra de productos
    def compra_productos(self):
        validacion1 = True
        validacion2 = True

# Busca el DNI ya registrado por el usuario que está usando el programa, asociándolo a uno de los clientes guardados
        while True:
            try:
                dni = input("\nIngrese su DNI: ")
                if dni == "" or not dni.isnumeric():
                    raise Exception
                elif list(filter(lambda x: x.cedula == dni, self.clientes)) == []:
                    print("""
No hay clientes con este DNI...""")
                    validacion1 = False
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

# Verifica que el cliente según su DNI tenga entradas VIP, ya que de lo contrario no podrá comprar productos
        if validacion1:
            cliente = list(filter(lambda x: x.cedula == dni, self.clientes))[0]
            if list(filter(lambda x: isinstance(x, Vip), cliente.entradas_compradas)) == []:
                print("""
No posee entradas VIP. No puede consumir productos...""")
                validacion2 = False
                
            if validacion2:
                entradas = list(filter(lambda x: isinstance(x, Vip), cliente.entradas_compradas))
                if cliente.descuento_rest:
                    print("""¡Por su DNI, ha sido beneficiado con un 15(%) de descuento en la compra de productos!
""")
# Filtra los estadios donde está la entrada VIP
                if len(entradas) > 1:
                    lista_ent = []
                    for ent in entradas:
                        estadio_selec = ent.estadio
                        if estadio_selec not in lista_ent:
                            lista_ent.append(estadio_selec)

                    while True:
                        try:
                            print("""
ESTADIOS donde compró entrada: """)
                            for i, ent1 in enumerate(lista_ent):
                                print(f"""
{i+1}. {ent1.nombre}""")
                            opc = int(input("""
Elija el número del estadio donde desea comprar: """))
                            
                            if opc not in range(1, len(lista_ent) + 1):
                                raise Exception
                            break
                        except:
                            print("Ingreso inválido...")
                    self.merge_sort(self.estadios, lambda x: x.nombre)
                    ind = self.binary_search(self.estadios, 0, len(self.estadios) - 1, lista_ent[opc - 1].nombre, lambda x: x.nombre)
                    estadio = self.estadios[ind]
                else:
                    self.merge_sort(self.estadios, lambda x: x.nombre)
                    ind = self.binary_search(self.estadios, 0, len(self.estadios)-1, entradas[0].estadio.nombre, lambda x: x.nombre)
                    estadio = self.estadios[ind]

# Filtra los restaurantes dentro del estadio seleccionado con entrada VIP
                if len(estadio.restaurantes) > 1:
                    while True:
                        try:
                            print(f"""
RESTAURANTES del estadio: {estadio.nombre}
""")
                            for i, restaurante in enumerate(estadio.restaurantes):
                                print(f"""{i+1}. {restaurante.nombre}""")
                            opc1 = int(input("""

Elija el número del restaurante donde desea comprar: """))
                            if opc1 not in range(1, len(estadio.restaurantes) + 1):
                                raise Exception
                            break
                        except:
                            print("Ingreso inválido...")

                    restaurante = estadio.restaurantes[opc1 - 1]
                else:
                    restaurante = estadio.restaurantes[0]

# Valida si es menor de edad para evitar la compra de bebidas alcohólicas
                productos = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
                if cliente.edad < 18:
                    print("""
No puede comprar bebidas alcohólicas. Usted es menor de edad...""")
                    productos = list(filter(lambda x: x.adicional in ["non-alcoholic", "plate", "package"], productos))
                else:
                    productos = list(filter(lambda x: x.adicional in ["plate", "package","non-alcoholic", "alcoholic"], productos))
    
                validacion3 = True
                if len(productos) == 0:
                    print("""
No se dispone de más productos""")
                    validacion3 = False

                if validacion3:
                    while True:
                        productos = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
                        if cliente.edad < 18:
                            productos = list(filter(lambda x: x.adicional in ["plate", "package", "non-alcoholic"], productos))
                        else:
                            productos = list(filter(lambda x: x.adicional in ["plate", "package","non-alcoholic", "alcoholic"], productos))

# Filtra los productos del estadio seleccionado para proceder con la compra de uno o varios
                        while True:
                            try:
                                print(f"""
PRODUCTOS del restaurante: {restaurante.nombre}""")
                                j = 0
                                for prod in productos:
                                    print(f"""
------------- {j+1} -------------""")
                                    print(prod.show())
                                    j += 1
                                prod_elec = int(input("""
Elija el número del producto que desea comprar: """))
                                if prod_elec not in range(1, j + 1):
                                    raise Exception
                                break
                            except:
                                print("Ingreso inválido...")

                        productos_def = productos
                        producto_def = productos_def[prod_elec - 1]
                        self.merge_sort(restaurante.productos, lambda x: x.nombre)
                        index = self.binary_search(restaurante.productos, 0, len(restaurante.productos) - 1, producto_def.nombre, lambda x: x.nombre)
                        producto_final = restaurante.productos[index]

                        while True: 
                            try:
                                cantidad = int(input("Ingrese la cantidad que desee comprar de este producto: "))
                                if cantidad not in range(1, producto_final.stock + 1):
                                    raise Exception
                                break
                            except:
                                print("Ingreso inválido...")

                        if cliente.descuento_rest:
                            compra = (producto_final.precio * cantidad) - ((producto_final.precio / 1.16) * cantidad * 0.15)
                            print(f"""
TOTAL A PAGAR (IVA incluido): {compra}$""")
                        else:
                            compra = producto_final.precio * cantidad
                            print(f"""
TOTAL A PAGAR (IVA incluido): {compra}$""")
                        
                        opcion = input("""
¿Quiere confirmar su compra? [s/n]: """)
                        while opcion not in ["s", "n"]:
                            print("Ingreso inválido...")
                            opcion = input("""
¿Quiere confirmar su compra? [s/n]: """)

# Muestra la información de compra con todos sus cálculos asociados
                        if opcion == "s":
                            print(f"""¡Su compra ha sido EXITOSA!

INFORMACIÓN DE COMPRA
=====================
PRODUCTO: {producto_final.nombre}
PRECIO (sin IVA): {(producto_final.precio) / 1.16}$
CANTIDAD COMPRADA: {cantidad}
---------------------
SUBTOTAL: {(producto_final.precio / 1.16) * cantidad}$
IMPUESTOS (16%): {(producto_final.precio / 1.16) * cantidad * 0.16}$""")
                            if cliente.descuento_rest:
                                print(f"""DESCUENTO (15%): {(producto_final.precio / 1.16) * cantidad * 0.15}$
TOTAL: {(producto_final.precio * cantidad) - ((producto_final.precio / 1.16) * cantidad * 0.15)}
""")
                            else:
                                print(f"""DESCUENTO (15%): 0$
TOTAL: {producto_final.precio * cantidad}
""")

                            for i in range(cantidad):
                                cliente.productos_comprados.append(producto_final)
                            producto_final.ventas_stock(cantidad)
                            producto_final.dinero_gastado()
                            cliente.gasto_productos()

                        else:
                            print("Compra cancelada...")
                            break

# Valida la compra potencial de otro producto
                        opcion1 = input("""
¿Desearía comprar otro producto? [s/n]: """)
                        while opcion1 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            opcion1 = input("""
¿Desearía comprar una entrada más? [s/n]: """)
                    
                        if opcion1 == "n":
                            print("""¡Gracias por haber comprado en EUROCOPA 2024!
""")
                            break

# Función que grafica todas las estadísticas relacionadas al estadio
    def grafica_estadisticas(self, abscissa, ordinate, opt, title, y_label):

        if opt == 1:
            data = ordinate
            fig = grafica.figure(figsize =(10, 7))
            ax = grafica.boxplot(data)
            grafica.title(title)
            grafica.ylabel(y_label)
            grafica.show()
        elif opt == 2:
            x = np.array(abscissa)
            y = np.array(ordinate)
            bar_colors = ['tab:red', 'tab:blue', 'tab:orange']
            grafica.bar(x, y, color = bar_colors, width = 0.5)
            grafica.title(title)
            grafica.ylabel(y_label)
            grafica.show()

# Función que muestra todas las estadísticas relacionadas al estadio
    def mostrar_estadisticas(self):
        print("""
Bienvenido/a a las estadísticas disponibles""")
        
        while True:
            print("""
Seleccione una estadística...
        1. Promedio de gasto de un cliente VIP en un partido
        2. Tabla con asistencia a los partidos (mejor a peor)
        3. Partido con mayor asistencia confirmada
        4. Partido con mayor cantidad de boletos vendidos
        5. Productos más vendidos
        6. Clientes con mayor cantidad de boletos comprados
        7. Volver al menú principal
""")
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,8):
                print("Ingreso inválido...")
                opcion = input("Ingrese el número de la opción que desea elegir: ")

            if opcion == "1":
                entradas_vip = list(filter(lambda cliente: type(cliente.entradas_compradas[0]) == Vip, self.clientes))
                if len(entradas_vip) != 0:
                    total_entradasvip = 0
                    for cliente in entradas_vip:
                        total_entradasvip += cliente.cant_entradavip
                    total_productos = 0
                    for cliente in entradas_vip:
                        total_productos += cliente.cant_productos
                    
                    promedio_gastado = (total_entradasvip + total_productos) / len(entradas_vip)

                    print(f"""
PROMEDIO DE GASTO DE CLIENTE VIP: {promedio_gastado}
""")
                    data = []
                    for cliente1 in entradas_vip:
                        total = cliente1.cant_entradavip + cliente1.cant_productos
                        data.append(total)

                    self.grafica_estadisticas(None, data, 1, "PROMEDIO GASTO: CLIENTE VIP", "GASTO")

                else:
                    print("""
No se han registrado clientes VIP...
""")

            elif opcion == "2":
                foo = list(filter(lambda g: g.asistencia_confirmada > 0, self.partidos))

                if len(foo) != 0:

                    print("""
                          Tabla con la asistencia a los partidos.
""")
                    filas = []
                    for i in range(1,len(foo)+1):
                        juego  = f"{foo[-i].local.nombre} vs {foo[-i].visitante.nombre}"
                        estadio = foo[-i].estadio.nombre
                        ent_general = foo[-i].estadio.capacidad[0] - foo[-i].entradas_general
                        ent_vip = foo[-i].estadio.capacidad[1] - foo[-i].entradas_vip
                        total_vendido = ent_general + ent_vip
                        asistencia = foo[-1].asistencia_confirmada
                        relacion = asistencia / total_vendido
                        filas.append([juego, estadio, asistencia, ent_general, ent_vip, total_vendido, relacion])

                    encabezados = ["Partido", "Estadio", "Asistencia", "Entradas General\n Vendidos", "Entradas VIP\n Vendidos", "Total de Entradas\n Vendidas", "Relación\n Asistencia/Ventas"]
                    print(tabulate(filas, encabezados, tablefmt="grid"))
                    print(""" """)

                    if len(foo) <= 3:

                        abscissa = []
                        ordinate = []
                        for i in range(1,len(foo)+1):
                            partido_nom = f"{foo[-i].local.nombre} vs {foo[-i].visitante.nombre}"
                            abscissa.append(partido_nom)
                            asistencia_nom = foo[-i].asistencia_confirmada
                            ordinate.append(asistencia_nom)
                        self.grafica_estadisticas(abscissa, ordinate, 2, "PARTIDOS CON MÁS ASISTENCIA", "ASISTENCIA")
                    else:

                        abscissa = []
                        ordinate = []
                        for i in range(1, 4):
                            partido_nom1 = f"{foo[-i].local.nombre} vs {foo[-i].visitante.nombre}"
                            abscissa.append(partido_nom1)
                            asistencia_nom1 = foo[-i].asistencia_confirmada
                            ordinate.append(asistencia_nom1)
                        self.grafica_estadisticas(abscissa, ordinate, 2, "TOP 3 PARTIDOS: MAYOR ASISTENCIA", "ASISTENCIA")
                else:
                    print("""
Actualmente, no hay asistencia confirmada a los partidos...
""")

            elif opcion == "3":
                variable = list(filter(lambda x: x.asistencia_confirmada > 0, self.partidos))
                if len(variable) != 0:

                    print(f"""
PARTIDO CON MAYOR ASISTENCIA:{variable[-1].local.nombre} vs {variable[-1].visitante.nombre} 
ASISTENCIA: {variable[-1].asistencia_confirmada} personas
ESTADIO: {variable[-1].estadio.nombre}
""")

                    abscissa = []
                    ordinate = []
                    for i in range(1, len(variable) + 1):
                        partido_nom2 = f"{variable[-i].local.nombre} vs {variable[-i].visitante.nombre}"
                        abscissa.append(partido_nom2)
                        asistencia_nom2 = variable[-i].asistencia_confirmada
                        ordinate.append(asistencia_nom2)
                    self.grafica_estadisticas(abscissa, ordinate, 2, "PARTIDOS CON MÁS ASISTENTES", "ASISTENCIA")

                else:
                    print("""
Actualmente, no hay asistencia confirmada a los partidos...
""")

            elif opcion == "4":
                variable1 = list(filter(lambda x: len(x.asientos_tomados) > 0, self.partidos))
                if len(variable1) != 0:

                    print(f"""
PARTIDO CON MÁS ENTRADAS VENDIDAS:{variable1[-1].local.nombre} vs {variable1[-1].visitante.nombre} 
ENTRADAS VENDIDAS: {len(variable1[-1].asientos_tomados)}
ESTADIO: {variable1[-1].estadio.nombre}
""")

                    abscissa = []
                    ordinate = []
                    for i in range(1, len(variable1) + 1):
                        partido_nom3 = f"{variable1[-i].local.nombre} vs {variable1[-i].visitante.nombre}"
                        abscissa.append(partido_nom3)
                        asistencia_nom3 = len(variable1[-i].asientos_tomados)
                        ordinate.append(asistencia_nom3)
                    self.grafica_estadisticas(abscissa, ordinate, 2, "PARTIDOS CON MÁS VENTAS", "BOLETOS VENDIDOS")

                else:
                    print("""
Actualmente, en ningún partido se han vendido entradas...
""")

            elif opcion == "5":
                lista_restaurantes = []
                for estadio1 in self.estadios:
                    for restaurante in estadio1.restaurantes:
                        lista_restaurantes.append(restaurante)
                
                self.merge_sort(lista_restaurantes, lambda x: x.nombre)
                print("""
RESTAURANTES:
""")
                while True:
                    for i, restaurante1 in enumerate(lista_restaurantes):
                        print(f"{i+1}. {restaurante1.nombre}")
                    
                    opc = input("""
Ingrese el número de un restaurante para ver sus productos más vendidos: """)
                    while not opc.isnumeric() or int(opc) not in range(1, len(lista_restaurantes) + 1):
                        print("Ingreso inválido...")
                        opc = input("""
Ingrese el número de un restaurante para ver sus productos más vendidos: """)

                    rest = lista_restaurantes[int(opc) - 1]
                    producs = list(filter(lambda x: x.ventas > 0, rest.productos))
                    self.merge_sort(producs, lambda x: x.ventas)

                    if len(producs) == 0:
                        print("""
Ningún producto ha sido vendido en este restaurante...""")
                        
                        ans1 = input("""
¿Quiere seguir viendo los productos más vendidos? [s/n]: """)
                        while ans1 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans1 = input("¿Quiere seguir viendo los productos más vendidos? [s/n]: ")
                        if ans1 == "s":
                            continue
                        else:
                            return

                    elif len(producs) <= 3:
                        print(f"""
TOP 3 productos más vendidos de '{rest.nombre}'""")
                        for i in range(1, len(producs)+1):
                            print(f"{i}. {producs[-i].nombre}: {producs[-i].ventas} VENTAS")
                            
                        abscissa = []
                        ordinate = []
                        for j in range(1, len(producs)+1):
                            abscissa.append(producs[-j].nombre)
                            ordinate.append(producs[-j].ventas)
                        self.grafica_estadisticas(abscissa, ordinate, 2, f"PRODUCTOS MÁS VENDIDOS: {rest.nombre}", "VENTAS")
                        
                        ans2 = input("""
¿Quiere seguir viendo los productos más vendidos? [s/n]: """)
                        while ans2 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans2 = input("¿Quiere seguir viendo los productos más vendidos? [s/n]: ")
                        if ans2 == "s":
                            continue
                        else:
                            return 
                    
                    else:
                        print(f"""
TOP 3 productos más vendidos de '{rest.nombre}'""")
                        for i in range(1,4):
                            print(f"{i}. {producs[-i].nombre}: {producs[-i].ventas} VENTAS")

                        abscissa = []
                        ordinate = []
                        for j in range(1, len(producs)+1):
                            abscissa.append(producs[-j].nombre)
                            ordinate.append(producs[-j].ventas)
                        self.grafica_estadisticas(abscissa, ordinate, 2, f"PRODUCTOS MÁS VENDIDOS: {rest.nombre}", "VENTAS")
                        
                        ans3 = input("""
¿Quiere seguir viendo los productos más vendidos? [s/n]: """)
                        while ans3 not in ["s", "n"]:
                            print("Ingreso inválido...")
                            ans3 = input("¿Quiere seguir viendo los productos más vendidos? [s/n]: ")
                        if ans3 == "s":
                            continue
                        else:
                            return

            elif opcion == "6":
                self.merge_sort(self.clientes, lambda x: len(x.entradas_compradas))
                cliente = self.clientes[-1]
                print(f"""
CLIENTE CON MÁS ENTRADAS COMPRADAS: {cliente.nombre}
COMPRA TOTAL: {len(cliente.entradas_compradas)} entradas
""")
                abscissa = []
                ordinate = []
                for n in range(1,len(self.clientes)+1):
                    nom = self.clientes[-n].nombre
                    abscissa.append(nom)
                    ent_cliente = len(self.clientes[-n].entradas_compradas)
                    ordinate.append(ent_cliente)
                self.grafica_estadisticas(abscissa, ordinate, 2, "CLIENTES CON MÁS ENTRADAS COMPRADAS", "ENTRADAS COMPRADAS")

            else:
                break

# Función que lee los archivos .pickle ya que aquí se guarda la información
    def leer_archivos(self, teams, stadiums, matches):
        try:
            with open("equipos.pickle", "rb") as file:
                self.equipos = pickle.load(file)
        except:
            self.register_data(teams, stadiums, matches)
            with open("equipos.pickle", "wb") as file:
                pickle.dump(self.equipos, file)
        try:
            with open("estadios.pickle", "rb") as file:
                self.estadios = pickle.load(file)
        except:
            self.register_data(teams, stadiums, matches)
            with open("estadios.pickle", "wb") as file:
                pickle.dump(self.estadios, file)
        try:
            with open("partidos.pickle", "rb") as file:
                self.partidos = pickle.load(file)
        except:
            self.register_data(teams, stadiums, matches)
            with open("partidos.pickle", "wb") as file:
                pickle.dump(self.partidos, file)
        try:
            with open("clientes.pickle", "rb") as file:
                self.clientes = pickle.load(file)
        except:
            with open("clientes.pickle", "wb") as file:
                pickle.dump(self.clientes, file)
        try:
            with open("entradas.pickle", "rb") as file:
                self.entradas = pickle.load(file)
        except:
            with open("entradas.pickle", "wb") as file:
                pickle.dump(self.entradas, file)
        try:
            with open("tipo_entradas.pickle", "rb") as file:
                self.tipo_entradas = pickle.load(file)
        except:
            with open("tipo_entradas.pickle", "wb") as file:
                pickle.dump(self.tipo_entradas, file)
        try:
            with open("entradas_verificadas.pickle", "rb") as file:
                self.entradas_verificadas = pickle.load(file)
        except:
            with open("entradas_verificadas.pickle", "wb") as file:
                pickle.dump(self.entradas_verificadas, file)

# Función que guarda los datos ingresados en los archivos .pickle para usarlos en cada inicio del programa
    def salvar_archivos(self):
        with open("equipos.pickle", "wb") as file_1:
            pickle.dump(self.equipos, file_1)
        with open("clientes.pickle", "wb") as file_2:
            pickle.dump(self.clientes, file_2)
        with open("entradas.pickle", "wb") as file_3:
            pickle.dump(self.entradas, file_3)
        with open("tipo_entradas.pickle", "wb") as file_4:
            pickle.dump(self.tipo_entradas, file_4)
        with open("entradas_verificadas.pickle", "wb") as file_5:
            pickle.dump(self.entradas_verificadas, file_5)
        with open("estadios.pickle", "wb") as file_6:
            pickle.dump(self.estadios, file_6)
        with open("partidos.pickle", "wb") as file_7:
            pickle.dump(self.partidos, file_7)

# Función que cumple el rol de menú principal y permite elegir una opción distinta donde cada una contiene una función del programa, además que inicia la lectura de los archivos .pickle con información guardada
    def menu(self, teams, stadiums, matches):
        self.register_data(teams, stadiums, matches)
        self.leer_archivos(teams, stadiums, matches)
        
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
        6. Cargar datos de API
        7. Guardar y salir
        """)
                
            opcion = input("Ingrese el número de la opción que desea elegir: ")
            while not opcion.isnumeric() or int(opcion) not in range(1,8):
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
                self.salvar_archivos()

            elif opcion == "3":
                print(f"""
{'~' * 100}""")
                self.confirmacion_asistencia()
                print(f"{'~' * 100}")
                self.salvar_archivos()

            elif opcion == "4":
                print(f"""
{'~' * 100}""")
                self.info_restaurantes()
                print(f"{'~' * 100}")

            elif opcion == "5":
                print(f"""
{'~' * 100}""")
                self.mostrar_estadisticas()
                print(f"{'~' * 100}")

            elif opcion == "6":
                print(f"""
{'~' * 100}""")
                ans1 = input("""
¿Quiere cargar los datos a su estado inicial? [s/n]: """)
                while ans1 not in ["s", "n"]:
                    print("Ingreso inválido...")
                    ans1 = input("¿Quiere cargar los datos a su estado inicial? [s/n]: ")
                
                if ans1 == "s":
                    self.estadios = []
                    self.partidos = []
                    self.entradas = []
                    self.tipo_entradas = {"General": [], "Vip": []}
                    self.entradas_verificadas = []
                    self.equipos = []
                    self.clientes = []
                    self.bebidas = []
                    self.comidas = []
                    self.register_data(teams, stadiums, matches)
                    print("""
Los datos fueron cargados correctamente...
El programa está en su estado inicial...
""")
                    print(f"{'~' * 100}")
                else:
                    print("""
Carga cancelada...""")

            else:
                print("""
Cerrando sesión...
Vuelva por más novedades del torneo internacional más competitivo...
¡LA EUROCOPA 2024!
""")
                self.salvar_archivos()
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
                self.salvar_archivos()
                break