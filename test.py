mapa_estadio = []
columnas = 10
limite = 900
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

asientos_tomados = []
 
for i in lista_abc[:filas]:
    fila = []
    for j in range(1, columnas + 1):
        asiento1 = f"{i}{j}"
        if asiento1 in asientos_tomados:
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
