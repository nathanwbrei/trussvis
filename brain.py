
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


@register("load")
def load_cmd(*args):
	"""Loads truss f from disk."""

	with (open("models/"+args[0])) as f:
		data = f.readlines()
		state.update(json.JSONDecoder().decode(data[0]))
		state['msg'] = "Loaded truss at: " + args[0]


@register("help")
def help_cmd(*args):
	""" Get help for a specified command. """

	if not args:
		# Print a long list of commands
		from hardcoded import helpmsg
		state['msg'] = helpmsg
	elif dispatch_table.has_key(args[0]):
		# Help string doubles as docstring
		state['msg'] = dispatch_table[args[0]].__doc__
	else:
		state['msg'] = str(args[0]) + ": command not found."
	

