from lib import *

'''
Q — queue of events, it can be: 
    + superior point of segment
    + inferior point of segment
    + possible intersection
BST — binary search tree, its nodes have points
    + make sure it pops() the leaf child at the very left
SegPoint — point that belongs to segment
    + has a list of segments
Q tree — sorts points by 
inoder — returns sorted
'''

class SegmPoint(Point): # point that can belong to segments
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.segments = []
    def add_segment(self, segment):
        self.segments.append(segment)
    def get_segments(self):
        return self.segments

def print_segments(segments):
    print("SEGMENTS")
    for segment in segments:
        print(f" · {segment}")

class Segment:
    def __init__(self, pointA: SegmPoint, pointB: SegmPoint, name=None):
        if pointA.greater_y(pointB):
            self.superior = pointA
            self.inferior = pointB
        else:
            self.superior = pointB
            self.inferior = pointA
        self.line = pts_to_line(self.superior, self.inferior)
        self.name = name
    def intersects_with(self, other):
        return segs_intersect(self, other)
    def __repr__(self):
        if self.name: return f"{self.name}"
        return f"{{{self.superior}, {self.inferior}}}"
    def __eq__(self, other):
        return self.superior == other.superior and self.inferior == other.inferior
    def __hash__(self): # makes segments hashable
        # return hash(f'{self.superior} {self.inferior}')
        return hash(tuple([self.superior, self.inferior]))

class Intersection:
    def __init__(self, point: SegmPoint, segments):
        self.point = point
        self.segments = segments
    def __repr__(self):
        res =  f"{self.point} ->"
        for segment in self.segments:
            res += f" {segment}"
        return res

def segs_intersect(seg1: Segment, seg2: Segment):
    # @FIXME
    # returns intersection of segment infinite lines,
    # but algorithm doesnt work when it returns the segments intersection
    if seg1 == seg2: return False
    intersection = seg1.line.intersects_with(seg2.line)
    #return intersection
    #if not intersection: return False
    #print(f"\tinsersection: {intersection}")
    #print("\t",x_min, x_max, y_min, y_max)
    if not intersection: return None
    print(f"\t\t\t\t{seg1} intersects with {seg2} on {intersection}")


    def in_seg_square(seg):
        x = [seg.inferior.x, seg.superior.x]
        y = [seg.inferior.y, seg.superior.y]
        x_min, x_max = min(x), max(x)
        y_min, y_max = min(y), max(y)
        return intersection.in_square(x_min, x_max, y_min, y_max)
    in_square1 = in_seg_square(seg1)
    in_square2 = in_seg_square(seg2)
    if in_square1 and in_square2:
        print("\tit is a valid intersection")
        return intersection
    else:
        print("\tit is not a valid intersection")
        return None
        # return False

    '''
    x1, y1 = seg1.superior.x, seg1.superior.y
    x2, y2 = seg1.inferior.x, seg1.inferior.y
    x3, y3 = seg2.superior.x, seg2.superior.y
    x4, y4 = seg2.inferior.x, seg2.inferior.y
    x, y = intersection.x, intersection.y
    if min(y1, y2) <= y <= max(y1, y2) and \
            min(y3, y4) <= y <= max(y3, y4) and \
            min(x1, x2) <= x <= max(x1, x2) and \
            min(x3, x4) <= x <= max(x3, x4):
        print("\t\t\t\tit is a valid intersection")
        return intersection
    else:
        print("\t\t\t\tit is not a valid intersection")
        return None
    '''
    #return intersection
# @TODO change in_square to only have x and y as parameters and define mins and max inside
def point_in_segment(point: Point, segment: Segment):
    x = [segment.inferior.x, segment.superior.x]
    y = [segment.inferior.y, segment.superior.y]
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    print(f"\t\t\t\t\t{point.in_line(segment.line)}, point in line")
    print(f"\t\t\t\t\t{point.in_square(x_min, x_max, y_min, y_max)}, point in square")
    return point.in_line(segment.line) and point.in_square(x_min, x_max, y_min, y_max)
# tests point in segment
#print(point_in_line(Point(1,0), Line(2,1,-2)))
#print(dist_pt_segment(Point(1,0), Point(0,2),Point(1,0)))
#print(point_in_segment(Point(1,0), Segment(SegmPoint(0,2),SegmPoint(1,0))))
#s2: (12.0, 75.0) -> (31.0, 40.0)
#s6: (78.0, 60.0) -> (26.0, 32.0)
#s2 = Segment(SegmPoint(12.0, 75.0), SegmPoint(31.0, 40.0), 's2')
#s6 = Segment(SegmPoint(78.0, 60.0), SegmPoint(26.0, 32.0), 's6')
#print(s2.intersects_with(s6))