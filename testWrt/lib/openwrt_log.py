from pprint import pformat
import re


class OpenWrtLog(object):

    def log_array(self, caller, array):
        for line in array:
            self.log("%s: %s" % (caller, line.strip('\n')))

    def log_file(self, filename):
        self.log_array(filename, self.cat(filename))

    def log_json(self, caller, json):
        out = re.sub(r'u\'([^\']*)\'', r' "\1"', pformat(json)).split('\n')
        self.log_array(caller, out)

    def log(self, msg):
        if self._hostname is None:
            self._hostname = self.hostname()
        print "[%s] %s" % (self._hostname, msg)
