
from config import TestSetup
import logging

from testWrt.lib.testing import assert_stdoutlines, assert_stderrlines

LOG = logging.getLogger("test")

class TestOpenWrt(object):
    """ These tests just test uci cli and without our uci module """
    def __init__(self):
        self.owrt = TestSetup.openwrt

    def test_uci_import(self):
        streams = self.owrt.execute("uci import tests")

        streams[0].write("config testconfig\n")
        streams[0].write("    option testoption testvalue\n")
        # shutdown in and output of stdin to send an EOF
        streams[0].channel.shutdown(2)
        assert_stderrlines(streams)
        assert_stdoutlines(streams)

    def test_uci_export(self):
        stdin, stdout, stderr = self.owrt.execute("uci export tests")
        outlines = stdout.readlines()
        errlines = stderr.readlines()
        LOG.debug("StdErr lines")
        LOG.debug(errlines)
        LOG.debug("StdOut lines")
        LOG.debug(outlines)
        assert outlines[0] == "package tests\n"
        assert outlines[2] == "config testconfig\n"
        assert outlines[3] == "\toption testoption 'testvalue'\n"
        assert len(errlines) == 0

    def test_uci_add(self):
        streams = self.owrt.execute_one_shot('uci add tests uciadd')
        assert_stderrlines(streams)

    def test_uci_set(self):
        streams = self.owrt.execute_one_shot('uci set tests.@uciadd[-1].testoption=foo')
        assert_stderrlines(streams)

    def test_uci_get(self):
        streams = self.owrt.execute_one_shot('uci get tests.@uciadd[-1]')
        assert_stderrlines(streams)
