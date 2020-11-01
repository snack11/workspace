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
        historyData = self.con2data.get(conn, "")
        if data == "\r\n":
            self.DoDealConnDat(conn, historyData)
            self.con2data.pop(conn, None)
        elif data.endswith("\n"):
            self.DoDealConnDat(conn, data)
            self.con2data.pop(conn, None)
        else:
            self.con2data[conn] = historyData + data

    def DoDealConnDat(self, conn, data):
        # 是否登录
        stat = self.con2stat.get(conn, False)
        if stat:
            self.EvalConnData(conn, data)
        else:
            if self.loginConFirm(data):
                self.con2stat[conn] = True
            else:
                self.write(conn, "{}\n".format("user passwd"))

    def EvalConnData(self, conn, data):
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
