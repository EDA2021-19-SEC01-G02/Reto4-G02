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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.singlelinkedlist import addLast
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

   landing: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre landing points
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                    'landing': None,
                    'cableconections': None,
                    'countries': None,
                    'paths': None
                    }

    analyzer['landing'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

    analyzer['countries'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')
    analyzer['cableconections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000)

# Funciones para agregar informacion al catalogo
def addLandingPoint(analyzer, service):
    """
    Adiciona los landing points al grafo como vertices y arcos entre los
    landing points adyacentes.

    Los vertices tienen por nombre el origen y destino
    seguido de el id del cable.  Por ejemplo:

    3316-2africa

    Si es un cable con una ruta diferente seria: 3316-africa-coast-to-europe-ace
    """
    format = formatVertex(service)
    origin = format[0]
    destination = format[1]
    sameVertex(service)
    length = service['cable_length']
    addlanding(analyzer, origin)
    addlanding(analyzer, destination)
    addConnection(analyzer, origin, destination, length)
    return analyzer

def addlanding(analyzer, cableid):
    """
    Adiciona un ladingpoint como un vertice del grafo
    """
        if not gr.containsVertex(analyzer['cableconections'], cableid):
            gr.insertVertex(analyzer['cableconections'], cableid)
        return analyzer
"""
def addRouteStop(analyzer, service):
    """
    #Agrega a un cable, una ruta que es servida en ese paradero
    """
    entry = mp.get(analyzer['landing'], service['landing_point_id'])
    if entry is None:
        lstlanding = lt.newList(cmpfunction=compareroutes)
        #tambien comparo rutas?
        lt.addLast(lstlanding, service['cable_id'])
        mp.put(analyzer['landing'], service['landing_point_id'], lstlanding)
    else:
        lstlanding = entry['value']
        info = service['cable_id']
        if not lt.isPresent(lstlanding, info):
            lt.addLast(lstlanding, info)
    return analyzer
    #para cada landing point adiciono el id del cable en la lista
"""

def addConnection(analyzer, origin, destination, cablelength):
    """
    Adiciona un arco entre dos landing points
    """
    edge = gr.getEdge(analyzer['cableconections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['cableconections'], origin, destination, cablelength)


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    origen = lt.newList()
    lt.addLast(origen,service['origin'])
    lt.addLast(origen,service['cable_id'])
    destino = lt.newList()
    lt.addLast(destino,service['destination'])
    lt.addLast(destino,service['cable_id'])
    return origen, destino
    """"
    origen = service['origin'] + '-' + service['cable_id']
    destino = service['destination'] + '-' + service['cable_id']
    return origen,destino
    """
    #en otro mapa guardar los ids como llaves y como valor el string service["origin"] y service["service[cable id"]
    

def sameVertex(service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['origin'] == service['destination']:
        service['cable_length'] = "0.100 km"

def loadlandings(analyzer, landing):
    mp.put(analyzer['landing'], landing["landing_point_id"], landing)
    pais= landing["name"].split(', ')[1].lower()
    idlanding = landing["landing_point_id"]
    addCountry(analyzer, pais , idlanding)

     

def addCountry(analyzer, country, idlanding):
    paises = analyzer['countries']
    if mp.contains(paises, country):
        value = me.getValue(mp.get(paises, country))
        lt.addLast(value, idlanding)
    else:
        lista = lt.newList()
        lt.addLast(lista, idlanding)
    mp.put(paises, country, lista)

def loadCapital(analyzer, capital):
    gr.insertVertex(analyzer['cableconections'], capital["CapitalName"])
    paises = analyzer['countries']
    country = capital["CountryName"].lower()
    if mp.contains(paises, country):
        value = me.getValue(mp.get(paises, country))




# Funciones para creacion de datos

# Funciones de consulta

def connected(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['vertex'] = scc.KosarajuSCC(analyzer['cableconections'])
    return scc.connectedComponents(analyzer['vertex'])

def totalStops(analyzer):
    """
    Retorna el total de landing points (vertices) del grafo
    """
    return gr.numVertices(analyzer['landing'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['landing'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
