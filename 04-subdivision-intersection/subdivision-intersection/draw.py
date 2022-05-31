from classes import Edge, Face
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

# plots
ax = plt.subplot()
patches = []

def separate(points):
    x, y = [], []
    for point in points:
        x.append(point.x)
        y.append(point.y)
    return x, y

def draw_from_edge(edge: Edge):
    '''
    Draws a figure given a start Edge by reading the Edge Linked List next Edge,
    saves figure as Polygon and adds it to the global list of patches.
    :param edge: Start edge for
    :return: None
    '''
    vertices = edge.figure_vertices()
    if len(vertices) > 2: # case of polygon
        xy = np.array([[point.x, point.y] for point in vertices])
        polygon = Polygon(xy, True)
        patches.append(polygon)
        x, y = separate(vertices + [vertices[0]])
    else:
        x, y = separate(vertices)
    ax.scatter(x, y, color='grey')
    ax.plot(x, y, color='grey')

def draw_faces(faces: dict):
    for face in faces.values(): draw_face(face)

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

def draw(folder):
    # patches
    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.5)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    ax.margins(0.05)
    plt.savefig(f"test-cases/{folder}/out.png")
    plt.show()