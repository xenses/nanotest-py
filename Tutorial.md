nanotest-py Tutorial
====================

nanotest is a lightweight, easy-to-use software testing library. If
you understand what that means, skip ahead to the next section header.


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



How to write tests
------------------

