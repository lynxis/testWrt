#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib.openwrt_ssh import SSHOpenWrt

KEYFILE = "/home/robin/Documents/42reports/firmware-tools/build/id_42r"

def print_error(msg):
    print msg
    exit(1)

if __name__ == "__main__":
    ts = testsetup.create_generic()
    device = SSHOpenWrt(hostname="192.168.1.1", password="test")

    if device.ping():
        device.log("reachable")
    else:
        device.log("not reachable")

    if device.portscan(22):
        device.log("SSH running")
    else:
        device.log("SSH not running")

    stdout, stderr = device.execute("echo Hello World")
    if (stdout) > 0:
        device.log("Command execution working")
    else:
        device.log("Command execution not working")

#    print "Device %s: Network device list: %s" % (device.hostname,
#                                                  device.network_interfaces())
#
#    for interface in device.network_interfaces():
#        if device.network_interface_state(interface):
#            print "Device %s: %s up" % (device.hostname, interface)
#        else:
#            print "Device %s: %s down" % (device.hostname, interface)
