#!/usr/bin/env python

from .wifinodes import *

class TestSetup(object):
    def __init__(self):
        # type: []
        self._devices = {}

    def addDevice(self, device):
        if device.name in self._devices:
            self._devices[device.name].append(device)
        else:
            self._devices[device.name] = [device]

def create_generic():
    tsetup = TestSetup()
    return tsetup
