from data import *
from lib import Point
from tabulate import tabulate
import math

from intersections.algoritmo import AlgoritmoBarrido
from intersections.Punto import Punto
from intersections.Segmento import Segmento

# @TODO check if segment already exists
def save_segments(edge: Edge): # saves a list of segments from the given edge
    segments = list()
    vertices = edge.figure_vertices()
    if len(vertices) > 2: vertices.append(edge.origin.point) # to close figure

    '''
    for index in range(len(vertices) - 1):
        start, end = vertices[index], vertices[index + 1]
        start_point = Punto(start.x, start.y)
        end_point = Punto(end.x, end.y)
        segment = Segmento(start_point, end_point, f"x{index}")
        segments.append(segment)
        
    '''
    edges = edge.figure_edges()
    if len(edges) > 2: edges.append(edge)
    for index in range(len(edges) - 1):
        curr_edge, next_edge = edges[index], edges[index + 1]
        start, end = curr_edge.origin, next_edge.origin
        start_point = Punto(start.point.x, start.point.y)
        end_point = Punto(end.point.x, end.point.y)
        segment = Segmento(start_point, end_point, curr_edge.name)
        segments.append(segment)

    return segments

def get_prime(edge_name): return f"{edge_name}p"
def get_biprime(edge_name): return f"{edge_name}pp"

def edge_atan2(edge: Edge): # @TODO get atan2
    # @FIXME case same x or same y, not triangle
    a, b = edge.origin.point, edge.next.origin.point
    co = abs(a.y - b.y) # opposite leg (cateto)
    ca = abs(a.x - b.x) # adjacent leg
    print(co, ca)
    return math.atan2(co, ca)

def sort_circular(circular): # @TODO sort by atan2
    return

def next(edge: Edge): # @TODO get next of sorted
    return

def print_edges(edges):
    rows = list()
    # print(f"\tedge\torigin\tpair\tnext\tprevious")
    for name, edge in edges.items():
        if edge:
            # print(f"\t{edge.name}\t{edge.origin.point}\t{edge.pair.name}\t{edge.next.name}\t{edge.previous.name}")
            # print(f"\t{edge.name}\t{edge.origin.point}\t{edge.pair.name}")
            rows.append([edge.name, edge.origin.name, edge.pair.name, edge.next.name, edge.previous.name])
    print(tabulate(rows, headers=["edge", "origin", "pair", "next", "previous"]))

def second_elem(tup):
    return tup[1]

def connect_layers(folder, layers):
    vertices, edges, faces = save_layers(folder, layers)

    segments = list()
    print(f"faces: {faces.keys()}")
    for face_name, face in faces.items():
        if face.inside:
            for inside in face.inside:
                segments += save_segments(inside)
        if face.outside:
            segments += save_segments(face.outside)

    print("segments:")
    [print(f"[{i}]{segment}") for i, segment in enumerate(segments)]

    barr = AlgoritmoBarrido(segments)
    barr.barrer()

    circular, primes, biprimes = list(), list(), list()
    print(f"intersections:")
    for index, intersection in enumerate(barr.R):
        print(f"[{index}]{intersection}")
        point = Point(intersection.point.x, intersection.point.y)
        new_vertex = Vertex(f"p{len(vertices)+1}", point, "incidente")

        for segment in intersection.segments: # reading segments that intersect
            edge = edges[segment.name] # segments represent edges, saved in map
            # each edge is divided in two: self prime and self biprime
            print(f"analyzing edge {edge.name} and its pair {edge.pair.name}")
            print(f"\t{edge.name}: next->{edge.next.name} previous->{edge.next.name}")

            # split edge
            prime_name = get_prime(edge.name)  # prime
            prime = Edge(name=prime_name, origin=edge.origin, face=edge.face)  # new edge
            edges[prime_name] = prime

            biprime_name = get_biprime(edge.name)
            biprime = Edge(name=biprime_name) # new edge
            edges[biprime_name] = biprime
            biprime.origin = new_vertex # biprimes have new vertex as origin

            # split pair
            edge_pair = edge.pair
            print(f"\t{edge_pair.name}: next->{edge_pair.next.name} previous->{edge_pair.next.name}")

            p_prime_name = get_prime(edge_pair.name)  # prime
            p_prime = Edge(name=p_prime_name, origin=edge_pair.origin, face=edge_pair.face)  # new edge
            edges[p_prime_name] = p_prime

            p_biprime_name = get_biprime(edge_pair.name)
            p_biprime = Edge(name=p_biprime_name)  # new edge
            edges[p_biprime_name] = p_biprime
            p_biprime.origin = new_vertex  # biprimes have new vertex as origin

            # pairs
            p_prime.pair = biprime
            p_biprime.pair = prime
            biprime.pair = p_prime
            prime.pair = p_biprime

            # next and previous — circular list
            prime.previous = edges[get_biprime(edge.previous.name)]
            print(f"\t{prime.name}.previous = {get_biprime(edge.previous.name)}")
            p_prime.previous = edges[get_biprime(edge_pair.previous.name)]
            print(f"\t{p_prime.name}.previous = {get_biprime(edge_pair.previous.name)}")
            biprime.next = edges[get_prime(edge.next.name)]
            print(f"\t{biprime.name}.next = {get_prime(edge.next.name)}")
            p_biprime.next = edges[get_prime(edge_pair.next.name)]
            print(f"\t{p_biprime.name}.next = {get_prime(edge_pair.next.name)}")


            # circular += [prime, biprime] # add both to list
            # primes += [prime, p_prime]
            # biprimes += [biprime, p_biprime]

            p1 = new_vertex.point
            def get_atan2(p1, p2):
                angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
                print(f"\t{angle} from {p1} to {p2}")
                return angle

            primes.append((prime, get_atan2(p1, prime.origin.point)))
            primes.append((p_prime, get_atan2(p1, p_prime.origin.point)))
            biprimes.append((biprime, get_atan2(p1, biprime.next.origin.point)))
            biprimes.append((p_biprime, get_atan2(p1, p_biprime.next.origin.point)))

        primes.sort(key=second_elem)
        biprimes.sort(key=second_elem)

        for index in range(len(intersection.segments) * 2):
            prime = primes[index][0]
            biprime = biprimes[index][0]
            circular += [prime, biprime]

        circular.reverse()
        print(f"circular list: \n\t{[edge.name for edge in circular]}")
        circ_len = len(circular)

        def circular_next(edge):
            return circular[(circular.index(edge) + 1) % circ_len]
        def circular_prev(edge):
            return circular[circular.index(edge) - 1]

        for segment in intersection.segments:  # reading segments that intersect
            edge = edges[segment.name]
            prime = edges[get_prime(edge.name)]  # segments represent edges, saved in map
            biprime = edges[get_prime(prime.name)]

            edge_pair = edge.pair
            p_prime = edges[get_prime(edge_pair.name)]
            p_biprime = edges[get_prime(p_prime.name)]

            # --- prime ---> · --- biprime --->
            # prime goes into intersection
            # biprime comes out of intersection

            # prime's next is circular next
            prime.next = circular_next(prime)
            p_prime.next = circular_next(p_prime)
            # biprime's previous is circular previous
            biprime.previous = circular_prev(biprime)
            p_biprime.previous = circular_prev(p_biprime)

            del edges[edge.name]
            del edges[edge_pair.name]

        print("\nINFO")
        print_edges(edges)


    return vertices, edges, faces