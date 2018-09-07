from Common.ECS.EntityManager import EntityManager


class Entity(object):
	__slots__ = ("_uid", "_componentsList")

	def __init__(self, uid):
		super(Entity, self).__init__(uid)
		self._uid = uid
		self._componentsList = dict()

	def __getattr__(self, component_var):
		return EntityManager.get_instance()[self].get(component_var, None)

	def __hash__(self):
		return hash(self._uid)
