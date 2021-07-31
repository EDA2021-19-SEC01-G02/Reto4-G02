"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar clusteres y landing points :")
    print("3- Encontrar ruta minima para envio de informacion:")
    print("4- Consultar infraestructura critica: ")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadAnalyzer(catalog)
        numedges = controller.landingPoints(catalog)
        numvertex = controller.totalConnections(catalog)
        primero = controller.informacionLanding(catalog)
        countries = controller.totalCountries(catalog)
        informacion = controller.informacionCountries(catalog)
        print('Total landing points: ' + str(numedges))
        print('Total conexiones landing points: ' + str(numvertex))
        print(' Id Primer landing point: ' + str(primero['landing_point_id']) + " ID: "  + str(primero["id"]) + " Nombre: "  + str(primero["name"]) + " Latitud: " + str(primero["latitude"]) + " Longitud: " + str(primero["longitude"]))
        print('Paises cargados: ' + str(countries))
        print('Poblacion ultimo pais cargado: ' + str(informacion["Population"]) + ' Usuarios de internet ultimo pais cargado: ' + str(informacion["Internet users"]))


    elif int(inputs[0]) == 2:
        lp1 = input("Ingrese el nombre del landing point 1: ")
        lp2 = input("Ingrese el nombre del landing point 2: ")
        conected = controller.connectedComponents(catalog)    
        cluster = controller.sameCluster(catalog,lp1,lp2)
        print('Elementos fuertemenete conectados: ' + str(conected))
        print('Los dos landing points pertenecen al mismo cluster : ' + str(cluster))
    

    else:
        sys.exit(0)
sys.exit(0)
