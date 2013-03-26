
# Dictionary of help strings
helpstrings = {"":
"""Available commands:

	geometry load stress deflection factorofsafety
	node edge pointload uniformload fixnode check
	load save reset 

Try "help cmd" for more info.
	""",
	"geometry" : "geometry: Show the current truss geometry.",
	"bcs" : "bcs: Show the boundary conditions: fixed pins, point loadings, uniform loadings, etc.",
	"stress" : "stress: Plot the stress in each member.",
	"deflection" : "deflection: Plot the deflection in each member.",
	"factorofsafety" : "factorofsafetly: Highlight Factor of Safety transgressions.",
	"node" : "node (coords): Add a new pinned joint.",
	"edge" : "edge (j1, j2): Add a new (pinned) member connecting two joints.",
	"pointload" : "pointload (n, L) : Add a point load vector L to joint n.",
	"uniformload" : "uniformload (m, L) : Add a uniform load vector L to member m.",
	"fixnode" : "fixnode (j): Specify joint j as being fixed in space.",
	"check" : "check: Troubleshoot and verify your model.",
	"load" : "load (f): Loads truss f from disk.",
	"save" : "save (f): Saves truss to disk with filename f.",
	"reset" : "reset: Clear the console and redraw the visualization."}

# We want to retrieve the massive dict from docstrs instead
helpmsg = """
Available commands:

	geometry bcs stress deflection factorofsafety
	node edge pointload uniformload fixnode check
	load save reset 

Try "help cmd" for more info."""



# A basic truss for us to work with. See p42
truss = {"edges" : [
			{"mid" : 0, "i0" : 0, "i1" : 1}, 
		 	{"mid" : 1, "i0" : 1, "i1" : 2}, 
			{"mid" : 2, "i0" : 2, "i1" : 3}, 
			{"mid" : 3, "i0" : 3, "i1" : 4}, 
			{"mid" : 4, "i0" : 1, "i1" : 3}, 
			{"mid" : 5, "i0" : 0, "i1" : 2}, 
			{"mid" : 6, "i0" : 2, "i1" : 4}],
		"nodes" : [
			{"iid" : 0, "x" : 0.0, "y" : 0.0}, 
			{"iid" : 1, "x" : 2.0, "y" : 3.0}, 
			{"iid" : 2, "x" : 4.0, "y" : 0.0}, 
			{"iid" : 3, "x" : 6.0, "y" : 3.0},			
			{"iid" : 4, "x" : 8.0, "y" : 0.0}]}
