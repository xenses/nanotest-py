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

in each test script. Three functions will be exported into your
namespace: two for testing and one for reporting. They are detailed
below."""

nanotest_run = 0
nanotest_pass = 0

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
        test_print_fail_msg(expr, given, msg, False)

def pisnt(expr, given, msg):
    """Test for difference.

pisnt() is named so that it will match pis().

Works exactly like pis(), but backwards: tests succeed if the
experimental and the given values are NOT equivalent."""
    global nanotest_pass
    if not _is_core(expr, given):
        nanotest_pass = nanotest_pass + 1
    else:
        test_print_fail_msg(test, given, msg, True)
    
def test_print_fail_msg(expr, given, msg, invert):
    print("Test {} FAILED: {}".format(nanotest_run, msg))
    if invert:
        print("Expected anything but '{}' and got it anyway".format(given))
    else:
        print("   Expected: '{}'".format(given))
        print("   Got     : '{}'".format(expr))

def test_print_summary():
    """Utility function which prints the number of tests run and
    passed. Should be called at the end of every test script."""
    print("{} {}".format(nanotest_run, nanotest_pass))

__all__ = ["pis", "pisnt", "test_print_summary"]
