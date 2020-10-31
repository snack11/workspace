# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 12:47 AM
# @Author  : Bao Haoyu
# @Site    :
# @File    : SysLog.py
import unittest
import logging
import traceback
from Common import Const
import sys
import functools
from Common.Tools.Utils.Utils import Singleton


def func_wrap(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        # warning 以上打出地址信息
        args = list(args)
        args[1] = "\n{}{}".format("".join(traceback.format_stack()[:-1]), args[1])
        func(*args, **kwargs)
    return wrap


class SysLog(logging.LoggerAdapter):
    @func_wrap
    def error(self, *args, **kwargs):
        super(SysLog, self).error(*args, **kwargs)

    @func_wrap
    def critical(self, *args, **kwargs):
        super(SysLog, self).critical(*args, **kwargs)


def regLog(klas, *args, **kwargs):
    if hasattr(klas, "logger"):
        return klas(*args, **kwargs)
    logger = logging.Logger(klas)
    logger_adapter = SysLog(logger, dict())
    file_handler = logging.FileHandler(filename=Const.logging_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)d行 %(funcName)s %(message)s")
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)d行 %(funcName)s %(message)s")
    )
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    klas.logger = logger_adapter
    return klas


class UnitTest(unittest.TestCase):
    def testLogging(self):

        @regLog
        class A(Singleton):
            def __init__(self):
                self.logger.info("yes")

            def lalog(self, info):
                self.logger.info(info)

        class B(A):
            pass

        A().lalog("ok ok!")
        A().logger.error("尝试一下中文")
        A().logger.info("???OK")
        B().logger.info("???")


if __name__ == "__main__":
    unittest.main()
