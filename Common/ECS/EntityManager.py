from Common.ECS.Entity import Entity


class EntityManager(object):
	__instance = None

	@classmethod
	def get_instance(cls):
		if cls.__instance is None:
			cls.__instance = cls()
		return cls.__instance

	def __init__(self):
		super(EntityManager, self).__init__()
		self.entity_to_components = dict()

	def __getitem__(self, entity):
		return self.entity_to_components.get(entity, None)

	@staticmethod
	def generate_id():
		import uuid
		return str(uuid.uuid1())

	def add_entity(self, uid=""):
		if uid:
			entity = Entity(uid)
		else:
			entity = Entity(self.generate_id())
		self.entity_to_components[entity] = None

	def del_entity(self, entity=None):
		if entity:
			self.entity_to_components.pop(entity)

	def del_entity_by_uid(self, uid=""):
		uid and self.entity_to_components.pop(uid, None)

	def entity_add_component(self, entity, component):
		pass

	def entity_del_component(self, entity, component):
		pass

