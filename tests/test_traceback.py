#!/usr/bin/env python

from testWrt import testsetup

from testWrt.lib import SSHOpenWrt

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
        device.log("sshd not running")
        exit(1)

    device.log("hostname: %s" % device._hostname)

    device.log_file("/etc/openwrt_release")
    device.log_file("/etc/openwrt_version")
    device.log_json("ubus.system.info",
                    device.ubus_call("system", "info"))
    device.log_json("ubus.system.board",
                    device.ubus_call("system", "board"))

    device.log_array("logread", device.logread())
    device.log_array("dmesg", device.dmesg())
