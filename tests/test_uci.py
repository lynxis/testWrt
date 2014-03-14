
from config import TestSetup
import logging

LOG = logging.getLogger("test")

class TestOpenWrt(object):
    """ These tests just test uci cli and without our uci module """
    def __init__(self):
        self.owrt = TestSetup.openwrt

    def test_uci_import(self):
        stdin, stdout, stderr = self.owrt.execute("uci import tests")

        stdin.write("config tsss\n")
        stdin.write("    option foo bar\n")
        # shutdown in and output of stdin to send an EOF
        stdin.channel.shutdown(2)
        outlines = stdout.readlines()
        errlines = stderr.readlines()
        LOG.debug("StdErr lines")
        LOG.debug(errlines)
        LOG.debug("StdOut lines")
        LOG.debug(outlines)
        assert len(errlines) == 0
        assert len(outlines) == 0

    def test_uci_export(self):
        stdin, stdout, stderr = self.owrt.execute("uci export tests")
        outlines = stdout.readlines()
        errlines = stderr.readlines()
        LOG.debug("StdErr lines")
        LOG.debug(errlines)
        LOG.debug("StdOut lines")
        LOG.debug(outlines)
        assert outlines[0] == "package tests\n"
        assert outlines[2] == "config tsss\n"
        assert outlines[3] == "\toption foo 'bar'\n"
        assert len(errlines) == 0

