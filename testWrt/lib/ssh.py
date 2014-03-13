
from .base import OpenWrtBase

import paramiko
from paramiko.util import retry_on_signal

import socket
SOCKET_TIMEOUT = 10


class SSHOpenWrt(OpenWrtBase):
    """
    Connects to the device using the paramiko ssh library
    """

    def __init__(self, hostname="192.168.1.1", password=None,
                 keyfile=None, port=22, user="root", **kwargs):
        """
        Initializes the OpenWrt Object and estasblishes a
        SSH Connection for command line execution
        """
        super(SSHOpenWrt, self).__init__(**kwargs)

        self.ip = hostname
        self.port = port
        self.keyfile = keyfile
        self.user = user
        self.password = password
        self._hostname = None
        self._ssh = paramiko.SSHClient()
        self.connect()

    def _ssh_socket(self, interface=None):
        """
        Returns a socket object for the ssh connection to the node.
        It is necessary for forcing paramiko to use a specific interface
        rather than just an ip address for binding the socket.
        """
        for (family, stype, _, _, sockaddr) in socket.getaddrinfo(
                self.ip, self.port, socket.AF_UNSPEC,
                socket.SOCK_STREAM):
            if stype == socket.SOCK_STREAM:
                af = family
                addr = sockaddr
                break
        else:
            af, _, _, _, addr = socket.getaddrinfo(
                self.ip, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        sock = socket.socket(af, socket.SOCK_STREAM)
        if interface is not None:
            sock.setsockopt(socket.SOL_SOCKET, 25, interface + '\0')
        sock.settimeout(SOCKET_TIMEOUT)
        retry_on_signal(lambda: sock.connect(addr))
        return sock

    def connect(self):
        """
        Establishes the paramiko connection using a keyfile or a
        username and password.
        """
        private_key = None
        if self.keyfile is not None:
            private_key = paramiko.RSAKey.from_private_key_file(self.keyfile)
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ret = self._ssh.connect(self.ip, username=self.user,
                                password=self.password, pkey=private_key,
                                allow_agent=True, look_for_keys=False, sock=None)
        self._ssh.load_system_host_keys()
        return ret

    def _strip_array(self, array):
        """
        Helper function to remove unwanted spaces and linefeeds
        """
        return [x.strip() for x in array]

    def execute_one_shot(self, command):
        """
        Implements the execute method over a SSH Connection
        Without any return value

        @param command with arguments
        @type str
        @rtype list
        """
        stdin, stdout, stderr = self._ssh.exec_command(command)
        stdin.close()
        return [self._strip_array(stdout.readlines()),
                self._strip_array(stderr.readlines())]

    def execute(self, command):
        """
        Implements the execute method over a SSH Connection
        """
        return self._ssh.exec_command(command)


    def execute_background(self, command):
        chan = self._ssh._transport.open_session()
        from thread import start_new_thread
        start_new_thread(chan.exec_command, (command,))
