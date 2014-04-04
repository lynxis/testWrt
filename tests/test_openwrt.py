
from config import TestSetup
from testWrt.lib import SSHOpenWrt
from testWrt.lib.uci import Uci, Config

from nose.tools import eq_

class TestOpenWrt(object):
    def __init__(self):
        # Todo how to change test method? via Config?
        self.owrt = TestSetup.openwrt

    def test_echo(self):
        stdout, stderr = TestSetup.openwrt.execute_one_shot("echo hello openwrt")
        eq_(stdout[0], "hello openwrt")

    def test_change_hostname(self):
        old = self.owrt.hostname()
        changeto = old + "testing"
        new = ""

        uci = Uci()
        uci.add_package("system")
        config = Config("system")
        config.set_option("hostname", changeto)
        uci.add_config("system", config)
        self.owrt.uci_merge(uci)

        self.owrt.execute_one_shot("/etc/init.d/system reload")
        new = self.owrt.hostname()
        self.owrt.uci("revert system")
        self.owrt.execute_one_shot("/etc/init.d/system reload")
        eq_(new, changeto)
