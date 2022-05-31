from draw import *
from layers import *

if __name__ == "__main__":
    # DEMO

    # ejemplo_01
    # draw_face(faces['f1'])
    # draw_face(faces['f2'])
    folder = 'ejemplo_01'
    layers = 2

    # ejemplo_02
    # folder = 'ejemplo_02'
    # layers = 2
    # vertices, edges, faces = save_layer(folder, f"0{2}")
    # draw_face(faces['f1'])
    # draw_face(faces['f2'])
    # draw_face(faces['f3'])
    # draw_face(faces['f4'])

    # ejemplo_03
    # folder = "ejemplo_03"
    # layers = 1
    #draw_face(faces['CARA2'])
    #draw_face(faces['CARA3'])
    #draw_face(faces['CARA4'])

    vertices, edges, faces = connect_layers(folder, layers)
    # after connecting
    vertices, edges, faces = save_layer(folder, f"0{layers + 1}")
    draw_faces(faces)

    draw(folder)
    # exit()