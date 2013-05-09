
from copy import deepcopy
import json



# Keep all of our state here. We pass the entire thing to the 
# frontend as JSON on each response.

empty_state = {"geom" : {"nodes":[], "edges":[]}, 
		 "vis"  : {"nodes":[], "edges":[]},
		 "bcs"  : {"fixednodes":[], "loadednodes":[], "loadededges":[]},
		 "msg"  :  "" }

state = deepcopy(empty_state)

# Our command interpreter picks up a command and an argument list, 
# and calls the function mapped to the command in a dispatch table.

dispatch_table = {}

def dispatch(cmd, *args):
	if dispatch_table.has_key(cmd):
		try:
			dispatch_table[cmd](*args)
		except Exception as e:
			state['msg'] = cmd+" failed" + "".join([" : " +str(s) for s in e.args])
	else:
		state['msg'] = "Unrecognized command `" + cmd + "`"
	print state['msg']

# We use a decorator to make our command interpreter as easy to 
# extend as possible. Simply append '@register(cmdname)' above 
# the function definition to register with the dispatch table. 

def register(name):
	def inner(f):
		dispatch_table[name] = f
	return inner


# Commands are defined here. 

# Each command has its own method. 
# The method must accept a variable number of arguments and 
# interpret them all by itself. Return value doesn't matter 
# right now. Side effects should be limited to the 'state'
# dictionary unless there is a REALLY good reason not to.



@register("geometry")
def geom_cmd(*args):
	"""Show the current truss geometry."""

	state['vis'] = deepcopy(state['geom'])
	state['msg'] = "Showing geometry."


@register("new")
def new_cmd(*args):
    state["geom"] = {"nodes":[], "edges":[]}
    state["vis"] = {"nodes":[], "edges":[]}
    state["bcs"] = {"fixednodes":[], "loadednodes":[], "loadededges":[]}
    state['msg'] = "Created new."

@register("stress")
def stress_cmd(*args):
    """Plot the stress indef run_statics(state):"""

    print "1"
    from trussmath import statics, colorize
    stresses, deflections, reactions = statics(state)
    print "2"
    state['vis'] = deepcopy(state['geom'])
    for m in state['vis']['edges']:

        k = m['mid']
        m['color'] = colorize(stresses[k], 5)

    state['msg'] = "Calculated statics."

    return state

@register("move")
def move_cmd(*args):
	""" move (n x y): Change a node's location """
	n = int(args[0][1:])
	x = float(args[1])
	y = float(args[2])
	state['geom']['nodes'][n]['x'] = x
	state['geom']['nodes'][n]['y'] = y
	state['vis'] = deepcopy(state['geom'])
	state['msg'] = "Successfully moved node."


@register("json")
def json_cmd(*args):
    from pprint import pformat
    state['msg'] = "Current state is:\n"+pformat(state)

@register("node")
def node_cmd(*args):
	"""	Node (coords): Add a new pinned joint. """
	x = float(args[0])
	y = float(args[1])

	nodes = state['geom']['nodes']
	nodes.append({"iid":len(nodes), "x":x, "y":y})
	state['vis'] = deepcopy(state['geom'])
	state['msg'] = "Successfully added node."


@register("fix")
def fix_cmd(*args):
    """ fix(node, direction): 
    node n in {n0, n1, ...}
    direction d in {0: "x", 1: "y"}"""
    if len(args) == 0:
        state['msg'] = "Current fixings:\n" + str(state['bcs']['fixednodes'])
    else:
	node = int(args[0][1:])
        direction = int(args[1])
        state['bcs']['fixednodes'].append({"iid":node, "fix":direction})
        state['msg'] = "Fixed n"+ str(node) + " in the x_"+ str(direction) + "direction." 
    return state

@register("load")
def load_cmd(*args):
    """load(node, direction, amount)
    """
    if len(args) == 0:
        state['msg'] = "Current loadings:\n" + str(state['bcs']['loadednodes'])
    else:
	node = int(args[0][1:])
        xload = int(args[1])
        yload = int(args[2])
        state['bcs']['loadednodes'].append({"iid":node, "x":xload, "y":yload})
        state['msg'] = "Loaded f(n"+ str(node) + ") = " + str(xload) + "i + " + str(yload) + "j"
    return state


@register("edge")
def edge_cmd(*args):
	"""edge (j1, j2): Add a new (pinned) member connecting two joints."""

	i0 = int(args[0][1:])
	i1 = int(args[1][1:])

	edges = state['geom']['edges']
	edges.append({"mid":len(edges), "i0":i0, "i1":i1})
	state['vis'] = deepcopy(state['geom'])
	state['msg'] = "Successfully added edge."


@register("delete")
def del_cmd(*args):
	"""del entity: Deletes the selected node or edge."""

	# if args[0][0] == "e":
	# 	# delete an edge

	# else:
	# 	# delete a node
	# 	i = int(args[0][1:])
	state['msg'] = "Too much trouble."


@register("open")
def open_cmd(*args):
	"""Loads truss f from disk."""

        if len(args)==0:
            state['msg'] = "ls functionality coming when I switch to a real database"
        else:
            with (open("models/"+args[0])) as f:
                    data = f.readlines()
                    state.update(json.JSONDecoder().decode(data[0]))
                    state['msg'] = "Opened truss at: " + args[0]


@register("save")
def load_cmd(*args):
	"""save f: Save truss under filename f."""

    	with (open("models/"+args[0], "w")) as f:
		data = json.JSONEncoder().encode(state)
		f.write(data)
		state['msg'] = "Saved truss to: " + args[0]


@register("help")
def help_cmd(*args):
	""" Get help for a specified command. """

	if not args:
		# Print a long list of commands
		state['msg'] = "Available commands:\n" + \
					   " ".join(dispatch_table.keys()) + \
					   "\nType `help cmd` for more info."
	elif dispatch_table.has_key(args[0]):
		# Help string doubles as docstring
		state['msg'] = dispatch_table[args[0]].__doc__
	else:
		state['msg'] = str(args[0]) + ": command not found."
	

