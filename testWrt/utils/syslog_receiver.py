import time
import socketserver
from queue import Queue
from _thread import start_new_thread


class SyslogServer():

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.data = Queue()

    def spawn(self):
        self.syslog_instance = start_new_thread(self.start, (self,))

    def read(self):
        return self.data.get()


    def start(self, *arg):
        try:
            server = socketserver.UDPServer(
                (self.hostname, self.port), self.handler())
            server.serve_forever(poll_interval=0.5)
        except (IOError, SystemExit):
            raise

    def handler(self):
        parent = self

        class SyslogHandler(socketserver.BaseRequestHandler):

            def handle(self):
                data = bytes.decode(self.request[0].strip())
                parent.data.put(str(data))
        return SyslogHandler
