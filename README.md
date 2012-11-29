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


Changes in version 2
----------------------------------

Nanotest 2 is a near-total rewrite, and as the major version number
bump indicates, it is backward-incompatible with the version 1
interface.

The major, incompatible changes are, in summary:

* The module is now object-based, and exports no symbols.

* The number of testing functions (now methods) is reduced to two.

* The module no longer relies on subprocesses and parsing textual
  output.
  
* Test results are now available as a report (old style) or as
  unparsed, JSON-formatted data.
  
* `--quiet` mode no longer exists.

Please keep reading for more complete information.



Tutorial
========

Running tests
-------------

After installation, run `nanotest-py` from the top-level directory of
a project. It will search the filesystem subtree under that directory
for directories named `tests`. Any files in these directories whose
names match `*.py` will be treated as test scripts.

By default, after the tests have been run, diagnostic information
about failing tests will be printed to the console. This is what
nanotest's own test suite looke like:

```
  $ nanotest-py
  TODO PLUG THIS IN AFTER THINGS SETTLE
  $
```

Specific test scripts instead of the whole suite:

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


How to write tests
------------------

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

Tests in nanotest-py are calls to `pis()`, `pisnt()`, or
`pis_deeply()`. This makes it easy to write tests as you code. Anytime
you add new code, correct a bug, or refactor something, that's a good
time to write a test (or, if you have a test suite, to rerun it).

All three functions take three arguments, in the same order:

* The experimental value (the value to be tested)

* The given value (the value which is accepted as "correct")

* A message string (printed if the test fails, to help identify the
  failing test)

All three functions do the same thing: test their *experimental* and
*given* values for equivalence. All three functions return True or
False.

nanotest-py is not a strict, blackbox, unit testing library. It can be
used as such, but it can also poke at the internals of objects,
examine program state variables, and generally inspect anything that a
programmer can get a handle on at any point in a program's life.

### Examples

```
>>> pis_deeply((1, 'a', 34), (1, 'a', 34), "identical tuples")
True
>>> struct = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
>>> pis_deeply(struct, struct, "identical blended composites")
True
>>> # these next two are failures, and will produce diagnostic output
... pis_deeply({'a':1}, {'a':1, 'b':2}, "these don't match")
FAILED test 5: these don't match
   Node root.dict.b exists in given struct but not experimental struct
False
>>> struct1 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
>>> struct2 = {'a':1, 'q':[11, 22, ('x', 'q'), 33], 'c':{'z':44}}
>>> pis_deeply(struct1, struct2, "these don't match either")
FAILED test 6: these don't match either
   Values at root.dict.q.list.2.tuple.1 don't match
   Expected 'y'; got 'q'
False
```

### Regexes

Frequently, in the real world, it is impossible to know exactly what a
value will be.  It may only be known that a value must be numeric, or
of a certain form (like a phone number).

`nanotest` allows these kinds of comparisons in tests by using regular
expression searches.  If a test's `given` value is a string which
begins with `:re:`, the remainder of the string is used as a regex
which the experimental value is matched

```
n.test('4873 2767 0909 2763', ':re:4\d{3} \d{4} \d{4} \d{4}', "visa number")
n.untest("Agamemnon Q. Huxtable", ':re:\d', "No numbers allowed in names")
```

This is also allowed with any and all values in the given struct of a
deep comparison.

```
# set up a string that matches a v4 (random) uuid
v4uuid = ':re:[\0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
# now mock up an object containing a random UUID
exp_val = { 'a':1, 'b':2, 'c':uuid.uuid4() }
# {'a': 1, 'c': UUID('0c490083-47b0-4462-a1fb-af6a593dc3fd'), 'b': 2}
n.test(exp_val, {'a':1, 'b':2, 'c':v4uuid}, "c will match using the stored regex")
True
```


Test injection
--------------------

Coming soon.
