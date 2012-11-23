import inspect
import re

version = "v2.0.0"

class Nanotester:
    """
    """
    def __init__(self):
        self.results = []
        self.re_re   = re.compile("\:re\:")

    def _result(self, success, given, xpmtl, msg, *args):
        res = {}
        if len(args) > 0:
            res['reason'] = args[0]
        else:
            res['reason'] = None
        # get filename, line num, stuff
        frame = inspect.getouterframes(inspect.currentframe())[3]
        #for f in frame: print(f)
        # frame, filename, linenum, function_name, lines, index
        res['file']  = frame[1]
        res['line']  = frame[2]
        res['pass']  = success
        res['xpect'] = given
        res['got']   = xpmtl
        res['msg']   = msg
        return res

    def test(self, xpmtl, given, msg):
        if type(xpmtl) != type(given):
            res = self._result(False, type(given), type(xpmtl), msg, "Types don't match")
            self.results.append(res)
        elif isinstance(xpmtl, (tuple, list, dict)):
            # build hashes, etc
            pass
        elif self.re_re.match(str(given)):
            # call _re_match
            pass
        else:
            self._is_eq(xpmtl, given, msg)

    def _is_eq(self, xpmtl, given, msg):
        if xpmtl == given:
            self.results.append(self._result(True, None, None, None, None))
        else:
            self.results.append(self._result(False, given, xpmtl, msg, None))

    def _re_match(self, xpmtl, given):
        if re.search(kw['given'][4:], str(kw['xpmtl'])):
            return True
        else:
            _set_err(reason="renomatch", errkey=key)
            return False

    def _compare(self, xpmtl, given):
        # build dict of hashed xpmtl structure.
        self.xhash = self._hash(xpmtl)
        # run hash function over given structure, in verify mode
        self.ghash = self._hash(given)
        # iterate over xpmtl dict for elements whose seen flag is not
        # set. fail if we find one.
        for k, v in nanoconf['deephash'].items():
            if v[1] == False:
                _set_err(reason="nomatchingiven", errkey=k)
                _print_deep_fail_msg(msg, None, None)
                return False
        return True

    def _hash(self, element):
        nodestack = []
        if isinstance(element, (tuple, list, dict)):
            # composites are handled here
            if isinstance(element, (dict,)):
                # dict
                nodestack.append('dict')
                for key in sorted(element.keys()):
                    nodestack.append(str(key))
                    _deep_build_hash(element[key], verify, msg)
                    nodestack.pop()
            else:
                if isinstance(element, (list,)):
                    nodestack.append('list')
                else:
                    nodestack.append('tuple')
                for idx, subelem in enumerate(element):
                    nodestack.append(str(idx))
                    _deep_build_hash(subelem, verify, msg)
                    nodestack.pop()
            nodestack.pop()
        else:
            # leafnodes handled here
            key = ".".join(nodestack)
