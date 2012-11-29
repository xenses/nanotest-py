import inspect
import re

version = "v2.0.0"

class Nanotester:
    """
    """
    def __init__(self):
        self.results   = []
        self.nodestack = []
        self.xhash = {}
        self.ghash = {}
        self.re_re   = re.compile("\:re\:")
        self.re_type = re.compile("\:ty\:")

    def _subresult(self, given, xpmtl, reason):
        sres = {}
        sres["xpect"]  = given
        sres["got"]    = xpmtl
        sres["reason"] = reason
        return sres

    def _result(self, success, given, xpmtl, msg, *args):
        res = {}
        reason = None
        if len(args) > 0:
            reason = args[0]
        # get filename, line num, stuff. should always want the -2nd
        # frame in the stack, since -1 is the exec(). this may need to
        # be cased when test injection is implemented
        frame = inspect.getouterframes(inspect.currentframe())[-2]
        # frame, filename, linenum, function_name, lines, index
        res["file"]  = frame[1]
        res["line"]  = frame[2]
        res["pass"]  = success
        res["msg"]  = msg
        res["comp"] = []
        res["comp"].append(self._subresult(given, xpmtl, reason))
        return res

    def test(self, xpmtl, given, msg, invert=False):
        if type(xpmtl) != type(given):
            res = self._result(False, type(given), type(xpmtl), msg, "Types don't match")
            self.results.append(res)
        elif isinstance(xpmtl, (tuple, list, dict)):
            self._hash_n_comp(xpmtl, given, msg, invert)
        else:
            self._test_scalar(xpmtl, given, msg, invert)

    def untest(self, xpmtl, given, msg):
        self.test(xpmtl, given, msg, invert=True)

    def _test_scalar(self, xpmtl, given, msg, invert):
        if self.re_re.match(str(given)):
            self._re_match(xpmtl, given, msg, invert)
        else:
            self._is_eq(xpmtl, given, msg, invert)

    def _is_eq(self, xpmtl, given, msg, invert):
        if (xpmtl == given and invert == False) or (xpmtl != given and invert == True):
            self.results.append(self._result(True, given, xpmtl, msg, None))
        else:
            self.results.append(self._result(False, given, xpmtl, msg, None))

    def _re_match(self, xpmtl, given, msg, invert):
        restr = given[4:]
        if re.search(restr, str(xpmtl)):
            self.results.append(self._result(True, restr, xpmtl, msg, None))
        else:
            if invert:
                self.results.append(self._result(True, restr, xpmtl, msg, None))
            else:
                self.results.append(self._result(False, restr, xpmtl, msg,
                                                 "regexp failure ('got' is not a match for 'expected')"))


    def _hash_n_comp(self, xpmtl, given, msg, invert):
        self.xhash = {}
        self._hash(given, self.xhash)
        self.ghash = {}
        self._hash(given, self.ghash)
        self._compare(msg, invert)

    def _hash(self, element, hashdict):
        self.nodestack = []
        if isinstance(element, (tuple, list, dict)):
            # composites are handled here
            if isinstance(element, (dict,)):
                self.nodestack.append('d')
                for key in sorted(element.keys(), key=lambda key: str(key)):
                    self.nodestack.append(str(key))
                    self._hash(element[key], hashdict)
                    self.nodestack.pop()
            else:
                if isinstance(element, (list,)):
                    self.nodestack.append('l')
                else:
                    self.nodestack.append('t')
                for idx, subelem in enumerate(element):
                    self.nodestack.append(str(idx))
                    self._hash(subelem, hashdict)
                    self.nodestack.pop()
            self.nodestack.pop()
        else:
            # leafnodes handled here
            key = ".".join(self.nodestack)
            hashdict[key] = element

    def _compare(self, msg, invert):
        if invert:
            mismatch = self._inv_compare(self.xhash, self.ghash)
            if not mismatch:
                mismatch = self._inv_compare(self.ghash, self.xhash)
            if not mismatch:
                self.nodestack.append(self._result(False, None, None, msg, "structs were identical"))
            self.nodestack.append(self._result(True, None, None, msg, None))
    #    for key in sorted(self.xhash.keys()):
    #        if key not in self.ghash:
                
    def _inv_compare(self, a, b):
        for key in sorted(a.keys()):
            if key not in b:
                return True
            else:
                self._test_scalar(a[key], b[key], "", False)
                if not self.results[-1]["pass"]:
                    self.results.pop()
                    return True
                self.results.pop()
        return False
