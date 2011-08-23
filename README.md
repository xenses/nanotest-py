nanotest-py
===========

A reimplementation of `nanotest.js` from my Javascript library, which
is itself a tiny, fragmentary implementation of Perl's `Test::More`.

*Don't complain that testing is too hard! Use nanotest and get to work!*

nanotest-py is Python 3 only.

----

Development HEAD is not guaranteed to be complete, or even in working
order. Stick to tagged releases (downloadable at Github) if you are
not comfortable with this.

----

This package includes `nanotest.py`, which is the test library proper,
and `nanotest`, a script which acts as the test harness/runner.

If you want to run the package's own tests before installation, feel
free:

    ./bin/nanotest

Installation is standard:

    python setup.py install

See `pydoc nanotest` for details on use and how to write test scripts
and `nanotest --help` for information on the runner/harness script.

For more information or to contact me, see the [module
homepage](https://github.com/firepear/nanotest-py/)
