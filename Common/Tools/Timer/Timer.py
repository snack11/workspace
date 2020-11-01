# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 2:53 AM
# @Author  : Bao Haoyu
# @Site    : 定时器结构, 一个简易的低效率的Timer结构（简易堆实现），有待C++底层以时间轮实现
# @File    : Timer.py.py
import time
import unittest
import heapq
import gevent
from Common import Const
from Common.Tools.Utils.IdManager import IdManager
from Common.Tools.Utils.Utils import Singleton


class TimerUnit(object):
    def __init__(self, start_time, last_time, callback, args, kwargs, repeat=False):
        super(TimerUnit, self).__init__()
        self.start_time = start_time  # 开始时间
        self.last_time = last_time  # 持续时间
        self.exec_time = self.start_time + self.last_time  # 下一次执行时间
        self.repeat = repeat
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False

    def trigger(self):
        if self.repeat and not self.cancelled:
            self.exec_time += self.last_time
            heapq._siftup(TimerSchedule().time_heap, 0)
        else:
            heapq.heappop(TimerSchedule().time_heap)
        if not self.cancelled:
            self.callback(*self.args, **self.kwargs)

    def __lt__(self, other):
        return self.exec_time < other.exec_time


class TimerSchedule(Singleton):
    # 该方案比时间轮方式消耗大很多，好处是易于理解实现, 不保证线程安全
    def __init__(self ):
        # 时间最小步长
        super(TimerSchedule, self).__init__()
        self.time_step = Const.time_step  # 每秒30帧
        self.startTime = self.last_time = self.now_time = time.time()
        self.now_num_step = 0
        self.time_heap = list()
        self.id2Timer = dict()
        self.cancelled_nums = 0

    def setTimeStep(self, value):
        self.time_step = value

    def tick(self):
        self.now_time = time.time()
        self.execChoices()
        sleep_time = self.startTime + self.time_step * self.now_num_step - time.time()
        if sleep_time > 0:
            # 使用协程库，不阻塞其他协程
            gevent.sleep(sleep_time)
        self.now_num_step += 1

    def execChoices(self):
        while len(self.time_heap) and self.time_heap[0].exec_time <= self.now_time:
            self.time_heap[0].trigger()

    def addTimer(self, last_time, callback, *args, **kwargs):
        return self.addInnerTimer(last_time, callback, args, kwargs, False)

    def addRepeatTimer(self, last_time, callback, *args, **kwargs):
        return self.addInnerTimer(last_time, callback, args, kwargs, True)

    def addInnerTimer(self, last_time, callback, args, kwargs, repeat):
        timer = TimerUnit(time.time(), last_time, callback, args, kwargs, repeat=repeat)
        heapq.heappush(self.time_heap, timer)
        tid = IdManager().genId()
        self.id2Timer[tid] = timer
        return tid

    def delTimer(self, tid):
        if tid not in self.id2Timer:
            return
        timer = self.id2Timer[tid]
        timer.cancelled = True
        self.cancelled_nums += 1
        if self.cancelled_nums / float(len(self.time_heap)) >= Const.cancel_limit:
            new_timer = []
            for item in self.time_heap:
                if not item.cancelled:
                    new_timer.append(item)
            self.time_heap = new_timer
            heapq.heapify(self.time_heap)
            self.cancelled_nums = 0


class UnitTest(unittest.TestCase):
    def testTime(self):
        a = TimerSchedule()
        b = TimerSchedule()
        self.assertEqual(a, b)
        start = time.time()

        def func():
            print(time.time())

        func()
        a.addTimer(0.7, func)
        a.addTimer(1.3, func)

        def funcB():
            print("b", time.time())

        tid = b.addRepeatTimer(0.2, funcB)

        def funcC(tid1):
            print("cancel b")
            TimerSchedule().delTimer(tid1)

        a.addTimer(1.0, funcC, tid)

        def funcD(p):
            print(p)
            if p != 10:
                return
            for i in xrange(50):
                a.delTimer(test_list[i * 2])

        test_list = []
        for i in xrange(100):
            test_list.append(a.addTimer(2 + i * 0.2, funcD, i))

        while a.now_time < start + 100.0:
            a.tick()


if __name__ == "__main__":
    unittest.main()
