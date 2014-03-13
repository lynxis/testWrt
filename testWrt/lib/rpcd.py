from .base import OpenWrtBase

class RPCDOpenWrt(OpenWrtBase):

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
