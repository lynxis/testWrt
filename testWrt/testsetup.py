#!/usr/bin/env python

import logging

from testWrt.lib import OpenWrtBase

LOG = logging.getLogger('testWrt')

class TestSetup(object):
    def __init__(self):
        # type: []
        self._devices = {}
        self._openwrt = None

    def add_device(self, device):
        if device.name in self._devices:
            self._devices[device.name].append(device)
        else:
            self._devices[device.name] = [device]

    def set_openwrt(self, openwrt):
        """ set your main test subject """
        if not isinstance(openwrt, OpenWrtBase):
            raise RuntimeError("Wrong type! Need an OpenWrtBase object)")
        if self._openwrt:
            LOG.warn("Already set an openwrt device")
        self._openwrt = openwrt

    @property
    def openwrt(self):
        """
        return an OpenWrt object (derived from OpenWrtBase)

        @rtype OpenWrtBase
        """
        return self._openwrt

def create_generic():
    tsetup = TestSetup()
    return tsetup
