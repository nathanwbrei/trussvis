
import math 
import numpy

def make_difference_matrix(state):

	edges, nodes = state["edges"], state["nodes"]

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
	edges = state["edges"]
	C = numpy.zeros([len(edges), len(edges)])
	for e in edges:
		mid = e['mid']
		# TODO: replace this with e.A * e.E / e.L
		C[mid][mid] = 1.
	C = numpy.matrix(C)
	return C



def apply_boundary_conditions(state, A, C):
    """Returns stiffness matrix K=A'CA with columns rearranged
    to handle boundary conditions. E.g. if node n is fixed in the x_0
    direction, u[2n]=f_n0, not u_n0 (which is known to be zero).
    This way we can solve for both the deflections and the reaction 
    forces in one step. Described in HaSch notebook, Apr 24."""

    # Calculate original (B.C.-agnostic) stiffness matrix
    K = A.transpose() * C * A


    # Calculate the forcing vector
    nodes = state["nodes"]
    f = numpy.matrix(numpy.zeros(2*len(nodes))).transpose()
    for b in state['bcs']['loadednodes']:
        f[2*b['iid']] += b['x']
        f[2*b['iid']+1] += b['y']

    # For each node fix, rearrange K
    for node in state['bcs']['fixednodes']:
        index = 2*node['iid']+node['fix']
        
        # Zero the corresponding column in K
        K[:,index] = 0

        # Make u[index] = f_index instead of 0
        K[index,index] = -1

    return K, f 



def deflections_and_reactions(state, u):
    """Splits the result vector u into two vectors, one describing the deflections
    of the entire system, the other describing the reaction forces. """

    deflections = u.copy()
    reactions = numpy.zeros(u.shape)
    for k in state['bcs']['fixednodes']:
        f = deflections[2*k['iid']+k['fix']]
        reactions[2*k['iid']+k['fix']] = f
        deflections[2*k['iid']+k['fix']] = 0
    return deflections, reactions

        

def statics(state):
    """Returns all numerical results from the static analysis. This is used
    by both the optimization backend and the visualization frontent."""

    A = make_difference_matrix(state)
    C = make_constitutive_matrix(state)
    K,f = apply_boundary_conditions(state, A, C)
#    u = numpy.linalg.solve(K, f)
    u = numpy.linalg.pinv(K) * f
    deflections, reactions = deflections_and_reactions(state, u)
    stresses = C*A*deflections

    return stresses, deflections, reactions    


def colorize(stress, maxstress):

    if stress>0:
        hue = 0. # red=tension
    else:
        hue = 0.66 # blue=compression
    sat = abs(stress/maxstress)
    val = 0.75 
    if abs(stress/maxstress) > 1:
        hue = 0.3
        sat = 1
    import colorsys
    r,g,b = colorsys.hsv_to_rgb(hue, sat, val) 
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)
    return "#" + "".join(map(chr, (r,g,b))).encode('hex')



	
