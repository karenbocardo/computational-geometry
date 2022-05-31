'''
edges linked list - reading data from files
'''
from classes import *

'''
ejemplo_01
    layer +
        01 +
            .ari
            .car
            .ver
        02 +
            .ari
            .car
            .ver
folder = ejemplo_01
layer = 01
'''
def read_files(folder, layer):
    vertices_ext, edges_ext, faces_ext  = 'ver', 'ari', 'car',  # extensions
    def read_file(filename):
        file = open(filename)
        return file.read().splitlines()[4:]
    def path(ext): return f"test-cases/{folder}/layer{layer}.{ext}"
    vertices_data = read_file(path(vertices_ext))
    edges_data = read_file(path(edges_ext))
    faces_data = read_file(path(faces_ext))
    return vertices_data, edges_data, faces_data

def save_layers(folder, layers):
    vertices, edges, faces = dict(), dict(), dict()
    for index in range(1, layers + 1):
        # layer = '01'
        new_vertices, new_edges, new_faces = save_layer(folder, f"0{index}")
        vertices |= new_vertices
        edges |= new_edges
        faces |= new_faces

    return vertices, edges, faces


def save_layer(folder, layer):
    '''
    Reads lines from three files that contain data for vertices, edges and data,
    and saves the data on instances of those classes. It also links all the objects
    among  them, creating an Edge Linked List.
    :param folder: Folder where files are stored
    :param layer: Number of layer on files
    :return:
    '''
    def says_none(s): return s == 'None'

    vertices_data, edges_data, faces_data = read_files(folder, layer)
    vertices_map, edges_map, faces_map = dict(), dict(), dict()
    for line in vertices_data: # reads and saves vertices
        # Nombre  x  y  Incidente
        name, x, y, incident = line.split()
        vertex = Vertex(name, Point(float(x), float(y)), incident)
        vertices_map[name] = vertex
    for line in edges_data: # reads and saves edges
        # Nombre  Origen  Pareja  Cara    Sigue   Antes
        name, origin, pair, face, next, previous = line.split()
        if says_none(next): next = None
        if says_none(previous): previous = None
        edge = Edge(name, origin, pair, face, next, previous)
        edges_map[name] = edge
    for line in faces_data: # reads and saves faces
        # Nombre  Interno Externo
        name, inside, outside  = line.split()
        if says_none(inside): inside = None
        elif inside.startswith('['): # inside is written a list
            inside = inside[1:-1] # remove brackets
            inside = inside.split(',')
        else:
            inside = [inside]
        if says_none(outside): outside = None
        face = Face(name, outside, inside)
        faces_map[name] = face

    # linking
    for vertex in vertices_map.values():
        # strings to replace: incident
        vertex.incident = edges_map[vertex.incident]
    for edge in edges_map.values():
        # strings to replace: origin, pair, face, next, previous
        edge.origin = vertices_map[edge.origin]
        edge.pair = edges_map[edge.pair]
        edge.face = faces_map[edge.face]
        if edge.next: edge.next = edges_map[edge.next] # can be None
        if edge.previous: edge.previous = edges_map[edge.previous] # can be None

    for face in faces_map.values():
        # strings to replace: outside, inside
        if face.outside: face.outside = edges_map[face.outside] # can be None
        if face.inside: # can be None
            face.inside = [edges_map[inside] for inside in face.inside]
    # return list(vertices_map.values()), list(edges_map.values()), list(faces_map.values())
    return vertices_map, edges_map, faces_map
