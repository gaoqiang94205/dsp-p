import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

class mount_dic():
    def __init__(self,source,target,type):
        self.source = source
        self.target = target
        self.type = type
d = '{"source":"aa","target":"cc","type":"vv"}'
m = json.loads(d)
print m
mount = mount_dic(**m)
print mount.source
