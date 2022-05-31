from classes import *

'''
implementation of a binary search tree that uses nodes values as points,
this points are special since they can belong to a list of segments
'''

class QNode:
    def __init__(self, point: SegmPoint):
        self.parent = None
        self.left = None
        self.right = None
        self.point = point
    def is_leaf(self):
        return not (self.left or self.right)
    def children(self):
        res = []
        if self.left: res.append(self.left)
        if self.right: res.append(self.right)
        return res
    def sibling(self):
        if not self.parent: return None
        if self.parent.left == self:
            return self.parent.right
        else: return self.parent.left

class QBST:
    def __init__(self):
        self.root = None
    def add_root(self, point):
        temp_node = QNode(point)
        self.root = temp_node
        return temp_node
    def add_left(self, parent, point):
        temp_node = QNode(point)
        parent.left = temp_node
        temp_node.parent = parent
        return temp_node
    def add_right(self, parent, point):
        temp_node = QNode(point)
        parent.right = temp_node
        temp_node.parent = parent
        return temp_node
    def ancestors(self, node):
        if not node: return []
        else: return self.ancestors(node.parent) + [node.point]
    def depth(self, node):
        if not node.parent:return 0
        else: return 1 + self.depth(node.parent)
    def height(self, node):
        if not node: return 0
        else: return 1 + max([self.height(node.left), self.height(node.right)])
    ### RECORRIDOS
    def eulerian(self, node):
        if not node: return []
        return [node.point] + self.eulerian(node.left) + [node.point] + \
               self.eulerian(node.right) + [node.point]
    def preorder(self, node):
        if not node: return []
        return [node.point] + self.preorder(node.left) + self.preorder(node.right)
    def inorder(self, node):
        if not node: return []
        return self.inorder(node.left) + [node] + self.inorder(node.right)
    def postorder(self, node):
        if not node: return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.point]
    def bfs(self, queu):
        if not queu: return []
        node = queu.pop()
        if node.left: queu = [node.left] + queu
        if node.right: queu = [node.right] + queu
        return [node.point] + self.bfs(queu)
    '''
    def insert(self, point, n=None):
        if not self.root:
            new = QNode(point)
            self.root = new
            return new
        if not n: n = self.root
        if point < n.point:
            if not n.left:
                new = QNode(point)
                n.left = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert(point, n.left)
        else:
            if not n.right:
                new = QNode(point)
                n.right = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert(point, n.right)
    '''
    def insert_by_x(self, point, n=None):
        if not self.root:
            new = QNode(point)
            self.root = new
            return new
        if not n: n = self.root
        # if point < n.point:
        if point.lower_x(n.point):
            if not n.left:
                new = QNode(point)
                n.left = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert_by_x(point, n.left)
        else:
            if not n.right:
                new = QNode(point)
                n.right = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert_by_x(point, n.right)
    def insert_by_y(self, point, n=None):
        if not self.root:
            new = QNode(point)
            self.root = new
            return new
        if not n: n = self.root
        # if point < n.point:
        if point.greater_y(n.point):
            if not n.left:
                new = QNode(point)
                n.left = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert_by_y(point, n.left)
        else:
            if not n.right:
                new = QNode(point)
                n.right = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert_by_y(point, n.right)
    '''
    def search(self, point):
        explorer = self.root
        while explorer:
            if point < explorer.point:
                explorer = explorer.left
            elif point > explorer.point:
                explorer = explorer.right
            else: break
        return explorer
    '''
    def search_by_x(self, point):
        explorer = self.root
        while explorer:
            if point.lower_x(explorer.point):
                explorer = explorer.left
            elif point.greater_x(explorer.point):
                explorer = explorer.right
            else: break
        return explorer
    def search_by_y(self, point):
        explorer = self.root
        while explorer:
            if point.y > explorer.point.y:
                explorer = explorer.left
            elif point.y < explorer.point.y:
                explorer = explorer.right
            else: break

        if explorer:
            if explorer.point != point:
                explorer = None
            else:
                print(f"found {point} in {explorer.point}")
        else: print(f"didnt find {point}")
        return explorer
    def get_min(self, node: QNode):
        if not node.left: return node
        return self.get_min(node.left)
        #return self.inorder(self.root)[0]
    def last_subtree(self, p):
        explorer = p
        while explorer.right: explorer = explorer.right
        return explorer
    def min_subtree(self, p):
        explorer = p
        while explorer.left: explorer = explorer.left
        return explorer
    def delete(self, p: QNode):
        if not p:
            return
        if p == self.root and p.is_leaf():
            self.root = None
        elif p.is_leaf():
            if p.parent.left == p: p.parent.left = None
            else: p.parent.right = None

        elif not p.left and p != self.root:
            if p.parent.left == p:
                p.parent.left = p.right
                p.right.parent = p.parent
            else:
                p.parent.right = p.right
                p.right.parent = p.parent

        elif not p.right and p != self.root:
            if p.parent.left == p:
                p.parent.left = p.left
                p.left.parent = p.parent
            else:
                p.parent.right = p.left
                p.left.parent = p.parent

        else: # has two children
            #replacement = self.last_subtree(p.left)
            replacement = self.min_subtree(p.right)
            p.point = replacement.point
            self.delete(replacement)
        #self.rebalance(p)
        #self.rebalance()
        return
    def relink(self, parent, child, is_left):
        if is_left: parent.left = child
        else: parent.right = child
        if child: child.parent = parent
    def rotate(self, p):
        x = p
        y = x.parent
        z = y.parent

        # if z is none
        if not z:
            self.root = x
            x.parent = None
        else:
            self.relink(z, x, y == z.left)
        if x == y.left:
            self.relink(y, x.right, True)
            self.relink(x, y, False)
        else:
            self.relink(y, x.left, False)
            self.relink(x, y, True)
    def restructure(self, x):
        y = x.parent
        z = y.parent
        if (x == y.right) == (y == z.right):
            self.rotate(y)
            return y
        else:
            self.rotate(x)
            self.rotate(x)
            return x
    def rebalance(self, p):
        x = p
        while True:
            if not x: return
            if not x.parent: return
            y = x.parent
            if not y.parent: return
            z = y.parent
            if self.height(z.right) - self.height(z.left) not in [-1, 0, 1]:
                self.restructure(self.tallest_grandchild(z))
            x = x.parent
    def tallest_child(self, node):
        if not node: return None
        else: return node.left if self.height(node.left) > self.height(node.right) else node.right
    def tallest_grandchild(self, node):
        child = self.tallest_child(node)
        return self.tallest_child(child)
    def __repr__(self):
        return self.tree_string(self.root)
    def tree_string(self, node):
        if not node: return ''
        res = '\t' * self.depth(node)
        #if node == self.root: res += f'{node.point}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        #else: res += f'{node.point}->{node.parent.point}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        res += f'{node.point}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        return res
        #print(node.point)
        #print(self.print_tree(node.left))
        #print(self.print_tree(node.right))
        #return [node] + self.preorder(node.left) + self.preorder(node.right)

