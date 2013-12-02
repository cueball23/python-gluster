import os
import sys

from . import peer
from . import volume 

class GlusterError(Exception):
    def __init__(self,value):
        self.value = value
    def _str_(self):
        return repr(self.value)

class GlusterWarning(Warning):
    def __init__(self,value):
        self.value = value
    def _str_(self):
        return repr(self.value)

if not os.geteuid()==0:
    raise GlusterError("Gluster commands require root permissions.")
