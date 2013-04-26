import numpy
import sys
sys.path.append('..')
from trussmath import *

state = {"geom":{"nodes": [{"iid":0, "x":1, "y":2},
                           {"iid":1, "x":1, "y":1},
                           {"iid":2, "x":0, "y":0},
                           {"iid":3, "x":2, "y":0}],
                 "edges": [{"mid":0, "i0":0, "i1":1},
                           {"mid":1, "i0":1, "i1":2},
                           {"mid":2, "i0":1, "i1":3}]},
	 "bcs":{"fixednodes": [{"iid":2, "fix":0},
                               {"iid":2, "fix":1},
                               {"iid":3, "fix":0},
                               {"iid":3, "fix":1}],
                "loadednodes": [{"iid":0, "x":0, "y":1}]}}


def test_make_difference_matrix():
    have = make_difference_matrix(state)
    print "Have :"
    print have.round(4)
    a = 1/math.sqrt(2)
    want = numpy.matrix([[0, 1., 0, -1., 0, 0, 0, 0.],[0,0,a,a,-a,-a,0,0],[0,0,-a,a,0,0,a,-a]])
    print "Want: "
    print want.round(4)
    print "Difference: "
    print have-want
    assert((have.round(10) == want.round(10)).all())


def test_make_constitutive_matrix():
    have = make_constitutive_matrix(state).round()
    want = numpy.matrix(numpy.eye(3,3))
    assert((have == want).all())


def test_make_stiffness_matrix():
    A = make_difference_matrix(state)
    C = make_constitutive_matrix(state)
    have = A.transpose()*C*A
    want =numpy.array(
        [[ 0. ,  0. ,  0. , -0. ,  0. ,  0. ,  0. ,  0. ],
        [ 0. ,  1. ,  0. , -1. ,  0. ,  0. ,  0. ,  0. ],
        [ 0. ,  0. ,  1. , -0. , -0.5, -0.5, -0.5,  0.5],
        [-0. , -1. , -0. ,  2. , -0.5, -0.5,  0.5, -0.5],
        [ 0. ,  0. , -0.5, -0.5,  0.5,  0.5,  0. ,  0. ],
        [ 0. ,  0. , -0.5, -0.5,  0.5,  0.5,  0. ,  0. ],
        [ 0. ,  0. , -0.5,  0.5,  0. ,  0. ,  0.5, -0.5],
        [ 0. ,  0. ,  0.5, -0.5,  0. ,  0. , -0.5,  0.5]])
    assert((have.round(10) == want).all())




# This is the two-node example from the HaSch notebook, 24 April.
state2 = {"geom":
            {"nodes": 
                [{"iid":0, "x":0, "y":0},
                {"iid":1, "x":10, "y":0}],
            "edges": 
                [{"mid":0, "i0":0, "i1":1}]},
        "bcs":
            {"fixednodes": 
                [{"iid":0, "fix":0},
                {"iid":0, "fix":1}],
            "loadednodes": 
                [{"iid":1, "x":1, "y":0}]}}


def test_apply_boundary_conditions():
    A = make_difference_matrix(state2)
    C = make_constitutive_matrix(state2)
    K_have, f_have= apply_boundary_conditions(state2, A, C)
    print "Have K="
    print K_have.round(2)
    print "Have f="
    print f_have.round(2)

    K_want = numpy.matrix([[-1.,0.,-1.,0.],[0,-1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,0.]])
    f_want = numpy.matrix([[0.],[ 0.],[ 1.],[ 0.]])
    print "Want K="
    print K_want.round(2)
    print "Want f="
    print f_want.round(2)
    assert((K_have.round(10) == K_want).all())
    assert((f_have.round(10) == f_want).all())

    
def test_results():

    have_stresses, have_deflections, have_reactions = statics(state2)

    want_stresses = numpy.matrix([[1]])
    want_deflections = numpy.matrix([[0,0,1,0]]).transpose()
    want_reactions = numpy.matrix([[-1, 0,0,0]]).transpose()
    print "Have stresses"
    print have_stresses
    print "Have deflections"
    print have_deflections
    print "Have reactions"
    print have_reactions



    assert((have_stresses.round(10) == want_stresses).all())
    assert((have_deflections.round(10) == want_deflections).all())
    assert((have_reactions.round(10) == want_reactions).all())



def test_colorize():

