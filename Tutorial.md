nanotest-py Tutorial
====================

nanotest is a lightweight, easy-to-use software testing library. This
document describes how to use the `nanotest-py` harness to run test
suites, and the general use of the `nanotest` library to write test
scripts.


How to use nanotest-py
----------------------

After installation, run `nanotest-py` from the top-level directory of
a project. It will search the filesystem subtree under that directory
for directories named `tests`.

Any files in these directories whose names match `*.py` will be
treated as test scripts.

By default, after the tests have been run, diagnostic information
about failing tests will be printed to the console. This is what
nanotest's own test suite looke like:

```
  $ nanotest-py
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

Raw test results can be obtained with the `--json` option. The output will be a list of objects, each of which looks like

```
{ file:   TEST_FILENAME
  line:   LINE_NUMBER
  pass:   SUCCESS_T/F
  xpect:  GIVEN_VALUE
  got:    EXPERIMENTAL_VALUE
  msg:    TEST_DESCRIPTION
  reason: ADDL_FAILURE_INFO }
```

How to write tests
------------------

Tests in nanotest-py are simply calls to `pis()`, `pisnt()`, or
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
### Regexes

The above examples show how to use nanotest to test for simple, rigid
equivalence. But frequently, in the real world, we cannot know exactly
what our data will be. We may know only that a value must be
numeric. We may know that a value must be of a certain form, like a
phone number.

To enable these kinds of comparisons in tests, nanotest checks to see
if its given value is a string which begins with `:re:`. If it is, the
remainder of the string is used as a regex which the experimental
value is tested against.

```
>>> pis('4873 2767 0909 2763', ':re:4\d{3} \d{4} \d{4} \d{4}', "visa number")
True
>>> pisnt("Agamemnon Q. Huxtable", ':re:\d', "No numbers allowed in names")
True
```

This is also allowed with any and all values in the given struct of a
`pis_deeply()` call.

```
>>> # set up a string that matches a v4 (random) uuid
... v4uuid = ':re:[\0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
>>>
>>> # now mock up an object containing a random UUID
... exp_val = { 'a':1, 'b':2, 'c':uuid.uuid4() }
>>> exp_val
{'a': 1, 'c': UUID('0c490083-47b0-4462-a1fb-af6a593dc3fd'), 'b': 2}
>>>
>>> pis_deeply(exp_val, {'a':1, 'b':2, 'c':v4uuid}, "c will match using the stored regex")
True
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
