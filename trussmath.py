
import math 
import numpy

# Remember, our coordgraph is stored as:

# state = {"geom" : {"nodes":[], "edges":[]}, 
# 		 "vis"  : {"nodes":[], "edges":[]},
# 		 "bcs"  : {"fixednodes":[], "loadednodes":[], "loadededges":[]},
# 		 "msg"  :  "" }


state = {"msg": "\nAvailable commands:\n\n\tgeometry bcs stress deflection factorofsafety\n\tnode edge pointload uniformload fixnode check\n\tload save reset \n\nTry \"help cmd\" for more info.", 
		"vis": {"nodes": [{"y": 0.0, "iid": 0, "x": 0.0}, {"y": 3.0, "iid": 1, "x": 2.0}, {"y": 0.0, "iid": 2, "x": 4.0}, {"y": 3.0, "iid": 3, "x": 6.0}, {"y": 0.0, "iid": 4, "x": 8.0}], 
				"edges": [{"i1": 1, "i0": 0, "mid": 0, "color": "#760000"}, {"i1": 2, "i0": 1, "mid": 1, "color": "#360000"}, {"i1": 3, "i0": 2, "mid": 2, "color": "#960000"}, {"i1": 4, "i0": 3, "mid": 3, "color": "#3c0000"}, {"i1": 3, "i0": 1, "mid": 4, "color": "#cf0000"}, {"i1": 2, "i0": 0, "mid": 5, "color": "#930000"}, {"i1": 4, "i0": 2, "mid": 6, "color": "#970000"}]}, 
		"geom": {"nodes": [{"y": 0.0, "iid": 0, "x": 0.0}, {"y": 3.0, "iid": 1, "x": 2.0}, {"y": 0.0, "iid": 2, "x": 4.0}, {"y": 3.0, "iid": 3, "x": 6.0}, {"y": 0.0, "iid": 4, "x": 8.0}], 
				"edges": [{"i1": 1, "i0": 0, "mid": 0}, {"i1": 2, "i0": 1, "mid": 1}, {"i1": 3, "i0": 2, "mid": 2}, {"i1": 4, "i0": 3, "mid": 3}, {"i1": 3, "i0": 1, "mid": 4}, {"i1": 2, "i0": 0, "mid": 5}, {"i1": 4, "i0": 2, "mid": 6}]}, 
		"bcs": {"loadededges": [], "loadednodes": [], "fixednodes": []}}

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

# atca_cmd(state2) should return [0 1 0 -1 0 0; 0 0 0 1 0 -1]

def atan(x0, y0, x1, y1):
	if x0 == x1 and y0 < y1:
		return math.pi/2
	if x0 == x1 and y0 > y1:
		return -math.pi/2
	else:
		return math.atan((y0 - y1)/(x0 - x1))


# @register("straess")
def atca_cmd(state):
	edges, nodes = state["geom"]["edges"], state["geom"]["nodes"]

	# Node displacements u => Edge elongations d
	A = numpy.zeros([len(edges), 2*len(nodes)])

	for e in edges: 
		i0x = nodes[e['i0']]['x']
		i0y = nodes[e['i0']]['y']
		i1x = nodes[e['i1']]['x']
		i1y = nodes[e['i1']]['y']

		# deal with i0
		theta = atan(i0x, i0y, i1x, i1y)
		# deal with the u
		A[e['mid']][2*e['i0']] = math.cos(theta)
		# deal with the v
		A[e['mid']][2*e['i0']+1] = math.sin(theta)

		# deal with i1
		theta = theta+math.pi
		# deal with the u
		A[e['mid']][2*e['i1']] = math.cos(theta)
		# deal with the v
		A[e['mid']][2*e['i1']+1] = math.sin(theta)

	#  Edge elongations d => Edge tensions w
	C = numpy.zeros([len(edges), len(edges)])
	for e in edges:
		mid = e['mid']
		# TODO: replace this with e.A * e.E / e.L
		C[mid][mid] = 100.

	# Construct stiffness matrix K = A'CA
	A = numpy.matrix(A)
	C = numpy.matrix(C)
	K = A.transpose() * C * A

	# Construct external force vector f = Ku
	f = numpy.matrix(numpy.zeros(2*len(nodes))).transpose()
	for b in state['bcs']['loadednodes']:
		f[2*b['iid']] = b['x']
		f[2*b['iid']+1] = b['y']

	# Prune fixed nodes from system
	delids = [2*n['iid']+n['fix'] for n in state['bcs']['fixednodes']]
	Kp = numpy.delete(K, delids, 1)
	fp = numpy.delete(f, delids, 0)

	# Solve the damn thing
	u = numpy.linalg.pinv(K)*f

	print K.round(3)
	

	return K, f, Kp, fp, u

	