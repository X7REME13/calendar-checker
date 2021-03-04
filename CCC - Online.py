import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets as pyg


def booleanizarHorarios(data):
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

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creden.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1W9Nv52R7Chugln-ta4j-7wZNyFObbd5Ou6VtY09V25A/edit?usp=sharing")
    nombreArchivo = "THIS SHIT WORKS"

    personas = []
    for x in range(1,len(sheet.worksheets()) - 1):
        sheet_instance = sheet.get_worksheet(x)
        dataList = sheet_instance.get_all_records()
        horario = {"inicio1": [], "final1": [],
                   "inicio2": [], "final2": []}
        for dia in dataList:
            horario["inicio1"].append(dia["Horario inicio 1"])
            horario["final1"].append(dia["Horario final 1"])
            horario["inicio2"].append(dia["Horario inicio 2"])
            horario["final2"].append(dia["Horario final 2"])

        personas.append(horario)

    horariosBooleanisados = booleanizarHorarios(personas)

    horariosCantDisponibles = procesarHorariosBooleanisados(horariosBooleanisados)

    horariosTabla = [["Hora","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]]

    for x in range(len(horariosCantDisponibles[0])):
        horariosTabla.append([x,horariosCantDisponibles[0][x],horariosCantDisponibles[1][x],horariosCantDisponibles[2][x],horariosCantDisponibles[3][x],horariosCantDisponibles[4][x],horariosCantDisponibles[5][x],horariosCantDisponibles[6][x]])

    resultados = sheet.get_worksheet((len(sheet.worksheets()) - 1))

    mensaje = resultados.update("A1",horariosTabla)

    print("═════════════════════════════════════════════════════════════════════")
    print(mensaje)
    print("═════════════════════════════════════════════════════════════════════")
