# testWrt
A testing framework to test openWrt release on specific hardware.

# license
AGPL v3.0

# pypkg
- pyssh

# requirements
- you need a configuratable switch
- a traffic generator
- a traffic receiver
- a wifi client
- a wifi accesspoint

shortcut here you need a manual tested openwrt release with a vlan-switch

# define a test:
vWAp  = VerifiedAP(essid="Bar", encryption="WPA2-PSK-AES", key="foofoo22")
vWCli = VerifiedWifiClient(essid="Foo", encryption="WPA2-PSK-AES", key="foofoo22")
tsetup.addDevice(vWAp)
tsetup.addDevice(vWCli)

