#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib import SSHOpenWrt

if __name__ == "__main__":
    ts = testsetup.create_generic()
    device = SSHOpenWrt(hostname="192.168.1.1")
    ret = device.ping()
    print(str(ret))
