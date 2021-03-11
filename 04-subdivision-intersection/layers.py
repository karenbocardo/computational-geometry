from data import *

#from intersections.algoritmo import AlgoritmoBarrido
#from intersections.Punto import Punto
#from intersections.Segmento import Segmento

def connect_layers(folder, layers):
    vertices, edges, faces = save_layers(folder, layers)
    return vertices, edges, faces

