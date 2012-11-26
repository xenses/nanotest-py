This is the Python implementation of nanotest, a tiny testing
library. Python 3.2+ is required due to use of the `argparse` module.

To run nanotest's own tests before installation:

    ./bin/nanotest-py

After that, installation is standard:

    python setup.py install

See `nanotest-py --help` for information on how to run tests. Read the
Tutorial document to learn how to write tests.


Changes and additions in version 2
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
  
* `--quiet` mode no longer exists
