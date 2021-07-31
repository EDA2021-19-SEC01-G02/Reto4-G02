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
from DISClib.ADT import orderedmap as om
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
                    'ids': None,
                    'countriesinfo': None,
                    'capitales': None,
                    'components': None
                    }

    analyzer['landing'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

    analyzer['countries'] = om.newMap(omaptype='RBT',
                                     comparefunction=compareCountries)

    analyzer['capitales'] = om.newMap(omaptype='RBT',
                                     comparefunction=compareCountries)
    
    analyzer['countriesinfo'] = om.newMap(omaptype='RBT',
                                     comparefunction=compareCountries)

    analyzer['ids'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

    analyzer['cableconections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareVertex)
    return analyzer

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

    origin = "<" + service['\ufefforigin'] + "-" + service['cable_id'] + ">"
    destination = "<" + service['destination'] + "-" + service['cable_id'] + ">"
    length = service['cable_length']
    if service['\ufefforigin'] == service['destination']:
        length = '0.100 km'
    addGraph(analyzer, origin, destination, length)
    addCapital(analyzer, origin, destination, length)
    return analyzer

def addGraph(analyzer, origen, destino, length):
    if not gr.containsVertex(analyzer['cableconections'],origen):
        gr.insertVertex(analyzer['cableconections'],origen)
    if not gr.containsVertex(analyzer['cableconections'],destino):
        gr.insertVertex(analyzer['cableconections'],destino)
    edge = gr.getEdge(analyzer['cableconections'], origen, destino)
    if edge is None:
        gr.addEdge(analyzer['cableconections'],origen, destino, length)
    return analyzer

def addCapital(analyzer, origen, destino, length):
    if mp.get(analyzer['landing'], origen) is not None and mp.get(analyzer['landing'], destino) is not None:
        pais_origen = mp.get(analyzer['landing'], origen)['value']['pais']
        print(pais_origen)
        pais_destino= mp.get(analyzer['landing'], destino)['value']['pais']
        info_origen = {'pais': pais_origen,
                        'origen':lt.newList(),
                        'peso': length}
        info_destino = {'pais': pais_destino,
                        'origen':lt.newList(),
                        'peso': length}
        capital_origen = om.get(analyzer['countriesinfo'], pais_origen)['value']['CapitalName']
        capital_destino = om.get(analyzer['countriesinfo'], pais_destino)['value']['CapitalName']
        entry = om.get(analyzer['capitales'], capital_origen)
        if entry is None:
            info_origen = {'pais': pais_origen,
                        'origen':lt.newList(),
                        'peso': length}
            om.put(analyzer['capitales'], capital_origen, info_origen)
        lt.addLast(entry['value']['origen'], origen)
        if entry['value']['peso'] < length:
            entry['value']['peso'] = length
        
        entrada = om.get(analyzer['capitales'], capital_destino)
        if entrada is None:
            info_destino = {'pais': pais_destino,
                            'origen':lt.newList(),
                            'peso': length}
            om.put(analyzer['capitales'], capital_destino, info_destino)
        lt.addLast(entrada['value']['origen'], destino)
        if entrada['value']['peso'] < length:
            entrada['value']['peso'] = length

def conectarCapitales(analyzer):
    llaves = om.keySet(analyzer['capitales'])
    for key in llaves:
        if om.get(analyzer['capitales'], key) is not None:
            entry = om.get(analyzer['capitales'], key)['value']
            for point in entry['origen']:
                if not gr.containsVertex(analyzer['cableconections'],key):
                    gr.insertVertex(analyzer['cableconections'],key)
                edge = gr.getEdge(analyzer['cableconections'], key, point)
                if edge is None:
                    gr.addEdge(analyzer['cableconections'],key, point, entry['peso'])
                edge1 = gr.getEdge(analyzer['cableconections'], point, key)
                if edge1 is None:
                    gr.addEdge(analyzer['cableconections'],point, key, entry['peso'])

    #en otro mapa guardar los ids como llaves y como valor el string service["origin"] y service["service[cable id"]


def loadlandings(analyzer, landing):
    entry = mp.get(analyzer['landing'], landing['landing_point_id'])
    pais= landing['name'].split(",")
    if len(pais) == 1:
        info = pais[0].strip()
    else:
        info = pais[1].strip()
    idlanding = landing["landing_point_id"]
    if entry is None:
        addinformacion = {'pais':info,
                                'informacion': landing}
        mp.put(analyzer['landing'], landing['landing_point_id'], addinformacion)
    addCountry(analyzer, info , idlanding)
 
def addCountry(analyzer, country, idlanding):
    paises = analyzer['countries']
    entry = om.get(paises, country)
    if entry is None:
        lista = lt.newList()
        lt.addLast(lista, idlanding)
        om.put(paises, country, lista)
    else:
        lt.addLast(entry['value'], idlanding)
    #para asegurarme que solo este agregando
    #lo cambie a un order map 

def loadCountries(analyzer, country):
    entry = om.get(analyzer['countriesinfo'], country['CountryName'])
    if entry is None:
        om.put(analyzer['countriesinfo'], country['CountryName'], country)
    return analyzer


# Funciones para creacion de datos

# Funciones de consulta

def connected(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['vertex'] = scc.KosarajuSCC(analyzer['cableconections'])
    return scc.connectedComponents(analyzer['vertex'])

def landingPoints(analyzer):
    """
    Retorna el total de landing points (vertices) del grafo
    """
    return gr.numVertices(analyzer['cableconections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['cableconections'])

def totalCountries(analyzer):
    return om.size(analyzer['countries'])

def informacionLanding(analyzer):
    primero = mp.get(analyzer['landing'], '3316')
    informacion = primero['value']['informacion']
    return informacion

def informacionCountries(analyzer):
    primero = om.get(analyzer['countriesinfo'], 'Chuuk')
    informacion = primero['value']
    return informacion

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['cableconections'])
    return scc.connectedComponents(analyzer['components'])

def sameCluster(analyzer, origen, destino):
    adyacentes = gr.adjacents(analyzer['cableconections'],origen)
    relacion = False
    if lt.isPresent(adyacentes, destino):
        relacion = True
    return relacion

"""
def sameCluster(analyzer, origen, destino):
    vertice1 = gr.containsVertex(analyzer['cableconections'], origen)
    vertice2 = gr.containsVertex(analyzer['cableconections'], destino)
    if vertice1 is False and vertice2 is False:
        return "0"
    elif vertice1 is False:
        return "1"
    elif vertice2 is False:
        return "2"
    else:
        return scc.stronglyConnected(analyzer['cableconections'], origen, destino)
"""

# Funciones utilizadas para comparar elementos dentro de una lista
def compareVertex(trip1,trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2['key']):
        return 1
    else:
        return -1
    #compara las llaves
def compareCountries(c1,c2):
    if (c1 == c2):
        return 0
    elif (c1 > c2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
