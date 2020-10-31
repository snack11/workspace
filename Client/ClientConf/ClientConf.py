# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 11:12 PM
# @Author  : Bao Haoyu
# @Site    :
# @File    : ClientConf.py.py
ServerConf = {
    "tick_interval": 0.033,
    "game_ip": "127.0.0.1",
    "game_port": 12345,
    "remote_debug_ip": "127.0.0.1",
    "remote_debug_port": 22346,
    "encryption": "None",
    "compression": "None",
    "telnet_port": 32346,
}

if __name__ == "__main__":
    import json
    with file("./ClientConf.json", "w") as f:
        json.dump(ServerConf, f)
