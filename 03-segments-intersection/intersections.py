from q_t import *
from matplotlib import pyplot as plt
from celluloid import Camera

def separate(points):
    x, y = [], []
    for point in points:
        x.append(point.x)
        y.append(point.y)
    return x, y

#fig = plt.figure()
#camera = Camera(fig)

'''
def plot_frame(point, segments):
    for segment in segments:
        x, y = separate([segment.sup, segment.inf])
        plt.plot(x, y, color='steelblue')
    camera.snap()
'''
# S: conjunto de segmentos de línea en el plano
def find_intersections(S):
    def process_event(p: SegmPoint):
        print(f"\tU = {p.segments}")
        U = set(p.segments) # set of segments with superior extreme on p
        L, C = set(), set()

        def find_segments():
            # find segments on T that contain p
            # read all segments in tree T
            # segments with inferior as p go into L
            # segments with p inside go into C
            print("\tfinding segments")
            inorder = T.inorder(T.root)
            for node in inorder:
                print(f"\t\tchecking {node.segment}")
                actual_segment = node.segment
                if p == actual_segment.inferior:
                    print(f"\t\tinserting {actual_segment} into L")
                    L.add(actual_segment)
                if point_in_segment(p, actual_segment):
                    print(f"\t\tinserting {actual_segment} into C")
                    C.add(actual_segment)

        find_segments()
        print(f"\tC = {list(C)}")
        print(f"\tL = {list(L)}")

        print(f"\tL|U|C = {L | U | C}")
        print(f"\tL|U = {L | U}")
        print(f"\tU|C = {U | C}")
        print(f"\tactual T: {[node.segment for node in T.inorder(T.root)]}")

        LUC = L|U|C
        if len(LUC) > 1:
            '''
            for segment1 in LUC:
                for segment2 in LUC:
                    if segment1 == segment2: continue
                    intersection = Intersection(p, segment1, segment2)
                    R.append(intersection)
            '''
            LUC_list = list(LUC)
            intersection = Intersection(p, LUC_list)
            print(f"\t\tadding intersection {intersection} to T")
            R.append(intersection)
            '''
            for index, segment1 in enumerate(LUC_list):
                for segment2 in LUC_list[index:]:
                    if segment1 == segment2: continue
                    intersection = Intersection(p, [segment1, segment2])
                    R.append(intersection)
            '''

        for segment in L|U:
            print(f"\t\tdeleting {segment} from T")
            if T.already_exists(segment):
                T.delete_by_value(segment, T.root, p)
            print(f"\t\t\tT after: {[node.segment for node in T.inorder(T.root)]}")


        UC = U|C
        for segment in UC:
            print(f"\t\tinserting {segment} into T")
            if not T.already_exists(segment):
                print(f"{segment} was not in the tree")
                T.insert(segment, p)
            print(f"\t\t\tT after: {[node.segment for node in T.inorder(T.root)]}")


        # find sl and sr on T given the point by looking for hitpoints,
        # not returning the hitpoint but the segment that stands right there

        if len(UC) == 0:
            print("\tU|C = null")
            s_l = T.pt_left_neighbour(p)
            s_r = T.pt_right_neighbour(p)
            print(f"\t\tsl = {s_l}")
            print(f"\t\tsr = {s_r}")
            find_events(s_l, s_r, p)
        else:
            print("\tU|C != null")
            UC_sort = dict()
            for segment in UC:
                # dictionary for each segment and its hitpoint with T line on p
                # sort array based on x
                # smallest x is the one in the left
                # biggest is the one in the right
                #if hit_point := T.get_hit_point(segment, p):
                hit_point = T.get_hit_point(segment, p)
                if hit_point: UC_sort[hit_point.x] = segment
            print(f"\t\tU|C in order {UC_sort}")
            UC_list = [x_value for x_value in UC_sort]
            if UC_list:
                left = min(UC_list)
                s_prime = UC_sort[left]  # segment at the very left
                right = max(UC_list)
                # s_l = T.seg_left_neighbour(p, s_prime)
                s_l = T.left_(p, s_prime)
                print(f"\t\tsl = {s_l}")
                print(f"\t\ts' = {s_prime}")
                if s_l and s_prime: find_events(s_l, s_prime, p)
                s_biprime = UC_sort[right]
                # s_r = T.seg_right_neighbour(p, s_biprime)
                s_r = T.right_(p, s_biprime)
                print(f"\t\ts'' = {s_biprime}")
                print(f"\t\tsr = {s_r}")
                if s_biprime and s_r: find_events(s_biprime, s_r, p)


    def find_events(s_l: Segment, s_r: Segment, p: SegmPoint):
        print(f"\t\t\tfinding events with sl={s_l} and sr={s_r}")
        intersection = segs_intersect(s_l, s_r)
        #print(f"\t\t\t\tthey intersect in {intersection}")
        #print(f"line is on {p}")
        #if not intersection: return
        #print(f"{s_l}: {s_l.superior} -> {s_l.inferior}")
        #print(f"{s_r}: {s_r.superior} -> {s_r.inferior}")
        #print(f"\t{s_l} intersects with {s_r} on {intersection}")
        if intersection:
            intersect_under = intersection.y < p.y
            print(f"\t\t\t\t{intersect_under} : intersection is above")
            intersect_left = intersection.y == p.y and intersection.x <= p.x
            print(f"\t\t\t\t{intersect_left} : intersection is left")
            event = SegmPoint(intersection.x, intersection.y)
            is_not_event = not Q.search_by_y(event) # if it is not already on tree
            print(f"\t\t\t\t{is_not_event} : is not an event yet")
            #print(is_not_event)
            if intersection and (intersect_under or intersect_left) and is_not_event:
            #if intersection and (intersect_under or intersect_left):
                print("\t\t\t\tadding intersection to Q")
                Q.insert_by_y(event)


    R = list() # list of intersections
    Q = QBST() # sort by y, queue of segment_points
    for segment in S: # initialize Q inserting segments end points
        superior = SegmPoint(segment.superior.x, segment.superior.y)
        inferior = SegmPoint(segment.inferior.x, segment.inferior.y)

        # check superior
        if not (superior_node := Q.search_by_y(superior)): # if it is not already on tree
            superior.add_segment(segment) # only superior ones are added
            print(f"inserting {superior} into Q")
            Q.insert_by_y(superior)
        else: # if it is already on tree
            superior_node.point.add_segment(segment)

        # check inferior
        if not (inferior_node := Q.search_by_y(inferior)):  # if it is not already on tree
            #inferior.add_segment(segment)
            print(f"inserting {inferior} into Q")
            Q.insert_by_y(inferior)
        # else:  # if it is already on tree
            # inferior_node.point.add_segment(segment)


    T = TBST() # swipe line, empty at first

    while Q.root:
        # p is a node
        print(f"Q = {[node.point for node in Q.inorder(Q.root)]}")
        p = Q.get_min(Q.root) # get next event
        Q.delete(p) # pop next event

        print(f"processing event {p.point}")
        process_event(p.point) # sends segment_point as event
        # plot_frame(p.point, segments)
        #print([node.point for node in Q.inorder(Q.root)])
        #print(Q)
    return R


#-------------------------- DEMO -----------------------------------------------------------------------------------
if __name__ == "__main__":
    def read_file(filename):
        file = open(filename)
        return file.read().splitlines()


    # test-cases/algorithmical/0.in
    # data = read_file(sys.argv[1])
    data = read_file('test-cases/visual/0.in')
    #data = read_file('test-cases/visual/0.in')
    if len(data[0].split()) < 2: data.remove(data[0])
    segments = list()
    for line in data:
        sep = line.split()
        point1 = SegmPoint(float(sep[0]), float(sep[1]))
        point2 = SegmPoint(float(sep[2]), float(sep[3]))
        if len(sep) > 4:
            name = sep[4]
            segment = Segment(point1, point2, name)
        else:
            segment = Segment(point1, point2)
        segments.append(segment)

    # print_segments(segments)
    # print_segments(segments)
    intersections = find_intersections(segments)
    print()
    print(f"found {len(intersections)} intersections:")
    for index, intersection in enumerate(intersections):
        print(f"[{index+1}] {intersection}")