def isLeaf(self):
    return not (self.left or self.right)

def rightMost(node):
    if node.right_child: return rightMost(node.right_child)
    else: return node.right_child

def getLeft(node):
    if node.parent.left_child == node:
        return
    if not node.parent.left_child: # is None
        return getLeft(node.parent)
    if node.parent.left_child: # is not None
        right = rightMost(node.parent.left_child)
        if right.isLeaf(): return right
        else: return right.left_child

