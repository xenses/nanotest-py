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
    else:
        _print_is_fail_msg(expr, given, msg, False)

def pisnt(expr, given, msg):
    """Test for difference.

pisnt() is named so that it will match pis().

Works exactly like pis(), but backwards: tests succeed if the
experimental and the given values are NOT equivalent."""
    global nanoconf
    if not _is_core(expr, given):
        nanoconf['pass'] = nanoconf['pass'] + 1
    else:
        _print_is_fail_msg(expr, given, msg, True)

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
            _deep_set_err("nomatchingiven", k)
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
        if verify:
            # in verify mode we build the element's key and check that
            # (1) it exists in deephash and (2) its value there is the
            # same as our value here. unless 1 and 2, it's a fail.
            key = ".".join(nanoconf['deepstack'])
            if key not in nanoconf['deephash']:
                _deep_set_err("nomatchinexpr", key)
                _print_deep_fail_msg(msg, None, None)
            else:
                # handle regexes if we're looking at one. if not, do a
                # simple comparison test. finally, pass if no error
                if re.match('\:re\:', str(element)) != None:
                    _deep_regex_comp(key, element, msg)
                elif nanoconf['deephash'][key][0] != element:
                    _deep_set_err("badvalue", key)
                    _print_deep_fail_msg(msg, nanoconf['deephash'][key], element)
                if not nanoconf['error']:
                    nanoconf['deephash'][key][1] = True
        else:
            nanoconf['deephash'][".".join(nanoconf['deepstack'])] = [element, False]


def _deep_regex_comp(key, element, msg):
    if re.search(element[4:], nanoconf['deephash'][key][0]):
        return
    else:
        _deep_set_err("renomatch", key)
        _print_deep_fail_msg(msg, nanoconf['deephash'][key], element)


def _deep_set_err(reason, key):
    global nanoconf
    nanoconf['error'] = True
    nanoconf['errcode'] = reason
    nanoconf['errkey'] = key

#-----------------------------------------------------------------------
    
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
