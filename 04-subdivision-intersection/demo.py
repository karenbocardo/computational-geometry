from draw import *

if __name__ == "__main__":
    # DEMO
    folder = 'ejemplo_03'

    layer = '01'
    vertices, edges, faces = save_data(folder, layer)

    draw_face(faces['CARA2'])
    draw_face(faces['CARA3'])
    draw_face(faces['CARA4'])

    draw()
    # exit()