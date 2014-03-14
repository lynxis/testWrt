import os
from subprocess import call  # ping()
import socket  # portscan()

from .uci import Uci

SOCKET_TIMEOUT = 10

class OpenWrtBase(object):

    """ generic openwrt model """

    def __init__(self, platform="generic", device="generic", rootfs=""):
        """ e.g. platform = "ar71xx"
                 device = "tl-wdr-4300"
                 rootfs = "squashfs"
        """
        self.platform = platform
        self.device = device
        self.rootfs = rootfs

    def execute(self, callstr):
        """ call @arg callstr. return a list of [stdin, stdout, stderr] """
        raise NotImplementedError()

    def execute_one_shot(self, callstr):
        """ call @arg callstr. return a list of [stdout, stderr] """
        raise NotImplementedError()

    def basename(self, path):
        stdout, stderr = self.execute("basename %s" % path)
        return stdout[0].strip()

    def cat(self, filename):
        """ 
        return @arg filename as array of lines
        """
        stdout, stderr = self.execute_one_shot("cat %s" % filename)
        return stdout

    def find(self, path):
        stdout, stderr = self.execute("find %s" % path)
        return stdout

    def hostname(self):
        """
        return devices hostname
        """
        return self.cat("/proc/sys/kernel/hostname")[0].strip()

    def dmesg(self):
        stdout, stderr = self.execute("dmesg")
        return stdout

    def logread(self, *args):
        stdout, stderr = self.execute("logread %s" % ' '.join(args))
        return stdout

    def ls(self, path):
        stdout, stderr = self.execute("ls %s" % path)
        return stdout

    def ping(self, count=1, wait=2):
        fh = open(os.devnull, "w")  # output catcher
        ret = call(["ping", "-c%s" % count, "-w%s" %
                   wait, self.ip], stdout=fh, stderr=fh)
        if ret == 0:
            return True
        else:
            return False

    def portscan(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SOCKET_TIMEOUT)
            result = sock.connect_ex((self.ip, port))
            if result == 0:
                ret = True
            else:
                ret = False
        except:
            ret = False
        sock.close()
        return ret

    def uci_load(self, ucistr):
        """ load a uci config same a `cat | uci import` """
        self.execute("echo " + ucistr + " | uci import ")

    def uci_merge(self, uci):
        """ merge uci into system configuration """
        if not isinstance(uci, Uci):
            raise RuntimeError("Uci is not an instance of Uci - use new module uci")
        # -m means merge
        for package, content in uci.packages.items():
            stdin, stdout, stderr = self.execute("uci -m import %s" % package)
        stdin.write("".join([config.export() for config in content]))
        stdin.channel.shutdown(2)

    def uci(self, param):
        """ set / get add list - see `uci --help` for param.
            e.g. uci("set wireless.radio0.channel=1")
        """
        # TODO: replace this with library calls?
        # TODO: replace this with ubus calls?
        return self.execute("uci " + param)
