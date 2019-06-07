# coding: utf-8
from Common.NetStreamServer import NetStreamServer
import Queue


class PyServer(object):
	__instance = None
	@classmethod
	def get_instance(cls):
		if cls.__instance is None:
			cls.__instance = cls()
		return cls.__instance

	def __init__(self):
		self.server = NetStreamServer()
		self.run = True
		self.message_queue = Queue()

	def init(self, host="127.0.0.1", port=51423):
		self.server.init(host, port)

	def start(self):
		self.server.start()
		while self.start():
			pass

	def deal_data(self, data):
		self.message_queue.push(data)

