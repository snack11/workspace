#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 2:03 AM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : Utils.py
# @Software: PyCharm
import unittest


class SingleTonAbandond(object):
    _instance = {}

    def __new__(cls):
        cls_name = cls.__name__
        cls._instance[cls_name] = cls._instance[cls_name] if cls_name in cls._instance \
            else super(SingleTonAbandond, cls).__new__(cls)
        return cls._instance[cls_name]


class SingleTonMetaClass(type):
    _instance = {}

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super(SingleTonMetaClass, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SingleTonMetaClass, cls).__call__(*args, **kwargs)
        return cls.__instance


class Singleton(object):
    __metaclass__ = SingleTonMetaClass


class UnitTest(unittest.TestCase):
    def testSingleTon(self):
        a = Singleton()
        b = Singleton()

        class Test(Singleton):
            def __init__(self):
                super(Test, self).__init__()
                self.a = 0.1
        d = Test()
        e = Test()
        d.a = 0.2

        class Test2(Singleton):
            def __init__(self, a1):
                self.a = a1
        f = Test2(1.2)
        g = Test2(1.3)

        self.assertEqual(f, g)
        self.assertEqual(f.a, g.a)
        self.assertEqual(a, b)
        self.assertNotEqual(a, d)
        self.assertEqual(d, e)
        self.assertNotEqual(b, e)
        self.assertEqual(e.a, 0.2)


if __name__ == "__main__":
    unittest.main()

