#!/usr/bin/env python

class OpenWrt(object):
    def __init__(self, platform="generic", device="generic", rootfs=""):
        """ e.g. platform = "ar71xx"
                 device = "tl-wdr-4300"
                 rootfs = "squashfs"
        """
        self.platform = platform
        self.device = device
        self.rootfs = rootfs

    def exec(self, callstr):
        """ call @arg callstr. return a list of [stdout, stderr] """
        raise NotImplementedError

    def uci_load(self, ucistr):
        """ load a uci config same a `cat | uci import` """
        self.exec("echo " + ucistr + " | uci import -")

    def uci(self, param):
        """ set / get add list - see `uci --help` for param.
            e.g. uci("set wireless.radio0.channel=1")
        """
        # TODO: replace this with library calls?
        self.exec(self, "uci " + param)

class SSHOpenWrt(OpenWrt):
    def __init__(self, address=None, **kwargs):
        super().__init__(**kwargs)
        if not address:
            raise RuntimeError("No address given")
        self._ssh = ConnectPySSH

    def exec(self, callstr):
        self._ssh.exec(callstr)

class RPCDOpenWrt(OpenWrt):
    """ Connect over rpc to openWrt device """
    def __init__(self, url, token):
        raise NotImplementedError

def init_openWrt_with_sshd(address=None):
    # must work with default + rescue openWrt
    if not address:
        raise RuntimeError("No address give")
    # connect
    # check for a prompt
    # passwd foo
    # start dropbear? or use a library and create a TelnetOpenWrt class
