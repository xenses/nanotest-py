import nanotest.core as nc
import nanotest.api as na

class Nanotester:
    """Initialize a nanotest tester object."""
    def __init__(self):
        self.version   = "2.1.0"
        self.results   = [] # test results go here
        self.nodestack = [] # used to build hash for struct compares
        self.xhash = {}     # experimental struct hash
        self.ghash = {}     # given struct hash

    def test(self, xpmtl, given, msg, invert=False):
        """Test two values for equality"""
        if type(xpmtl) != type(given):
            res = nc.result(False, type(given), type(xpmtl), msg, "Types don't match")
            self.results.append(res)
        elif isinstance(xpmtl, (tuple, list, dict)):
            nc.deepcomp(self, xpmtl, given, msg, invert)
        else:
            passed, reason = nc.comp(self, xpmtl, given, msg, invert)
            self.results.append(nc.result(passed, given, xpmtl, msg, reason))
                
    def untest(self, xpmtl, given, msg):
        """Test two values for inequality"""
        self.test(xpmtl, given, msg, invert=True)

    def source_api(self, filename):
        """Source API tests from a given file"""
        pass

    def atest(self, xpmtl):
        """Do an API test for equality"""
        pass

    def auntest(self, xpmtl):
        """Do an API test for inequality"""
        pass
