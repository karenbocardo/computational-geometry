from lib import Point

class Vertex():
    def __init__(self, name, point, incident):
        self.name = name
        self.point = point
        self.incident = incident # initially a string

class Edge():
    def __init__(self, name=None, origin=None, pair=None, face=None, next=None, previous=None):
        self.name = name
        self.origin = origin
        self.pair = pair
        self.face = face
        self.next = next
        self.previous = previous
    def figure_vertices(self):
        '''
        :return: List of the points of the vertices that start in this edge
        '''
        vertices = list()  # list of points
        curr = self
        while curr:  # cicle to read figure edges
            vertex = curr.origin
            vertices.append(vertex.point)
            next_edge = curr.next
            if next_edge == self: break
            curr = next_edge
        return vertices
    def figure_edges(self):
        '''
        :return: List of the edges connected to this edge
        '''
        edges = list()  # list of points
        curr = self
        while curr:  # cicle to read figure edges
            edges.append(curr)
            next_edge = curr.next
            if next_edge == self: break
            curr = next_edge
        return edges

class Face():
    def __init__(self, name, outside, inside):
        self.name = name
        self.outside = outside
        self.inside = inside # list
    # def add_inside(self, edge): self.inside.append(edge)

class Cycle():
    def __init__(self, name, edges, left, is_internal):
        self.name = name
        self.edges = edges
        self.left = left
        self.is_internal = is_internal


'''
    #data = read_file(sys.argv[1])
    data = read_file('0.in')
if len(data[0].split()) < 2: data.remove(data[0])
segments = list()
for line in data:
    sep = line.split()
    point1 = SegmPoint(float(sep[0]), float(sep[1]))
    point2 = SegmPoint(float(sep[2]), float(sep[3]))
    if len(sep) > 4:
        name = sep[4]
        segment = Segment(point1, point2, name)
    else: segment = Segment(point1, point2)
    segments.append(segment)
'''