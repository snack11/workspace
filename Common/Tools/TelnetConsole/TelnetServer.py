# -*- coding: utf-8 -*-
# @Time    : 2020/1/5 2:17 PM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : TelnetServer
import unittest
from Common import Const
from Common.Tools.RPC.Net.TCPServer import TcpServerGeventBased
from Common.Tools.Timer.Timer import TimerSchedule
from Common.Const import LoginState

userDict = {'whathappen': 'asdasd'}


class TelnetServer(TcpServerGeventBased):
    def loginConFirm(self, data_):
        # 密码验证
        data_ = data_.split(' ')
        if len(data_) != 2:
            return False
        if data_[0] not in userDict:
            return False
        if data_[1] != userDict[data_[0]]:
            return False
        return True

    def __init__(self, ip, port, backlog=None):
        super(TelnetServer, self).__init__(ip, port, backlog)
        self.con2stat = {}
        self.con2data = {}

    def DealConnData(self, conn, data):
        # 取完整数据
        try:
            historyData = self.con2data.get(conn, "")
            if data == "\r\n":
                self.DoDealConnDat(conn, historyData)
                self.con2data.pop(conn, None)
            elif data.endswith("\n"):
                self.DoDealConnDat(conn, data)
                self.con2data.pop(conn, None)
            else:
                self.con2data[conn] = historyData + data
        except Exception as e:
            self.logger.error(e)
            import sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, exc_traceback)

    def BrainAns(self, conn, data):
        if data == '\r\n':
            pass
        if data.startswith('ip'):
            from Common.Tools.Utils.Utils import getLocalIP
            IPAdress = getLocalIP()
            self.write(conn, "\r\n{}\r\n".format(IPAdress))


        else:   self.EvalConnData(conn, data)

    def DoDealConnDat(self, conn, data):
        # 是否登录
        stat = self.con2stat.get(conn, False)
        if stat:
            self.BrainAns(conn, data)
        else:
            if self.loginConFirm(data):
                self.con2stat[conn] = True
                self.write(conn, "{}\r\n".format("welcome"))
            else:
                self.write(conn, "\r\n{}\r\n".format("user passwd"))

    def EvalConnData(self, conn, data):
        try:

            comp = compile(data, "telnet_command", "single")
            ans = eval(data, {"s": self}, locals())
            self.write(conn, "{}\n".format(ans))
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            self.logger.error("Traceback: {}, data: {}".format(trace, data))


class UnitTest(unittest.TestCase):
    def testTelnetServer(self):
        s = TelnetServer(Const.telnetUrl, Const.telnetPort)
        while True:
            s.tick()
            TimerSchedule().tick()


if __name__ == "__main__":
    unittest.main()
