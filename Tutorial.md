nanotest-py Tutorial
====================

nanotest is a lightweight, easy-to-use software testing library. This
document describes how to use the `nanotest` harness to run test
suites, and the general use of the `nanotest.py` library to write test
suites. Please see `pydoc nanotest` for detailed information on the
functions contained in the nanotest library.


How to use nanotest-py
----------------------

After installation, just run `nanotest` from anywhere (but most likely
from the top-level directory of your project). It will search the
filesystem subtree under your current directory for directories named
`tests`.

Any files named `*.py` in such a directory will be run as test
scripts. This means you can have all of a project's tests in one
place, or you can scatter them around the codebase. Whatever makes
sense to you.

As tests run, diagnostic information about tests which fail will be
printed to the console. After each script completes, a summary of
passing and failing tests will be printed. After all scripts have been
executed, a summary of all tests will be printed.

```
  # a run of nanotest's own test suite
  $ nanotest
  Begin run: searching for modules and tests.
     ./tests/00-pis_pisnt.py: 20/20 passing; ok
     ./tests/01-pis_deeply-hashing.py: 68/68 passing; ok
     ./tests/02-pis_deeply-success.py: 11/11 passing; ok
     ./tests/03-pis_deeply-fail.py: 60/60 passing; ok
  End of run
     Tests passing: 159/159, in 4 script(s)
  Success
  $
```

If you want less output, use the `--quiet` option. If you want no
output at all, use `--silent` instead.

nanotest will exit with a code of 1 if any tests fail. If a test
script aborts, its exit code will be passed along and nanotest will
exit with that same code.

(Except for codes above 255, which are reported by the shell as their
value mod 256. In these cases, nanotest will print the actual value
for you and then force the return code to 113. Interestingly, Python
itself tends to abort with a code of 256, which would result in a code
of 0 -- success! -- being reported by bash after nanotest has just
informed you that a test script blew up, and it is aborting the run.)


What's a test script?
---------------------

nanotest-py test scripts are just Python programs. The basic skeleton
is:

```
  from nanotest import *

  # code and tests go here

  nanotest_summary()
```

The `import` line will put 4 functions in your namespace: `pis()`,
`pisnt()`, `pis_deeply()`, and `nanotest_summary()`. The first three
are the actual test functions of nanotest. The last is a simple
reporting function which outputs the script results to the test
harness.

This function, `nanotest_summary()`, is called on the last line of a
test script. For accurate reporting of results, it must be the last
thing that happens in a test script.

In the middle go the tests, and whatever setup and/or teardown code is
needed for those tests. There are no restrictions or prescriptions of
any sort. It's not even required that a test script actually call any
of the testing functions, though this isn't going to do much to help
ensure that software is operating correctly.


What's a test suite?
--------------------

Simply a collection of one or more test scripts. Using nanotest itself
as an example, the test suite is made of 4 scripts:

* tests/00-pis_pisnt.py
* tests/01-pis_deeply-hashing.py
* tests/02-pis_deeply-success.py
* tests/03-pis_deeply-fail.py

Each of these scripts contains tests which exercise a specific bit of
the library's functionality. The first tests the `pis` and `pisnt`
functions. The second tests the hashing algorithm which drives the
`pis_deeply` function. The third does positive (successful tests)
testing of `pis_deeply` itself. The fourth tests `pis_deeply` in its
failure modes.

There's no right or wrong way to construct a test suite, but this sort
of division is fairly typical.


How to write tests
------------------

