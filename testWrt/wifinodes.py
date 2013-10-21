#!/usr/bin/env python

class VerifiedManagedWifi(object):
    def __init__(self, essid=None, encryption=None, key=None, channel=None, mac=None):
        self.essid = essid
        self.encryption = encryption
        self.key = key
        self.channel = channel

    @property
    def name(self):
        raise NotImplementedError

class VerifiedWifiClient(VerifiedManagedWifi):
    @property
    def name(self):
        return "VerifiedWifiClient"

class VerifiedAP(VerifiedManagedWifi):
    @property
    def name(self):
        return "VerifiedWifiClient"

