# -*- coding: utf-8 -*-
# @Time    : 2020/1/5 2:17 PM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : TelnetServer
import unittest
from Common import Const
from Common.Tools.RPC.Net.TCPServer import TcpServerGeventBased
from Common.Tools.Timer.Timer import TimerSchedule


class TelnetServer(TcpServerGeventBased):
    def DealConnData(self, conn, data):
        try:
            comp = compile(data, "telnet_command", "single")
            ans = eval(data, {"s": self}, locals())
            self.write(conn, "{}\n".format(ans))
        except Exception as e:
            self.logger.error(e)
            import sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, exc_traceback)


class UnitTest(unittest.TestCase):
    def testTelnetServer(self):
        s = TelnetServer(Const.telnetUrl, Const.telnetPort)
        while True:
            s.tick()
            TimerSchedule().tick()


if __name__ == "__main__":
    unittest.main()
