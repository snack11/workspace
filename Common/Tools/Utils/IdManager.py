# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:17 AM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : IdManager.py.py
import unittest
from timeit import timeit

from Common.Tools.Utils import Utils
import uuid


class IdManager(Utils.Singleton):
    id_style = {
        "uuid4": lambda *_: uuid.uuid4()
    }

    @classmethod
    def genId(cls, id_type="uuid4", *args):
        return cls.id_style[id_type](*args)


class UnitTest(unittest.TestCase):
    def testGenId(self):
        for skey in IdManager.id_style:
            test_str = "IdManager().genId('{}')".format(skey)
            self.assertLess(timeit(stmt=test_str, setup="from IdManager import IdManager", number=1,), 5e-4)


if __name__ == "__main__":
    unittest.main()