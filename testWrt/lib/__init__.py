from openwrt_base import OpenWrtBase
from openwrt_log import OpenWrtLog
from openwrt_ubus import OpenWrtUbus
from openwrt_gpio import OpenWrtGpio

import openwrt_base as openwrt_base

class base(OpenWrtBase):
    pass
base.__bases__ = (OpenWrtBase, OpenWrtLog, OpenWrtUbus, OpenWrtGpio)

openwrt_base.OpenWrtBase = base