import pymongo

class Db:
	def Db(host="localhost", port=27017):
		conn = pymongo.Connection(host, port)
		self.host = host
		self.port = port
		self.models = conn['trussvis']['models']
		self.users = conn['trussvis']['users']

	def list_trusses(self, user):
		return " ".join(self.models.find({"user":user},{"name":1}))

	def load_truss(self, user, truss):
		self..find
		return state

	def save_truss(self, user, truss):
		truss['msg'] = "Truss saved."
		self.models.save(truss.update({"user":user}))
		return truss

	def new_user(self, user, password):
		self.users.save({"user":user, "pass":password})
		return "User created."

	def get_credentials(self, user):
		return self.users.find_one({"name":user})


