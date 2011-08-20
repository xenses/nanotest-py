import nanotest # we only do this because we're testing the module itself!
from nanotest import *

# success
#
# the trivial case
pis_deeply(1, 1, "1 should equal 1")
pis(nanotest.nanotest_error, False, "no error (1)")
# tuple
pis_deeply((1, 'a', 34), (1, 'a', 34), "identical tuples")
pis(nanotest.nanotest_error, False, "no error (2)")
# list
pis_deeply([1, 'a', 34], [1, 'a', 34], "identical lists")
pis(nanotest.nanotest_error, False, "no error (3)")
# dict
pis_deeply({'a':22, 'b':"foo"}, {'a':22, 'b':"foo"}, "identical dicts")
pis(nanotest.nanotest_error, False, "no error (4)")
# blended
struct = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
pis_deeply(struct, struct, "identical blended composites")
pis(nanotest.nanotest_error, False, "no error (5)")

# end-of-run
nanotest_summary();
