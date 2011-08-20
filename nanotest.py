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

nanotest_run = 0
nanotest_pass = 0
nanotest_deepstack = ['root']
nanotest_deephash  = {}
nanotest_error = False

def _is_core(expr, given):
    global nanotest_run
    nanotest_run += 1
    if expr == given:
        return True
    return False

def pis(expr, given, msg):
    """Test for equivalence.

pis() should be named is(), but 'is' is a keyword in Python.

Takes 3 arguments: an experimental value, a given value, and a
message. The first two can be any valid Python expression; the third
should be a string.

If the experimental and given values are equivalent, the test is a
success and nothing happens. If they are different, the test is a
failure and the message will be printed to STDOUT.
"""
    global nanotest_pass
    if _is_core(expr, given):
        nanotest_pass += 1
    else:
        _print_is_fail_msg(expr, given, msg, False)

def pisnt(expr, given, msg):
    """Test for difference.

pisnt() is named so that it will match pis().

Works exactly like pis(), but backwards: tests succeed if the
experimental and the given values are NOT equivalent."""
    global nanotest_pass
    if not _is_core(expr, given):
        nanotest_pass = nanotest_pass + 1
    else:
        _print_is_fail_msg(expr, given, msg, True)

#-----------------------------------------------------------------------

def pis_deeply(expr, given, msg):
    """Test composite datastructures for equivalence.

Like pis()and pisnt(), pis_deeply() takes three arguments: an
experimental value, a given value, and a message. The first two should
be composite data structures (lists, dictionaries, tuples), and they
may be as deeply nested as you please. The third should be a string.

The experimental and given structures will be compared for both
composition and content. If they are not identical, the test fails and
the message will be printed to STDOUT. Since this comparison is more
complex than the one performed by pis/nt(), additional information
about the exact nature of the failure will also be printed."""
    global nanotest_run
    nanotest_run += 1
    # ensure stack and hash are empty
    if len(nanotest_deepstack) > 1:
        nanotest_deepstack = ['root']
    if len(nanotest_deephash) > 0:
        nanotest_deephash = {}

    # build dict of hashed expr structure. value is a 2-element list;
    # 0 is actual value of leafnodes, 1 is a "seen" flag
    _deep_build_hash(expr, False, None)

    # run hash function over given structure, but don't build struct
    # from it. as each leafnode is found, look for its hash and value
    # in the expr dict. if matching, set expr "seen" flag. if not,
    # fail
    _deep_build_hash(given, True, msg)
    if nanotest_error:
        return

    # assuming no failures yet, iterate over expr dict for elements
    # whose seen flag is not set. fail if we find one.



def _deep_build_hash(element, verify, msg):
    if nanotest_error:
        return
    global nanotest_deepstack
    global nanotest_deephash
    #elem_type = type(element) # for later, change 'if isinstance...' to 'if x == type(THING)'
    if isinstance(element, (tuple, list, dict)):
        if isinstance(element, (dict,)):
            nanotest_deepstack.append('dict')
            for key in sorted(element.keys()):
                nanotest_deepstack.append(key)
                _deep_build_hash(element[key], verify, msg)
                nanotest_deepstack.pop()
        else:
            if isinstance(element, (list,)):
                nanotest_deepstack.append('list')
            else:
                nanotest_deepstack.append('tuple')
            for idx, subelem in enumerate(element):
                nanotest_deepstack.append(str(idx))
                _deep_build_hash(subelem, verify, msg)
                nanotest_deepstack.pop()
        nanotest_deepstack.pop()
    else:
        # we're a leafnode
        if verify:
            key == ".".join(nanotest_deepstack)
            if node not in nanotest_deephash:
                _print_deep_fail_msg(msg, "nomatchinexpr", key, None, None)
            else:
                if nanotest_deephash[key] != element:
                    _print_deep_fail_msg(msg, "nomatchinexpr", key, nanotest_deephash[key], element)
                else:
                    nanotest_deephash[key][1] = True
        else:
            nanotest_deephash[".".join(nanotest_deepstack)] = [element, False]

#-----------------------------------------------------------------------
    
def _print_is_fail_msg(expr, given, msg, invert):
    print("FAILED test {}: {}".format(nanotest_run, msg))
    if invert:
        print("   Expected anything but '{}' and got it anyway".format(given))
    else:
        print("   Expected: '{}'".format(given))
        print("   Got     : '{}'".format(expr))


def _print_deep_fail_msg(msg, mode, key, expr, given):
    global nanotest_error
    nanotest_error = True
    print("FAILED test {}: {}".format(nanotest_run, msg))
    if mode == "badvalue":
        print("   Values at {} don't match".format(key))
        print("   Expected '{}'; got '{}'".format(expr, given))
    elif mode == "nomatchinexpr":
        print("   Node {} exists in given struct but not experimental struct".format(key))
    elif mode == "nomatchingiven":
        print("   Node {} exists in experimental struct but not given struct".format(key))


def nanotest_summary():
    """Utility function which prints the number of tests run and
    passed. Should be called at the end of every test script."""
    print("{} {}".format(nanotest_run, nanotest_pass))

__all__ = ["pis", "pisnt", "pis_deeply", "nanotest_summary"]
