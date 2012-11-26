This is the Python implementation of nanotest, a tiny testing
library. Python 3.2+ is required due to use of the `argparse` module.

To run nanotest's own tests before installation:

    ./bin/nanotest-py

After that, installation is standard:

    python setup.py install

See `nanotest-py --help` for information on how to run tests. Read the
Tutorial document to learn how to write tests.


Upgrading from version 1
------------------------

It seems that Python's distribution tools do not make allowances for
removing software. Therefore, you should manually remove the old
`nanotest` executable, which is installed at

```
/usr/bin/nanotest
```

And you may also wish to uninstall the old nanotest module(s). They
will be at one or both of these paths:

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

Please see the tutorial for more complete information.
