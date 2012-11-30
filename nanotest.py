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

    def _subresult(self, xpmtl, given, reason):
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
        res["comp"].append(self._subresult(xpmtl, given, reason))
        return res

    def test(self, xpmtl, given, msg, invert=False):
        if type(xpmtl) != type(given):
            res = self._result(False, type(given), type(xpmtl), msg, "Types don't match")
            self.results.append(res)
        elif isinstance(xpmtl, (tuple, list, dict)):
            self._hash_n_comp(xpmtl, given, msg, invert)
        else:
            passed, reason = self._test_scalar(xpmtl, given, msg, invert)
            self.results.append(self._result(passed, given, xpmtl, msg, reason))
                

    def untest(self, xpmtl, given, msg):
        self.test(xpmtl, given, msg, invert=True)

    def _test_scalar(self, xpmtl, given, msg, invert):
        if self.re_re.match(str(given)):
            return self._re_match(xpmtl, given, msg, invert)
        else:
            return self._is_eq(xpmtl, given, msg, invert)

    def _is_eq(self, xpmtl, given, msg, invert):
        if (xpmtl == given and invert == False) or (xpmtl != given and invert == True):
            return True, None
        else:
            return False, None

    def _re_match(self, xpmtl, given, msg, invert):
        restr = given[4:]
        if re.search(restr, str(xpmtl)):
            return True, None
        else:
            if invert:
                return True, None
            else:
                return False, "regexp failure ('got' is not a match for 'expected')"


    def _hash_n_comp(self, xpmtl, given, msg, invert):
        self.nodestack = []
        self.xhash = {}
        self._hash(xpmtl, self.xhash)
        self.nodestack = []
        self.ghash = {}
        self._hash(given, self.ghash)
        self._compare(msg, invert)

    def _hash(self, element, hashdict):
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
                self.results.append(self._result(False, None, None, msg, "structs were identical"))
            self.results.append(self._result(True, None, None, msg, None))
            return
        
        failed = False        
        for key in sorted(self.xhash.keys()):
            if key not in self.ghash:
                result = "node {} (value '{}') only in exp. struct".format(key, self.xhash[key])
                if failed:
                    self.results[-1]["comp"].append(self._subresult(None, None, result))
                else:
                    failed = True
                    self.results.append(self._result(False, None, None, msg, result))
            else:
                passed, reason = self._test_scalar(self.ghash[key], self.xhash[key], None, False)
                if not passed:
                    result= "node {} values don't match".format(key)
                    if failed:
                        self.results[-1]["comp"].append(self._subresult(self.ghash[key], self.xhash[key], result))
                    else:
                        failed = True
                        self.results.append(self._result(False, self.ghash[key], self.xhash[key], msg, result))
        for key in sorted(self.ghash.keys()):
            if key not in self.xhash:
                result = "node {} (value '{}') only in given struct".format(key, self.ghash[key])
                if failed:
                    self.results[-1]["comp"].append(self._subresult(None, None, result))
                else:
                    failed = True
                    self.results.append(self._result(False, None, None, msg, result))
        if not failed:
            self.results.append(self._result(True, None, None, msg, None))

    def _inv_compare(self, a, b):
        for key in sorted(a.keys()):
            if key not in b:
                return True
            else:
                passed, reason = self._test_scalar(a[key], b[key], None, False)
                if not passed: return True
        return False
