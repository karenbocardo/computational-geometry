from lib import Point

class Vertex():
    def __init__(self, name, point, incident):
        self.name = name
        self.point = point
        self.incident = incident # initially a string
    def get_coordinates(self):
        return self.x, self.y

class Edge():
    def __init__(self, name, origin, pair, face, next, previous):
        self.name = name
        self.origin = origin
        self.pair = pair
        self.face = face
        self.next = next
        self.previous = previous

class Face():
    def __init__(self, name, outside, inside):
        self.name = name
        self.outside = outside
        self.inside = inside # list
    # def add_inside(self, edge): self.inside.append(edge)


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