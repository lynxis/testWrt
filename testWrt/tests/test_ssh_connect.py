#!/usr/bin/env python

from testWrt import testsetup
from testWrt.openwrt import SSHOpenWrt

KEYFILE = "/home/robin/Documents/42reports/firmware-tools/build/id_42r"

if __name__ == "__main__":
    ts = testsetup.create_generic()
    ret = "hello openwrt"
    device = SSHOpenWrt(hostname="192.168.1.1", keyfile=KEYFILE)
    ret = device.execute("echo hello openwrt")
    if ret[0].strip() != "hello openwrt":
    	print False
    print True