class TNode:
    def __init__(self, segment: Segment):
        self.parent = None
        self.left = None
        self.right = None
        self.segment = segment
    def is_leaf(self):
        return not (self.left or self.right)
    def children(self):
        res = []
        if self.left: res.append(self.left)
        if self.right: res.append(self.right)
        return res
    def sibling(self):
        if not self.parent: return None
        if self.parent.left == self:
            return self.parent.right
        else: return self.parent.left

class TBST:
    def __init__(self):
        self.root = None
    def add_root(self, segment):
        temp_node = TNode(segment)
        self.root = temp_node
        return temp_node
    def add_left(self, parent, segment):
        temp_node = TNode(segment)
        parent.left = temp_node
        temp_node.parent = parent
        return temp_node
    def add_right(self, parent, segment):
        temp_node = TNode(segment)
        parent.right = temp_node
        temp_node.parent = parent
        return temp_node
    def ancestors(self, node):
        if not node: return []
        else: return self.ancestors(node.parent) + [node.segment]
    def depth(self, node):
        if not node.parent:return 0
        else: return 1 + self.depth(node.parent)
    def height(self, node):
        if not node: return 0
        else: return 1 + max([self.height(node.left), self.height(node.right)])
    ### RECORRIDOS
    def eulerian(self, node):
        if not node: return []
        return [node.segment] + self.eulerian(node.left) + [node.segment] + \
               self.eulerian(node.right) + [node.segment]
    def preorder(self, node):
        if not node: return []
        return [node.segment] + self.preorder(node.left) + self.preorder(node.right)
    def inorder(self, node: TNode):
        if not node: return []
        return self.inorder(node.left) + [node] + self.inorder(node.right)
    def postorder(self, node):
        if not node: return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.segment]
    def bfs(self, queu):
        if not queu: return []
        node = queu.pop()
        if node.left: queu = [node.left] + queu
        if node.right: queu = [node.right] + queu
        return [node.segment] + self.bfs(queu)
    def get_line(self, point): # línea horizontal a la altura del punto dado
        return pts_to_line(point, Point(point.x + 1, point.y))
    def get_hit_point(self, segment: Segment, point):
        # dónde choca el segmento dado con una línea horizontal a la altura del punto dado si fuera una línea infinita
        T_line = self.get_line(point)
        hit_point = segment.line.intersects_with(T_line)
        return hit_point
    def lower_hit_point(self, current: Segment, other: Segment, point: Point):
        current_hit_point = self.get_hit_point(current, point)
        other_hit_point = self.get_hit_point(other, point)
        if current_hit_point and other_hit_point:
            return current_hit_point.x < other_hit_point.x
        return False
    def already_exists(self, segment: Segment):
        return segment in set([node.segment for node in self.inorder(self.root)])
    def insert(self, segment: Segment, p, n=None):
        # point is the actual point on which the line T lies (actual event)
        point = Point(p.x, p.y - eps) # below p
        if not self.root:
            new = TNode(segment)
            self.root = new
            return new
        if not n: n = self.root
        if segment.line.is_horizontal(): # si el segmento es horizontal, insertarlo al final
            parent = self.last_subtree(n.right)
            new = TNode(segment)
            new.parent = parent
            self.rebalance(new)
            return new

        # hit points:
        # en que x choca el segmento que vamos a meter con la línea horizontal si fuera una línea infinita
        # en qué x choca el segmento n (el que estamos visitando) con la línea horizontal si fuera una línea infinita
        # comparar la x de los hit points, así se sabe si vas a la izquierda o a la derecha
        #n_hit_point = self.get_hit_point(n.segment, point)
        #seg_hit_point = self.get_hit_point(segment, point)
        # if segment < n.segment:
        #if seg_hit_point.x < n_hit_point.x:
        if segment == n.segment:
            print(f"node with {n.segment} already exists")
            return
        if self.lower_hit_point(segment, n.segment, point):
            if not n.left:
                new = TNode(segment)
                n.left = new
                new.parent = n
                self.rebalance(new)
                return new
            if n.left.segment == segment: print("YA EXISTE")
            else:
                self.insert(segment, point, n.left)
        elif self.lower_hit_point(n.segment, segment, point):
            if not n.right:
                new = TNode(segment)
                n.right = new
                new.parent = n
                self.rebalance(new)
                return new
            if n.right.segment == segment:
                print("YA EXISTE")
            else:
                self.insert(segment, point, n.right)

        else:
            print("eran iguales")

    def search(self, segment, point):
        explorer = self.root
        while explorer:
            if segment == explorer.segment: break
            if segment.self.lower_hit_point(segment, explorer.segment, point):
                explorer = explorer.left
            else:
                explorer = explorer.right
        return explorer


    def pt_right_neighbour(self, point: Point, node=None):
        if not self.root: return
        if not node: node = self.root
        node_hit_point = self.get_hit_point(node.segment, point)
        if node_hit_point and point.x < node_hit_point.x:
            if not node.left: return node.segment
            else: return self.pt_right_neighbour(point, node.left)
        else:
            if not node.right: return node.segment
            else: return self.pt_right_neighbour(point, node.right)
    def pt_left_neighbour(self, point: Point, node=None):
        if not self.root: return
        if not node: node = self.root
        node_hit_point = self.get_hit_point(node.segment, point)
        if node_hit_point and node_hit_point.x < point.x:
            if not node.left: return node.segment
            else: return self.pt_left_neighbour(point, node.left)
        else:
            if not node.right: return node.segment
            else: return self.pt_left_neighbour(point, node.right)
    def seg_left_neighbour(self, p: Point, segment: Segment, node=None):
        if not self.root: return
        if not node: node = self.root
        if self.lower_hit_point(segment, node.segment, p):
            if not node.left: return node.segment
            else: return self.seg_left_neighbour(p, segment, node.left)
        else:
            if not node.right: return node.segment
            else: return self.seg_left_neighbour(p, segment, node.right)
    def seg_right_neighbour(self, p: Point, segment: Segment, node=None):
        if not self.root: return
        if not node: node = self.root
        if self.lower_hit_point(node.segment, segment, p):
            if not node.left: return node.segment
            else: return self.seg_right_neighbour(p, segment, node.left)
        else:
            if not node.right: return node.segment
            else: return self.seg_right_neighbour(p, segment, node.right)
    def right_(self, p: Point, segment: Segment):
        #p = Point(point.x, point.y - eps)
        to_sort = dict()
        for node in self.inorder(self.root):
            to_sort[node] = self.get_hit_point(node.segment, p).x
        hit_point_x = self.get_hit_point(segment, p).x
        for node in sorted(to_sort, key=to_sort.get):
            node_hit_point_x = to_sort[node]
            if hit_point_x < node_hit_point_x:
                return node.segment
        '''
        for node in inorder:
            if self.lower_hit_point(segment, node.segment, p):
                return node.segment
        '''
        return None
    def left_(self, p: Point, segment: Segment):
        to_sort = dict()
        #p = Point(point.x, point.y-eps)
        for node in self.inorder(self.root):
            to_sort[node] = self.get_hit_point(node.segment, p).x
        hit_point_x = self.get_hit_point(segment, p).x
        for node in sorted(to_sort, key=to_sort.get, reverse=True):
            node_hit_point_x = to_sort[node]
            if hit_point_x > node_hit_point_x:
                return node.segment
        '''
        for node in inorder[::-1]:
            if self.lower_hit_point(node.segment, segment, p):
                return node.segment
        '''
        return None
    def get_min(self, node: TNode):
        if not node.left: return node
        return self.get_min(node.left)
    def last_subtree(self, p):
        '''
        explorer = p
        while explorer.right: explorer = explorer.right
        return explorer
        '''
        explorer = p
        while explorer:
            if explorer.right: explorer = explorer.right
        return explorer
    def min_subtree(self, p):
        explorer = p
        while explorer.left: explorer = explorer.left
        return explorer
    def delete(self, p: TNode):
        if not p:
            return
        if p == self.root and p.is_leaf():
            self.root = None
        elif p.is_leaf():
            if p.parent.left == p: p.parent.left = None
            else: p.parent.right = None

        elif not p.left and p != self.root:
            if p.parent.left == p:
                p.parent.left = p.right
                p.right.parent = p.parent
            else:
                p.parent.right = p.right
                p.right.parent = p.parent

        elif not p.right and p != self.root:
            if p.parent.left == p:
                p.parent.left = p.left
                p.left.parent = p.parent
            else:
                p.parent.right = p.left
                p.left.parent = p.parent

        else: # has two children
            #replacement = self.last_subtree(p.left)
            replacement = self.min_subtree(p.right)
            p.segment = replacement.segment
            self.delete(replacement)
        #self.rebalance(p)
        #self.rebalance()
        return
    def delete_by_value(self, segment : Segment, node, point: Point):
        #point = Point(p.x, p.y - eps)  # below p
        '''
        :param segment: segment to search
        :param n: will stand as current node
        :return:
        '''
        # root -> node root de subarbol
        if not node: return node # ?
        if segment == self.root.segment: print("segment to delete is root")
        # segment is in the left subtree
        if self.lower_hit_point(segment, node.segment, point):
            self.delete_by_value(segment, node.left, point)
        # segment is in current node
        elif segment == node.segment:
            p = node # node to delete is p
            if segment.__repr__() == 's2': print(f"reached {segment}")
            if p == self.root and p.is_leaf():
                self.root = None
            elif p.is_leaf():
                if p.parent.left == p: p.parent.left = None
                else: p.parent.right = None

            elif not p.left and p != self.root:
                if p.parent.left == p: # left child
                    p.parent.left = p.right
                    p.right.parent = p.parent
                else:
                    p.parent.right = p.right
                    p.right.parent = p.parent

            elif not p.right and p != self.root:
                if p.parent.left == p:
                    p.parent.left = p.left
                    p.left.parent = p.parent
                else:
                    p.parent.right = p.left
                    p.left.parent = p.parent

            else: # has two children
                print("has two children")
                #replacement = self.last_subtree(p.left)
                replacement = self.min_subtree(p.right)
                p.segment = replacement.segment
                self.delete(replacement)
            #self.rebalance(p)
            #self.rebalance()

        # segment is in the right subtree
        else: self.delete_by_value(segment, node.right, point)
        return
    def relink(self, parent, child, is_left):
        if is_left: parent.left = child
        else: parent.right = child
        if child: child.parent = parent
    def rotate(self, p):
        x = p
        y = x.parent
        z = y.parent

        # if z is none
        if not z:
            self.root = x
            x.parent = None
        else:
            self.relink(z, x, y == z.left)
        if x == y.left:
            self.relink(y, x.right, True)
            self.relink(x, y, False)
        else:
            self.relink(y, x.left, False)
            self.relink(x, y, True)
    def restructure(self, x):
        y = x.parent
        z = y.parent
        if (x == y.right) == (y == z.right):
            self.rotate(y)
            return y
        else:
            self.rotate(x)
            self.rotate(x)
            return x
    def rebalance(self, p):
        x = p
        while True:
            if not x: return
            if not x.parent: return
            y = x.parent
            if not y.parent: return
            z = y.parent
            if self.height(z.right) - self.height(z.left) not in [-1, 0, 1]:
                self.restructure(self.tallest_grandchild(z))
            x = x.parent
    def tallest_child(self, node):
        if not node: return None
        else: return node.left if self.height(node.left) > self.height(node.right) else node.right
    def tallest_grandchild(self, node):
        child = self.tallest_child(node)
        return self.tallest_child(child)
    def __repr__(self):
        return self.tree_string(self.root)
    def tree_string(self, node):
        if not node: return ''
        res = '\t' * self.depth(node)
        #if node == self.root: res += f'{node.point}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        #else: res += f'{node.point}->{node.parent.point}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        res += f'{node.segment}\n{self.tree_string(node.left)}{self.tree_string(node.right)}'
        return res
        #print(node.point)
        #print(self.print_tree(node.left))
        #print(self.print_tree(node.right))
        #return [node] + self.preorder(node.left) + self.preorder(node.right)

'''
# QBST test
x_tree, y_tree = QBST(), QBST()
pts = [SegmPoint(-1,3), SegmPoint(1,0), SegmPoint(2,2), SegmPoint(-2,0)]
for point in pts:
    x_tree.insert_by_x(point)
    y_tree.insert_by_y(point)
print([node.point for node in x_tree.inorder(x_tree.root)])
print([node.point for node in y_tree.inorder(y_tree.root)])
'''
'''
#TBST test
tree = TBST()
s1 = Segment(SegmPoint(3,4),SegmPoint(1,-1),'s1')
s2 = Segment(SegmPoint(0,3),SegmPoint(2,0),'s2')
s3 = Segment(SegmPoint(1.5,2.5),SegmPoint(4,-1),'s3')
print('insertando s1')
tree.insert(s1, SegmPoint(3,4))
print('insertando s2')
tree.insert(s2, SegmPoint(0,3))
print('insertando s3')
tree.insert(s3, SegmPoint(1.5,2.5))
print(tree)
#tree.delete_by_value(s1, tree.root, SegmPoint(1.5,2.5))
#print(tree)


print("right:", tree.pt_right_neighbour(Point(1.6,2.5)))
print("left:", tree.pt_left_neighbour(Point(1.6,2.5)))
'''
