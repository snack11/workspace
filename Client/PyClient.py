# coding:utf-8
import sys
from Common.NetStreamClient import NetStreamClient
sys.path.append("../")


class PyClient(object):
	__instance = None

	@classmethod
	def get_instance(cls):
		if cls.__instance is None:
			cls.__instance = cls()
		return cls.__instance

	def __init__(self):
		self.client = NetStreamClient()

	def send(self, msg):
		self.client.send(msg)
		self.client.process()


if __name__ == '__main__':
	client = PyClient()
	client.client.connect("127.0.0.1", 51423)
	while 1:
		import time
		time.sleep(0.5)
		client.client.send("asd")
		client.client.process()
