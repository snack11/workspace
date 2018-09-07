# coding:utf-8
import sys
import socket
import logging
import select
from Common import Const
sys.path.append("../")
logging.basicConfig(filename="NetServerLog.log", level=logging.INFO)


class NetStreamServer(object):
	def __init__(self, logic_server):
		super(NetStreamServer, self).__init__()
		self.host = None
		self.port = None
		self.socket = None
		self.state = Const.NET_CLOSE
		self.clients = {}
		self.inputs = []
		self.logic_server = logic_server

	def init(self, host="127.0.0.1", port=51423):
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.state = Const.NET_CLOSE
		self.clients = {}
		self.inputs = []

	def start(self):
		try:
			self.socket.bind((self.host, self.port))
		except socket.error as es:
			try:
				self.socket.close()
				logging.error("socket_error_in_bind:{}".format(es))
			except Exception as e:
				logging.error("socket_error_in_close:{}".format(e))
			return -1
		self.state = Const.NET_RUNNING
		self.in_running()

	def in_running(self):
		self.socket.listen(5)
		self.socket.setblocking(False)
		self.inputs = [self.socket, ]
		while self.state == Const.NET_RUNNING:
			rs, ws, es = select.select(self.inputs, [], [])
			for fd in rs:
				if fd == self.socket:
					conn, addr = fd.accept()
					self.inputs.append(conn)
					self.clients[fd] = conn
				else:
					recv = ""
					try:
						# 粘包
						conn = self.clients[fd]
						data = conn.recv(1024)
						# print "data:{}".format(data)
						while len(data) == 1024:
							recv = "{}{}".format(recv, data)
							data = conn.recv(1024)
						recv = "{}{}".format(recv, data)
						if recv:
							print int(recv[0:1])
						else:
							# 断开连接
							self.inputs.remove(conn)
							self.clients.pop(conn)
							continue
					except socket.error:
						logging.error(fd.getpeername(), 'disconnected')
					self.logic_server.deal_data(recv)
					# recv and conn.sendall(recv)  # todo 扔到主线程处理

	def close(self):
		self.init(self.host, self.port)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--host', type=str, default="127.0.0.1", help='host')
	parser.add_argument('--port', type=int, default=51423, help='port')
	args = parser.parse_args()
	s = NetStreamServer()
	s.init(args.host, args.port)
	s.start()
