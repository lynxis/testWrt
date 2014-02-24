#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib import SSHOpenWrt, OpenWrtLog

SSHOpenWrt = type('Base', (SSHOpenWrt, OpenWrtLog), {})

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

    syslog = device.spawn_logserver("192.168.1.2", 5555)

    msg = "This IS a test"
    msg_seen = False

    while not msg_seen:
        device.execute("logger %s" % msg)
        if msg in syslog.read():
            msg_seen = True

    device.log("Message successfully received on %s:%s" %
               (syslog.hostname, syslog.port))
