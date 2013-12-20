#!/usr/bin/env python

from testWrt import testsetup
from testWrt.openwrt import SSHOpenWrt

KEYFILE = "/home/robin/Documents/42reports/firmware-tools/build/id_42r"



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

    host = device.device_hostname()
    device.log("hostname: %s" % host)
    device.hostname = host

    device.log_file("/etc/openwrt_release")
    device.log_file("/etc/openwrt_version")
    device.log_ubus_call("system", "info")
    device.log_ubus_call("system", "board")
    
    for file in device.find("/sys/kernel/debug/usb/"):
        device.log_file(file)
    for file in device.find("/sys/bus/usb/"):
        device.log_file(file)
    for file in device.find("/sys/devices/platform/ehci-platform/"):
        device.log_file(file)
