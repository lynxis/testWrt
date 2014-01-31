import json
import re


class OpenWrtUbus(object):

    def ubus_call(self, namespace, method):
        out = self.ubus_cmd("call %s %s" % (namespace, method))
        return json.loads(''.join(out))

    def ubus_cmd(self, command):
        stdout, stderr = self.execute("ubus %s" % command)
        return stdout

    def ubus_list(self, command):
        """
        Trying to parse the ubus list command to get
        some idea about callable methods and their params
        """
        try:
            ptrn = re.compile("'(.*)' (@.*)")
            ptrn2 = re.compile("\t\"(.*)\": { (.*) }")
            namespaces = self.ubus_cmd("list -v")
            for ns in namespaces:
                m = ptrn.match(ns)
                m2 = ptrn2.match(ns)
                if m:
                    print "Namespace: %s" % m.group(1)
                else:
                    if m2:
                        param = [x.strip('"') for x in m2.group(2).split(",")]
                        print "Method: %s(%s)" % (m2.group(1), param)
                    else:
                        print "Unknown: %s" % ns
        except Exception, err:
            print "Error %s" % err
