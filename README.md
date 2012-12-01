nanotest-py README and Tutorial
===============================

Nanotest is a lightweight, easy-to-use software testing
library. `nanotest-py` is the Python implementation of it.

This document describes how to install nanotest-py, how to use it to
run test suites, and how to write test scripts for it.

Installation
------------

Python 3.2+ is required due to use of the `argparse` module.

To run nanotest's own tests before installation:

    ./bin/nanotest-py # this will fail if nanotest v1 is installed
                      # see below for more info

After that, installation is standard:

    python setup.py install

See `nanotest-py --help` for quick online help on how to run
tests. Read the tutorial below for more comlpete information.


Upgrading from version 1
------------------------

It seems that Python's distribution tools do not make allowances for
removing software. Therefore, you should manually remove the old
`nanotest` executable, which is installed at

```
/usr/bin/nanotest
```

You should also uninstall the old nanotest module(s), which will be at
one or both of these paths:

```
/usr/lib/python3.2/site-packages/nanotest*
/usr/lib/python3.3/site-packages/nanotest*
```

My apologies for this being necessary.


Tutorial
========

Running tests
-------------

After installation, run `nanotest-py` in the top-level directory of a
project. It will scan that directory, and all subdirctories, for
directories named `tests/`. Any files in these directories whose names
match `*.py` will be treated as test scripts.

After the tests have been run, diagnostic information about failing
tests will be printed to the console. This is what nanotest's own test
suite looks like:

```
$ nanotest-py
./tests/00-core.py      18/18 passing    ok
./tests/01-re.py        12/12 passing    ok
./tests/02-hash.py      26/26 passing    ok
./tests/03-invcomp.py   3/3 passing      ok
./tests/04-comp.py      3/3 passing      ok
62/62 passing in 5 files
$
```

It is possible to run specific scripts instead of the whole suite:

```
# run just one script
nanotest-py tests/test1.py

# run two, in this order
nanotest-py tests/test3.py tests/test1.py
```

### Silent mode

Output can be supressed with the `--silent` option. In this case,
check the return code of `nanotest-py` to see if the test suite was
successful or not.

* 0 - Success
* 1 - Failure
* 2 - No tests found

(These return codes apply to all modes of operation.)

### JSON

Raw test results can be obtained with the `--json` option. The output
will be a list of objects, each of which looks like

```
{ file:   TEST_FILENAME
  line:   LINE_NUMBER
  pass:   SUCCESS_T/F
  msg:    TEST_DESCRIPTION
  comp:   [ { xpect:  GIVEN_VALUE
              got:    EXPERIMENTAL_VALUE
              reason: ADDL_TEST_INFO }, ... ] }
```

The `comp` field contains a list of comparison data objects.  Tests of
scalar values will involve a single comparison, but tests on
datastructres may generate a list of many objects if the structs do
not match.


Writing tests
-------------

`nanotest` is an object-based module. The boilerplate for a test
script is

```
import nanotest

n = nanotest.Nanotester()
```

The `nanotest` object is called `n` by convention, just as test
scripts live in directories named `tests/` by convention. If the
object has a different name, the test harness (`nanotest-py`) will not
be able to examine the results of the tests, and that script as a
whole will be treated as a no-op.

Individual tests in are simply calls to `n.test()` (to test for
equality) or `n.untest()` (to test for inequality). This makes it easy
to write tests as you code.

Both functions take three arguments, in the same order:

* The experimental value (the value to be tested)

* The given value (the value which is accepted as "correct")

* A message string (printed if the test fails, to help identify the
  failing test)

Nanotest is not a strict, blackbox, unit testing library. It can be
used as such, but since tests are just method calls, it can also poke
at the internals of objects, examine program state variables, and
generally inspect anything that a programmer can get a handle on at
any point in a program's life. Some examples:

```
n.test(1, 1, "Yes, of course")
n.test(myvar, somevalue, "Another simple test")
n.test((2 + 2), 4, "Expressions on both sides will be evaluated")
n.test(myfunc(withargs), False, "This is a pass if myfunc returns False")
```

### Testing with regexeps

Frequently, in the real world, it is impossible to know exactly what a
value will be.  It may only be known that a value must be numeric, or
that it will take a certain form (like a phone number).

Nanotest allows these kinds of comparisons in tests by using regular
expression searches.  If a test's `given` value is a string which
begins with `:re:`, the remainder of the string is used as a regex
which the experimental value is matched

```
n.test(user.ccn, ':re:4\d{3}\s?\d{4}\s?\d{4}\s?\d{4}', "Should be a valid visa number")
n.untest(user.name, ':re:\d', "Form should have disallowed numbers in names")
```

### Comparing datastructures

Nanotest is not limited to comparing scalar values. If both arguments
to `test()` (or `untest()`) are a list, tuple, or dict, the structures
will be tested to see if:

* they have the same number of elements
* they have the same type of elements, in the same places
* all matching elements hold the same value

If all these conditions are met, for all nodes of both structs, the
test passes. In JSON output mode, there will be a single entry in the
test data.

In the case of failure, however, there will be one element in the
`comp` list (in JSON mode) or one printed diagnostic (in the default
console report mode) for _every mismatch_ between the two
structures. The exception to this is that when a missing node is
encountered, no siblings or child nodes will be examined, as this
could cause large cascades of spurious mismatch reports.

Finally, any and all values in the given struct of a test can be
regexps, just as any given value in a test with two scalar values can.

Developer tests
---------------

The purpose of testing is to prove, to the best of one's ability, that
software does what one believes it does, and behaves as one believes
it should behave.

A problem with this is that sometimes, as the developer of a piece of
software, you want to test for expected _failure,_ But including these
sorts of tests in a suite would be, to users running the suite to
prove your software, irritating at best and off-putting at worst.

One solution is write tests which succeed by testing for the
side-effects or results of a failure. Another is to use inversions of
logic to turn a failure into a success (and thus a passing test). But
sometimes neither of these what you want.

For those times, `nanotest-py` supports the concept of developer
tests: test scripts which are not run by default. To make a script
into a devtest, just give it a name ending with `DEV.py`. These
scripts are run only when the `--dev` option is passed to the nanotest
runner.

Test injection
--------------

Coming in v2.1.0!


---

I hope you find nanotest useful. If you have any questions,
suggestions, or other comments, please contact me by email or through
Github.

Shawn Boyette
<shawn@firepear.net>
