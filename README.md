nanotest-py README and Tutorial
===============================

Nanotest is a lightweight, easy-to-use software testing
library. `nanotest-py` is the Python implementation of it.

This document describes how to install nanotest-py, how to use it to
run test suites, and how to write test scripts for it.

Installation
------------

_If you are still using v1.x of nanotest, please remove it by hand. I
apologize for the inconvenience._

Python 3.2+ or 2.7+ is required due to use of the `argparse` module.

To run nanotest's own tests before installation:

    ./bin/nanotest-py # this will fail if nanotest v1 is installed
                      # see below for more info

After that, installation is standard:

    python setup.py install

See `nanotest-py --help` for quick online help on how to run
tests. Read the tutorial below for more comlpete information.


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
  pass:   BOOL
  msg:    TEST_DESCRIPTION
  comp:   [ { xpect:  GIVEN_VALUE
              got:    EXPERIMENTAL_VALUE
              reason: ADDL_TEST_INFO }, ... ] }
```

The `comp` field contains a list of comparison data objects.  Tests of
scalar values will involve a single comparison, but tests on
datastructres may generate a list of many objects if the structs do
not match.


Further reading
===============

For information on writing tests, creating a test suite, and more,
head to the
[nanotest-py wiki](http://github.com/firepear/nanotest-py/wiki/).
