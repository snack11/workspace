# -*- coding: utf-8 -*-
# @Time    : 2019/6/9 2:48 AM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : TcpClient.py
import unittest
from gevent import socket, spawn
from Common import Const
from Common.Tools.Logging.SysLog import regLog
from Common.Tools.Timer.Timer import TimerSchedule


@regLog
class TcpClient(object):
    def __init__(self, addr, port):
        self.socket = None
        self.address = addr
        self.port = port
        self.initSocket(self.address, self.port)

    def initSocket(self, address, port):
        try:
            if self.socket:
                self.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((address, port))
            spawn(self.receive)
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def send(self, message):
        try:
            if self.socket:
                self.logger.info("send: {}".format(message))
                self.socket.send(message.encode("gb2312"))
        except socket.error as e:
            self.logger.info(e)
            self.close()

    def receive(self):
        try:
            while self.socket:
                data = self.socket.recv(Const.socket_const_bytes).decode("utf-8")
                self.logger.info("receive: {}".format(data))
                if not data:
                    self.close()
        except Exception as e:
            self.logger.info(e)
            self.close()

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None


class UnitTest(unittest.TestCase):
    def testClient(self):
        tcli = TcpClient(Const.testUrl, Const.testPort)
        TimerSchedule().addRepeatTimer(2, tcli.send, "alive")
        while True:
            TimerSchedule().tick()


if __name__ == "__main__":
    unittest.main()