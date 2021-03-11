from draw import *

if __name__ == "__main__":
    # DEMO
    folder = 'ejemplo_03'

    layer = '01'
    vertices, edges, faces = save_data(folder, layer)

    draw_face(faces['CARA2'])
    draw_face(faces['CARA3'])
    draw_face(faces['CARA4'])

    # patches
    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.5)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    ax.margins(0.05)
    plt.savefig("fig.png")
    # plt.show()
    # exit()