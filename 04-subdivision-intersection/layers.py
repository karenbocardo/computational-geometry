from data import *

from intersections.algoritmo import AlgoritmoBarrido
from intersections.Punto import Punto
from intersections.Segmento import Segmento

# @TODO check if segment already exists
def save_segments(edge: Edge): # saves a list of segments from the given edge
    segments = list()
    vertices = edge.figure_vertices()
    if len(vertices) > 2: vertices.append(edge.origin.point) # to close figure

    '''
    for index in range(len(vertices) - 1):
        start, end = vertices[index], vertices[index + 1]
        start_point = Punto(start.x, start.y)
        end_point = Punto(end.x, end.y)
        segment = Segmento(start_point, end_point, f"x{index}")
        segments.append(segment)
        
    '''
    edges = edge.figure_edges()
    if len(edges) > 2: edges.append(edge)
    for index in range(len(edges) - 1):
        curr_edge, next_edge = edges[index], edges[index + 1]
        start, end = curr_edge.origin, next_edge.origin
        start_point = Punto(start.point.x, start.point.y)
        end_point = Punto(end.point.x, end.point.y)
        segment = Segmento(start_point, end_point, curr_edge.name)
        segments.append(segment)

    return segments

def get_prime(edge_name): return f"{edge_name}_"
def get_biprime(edge_name): return f"{edge_name}__"

def connect_layers(folder, layers):
    vertices, edges, faces = save_layers(folder, layers)

    segments = list()
    print(f"faces: {faces.keys()}")
    for face_name, face in faces.items():
        if face.inside:
            for inside in face.inside:
                segments += save_segments(inside)
        if face.outside:
            segments += save_segments(face.outside)

    print("segments:")
    [print(f"[{i}]{segment}") for i, segment in enumerate(segments)]

    barr = AlgoritmoBarrido(segments)
    barr.barrer()

    print(f"intersections:")
    for index, intersection in enumerate(barr.R):
        print(f"[{index}]{intersection}")
        point = Point(intersection.point.x, intersection.point.y)
        new_vertex = Vertex(f"p{len(vertices)+1}", point, "incidente")

        for segment in intersection.segments: # reading segments that intersect
            edge = edges[segment.name] # segments represent edges, saved in map
            # each edge is divided in two: self prime and self biprime

            prime_name = get_prime(edge.name) # prime
            edges[prime_name] = edges.pop(edge.name) # prime will take original edge place
            prime = edges[prime_name]
            prime.name = prime_name

            biprime_name = get_biprime(edge.name)
            biprime = Edge(biprime_name,origin=None, pair=None, face=None, next=None, previous=None) # new edge
            edges[biprime_name] = biprime

            biprime.origin = new_vertex # biprimes have new vertex as origin
            print(edge.pair.name)
            pair_name = get_biprime(edge.pair.name) # pair
            if not pair_name in edges: # if pair doesnt already exist
                edges[pair_name] = None
            prime.pair = edges[pair_name]

    return vertices, edges, faces