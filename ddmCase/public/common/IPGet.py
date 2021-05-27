# !/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import re


def innerIPGet():
    """
    查询本机内网ip地址
    :return: ip
    """
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def outerIPGet():
    """
    查询本机局域网对外的外网ip
    :return: ip
    """
    p = subprocess.Popen('cmd /u /c curl ifconfig.me', stdout=subprocess.PIPE)
    result = p.communicate()
    text = result[0].decode(encoding="utf-8")
    # print(text)
    outer_ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)[0]
    if outer_ip:
        return outer_ip
    else:
        print("查找不到外网ip，请检查网络环境")


if __name__ == '__main__':
    print(innerIPGet())
    # print(outerIPGet())
