from math import *

eps = 10**-4

#gcd(a,b,c) = gcd(a, gcd(b,c))
def gcd(a, b):
    if b == 0: return a
    else: return gcd(b, a%b)
def minimize(a, b, c):
    divisor = gcd(a, gcd(b,c))
    return (a / divisor, b / divisor, c / divisor)

def eq_values(a, b):
    return abs(a - b) < eps

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return eq_values(self.x, other.x) and eq_values(self.y, other.y)
    #def __hash__(self): # makes segments hashable
    #    return hash(f'{self.x},{self.y}')
    '''
    def __eq__(self, other):
        return abs(self.x - other.x) < eps and abs(self.y - other.y) < eps
    '''
    def __repr__(self):
        return f"({self.x}, {self.y})"
    '''
    def __cmp__(self, other):
        if self.x > other.x: return 1
        elif self.x < other.x: return -1
        else: return 0
    '''
    # lexicográfico
    '''
    def __lt__(self, other):
        if self.x == other.x: return self.y < other.y
        else: return self.x < other.x
    def __gt__(self, other):
        if self.x == other.x: return self.y > other.y
        else: return self.x > other.x
    '''
    def lower_x(self, other):
        if eq_values(self.x, other.x): return self.y < other.y
        else: return self.x < other.x
    def greater_x(self, other):
        if self.x == other.x: return self.y > other.y
        else: return self.x > other.x
    '''
    # order by element y, from top to bottom
    def __lt__(self, other):
        if self.y == other.y: return self.x < other.x
        else: return self.y > other.y
    def __gt__(self, other):
        if self.y == other.y: return self.x > other.x
        else: return self.y < other.y
    '''
    def lower_y(self, other): # inferior right
        if eq_values(self.y, other.y): return self.x > other.x
        else: return self.y < other.y
    def greater_y(self, other): # superior left
        if eq_values(self.y, other.y): return self.x < other.x
        else: return self.y > other.y

    def elements(self):
        return [self.x, self.y]
    def distance_to(self, other):
        return distance(self, other)
    def rotate(self, theta):
        return Point(self.x * cos(theta) - self.y * sin(theta), self.x * sin(theta) + self.y * cos(theta))
    def in_square(self, x_min, x_max, y_min, y_max):
        return inside_square(self, x_min, x_max, y_min, y_max)
    def in_line(self, line):
        return point_in_line(self, line)

# left to right
def sort_x(point: Point): return point.x
def sort_pts_x(points):
    return sorted(points, key=sort_x)
# bottom to top
def sort_y(point: Point): return point.y
def sort_pts_y(points):
    return sorted(points, key=sort_y, reverse=True)


class Line:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
    def __eq__(self, other):
        return abs(self.a - other.a) < eps and abs(self.b - other.b) < eps and abs(self.c - other.c) < eps
    def __repr__(self):
        return f"({self.a},{self.b},{self.c})"
    def elements(self):
        return [self.a, self.b, self.c]
    def slope(self):
        if self.b == 0: return False
        else: return - (self.a / self.b)
    def is_vertical(self):
        return self.b == 0
    def is_horizontal(self):
        return self.slope() == 0
    def parallel_to(self, other):
        return parallels(self, other)
    def equal_to(self, other):
        return equals(self, other)
    def intersects_with(self, other):
        return lines_intersect(self, other)

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return abs(self.x - other.x) < eps and abs(self.y - other.y) < eps
    def __repr__(self):
        return f"<{self.x}, {self.y}>"
    def elements(self):
        return [self.x, self.y]
    def scalar(self, s):
        return scalar(self, s)
    def dot(self, other):
        return dot_product(self, other)
    def cross(self, other):
        return cross_product(self, other)
    def norm(self):
        return sqrt(self.x**2 + self.y**2)
    def squared_norm(self):
        return self.x**2 + self.y**2

### point
def distance(point1, point2):
    return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
def angle(pointA, pointO, pointB):
    vecOA = to_vector(pointO, pointA)
    vecOB = to_vector(pointO, pointB)
    return acos(vecOA.dot(vecOB) / (vecOA.norm()*vecOB.norm()))
