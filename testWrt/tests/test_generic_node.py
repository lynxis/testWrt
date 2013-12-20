#!/usr/bin/env python

from testWrt import testsetup
from testWrt.openwrt import SSHOpenWrt

KEYFILE = "/home/robin/Documents/42reports/firmware-tools/build/id_42r"

if __name__ == "__main__":
    ts = testsetup.create_generic()
    device = SSHOpenWrt(hostname="192.168.1.1", password="test")

    if device.ping():
        print "Device %s: reachable" % device.hostname
    else:
        print "Device %s not reachable" % device.hostname
        exit(1)

    if device.portscan(22):
        print "Device %s: SSH running" % device.hostname
    else:
        print "Device %s: SSH not running" % device.hostname
        exit(1)

    print "Device %s: %s" % (device.hostname,
                             device.execute("echo Hello World")[0].strip())

    print "Device %s: Network device list: %s" % (device.hostname,
                                                  device.network_interfaces())

    for interface in device.network_interfaces():
        if device.network_interface_state(interface):
            print "Device %s: %s up" % (device.hostname, interface)
        else:
            print "Device %s: %s down" % (device.hostname, interface)

    device.ubus("123")
