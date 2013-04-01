import numpy

import sys
sys.path.append('..')
from trussmath import *

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


def test_make_graph_matrix():
	
	have = make_graph_matrix(state2).round()
	want = numpy.matrix('[0 1. 0 -1. 0 0.; 0 0. 0 1. 0 -1.]')
	assert((have == want).all())
