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

[*Technical note*: Except for codes above 255, which are reported by
the shell as their value mod 256. In these cases, nanotest will print
the actual value for you and then force the return code to
113. Interestingly, Python itself tends to abort with a code of 256,
which would result in a code of 0 -- success! -- being reported by
bash after nanotest has just informed you that a test script blew up,
and it is aborting the run.]


How to write tests
------------------

Tests in nanotest-py are simply calls to `pis()`, `pisnt()`, or
`pis_deeply()`. This makes it easy to write tests as you code. Anytime
you add new code, correct a bug, or refactor something, that's a good
time to write a test.

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

Here are some simple examples of `pis()` and `pisnt()`.

```
$ python
Python 3.2.2 (default, Sep  5 2011, 04:33:58)
[GCC 4.6.1 20110819 (prerelease)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from nanotest import *
>>>
>>> def square(x):
...   return x * x
...
>>> pis( square(4), 16, "4 squared is 16")
True
>>> pisnt( square(9), 45, "9*9 should not be 9*5")
True
```

As shown above, tests don't have to be contained in anything. They can
be used and experimented with in the Python repl, just like everything
else.

`pis_deeply` works the same way, but is more powerful. It expects its
experimental and given values to be *compound types*
(*i.e. structures*). The structures may be of arbitrary depth and
construction. It will return True only when both structures are
*congruent*, when all nodes are of *the same type*, and when all leaf
nodes hold *the same values*.

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


What's a test script?
---------------------

nanotest-py test scripts are just Python programs which contain
tests. The basic skeleton is:

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
`pis_deeply` function. The third does positive testing
(i.e. successful tests) of `pis_deeply` itself. The fourth tests
`pis_deeply` in its failure modes.

There's no right or wrong way to construct a test suite, but this sort
of functional division is fairly typical.
