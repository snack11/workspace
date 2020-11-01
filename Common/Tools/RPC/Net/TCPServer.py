# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 11:05 PM
# @Author  : Bao Haoyu
# @Site    : 目标是不开多线程（python有全局锁，多线程效率低），用协程实现sock的服用逻辑
# 思考很久，之后决定用各个版本实现一下。
# @File    : TCPServer.py
import traceback
import unittest

from Common import Const
from Common.Const import NONBLOCKING
from Common.Tools.Logging.SysLog import regLog
from Common.Tools.Timer.Timer import TimerSchedule
from gevent import socket, spawn


@regLog
class TcpServerGeventBased(object):
    #  限制很大，不推荐使用，如果要使用必须保证主线程没有阻塞
    def __init__(self, ip, port, backlog=None):
        super(TcpServerGeventBased, self).__init__()
        self.socket = None
        self.ip = ip
        self.port = port
        self.backlog = backlog
        self.conns = list()
        self.in_accepting = False
        self.initSocket()

    def initSocket(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False)
        self.socket.listen(self.backlog if self.backlog else socket.SOMAXCONN)

    def receive(self, conn):
        try:
            can_receive = True
            while can_receive:
                data = conn.recv(Const.socket_const_bytes).decode("utf-8")
                self.logger.info("receive: {}".format(data))
                if not data:
                    can_receive = False
                    self.closeConnection(conn)
                else:
                    self.DealConnData(conn, data)
        except Exception as e:
            self.logger.info(str(e))
            self.closeConnection(conn)

    def DealConnData(self, conn, data):
        pass

    def write(self, conn, message):
        try:
            conn.send(message.encode("gb2312"))
        except Exception as e:
            self.closeConnection(conn)
            self.logger.info(e)

    def closeConnection(self, conn):
        try:
            self.logger.info("stop connection {}".format(conn))
            conn.shutdown(socket.SHUT_WR)
            conn.close()
        except Exception as e:
            self.logger.info(e)
        if conn in self.conns:
            self.conns.remove(conn)

    def tick(self):
        client = None
        try:
            client, address = self.socket.accept()
        except socket.error as e:
            if e.args[0] in NONBLOCKING:
                return
            self.logger.info(traceback.format_exc() + '\n' + str(e))
        finally:
            if client:
                self.conns.append(client)
                spawn(self.receive, client)


class UnitTest(unittest.TestCase):
    def testServerGeventBased(self):
        s = TcpServerGeventBased(Const.testUrl, Const.testPort)
        def writeAll():
            if s.conns:
                for conn in list(s.conns):
                    s.write(conn, "hello world")
        TimerSchedule().addRepeatTimer(1, writeAll)
        while True:
            s.tick()
            # time的tick中会释放协程
            TimerSchedule().tick()


if __name__ == "__main__":
    unittest.main()
