from draw import *
from layers import *

if __name__ == "__main__":
    # DEMO
    folder = 'ejemplo_01'
    layers = 2
    vertices, edges, faces = connect_layers(folder, layers)

    # ejemplo_01
    draw_face(faces['f1'])
    draw_face(faces['f2'])

    # ejemplo_03
    #draw_face(faces['CARA2'])
    #draw_face(faces['CARA3'])
    #draw_face(faces['CARA4'])

    draw()
    # exit()