import pandas as pd


def booleanisarHorarios(data):
    horariosPorPersonas = []
    for value in data:
        horarioBool = [[], [], [], [], [], [], []]
        for x in range(7):
            horaInicioDisp1 = value["inicio1"][x]
            horaFinalDisp1 = value["final1"][x]
            horaInicioDisp2 = value["inicio2"][x]
            horaFinalDisp2 = value["final2"][x]

            for hora in range(24):
                horarioBool[x].append(
                    (horaInicioDisp1 <= hora < horaFinalDisp1) or (horaInicioDisp2 <= hora < horaFinalDisp2))

        horariosPorPersonas.append(horarioBool)

    return horariosPorPersonas


def procesarHorariosBooleanisados(horariosBooleanisados):
    horariosCantDisponibles = [[], [], [], [], [], [], []]

    for dia in range(7):
        for hora in range(24):
            disponible = 0
            for persona in horariosBooleanisados:
                if persona[dia][hora]:
                    disponible += 1
            horariosCantDisponibles[dia].append(disponible)

    return horariosCantDisponibles


if __name__ == '__main__':

    # nombreArchivo = input(">> Ingrese el nombre del archivo sin extension: ")
    nombreArchivo = "Horarios"
    archivoEntero = None
    while archivoEntero == None:
        try:
            archivoEntero = pd.ExcelFile(nombreArchivo + ".xlsx")
        except Exception:
            print("<< No se encuentra el archivo en el directorio actual."
                  "\n   Compruebe si el nombre es el correcto o si esta en"
                  "\n   el mismo directorio que este programa")
            print("═════════════════════════════════════════════════════════════════════")
            nombreArchivo = input(">> Ingrese el nombre del archivo sin extension: ")

    personas = []

    for x in range(len(archivoEntero.sheet_names) - 1) :
        archivo = pd.read_excel(archivoEntero, x)
        dataList = archivo.to_dict("list")
        horario = {"inicio1": dataList["Horario inicio 1"], "final1": dataList["Horario final 1"],
                   "inicio2": dataList["Horario inicio 2"], "final2": dataList["Horario final 2"]}
        personas.append(horario)

    horariosBooleanisados = booleanisarHorarios(personas)

    horariosCantDisponibles = procesarHorariosBooleanisados(horariosBooleanisados)


    horariosTabla = {
        "Lunes": horariosCantDisponibles[0],
        "Martes": horariosCantDisponibles[1],
        "Miercoles": horariosCantDisponibles[2],
        "Jueves": horariosCantDisponibles[3],
        "Viernes": horariosCantDisponibles[4],
        "Sabado": horariosCantDisponibles[5],
        "Domingo": horariosCantDisponibles[6]
    }

    dataFrame = pd.DataFrame(horariosTabla)

    nombreArchivo = nombreArchivo + " - Procesados.xlsx"

    dataFrame.to_excel(nombreArchivo)

    print(dataFrame)
    print("═════════════════════════════════════════════════════════════════════")
    print("<< Se guardo correctamente el archivo con los horarios disponibles."
          "\n   Puede encontrar el archivo en la misma carpeta que el programa"
          "\n   con el nombre:", nombreArchivo)
