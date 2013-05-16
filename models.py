
# Models for trussvis
# Back to object-orientation!


class State(object):
    nodes = {}
    edges = {}
    nid_counter = 0
    eid_counter = 0

    def new_node(self, x, y):
        self.nodes[self.nid_counter] = Node(x,y)
        self.nid_counter += 1

    def new_edge(self, n0, n1):
        self.edges[self.eid_counter] = Edge(n0, n1)
        self.eid_counter += 1

    def parse_json(self, json):
        pass
    
    def to_json(self):
        pass

class Node(object):
    def __init__(self, nid, x, y):
        self.nid = nid
        self.x = x
        self.y = y

class Edge(object):
    def __init__(self, eid, n0, n1):
        self.eid = eid
        self.n0 = n0
        self.n1 = n1
        self.stress = 0
        self.stress_color = 0
        
