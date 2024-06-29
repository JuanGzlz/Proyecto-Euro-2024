while True:
    try:
        id_entrada = int(input("Ingrese el ID de la entrada para verificarla y confirmar su asistencia: "))
        if len(str(id_entrada)) == 10:
            break
        else:
            print("Ingreso inválido...")
    except ValueError:
        print("Ingreso inválido...")