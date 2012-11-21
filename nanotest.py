import re

class Nanotester:
    """
    """
    def __init__(self):
        self.tests_total = 0
        self.tests_pass  = 0
        self.re_re   = re.compile("\:re\:")

    def test(self, xpmtl, given):
        # all we do here is parcel out work to the appropriate helper
        # function and note the results
        if self.re_re.match(str(given)):
            # call _re_match
            pass

    def _is_eq(self, xpmtl, given):
        if xpmtl == given:
            return True
        return False

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
