

class State(object):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def edge(self, id):
    

class Node(object):
    counter = 0
    def __init__(self, x, y):
        self.id = Node.counter
        Node.counter += 1
        self.x = x
        self.y = y
        self.load_x = 0
        self.load_y = 0
        self.fix_x = 0
        self.fix_y = 0

    def load(self, load_x, load_y):
        self.load_x = load_x
        self.load_y = load_y

    def fix(self, fix_x, fix_y):
        self.fix_x = fix_x
        self.fix_y = fix_y


class Edge(object):
    counter = 0
    def __init__(self, n0, n1):
        self.id = Edge.counter
        Edge.counter += 1
        self.n0 = n0
        self.n1 = n1
        self.thickness = 10
        self.stress = 0
        self.material = None

