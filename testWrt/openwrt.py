#!/usr/bin/env python

import json
import paramiko
import re
import socket

from pprint import pformat
from paramiko.util import retry_on_signal
from subprocess import call


SOCKET_TIMEOUT = 10


class OpenWrt(object):

    def __init__(self, platform="generic", device="generic", rootfs=""):
        """ e.g. platform = "ar71xx"
                 device = "tl-wdr-4300"
                 rootfs = "squashfs"
        """
        self.platform = platform
        self.device = device
        self.rootfs = rootfs

    def execute(self, callstr):
        """ call @arg callstr. return a list of [stdout, stderr] """
        raise NotImplementedError()

    def uci_load(self, ucistr):
        """ load a uci config same a `cat | uci import` """
        self.execute("echo " + ucistr + " | uci import -")

    def uci(self, param):
        """ set / get add list - see `uci --help` for param.
            e.g. uci("set wireless.radio0.channel=1")
        """
        # TODO: replace this with library calls?
        self.execute(self, "uci " + param)


class SSHOpenWrt(OpenWrt):

    def __init__(self, hostname="192.168.1.1", password=None,
                 keyfile=None, port=22, user="root", **kwargs):
        super(SSHOpenWrt, self).__init__(**kwargs)

        self.ip = hostname
        self.hostname = hostname
        self.port = port
        self.keyfile = keyfile
        self.user = user
        self.password = password

        self._ssh = paramiko.SSHClient()
        self.connect()

    def cat(self, filename):
        return self.execute("cat %s" % filename)

    def log_file(self, filename):
        self.log_array(filename, self.cat(filename))

    def log_ubus_call(self, namespace, method):
        return self.log_json("ubus/%s/%s" % (namespace, method),
                             self.ubus_call(namespace, method))

    def ubus_call(self, namespace, method):
        out = self.ubus_cmd("call %s %s" % (namespace, method))
        return json.loads(''.join(out))

    def ubus_cmd(self, command):
        return self.execute("ubus %s" % command)

    def log_array(self, caller, array):
        for line in array:
            self.log("%s: %s" % (caller, line.strip('\n')))

    def log_json(self, caller, json):
        out = re.sub(r'u\'([^\']*)\'', r' "\1"', pformat(json)).split('\n')
        self.log_array(caller, out)

    def device_hostname(self):
        return self.cat("/proc/sys/kernel/hostname")[0].strip()

    def _ssh_socket(self, interface=None):
        for (family, stype, _, _, sockaddr) in socket.getaddrinfo(
                self.hostname, self.port, socket.AF_UNSPEC,
                socket.SOCK_STREAM):
            if stype == socket.SOCK_STREAM:
                af = family
                addr = sockaddr
                break
        else:
            af, _, _, _, addr = socket.getaddrinfo(
                self.hostname, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        sock = socket.socket(af, socket.SOCK_STREAM)
        if interface is not None:
            sock.setsockopt(socket.SOL_SOCKET, 25, interface + '\0')
        sock.settimeout(SOCKET_TIMEOUT)
        retry_on_signal(lambda: sock.connect(addr))
        return sock

    def connect(self):
        private_key = None
        if self.keyfile is not None:
            private_key = paramiko.RSAKey.from_private_key_file(self.keyfile)
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ret = self._ssh.connect(self.hostname, username=self.user,
                                password=self.password, pkey=private_key,
                                allow_agent=True, sock=None)
        self._ssh.load_system_host_keys()
        return ret

    def portscan(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SOCKET_TIMEOUT)
            result = sock.connect_ex((self.hostname, port))
            if result == 0:
                ret = True
            else:
                ret = False
        except:
            ret = False
        sock.close()
        return ret

    def ping(self, count=1, wait=2):
        fh = open("NUL", "w")  # output catcher
        ret = call(["ping", "-c%s" % count, "-w%s" %
                   wait, self.ip], stdout=fh, stderr=fh)
        if ret == 0:
            return True
        else:
            return False

    def execute(self, command):
        stdin, stdout, stderr = self._ssh.exec_command(command)
        return stdout.readlines()

    def network_interfaces(self):
        try:
            # TODO: use ubus commands here
            devs = [x.strip() for x in self.execute("ls /sys/class/net/")]
        except:
            devs = ""
        return devs

    def network_interface_state(self, interface):
        try:
            # TODO: use ubus commands here
            ret = self.execute("cat /sys/class/net/%s/carrier" % interface)
            if "1" in ret[0]:
                return True
            return False
        except:
            return False

    def log(self, msg):
        print "[%s] %s" % (self.hostname, msg)

    def ubus(self, command):
        try:
            ptrn = re.compile("'(.*)' (@.*)")
            ptrn2 = re.compile("\t\"(.*)\": { (.*) }")
            namespaces = self.execute("ubus list -v")
            for ns in namespaces:
                m = ptrn.match(ns)
                m2 = ptrn2.match(ns)
                if m:
                    print "Namespace: %s" % m.group(1)
                else:
                    if m2:
                        param = [x.strip('"') for x in m2.group(2).split(",")]
                        print "Method: %s(%s)" % (m2.group(1), param)
                    else:
                        print "Unknown: %s" % ns
        except Exception, err:
            print "Error %s" % err


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
