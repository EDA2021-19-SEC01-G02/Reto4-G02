"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newAnalyzer()
    return catalog

# Funciones para la carga de datos
def loadAnalyzer(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    landingsfile = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(landingsfile, encoding="utf-8"),
                                delimiter=",")
    for point in input_file:
        model.loadlandings(analyzer, point)

    countriessfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(countriessfile, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        model.loadCountries(analyzer, country)
    
    servicesfile = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.addLandingPoint(analyzer, service)
    model.conectarCapitales(analyzer)


    return analyzer


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def landingPoints(analyzer):
    """
    Retorna el total de landing points (vertices) del grafo
    """
    return model.landingPoints(analyzer)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return model.totalConnections(analyzer)


def totalCountries(analyzer):
    return model.totalCountries(analyzer)

def informacionLanding(analyzer):
    return model.informacionLanding(analyzer)

def informacionCountries(analyzer):
    return model.informacionCountries(analyzer)

def connectedComponents(analyzer):
    return model.connectedComponents(analyzer)
    
def sameCluster(analyzer, origen, destino):
    return model.sameCluster(analyzer, origen, destino)

def minimumPath(analyzer, c1, c2):
    return model.minimumPath(analyzer, c1, c2)