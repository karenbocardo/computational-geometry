from data import *

from intersections.algoritmo import AlgoritmoBarrido
from intersections.Punto import Punto
from intersections.Segmento import Segmento

def save_segments(edge: Edge): # saves a list of segments from the given edge
    segments = list()
    vertices = edge.figure_vertices()
    if len(vertices) > 2: vertices.append(edge.origin.point) # to close figure

    for index in range(len(vertices) - 1):
        start, end = vertices[index], vertices[index + 1]
        start_point = Punto(start.x, start.y)
        end_point = Punto(end.x, end.y)
        segment = Segmento(start_point, end_point)
        segments.append(segment)

    return segments

def connect_layers(folder, layers):
    vertices, edges, faces = save_layers(folder, layers)

    segments = list()
    print(faces)
    for face_name, face in faces.items():
        if face.inside:
            for inside in face.inside:
                segments += save_segments(inside)

    print("segments:")
    [print(f"[{i}]{segment}") for i, segment in enumerate(segments)]

    barr = AlgoritmoBarrido(segments)
    barr.barrer()
    print(f"intersections:")
    [print(inter) for inter in barr.R]


    return vertices, edges, faces

