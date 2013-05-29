import re

import nanotest.core as nc

class Nanotester:
    """Initialize a nanotest tester object."""
    def __init__(self):
        self.version   = "2.1.0"
        self.results   = [] # test results go here
        self.nodestack = [] # used to build hash for struct compares
        self.xhash = {}     # experimental struct hash
        self.ghash = {}     # given struct hash
        self.re_re   = re.compile("\:re\:")
        self.re_type = re.compile("\:ty\:")

    def test(self, xpmtl, given, msg, invert=False):
        """Test two values for equality"""
        if type(xpmtl) != type(given):
            res = nc.result(self, False, type(given), type(xpmtl), msg, "Types don't match")
            self.results.append(res)
        elif isinstance(xpmtl, (tuple, list, dict)):
            self.nc.deepcomp(xpmtl, given, msg, invert)
        else:
            passed, reason = nc.comp(self, xpmtl, given, msg, invert)
            self.results.append(nc.result(self, passed, given, xpmtl, msg, reason))
                
    def untest(self, xpmtl, given, msg):
        """Test two values for inequality"""
        self.test(xpmtl, given, msg, invert=True)
