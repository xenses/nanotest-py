"""This module implements a tiny slice of the functionality of Perl's
Test::More. Its job is to make unit/whitebox testing quick and
easy.

It has a counterpart script, also called 'nanotest', which acts as the
test harness/runner. The harness searches for test scripts in and
below the current directory, runs them, reports their individual
findings, then issues a summary for the entire test suite.

Test scripts must live in a directory named 'tests', and they must
have the extension '.py'. Scripts are simply Python programs and may
be written however you please.

This module is used by doing

    from nanotest import *

in each test script. Four functions will be exported into your
namespace: three for testing and one for reporting. They are detailed
below."""

import re

nanoconf = { 'run':0,
             'pass':0,
             'deepstack':['root'],
             'deephash':{},
             'error':False,
             'errmode':None,
             'errkey':None,
             'quiet':False,
             'silent':False, }

def _is_core(expr, given):
    global nanoconf
    nanoconf['run'] += 1
    if expr == given:
        return True
    return False

def pis(expr, given, msg):
    """Test for equivalence.

pis() should be named is(), but 'is' is a keyword in Python.

Takes 3 arguments: an experimental value, a given value, and a
message. The first two can be any valid Python expression; the third
should be a message string.

If the experimental and given values are equivalent, the test is a
success and nothing happens. If they are different, the test is a
failure and the message will be printed to STDOUT.
"""
    global nanoconf
    if _is_core(expr, given):
        nanoconf['pass'] += 1
        return True
    else:
        _print_is_fail_msg(expr, given, msg, False)
        return False

def pisnt(expr, given, msg):
    """Test for difference.

pisnt() is named so that it will match pis().

Works exactly like pis(), but backwards: tests succeed if the
experimental and the given values are NOT equivalent."""
    global nanoconf
    if not _is_core(expr, given):
        nanoconf['pass'] = nanoconf['pass'] + 1
        return True
    else:
        _print_is_fail_msg(expr, given, msg, True)
        return False

#-----------------------------------------------------------------------

def pis_deeply(expr, given, msg):
    """Test composite datastructures for equivalence.

Like pis()and pisnt(), pis_deeply() takes three arguments: an
experimental value, a given value, and a message. The first two should
be composite data structures (lists, dictionaries, tuples), and they
may be as deeply nested as you please. The third should be a message
string.

The experimental and given structures will be tested for "congruence"
(that is, they have the same structure and the same values at all
endpoints of the structure). If they do not match, the test fails and
the message will be printed to STDOUT.

Since this comparison is more complex than the one performed by
pis/nt(), additional information about the exact nature of the failure
will also be printed.

In the given structure, any string value which begins with ':re:' will
be treated as a regular expression to be tested against with re.search
(after the prefix has been removed, of course). This allows testing
for things whose exact value cannot be known in advance, but whose
general format or basic parameters is established."""
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
        return
    # iterate over expr dict for elements whose seen flag is not
    # set. fail if we find one.
    for k, v in nanoconf['deephash'].items():
        if v[1] == False:
            _set_err(reason="nomatchingiven", key=k)
            _print_deep_fail_msg(msg, None, None)
            return
    # made it here? pass.
    nanoconf['pass'] += 1


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
                nanoconf['deepstack'].append(key)
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
                _set_err(reason="nomatchinexpr", key=key)
                _print_deep_fail_msg(msg, None, None)
            else:
                # handle regexes if we're looking at one. 
                if re.match('\:re\:', str(element)) != None:
                    if not _regex_comp(key, element, msg):
                        _print_deep_fail_msg(msg, nanoconf['deephash'][key], element)
                # no, it's a regular comparison
                elif nanoconf['deephash'][key][0] != element:
                    _set_err(reason="badvalue", key=key)
                    _print_deep_fail_msg(msg, nanoconf['deephash'][key], element)
                # regardless, set seen flag if we haven't failed
                if not nanoconf['error']:
                    nanoconf['deephash'][key][1] = True
        else:
            nanoconf['deephash'][key] = [element, False]


def _regex_comp(key, given, msg):
    expr = nanoconf['deephash'][key][0]
    if re.search(given[4:], str(expr)):
        return True
    else:
        _set_err(reason="renomatch", key=key)
        return False

#-----------------------------------------------------------------------
    
def _set_err(**kw):
    global nanoconf
    nanoconf['error'] = True
    nanoconf['errcode'] = kw['reason']
    nanoconf['errkey'] = kw['key']

def _print_is_fail_msg(expr, given, msg, invert):
    if nanoconf['silent']:
        return
    print("FAILED test {}: {}".format(nanoconf['run'], msg))
    if invert:
        print("   Expected anything but '{}' and got it anyway".format(given))
    else:
        print("   Expected: '{}'".format(given))
        print("   Got     : '{}'".format(expr))


def _print_deep_fail_msg(msg, expr, given):
    if nanoconf['silent']:
        return
    print("FAILED test {}: {}".format(nanoconf['run'], msg))
    if nanoconf['errcode'] == "badvalue":
        print("   Values at {} don't match".format(nanoconf['errkey']))
        print("   Expected '{}'; got '{}'".format(expr, given))
    elif nanoconf['errcode'] == "nomatchinexpr":
        print("   Node {} exists in given struct but not experimental struct".format(nanoconf['errkey']))
    elif nanoconf['errcode'] == "nomatchingiven":
        print("   Node {} exists in experimental struct but not given struct".format(nanoconf['errkey']))
    elif nanoconf['errcode'] == "renomatch":
        print("   Node {} does not match regex '{}'".format(nanoconf['errkey'], given))


def nanotest_summary():
    """Utility function which prints the number of tests run and
    passed. Should be called at the end of every test script."""
    print("{} {}".format(nanoconf['run'], nanoconf['pass']))

__all__ = ["pis", "pisnt", "pis_deeply", "nanotest_summary"]
