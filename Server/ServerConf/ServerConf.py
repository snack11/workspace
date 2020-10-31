# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 11:12 PM
# @Author  : Bao Haoyu
# @Site    :
# @File    : ServerConf.py.py
ServerConf = {
    "tick_interval": 0.033,
    "game_ip": "127.0.0.1",
    "game_port": 12345,
    "remote_debug_ip": "127.0.0.1",
    "remote_debug_port": 22345,
    "encryption": "None",
    "compression": "None",
    "telnet_port": 32345,
}

if __name__ == "__main__":
    import json
    with file("./ServerConf.json", "w") as f:
        json.dump(ServerConf, f)