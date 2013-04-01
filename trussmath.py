
import math 
import numpy

# Remember, our coordgraph is stored as:

# state = {"geom" : {"nodes":[], "edges":[]}, 
# 		 "vis"  : {"nodes":[], "edges":[]},
# 		 "bcs"  : {"fixednodes":[], "loadednodes":[], "loadededges":[]},
# 		 "msg"  :  "" }


state2 = {"geom":{"nodes": [{"iid":0, "x":0, "y":2},
					{"iid":1, "x":0, "y":1},
					{"iid":2, "x":0, "y":0}],
			"edges": [{"mid":0, "i0":0, "i1":1},
					{"mid":1, "i0":1, "i1":2}]},
			"bcs":{"fixednodes": [{"iid":0, "fix":0},
					{"iid":2, "fix":0},
					{"iid":2, "fix":1}],
				"loadednodes": [{"iid":0, "x":0, "y":1},
					{"iid":1, "x":0, "y":1},
					{"iid":2, "x":0, "y":1}]}}



def make_difference_matrix(state):

	edges, nodes = state["geom"]["edges"], state["geom"]["nodes"]

	# Node displacements u => Edge elongations d
	A = numpy.zeros([len(edges), 2*len(nodes)])

	for e in edges: 
		i0x = nodes[e['i0']]['x']
		i0y = nodes[e['i0']]['y']
		i1x = nodes[e['i1']]['x']
		i1y = nodes[e['i1']]['y']

		# deal with i0
		theta = math.atan2(i0y-i1y, i0x-i1x)
		# deal with the u
		A[e['mid']][2*e['i0']] = math.cos(theta)
		# deal with the v
		A[e['mid']][2*e['i0']+1] = math.sin(theta)

		# deal with i1
		theta = math.atan2(i1y-i0y, i1x-i0x)
		# deal with the u
		A[e['mid']][2*e['i1']] = math.cos(theta)
		# deal with the v
		A[e['mid']][2*e['i1']+1] = math.sin(theta)

	A = numpy.matrix(A)
	return A

def make_constitutive_matrix(state):
	#  Edge elongations d => Edge tensions w
	edges = state["geom"]["edges"]
	C = numpy.zeros([len(edges), len(edges)])
	for e in edges:
		mid = e['mid']
		# TODO: replace this with e.A * e.E / e.L
		C[mid][mid] = 100.
	C = numpy.matrix(C)
	return C


def make_balance_vector(state):
	# Construct external force vector f = Ku
	nodes = state["geom"]["nodes"]
	f = numpy.matrix(numpy.zeros(2*len(nodes))).transpose()
	for b in state['bcs']['loadednodes']:
		f[2*b['iid']] = b['x']
		f[2*b['iid']+1] = b['y']
	return f

def make_stiffness_matrix(state, A, C):
	# Construct stiffness matrix K = A'CA
	return A.transpose() * C * A


def prune_fixed_boundaries(state, K, f):
	# Prune fixed nodes from system
	delids = [2*n['iid']+n['fix'] for n in state['bcs']['fixednodes']]
	Kp = numpy.delete(K, delids, 1)
	fp = numpy.delete(f, delids, 0)
	print "pruning fixed boundaries. was:"
	print K.shape
	print f.shape
	print "is:"
	print Kp.shape
	print fp.shape


	return Kp, fp


def deflections(K, f):
	print K.shape
	print f.shape
	# Solve the damn thing
	return numpy.linalg.pinv(K)*f


def get_annotated_stresses(state):

	A = make_difference_matrix(state)
	C = make_constitutive_matrix(state)
	K = make_stiffness_matrix(state, A, C)
	f = make_balance_vector(state)
	K, f = prune_fixed_boundaries(state, K, f)
	u = deflections(K, f)

	return A, C, f, K, u

	