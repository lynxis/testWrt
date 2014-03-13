#!/usr/bin/env python

from testWrt import testsetup
from testWrt.lib import SSHOpenWrt

import unittest

class TestSSHOpenWrt(object):
    def test_connect(self):
        ts = testsetup.create_generic()
        device = SSHOpenWrt(hostname="192.168.1.1")
        stdout, stderr = device.execute_one_shot("echo hello openwrt")
        assert(stdout[0].strip() == "hello openwrt")
