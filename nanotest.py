import inspect
import re

version = "v2.0.0"

class Nanotester:
    """
    """
    def __init__(self):
        self.results   = []
        self.nodestack = []
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
            # build hashes, etc
            pass
        elif self.re_re.match(str(given)):
            self._re_match(xpmtl, given, msg, invert)
        else:
            self._is_eq(xpmtl, given, msg, invert)

    def untest(self, xpmtl, given, msg):
        self.test(xpmtl, given, msg, invert=True)
        
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


    def _compare(self, xpmtl, given):
        # build dict of hashed xpmtl structure.
        self.nodestack = []
        self.xhash = {}
        self._hash(given, self.xhash)
        # run hash function over given structure, in verify mode
        self.nodestack = []
        self.ghash = {}
        self._hash(given, self.ghash)
        # iterate over xpmtl dict for elements whose seen flag is not
        # set. fail if we find one.
        #for k, v in nanoconf['deephash'].items():
        #    if v[1] == False:
        #        _set_err(reason="nomatchingiven", errkey=k)
        #        _print_deep_fail_msg(msg, None, None)
        #        return False
        #return True

    def _hash(self, element, hashdict):
        if isinstance(element, (tuple, list, dict)):
            # composites are handled here
            if isinstance(element, (dict,)):
                # dict
                self.nodestack.append('d')
                for key in sorted(element.keys()):
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
            key = "".join(self.nodestack)
            hashdict[key] = element
