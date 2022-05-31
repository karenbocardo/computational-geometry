class Node:
    def __init__(self, value=-1e100):
        self.parent = None
        self.left = None
        self.right = None
        self.value = value

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


class BST:
    def __init__(self):
        self.root = None

    def add_root(self, value):
        temp_node = Node(value)
        self.root = temp_node
        return temp_node

    def add_left(self, parent, value):
        temp_node = Node(value)
        parent.left = temp_node
        temp_node.parent = parent
        return temp_node

    def add_right(self, parent, value):
        temp_node = Node(value)
        parent.right = temp_node
        temp_node.parent = parent
        return temp_node

    def ancestors(self, node):
        if not node: return []
        else: return self.ancestors(node.parent) + [node.value]

    def depth(self, node):
        if not node.parent:return 0
        else: return 1 + self.depth(node.parent)

    def height(self, node):
        if not node: return 0
        else: return 1 + max([self.height(node.left), self.height(node.right)])

    ### RECORRIDOS
    def eulerian(self, node):
        if not node: return []
        return [node.value] + self.eulerian(node.left) + [node.value] + \
               self.eulerian(node.right) + [node.value]

    def preorder(self, node):
        if not node: return []
        return [node.value] + self.preorder(node.left) + self.preorder(node.right)

    def inorder(self, node):
        if not node: return []
        return self.inorder(node.left) + [node] + self.inorder(node.right)

    def postorder(self, node):
        if not node: return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.value]

    def bfs(self, queu):
        if not queu: return []
        node = queu.pop()
        if node.left: queu = [node.left] + queu
        if node.right: queu = [node.right] + queu
        return [node.value] + self.bfs(queu)

    def insert(self, value, n=None):
        if not self.root:
            new = Node(value)
            self.root = new
            return new
        if not n: n = self.root
        if value < n.value:
            if not n.left:
                new = Node(value)
                n.left = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert(value, n.left)
        else:
            if not n.right:
                new = Node(value)
                n.right = new
                new.parent = n
                self.rebalance(new)
                return new
            else:
                self.insert(value, n.right)

    def search(self, value):
        explorer = self.root
        while explorer:
            if value < explorer.value:
                explorer = explorer.left
            elif value > explorer.value:
                explorer = explorer.right
            else: break
        return explorer

    def last_subtree(self, p):
        explorer = p
        while explorer.right: explorer = explorer.right
        return explorer

    def delete(self, p):
        if not p: return
        if p == self.root: self.root = None

        elif p.is_leaf():
            if p.parent.left == p: p.parent.left = None
            else: p.parent.right = None

        elif not p.left:
            if p.parent.left == p: p.parent.left = p.right
            else: p.parent.right = p.right

        elif not p.right:
            if p.parent.left == p: p.parent.left = p.left
            else: p.parent.right = p.left

        else:
            replacement = self.last_subtree(p.left)
            p.value = replacement.value
            self.delete(replacement)
        self.rebalance(p)
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

# tree = BST()