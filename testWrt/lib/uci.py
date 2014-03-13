""" uci parsing """

import logging
import re

class UciError(RuntimeError):
    pass

class UciWrongTypeError(UciError):
    pass

class UciNotFoundError(UciError):
    pass

class UciParseError(UciError):
    pass

class Config(object):
    def __init__(self, uci_type, name=None):
        self.uci_type = uci_type
        self.name = name
        # options are key -> str(value)
        # lists are key -> [value x, value y]
        self.keys = {}

    def add_list(self, key, value):
        if key in self.keys:
            self.keys[key].append(value)
        else:
            self.keys[key] = [value]

    def remove_list_pos(self, key, pos):
        try:
            if not isinstance(self.keys[key], list):
                raise UciWrongTypeError
            del self.keys[key][pos]
        except(ValueError, KeyError):
            return

    def remove_list_value(self, key, value):
        try:
            self.keys[key].remove(value)
        except(ValueError, KeyError):
            return

    def set_option(self, key, value):
        if key in self.keys:
            if isinstance(self.keys[key], list):
                raise UciWrongTypeError()
        self.keys[key] = value

    def remove_option(self, key):
        if key in self.keys:
            del self.keys[key]

    def export(self):
        export = []
        if self.name:
            export.append("config '%s' '%s'\n" % (self.uci_type, self.name))
        else:
            export.append("config '%s'\n" % (self.uci_type))
        for opt_list in self.keys:
            if isinstance(self.keys[opt_list], list):
                export.extend([("\tlist '%s' '%s'\n" % (opt_list, element)) for element in self.keys[opt_list]])
            else:
                export.append("\toption '%s' '%s'\n" % (opt_list, self.keys[opt_list]))
        export.append('\n')
        return ''.join(export)

    def __repr__(self):
        return "Config[%s:%s] %s" % (self.uci_type, self.name, repr(self.keys))

class Package(list):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def add_config(self, config):
        self.append(config)

class Uci(object):
    logger = logging.getLogger('uci')
    def __init__(self):
        self.packages = {}

    def add_package(self, package_name):
        if package_name not in self.packages:
            self.packages[package_name] = Package(package_name)
        return self.packages[package_name]

    def add_config(self, package_name, config):
        if not isinstance(config, Config):
            return RuntimeError()
        if package_name not in self.packages:
            self.packages[package_name] = Package()
        self.packages[package_name].append(config)

    def del_config(self, config):
        pass

    def del_path(self, path):
        pass

    def export_tree(self):
        export = []
        for package, content in self.packages.items():
            export.append("package '%s'\n" % package)
            export.append("\n")
            export.extend([config.export() for config in content])
        return "".join(export)

    def test_split_into_parts(self):
        for single_foo in ["foo", '"foo"', "'foo'"]:
            assert self.split_into_parts(single_foo) == ['foo']

        for double_foo in ['foo foo', "foo 'foo'", 'foo "foo"', '"foo" \'foo\'']:
            assert self.split_into_parts(double_foo) == ["foo", "foo"]

    def split_into_parts(self, line):
        """
        split line into a list of strings
        e.g.
            line = "config 'fooo' 'fooo' "
            will be splitted into ['config', 'fooo', 'fooo']

            split_into_parts('goo "foo') => raise Exception
        """

        orig_line = line

        # all regex have 2 groups '()()'
        # the first group is our token, the second the rest of the string(likely without whitespaces or tabs)
        # "config foo bar" -> groups() = ('config', 'foo bar')
        reg_without = re.compile(r"^([^'\"][^ \t]*)[ \t]*(.*)$")
        reg_single = re.compile(r"^'([^']*)'[ \t]*(.*)$")
        reg_double = re.compile(r'^"([^"]*)"[ \t]*(.*)$')

        splitted = []

        # a line can only be matched by one reg not two or more.
        while len(line):
            matches = [reg.match(line) for reg in [reg_single, reg_double, reg_without] if reg.match(line)]

            if len(matches) == 0:
                self.logger.info("Can not parse complete Line:%s" % orig_line)
                self.logger.info("Unparsable Parts:%s" % line)
                return splitted
            else:
                splitted.append(matches[0].groups()[0])
                line = matches[0].groups()[1]

        return splitted

    def load_tree(self, export_tree):
        package = None
        config = None

        reg_strip_white = re.compile(r"[ \t]*([^ \t].*)$")

        for line in export_tree.splitlines():
            match = reg_strip_white.match(line)
            if match:
                line = match.groups()[0]

            tokens = self.split_into_parts(line)
            if not tokens:
                continue

            if line.startswith('config'):
                if tokens[0] == 'config':
                    if len(tokens) == 2:
                        if package is None:
                            self.logger.info("Ignoring config %s" % (tokens[1]))
                        else:
                            config = Config(tokens[1])
                            package.add_config(config)
                        continue

                    elif len(tokens) == 3:
                        if package is None:
                            self.logger.info("Ignoring config %s %s" % (tokens[1], tokens[2]))
                        else:
                            config = Config(tokens[1], tokens[2])
                            package.add_config(config)
                        continue

            elif line.startswith('package'):
                if len(tokens) == 2 and tokens[0] == 'package':
                    package = self.add_package(tokens[1])
                    continue

            elif line.startswith('option'):
                if len(tokens) == 3 and tokens[0] == 'option':
                    if config is None:
                        self.logger.info("Ignoring option - no config %s %s" % (tokens[1], tokens[2]))
                    else:
                        config.set_option(tokens[1], tokens[2])
                    continue

            elif line.startswith('list'):
                if len(tokens) == 3 and tokens[0] == 'list':
                    if config is None:
                        self.logger.info("Ignoring option - no config %s %s" % (tokens[1], tokens[2]))
                    else:
                        config.add_list(tokens[1], tokens[2])
                    continue

            self.logger.warn("Can not parse foo '%s' %s" % (line, tokens))
            # error


class UciConfig(object):
    """ Class for configurations - like network... """
    pass

if __name__ == '__main__':
    uci_export = open('uci_export')
    alles = uci_export.read(1000000)
    logging.basicConfig()
    ucilog = logging.getLogger('uci')
    ucilog.setLevel(logging.DEBUG)
    uci = Uci()
    uci.load_tree(alles)
    print(uci.export_tree())
