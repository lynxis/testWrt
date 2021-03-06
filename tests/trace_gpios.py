#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib import SSHOpenWrt

if __name__ == "__main__":
    ts = testsetup.create_generic()
    device = SSHOpenWrt(hostname="192.168.1.1", password="test")

    if device.ping():
        device.log("reachable")
    else:
        device.log("not reachable")
        exit(1)

    if device.portscan(22):
        device.log("sshd running")
    else:
        device.lg("sshd not running")
        exit(1)

    device.log_json("gpio_count", device.gpio_count())
    device.log_json("gpio_inspect", device.gpio_inspect_all())
