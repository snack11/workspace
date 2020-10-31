# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 11:09 PM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : SimpleServer.py.py
import json

from Common.Tools.Logging.SysLog import regLog
from Common.Tools.Timer.Timer import TimerSchedule
from Common.Tools.Utils.Utils import Singleton


@regLog
class SimpleServer(Singleton):
    def __init__(self, config_path):
        self.run = False
        self.config = self.jsonConf(config_path)

    @staticmethod
    def jsonConf(addr):
        with open(addr, "r") as f:
            return json.loads(f.read())

    def startServer(self):
        self.run = True
        self.runServer()

    def runServer(self):
        while self.run:
            try:
                TimerSchedule().tick()
            except Exception as e:
                self.logger.info(str(e))
                self.run = False

    def closeServer(self):
        self.run = False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="./Server/ServerConf/ServerConf.json", help="write the config path")
    config = parser.parse_args().config
    SimpleServer(config).startServer()
