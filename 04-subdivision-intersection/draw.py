from data import *
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt


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
        coordinates = [vertex.x, vertex.y]
        vertices.append(coordinates)

        next_edge = curr.next
        if next_edge == edge: break
        curr = next_edge

    xy = np.array(vertices)
    polygon = Polygon(xy, True)
    patches.append(polygon)


def draw_face(face_name):
    '''
    Uses the draw_from_edge function to draw all the figures either outside
    or inside a Face.
    :param face_name: Name of the face to draw
    :return: None
    '''
    face = faces[face_name]
    if face.inside:
        for inside in face.inside:
            draw_from_edge(inside)
    if face.outside:
        draw_from_edge(face.outside)

if __name__ == "__main__":
    # DEMO
    folder = 'ejemplo_03'
    layer = '01'
    vertices, edges, faces = save_data(folder, layer)

    ax = plt.subplot()
    patches = []

    draw_face('CARA2')
    draw_face('CARA3')
    draw_face('CARA4')

    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.5)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    ax.margins(0.05)
    plt.savefig("fig.png")
    # plt.show()
    # exit()

