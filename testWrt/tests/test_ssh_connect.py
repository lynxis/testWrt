#!/usr/bin/env python

from testWrt import testsetup

if __name__ == "__main__":
    ts = testsetup.create_generic()
    device = SSHOpenWrt(Ip="192.168.1.1", password="admin")
    ret = device.exec("hello openwrt")
    if ret != "hello openwrt":
        raise TestException
