"""
This is the sample config.py

create your own config.py which match your testsetup
It will be imported by device tests
"""

from testWrt import testsetup

TestSetup = testsetup.TestSetup()
TestSetup.set_openwrt("192.168.2.1")
