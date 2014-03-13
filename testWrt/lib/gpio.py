GPIO_PATH = "/sys/class/gpio/"


class OpenWrtGpio(object):

    def gpio_count(self):
        GPIOCHIP_WILDCARD = "%s/gpiochip* -d" % GPIO_PATH
        ret = {}

        gpio_chips = self.ls(GPIOCHIP_WILDCARD)

        for chip in gpio_chips:
            ret[self.basename(chip)] = int(self.cat("%s/ngpio" % chip)[0])

        return ret

    def _gpio_exists(self, gpio):
        gpio_path = "%s/gpio%i" % (GPIO_PATH, gpio)
        if len(self.ls("%s -d" % gpio_path)) == 0:
            return False
        else:
            return True

    def gpio_export(self, gpio):
        if self._gpio_exists(gpio):
            return True
        self.execute("echo %s > %s/export" % (gpio, GPIO_PATH))
        return False

    def gpio_unexport(self, gpio):
        return self.execute("echo %s > %s/unexport" % (gpio, GPIO_PATH))

    def _gpio_value(self, gpio_path, value):
        output = self.cat("%s/%s" % (gpio_path, value))
        if len(output) > 0:
            return output[0]
        return "Unknown"

    def gpio_inspect(self, gpio):
        ret = {}

        gpio_path = "%s/gpio%i" % (GPIO_PATH, gpio)

        ret["exists"] = self._gpio_exists(gpio)
        ret["active_low"] = self._gpio_value(gpio_path, "active_low")
        ret["direction"] = self._gpio_value(gpio_path, "direction")
        ret["value"] = self._gpio_value(gpio_path, "value")
        return ret

    def gpio_inspect_all(self):
        """
        returns the state of all gpios 
        """
        ret = {}
        for chip, ngpio in self.gpio_count().iteritems():
            ret[chip] = {}
            for gpio in xrange(0, int(ngpio)):
                exported_before = self.gpio_export(gpio)
                ret[chip]["gpio%i" % gpio] = self.gpio_inspect(gpio)
                if not exported_before:
                    self.gpio_unexport(gpio)
        return ret
