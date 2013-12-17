#!/usr/bin/env python

from testWrt import testsetup
from testWrt.openwrt import SSHOpenWrt

if __name__ == "__main__":
    ts = testsetup.create_generic()
    ret = "hello openwrt"
    device = SSHOpenWrt(ip="192.168.1.1", password="admin")
    ret = device.execute("hello openwrt")
    if ret != "hello openwrt":
        print "error"
