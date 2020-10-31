# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 2:13 AM
# @Author  : Bao Haoyu
# @Site    : 
# @File    : Const.py.py
import errno

# logging 相关
logging_path = "/Users/snack/WorkSpace/SpecialCode/LogInfo/log.log"

# timer 相关
time_step = 0.033
cancel_limit = 0.3  # 0.3的timer被取消时，重新抉择timer


class TimerMode(object):
    TimerCancel = 0x00
    TimerReplace = 0x01


# socket相关
testUrl = "localhost"
testPort = 22347
NONBLOCKING = (errno.EAGAIN, errno.EWOULDBLOCK)
socket_const_bytes = 1024

# console 相关
telnetUrl = "192.168.0.102"
telnetPort = 22348


if __name__ == "__main__":
    pass
