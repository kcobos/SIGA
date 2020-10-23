# -*- coding: utf-8 -*-
import argparse
import csv
import json
import urllib.request
import numpy

parser = argparse.ArgumentParser(description='Proceso para poblar la BBDD.')
parser.add_argument('-u','--url', help='URL de la API REST', default='http://192.168.1.x:8080')
parser.add_argument('-e', '--estados', help='Creación de estados', action='store_true')
args = parser.parse_args()

estados = [0,1,2]
pesos = [0.3, 0.6, 0.1]

url = args.url
csv_file = "plazas.csv"

with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader, None)
    for row in reader:
        # print(
        # "id",row[0],
        # "direccion",row[1],
        # "numero",row[2],
        # "plazas",row[3],
        # "observacion",row[4],
        # "latitud",row[5],
        # "longitud",row[6]
        # )

        # añadir id_ubicacion
        url_ubicacion = url+"/ubicacion/nueva"
        if row[2] == "":
            direccion = row[1]+", S/N"
        else:
            direccion = row[1]+", "+row[2]
        parametros = json.dumps({
                        "direccion": direccion,
                        "latitud": row[5],
                        "longitud": row[6],
                        "observaciones": row[4]
                    }).encode('utf8')
        req = urllib.request.Request(url_ubicacion, data=parametros, headers={'content-type': 'application/json'}, method='POST')
        response = urllib.request.urlopen(req)

        res = json.loads(response.read().decode('utf8'))
        if res["estado"]:
            id = res["id"]
            # añadir plazas de la ubicacion
            url_plaza = url+"/plaza/nueva"
            parametros_plaza = json.dumps({
                            "id_ubicacion": id
                        }).encode('utf8')
            for i in range(int(row[3])):
                req = urllib.request.Request(url_plaza, data=parametros_plaza, headers={'content-type': 'application/json'}, method='POST')
                response = urllib.request.urlopen(req)
                res = json.loads(response.read().decode('utf8'))
                if res["estado"]:
                    if args.estados:
                        id_plaza = res["id"]
                        # actualizar estado de plaza
                        estado_nuevo = numpy.random.choice(estados, p=pesos)
                        req = urllib.request.Request(url+"/plaza/"+str(id_plaza)+"/estado/"+str(estado_nuevo), method='PUT')
                        response = urllib.request.urlopen(req)
                        res = json.loads(response.read().decode('utf8'))
                        if not res["actualizado"]:
                            print("ERROR ACTUALIZAR ESTADO")
                            print(res)
                            exit()
                else:
                    print("ERROR AÑADIR PLAZA")
                    print(res)
                    exit()
        else:
            print("ERROR AÑADIR UBICACION")
            print(res)
            exit()
