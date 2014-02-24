#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib import SSHOpenWrt

from paramiko import util

if __name__ == "__main__":
    util.log_to_file("/tmp/logggg")

    ts = testsetup.create_generic()
    device = SSHOpenWrt(hostname="192.168.1.1")
    stdout, stderr = device.execute("echo hello openwrt")
    if stdout[0].strip() != "hello openwrt":
        print(False)
    print(True)