def ccw(pointP, pointQ, pointR):
    vecPQ = to_vector(pointP, pointQ)
    vecPR = to_vector(pointP, pointR)
    return cross_product(vecPQ, vecPR) > 0

def ccw(points):
    pointP, pointQ, pointR = points
    vecPQ = to_vector(pointP, pointQ)
    vecPR = to_vector(pointP, pointR)
    return cross_product(vecPQ, vecPR) > 0
def collinear(pointP, pointQ, pointR):
    vecPQ = to_vector(pointP, pointQ)
    vecPR = to_vector(pointP, pointR)
    return abs(cross_product(vecPQ, vecPR)) < eps

### line
def pts_to_line(p1, p2):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    a = y1 - y2
    b = x2 - x1
    c = (x1 * y2) - (x2 * y1)
    a, b, c = minimize(a, b, c)
    return Line(a, b, c)

### vector
def to_vector(pointA, pointB):
    return Vector(pointB.x - pointA.x, pointB.y - pointA.y)
def parallels(line1, line2):
    # vertical
    # if line1.b == 0: return line2.b == 0
    if not line1.slope(): return bool(not line2.slope())
    # same slope
    return line1.slope() == line2.slope()
def equals(line1, line2):
    a1, b1, c1 = minimize(line1.a, line1.b, line1.c)
    a2, b2, c2 = minimize(line2.a, line2.b, line2.c)
    return a1 == a2 and b1 == b2 and c1 == c2
    #a1, b1, c1 = line1.elements()
    #a2, b2, c2 = line2.elements()
    #return a1 / a2 == b1 / b2 == c1 / c2
def lines_intersect(line1: Line, line2: Line):
    if line1.parallel_to(line2): return False
    a1, b1, c1 = line1.elements()
    a2, b2, c2 = line2.elements()
    x = ((b1 * c2) - (b2 * c1))/((a1 * b2) - (a2 * b1))
    y = ((a2 * c1) - (a1 * c2))/((a1 * b2) - (a2 * b1))
    return Point(x, y)
def scalar(vector, s):
    return Vector(vector.x * s, vector.y * s)
def translate(point, vector):
    return Point(point.x + vector.x, point.y + vector.y)
def dot_product(vectorA, vectorB):
    return vectorA.x * vectorB.x + vectorA.y * vectorB.y
def cross_product(vectorA, vectorB):
    return vectorA.x * vectorB.y - vectorA.y * vectorB.x
def dist_pt_line(pointP, pointA, pointB):
    # distance point to line
    # line goes over points a and b
    vecAP = to_vector(pointA, pointP)
    vecAB = to_vector(pointA, pointB)
    u = vecAP.dot(vecAB) / vecAB.squared_norm()
    c = translate(pointA, vecAB.scalar(u))
    return pointP.distance_to(c)

def dist_pt_segment(pointP, pointA, pointB): # A,B are segment points
    vecAP = to_vector(pointA, pointP)
    vecAB = to_vector(pointA, pointB)
    u = vecAP.dot(vecAB) / vecAB.squared_norm()
    if u < 0: return pointP.distance_to(pointA)
    elif u > 1: return pointP.distance_to(pointB)
    else:
        c = translate(pointA, scalar(vecAB, u))
        return pointP.distance_to(c)
def inside_square(point: Point, x_min, x_max, y_min, y_max):
    x, y = point.x, point.y
    in_x = x >= x_min and x <= x_max
    in_y = y >= y_min and y <= y_max
    return in_x and in_y
def point_in_line(point: Point, line: Line):
    return line.a * point.x + line.b * point.y + line.c == 0
'''
# ejercicio 1
print(Point(2,2).distance(Point(6,5)))
print(Point(10,3).rotate(pi/2))
print(Point(10,3).rotate(radians(77)))
print(Line.pts_to_line(Point(2,2),Point(4,3)))
print(Line.pts_to_line(Point(2,2),Point(2,4)))
'''
#print(inside_square(Point(1,1), 0,2,0,2))
