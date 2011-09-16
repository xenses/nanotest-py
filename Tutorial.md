nanotest-py Tutorial
====================

nanotest is a lightweight, easy-to-use software testing library. If
you understand what that means, skip ahead to the next section header.


How to use nanotest-py
----------------------

After installation, just run `nanotest` from anywhere. It will search
the filesystem subtree under your current directory for directories
named `tests`.

Any files named `*.py` in such a directory will be run as test scripts.

As tests run, diagnostic information about tests which fail will be
printed to the console. After each script completes, a summary of
passing and failing tests will be printed. After all scripts have been
executed, a summary of all tests will be printed.

If you want less output, use the `--quiet` option. If you want no
output at all, use `--silent` instead.

nanotest will always exit with a code of 1 if any tests fail. If a
script aborts, its exit code will be passed along (except codes above
255, which are out-of-spec and forced to 113 after printing, if silent
mode is not in effect).


What's a test script?
---------------------


How to write tests
------------------