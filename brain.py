
from copy import deepcopy
import json



# Keep all of our state here. We pass the entire thing to the 
# frontend as JSON on each response.

empty_state = {"nodes" : [], "edges" : [], "message" : "Welcome to trussvis!"}
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


@register("stress")
def stress_cmd(*args):
    """Plot the stress indef run_statics(state):"""

    from trussmath import statics
    stresses, deflections, reactions = statics(state)
    state['msg'] = "Calculated statics."
    return state

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

