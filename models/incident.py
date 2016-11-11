
class Incident(object):
	"""docstring for Incident"""
	def __init__(self, ID, description, address, active, latitude, longitude, time, title, organizations):
		self.id = ID
		self.description = description
		self.address = address
		self.active = active
		self.latitude = latitude
		self.longitude = longitude
		self.time = time
		self.title = title
		self.organizations = organizations

	def __eq__(self, other):
		return self.id == other.id




