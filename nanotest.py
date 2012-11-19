import re

class Nanotest:
    """
    """
    def __init__():
        pass

    def _is_core(expr, given):
        global nanoconf
        nanoconf['run'] += 1
        if re.match('\:re\:', str(given)) != None:
            if _regex_comp(expr=expr, given=given):
                return True
        else:
            if expr == given:
                return True
            return False

    def _is(expr, given, msg):
        global nanoconf
        passed = _is_core(expr, given)
        if  passed:
            nanoconf['pass'] += 1
        else:
            if nanoconf['errcode'] == 'renomatch':
                _print_re_fail_msg(msg=msg, expr=expr, given=given)
            else:
                _print_is_fail_msg(expr=expr, given=given, msg=msg)
        return passed

    def _isnt(expr, given, msg):
        global nanoconf
        passed = not _is_core(expr, given)
        if  passed:
            nanoconf['pass'] = nanoconf['pass'] + 1
        else:
            if nanoconf['errcode'] == 'renomatch':
                _print_re_fail_msg(msg=msg, expr=expr, given=given, pisnt=True)
            else:
                _print_is_fail_msg(expr=expr, given=given, msg=msg, pisnt=True)
        return passed

    def _is_deeply(expr, given, msg):
        # reset state
        global nanoconf
        nanoconf['error'] = False
        nanoconf['errcode'] = None
        nanoconf['errkey']  = None
        nanoconf['run'] += 1
        if len(nanoconf['deepstack']) > 1:
            nanoconf['deepstack'] = ['root']
        if len(nanoconf['deephash']) > 0:
            nanoconf['deephash'] = {}
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
        # made it here? pass.
        nanoconf['pass'] += 1
        return True

    def _deep_build_hash(element, verify, msg):
        global nanoconf
        if nanoconf['error']:
            return
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
            if verify:
                # make sure our key is in the expr hash
                if key not in nanoconf['deephash']:
                    _set_err(reason="nomatchinexpr", errkey=key)
                    _print_deep_fail_msg(msg, None, None)
                else:
                    # handle regexes if we're looking at one. 
                    if re.match('\:re\:', str(element)) != None:
                        if not _regex_comp(expr=nanoconf['deephash'][key][0], given=element, key=key):
                            _print_deep_re_fail_msg(msg, nanoconf['deephash'][key][0], element)
                    # no, it's a regular comparison
                    elif nanoconf['deephash'][key][0] != element:
                        _set_err(reason="badvalue", errkey=key)
                        _print_deep_fail_msg(msg, nanoconf['deephash'][key][0], element)
                    # regardless, set seen flag if we haven't failed
                    if not nanoconf['error']:
                        nanoconf['deephash'][key][1] = True
            else:
                nanoconf['deephash'][key] = [element, False]

    def _regex_comp(key=None, **kw):
        if re.search(kw['given'][4:], str(kw['expr'])):
            return True
        else:
            _set_err(reason="renomatch", errkey=key)
            return False
