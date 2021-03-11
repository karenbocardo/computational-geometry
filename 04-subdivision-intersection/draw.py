from data import *
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

# plots
ax = plt.subplot()
patches = []

def draw_from_edge(edge: Edge):
    '''
    Draws a figure given a start Edge by reading the Edge Linked List next Edge,
    saves figure as Polygon and adds it to the global list of patches.
    :param edge: Start edge for
    :return: None
    '''
    vertices = list()
    curr = edge
    while curr: # cicle to read figure edges
        vertex = curr.origin
        coordinates = [vertex.point.x, vertex.point.y]
        vertices.append(coordinates)

        next_edge = curr.next
        if next_edge == edge: break
        curr = next_edge

    xy = np.array(vertices)
    polygon = Polygon(xy, True)
    patches.append(polygon)


def draw_face(face: Face):
    '''
    Uses the draw_from_edge function to draw all the figures either outside
    or inside a Face.
    :param face_name: Name of the face to draw
    :return: None
    '''
    #face = faces[face_name]
    if face.inside:
        for inside in face.inside:
            draw_from_edge(inside)
    if face.outside:
        draw_from_edge(face.outside)

