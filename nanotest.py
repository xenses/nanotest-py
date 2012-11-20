import re

class Nanotester:
    """
    """
    def __init__(self):
        self.tests_total = 0
        self.tests_pass  = 0
        self.re_re   = re.compile("\:re\:")

    def test(self, xpmt, given):
        # all we do here is parcel out work to the appropriate helper
        # function and note the results
        if self.re_re.match(str(given)):
            # call _re_match
            pass

    def _is_eq(self, expr, given):
        if expr == given:
            return True
        return False

    def _re_match(key=None, **kw):
        if re.search(kw['given'][4:], str(kw['expr'])):
            return True
        else:
            _set_err(reason="renomatch", errkey=key)
            return False

    def _compare(expr, given, msg):
        # build dict of hashed expr structure.
        _deep_build_hash(expr, False, None)
        # run hash function over given structure, in verify mode
        _deep_build_hash(given, True, msg)
        if nanoconf['error']:
            return False
        # iterate over expr dict for elements whose seen flag is not
        # set. fail if we find one.
        for k, v in nanoconf['deephash'].items():
            if v[1] == False:
                _set_err(reason="nomatchingiven", errkey=k)
                _print_deep_fail_msg(msg, None, None)
                return False
        return True

    def _hash(element, verify, msg):
        if isinstance(element, (tuple, list, dict)):
            # composites are handled here
            if isinstance(element, (dict,)):
                # dict
                nanoconf['deepstack'].append('dict')
                for key in sorted(element.keys()):
                    nanoconf['deepstack'].append(str(key))
                    _deep_build_hash(element[key], verify, msg)
                    nanoconf['deepstack'].pop()
            else:
                if isinstance(element, (list,)):
                    nanoconf['deepstack'].append('list')
                else:
                    nanoconf['deepstack'].append('tuple')
                for idx, subelem in enumerate(element):
                    nanoconf['deepstack'].append(str(idx))
                    _deep_build_hash(subelem, verify, msg)
                    nanoconf['deepstack'].pop()
            nanoconf['deepstack'].pop()
        else:
            # leafnodes handled here
            key = ".".join(nanoconf['deepstack'])
