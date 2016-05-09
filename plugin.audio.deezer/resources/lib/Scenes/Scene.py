
class Scene(object):
	def __init__(self, sceneRouter, name = "scene", title = "Scene"):
		print "Initialise Scene"
		self.sceneRouter = sceneRouter
		self.name = name
		self.title = title

	def setView(self, view):
		self.view = view
		self.view.show()

	def __repr__(self):
		return self.title
	def __str__(self):
		return self.__repr__()