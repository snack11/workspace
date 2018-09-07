import sys
sys.path.append("../")
import threading
from Common import Const
import logging
logging.basicConfig(filename="ConsoleLog.log", level=logging.INFO)
import traceback

class Console(object):
	def __init__(self, server):
		super(Console, self).__init__()
		self.server = server

	def start(self):
		self.state = Const.CONSOLE_OPEN
		self.console = threading.Thread(target=self.Run).start()

	def Run(self):
		while self.state == Const.CONSOLE_OPEN:
			try:
				data = input("<<:")
				exec(data)
			except Exception as e:
				info = traceback.format_exc()
				print(info)
				logging.debug(e)

	def close(self):
		self.state = Const.CONSOLE_CLOSE

if __name__ == '__main__':
	Console(1).start()
