
from copy import deepcopy
import json



# Keep all of our state here. We pass the entire thing to the 
# frontend as JSON on each response.

state = {"geom" : {"nodes":[], "edges":[]}, 
		 "vis"  : {"nodes":[], "edges":[]},
		 "bcs"  : {"fixednodes":[], "loadednodes":[], "loadededges":[]},
		 "msg"  :  "" }

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


@register("stress")
def stress_cmd(*args):
	"""Plot the stress in each member."""

	import random
	state['vis'] = deepcopy(state['geom'])
	for m in state['vis']['edges']:
		m['color'] = "#" + hex(random.randint(50,255))[2:4] + "0000"
	state['msg'] = "Showing stress distribution."

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


@register("node")
def node_cmd(*args):
	"""	Node (coords): Add a new pinned joint. """
	x = float(args[0])
	y = float(args[1])

	nodes = state['geom']['nodes']
	nodes.append({"iid":len(nodes), "x":x, "y":y})
	state['vis'] = deepcopy(state['geom'])
	state['msg'] = "Successfully added node."


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


@register("load")
def load_cmd(*args):
	"""Loads truss f from disk."""

	with (open("models/"+args[0])) as f:
		data = f.readlines()
		state.update(json.JSONDecoder().decode(data[0]))
		state['msg'] = "Loaded truss at: " + args[0]


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
	

