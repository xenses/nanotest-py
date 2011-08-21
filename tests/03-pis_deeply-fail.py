import nanotest # we only do this because we're testing the module itself!
from nanotest import *


# failures
#
# value mismatch, trivial
nanotest.nanoconf["silent"] = True
pis_deeply(1, 2, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],             0, "No tests passing after trivial fail")
pis(nanotest.nanoconf["error"],         True, "error has been set")
pis(nanotest.nanoconf['errcode'], "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'],      "root", "error was on root elem")
nanotest.nanoconf['pass'] += 1 # all's good here, treat as pass
# value mismatch, tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2), (1, 3), "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                5, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],            True, "error has been set")
pis(nanotest.nanoconf['errcode'],    "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.tuple.1", "error was on 2nd tuple elem")
nanotest.nanoconf['pass'] += 1
# value mismatch, list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2, 3, 4], [4, 1, 2, 3], "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               10, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.list.0", "error was on 1st list elem")
nanotest.nanoconf['pass'] += 1
# value mismatch, dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1, 'b':2}, {'a':1, 'b':4}, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               15, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.b", "error was on dict elem 'b'")
nanotest.nanoconf['pass'] += 1
# value mismatch, blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'q'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               20, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.1", "yeah, it was here")
nanotest.nanoconf['pass'] += 1

# not-found in experimental (1st arg), tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2), (1, 2, 3), "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 25, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],   "root.tuple.2", "3rd tuple elem doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in experimental (1st arg), list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2], [1, 2, 3], "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 30, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.list.2", "3rd list elem doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in experimental (1st arg), dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1}, {'a':1, 'b':2}, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 35, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.dict.b", "dict elem 'b' doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in experimental (1st arg), blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'y', 'z'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               40, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "nomatchinexpr", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.2", "yeah, it was here")
nanotest.nanoconf['pass'] += 1

# not-found in given (2nd arg), tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2, 3), (1, 2), "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 45, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],   "root.tuple.2", "3rd tuple elem doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in given (2nd arg), list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2, 3], [1, 2], "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 50, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.list.2", "3rd list elem doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in given (2nd arg), dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1, 'b':2}, {'a':1}, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 55, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.dict.b", "dict elem 'b' doesn't exist in expr")
nanotest.nanoconf['pass'] += 1
# not-found in given (2nd arg), blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y', 'z'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               60, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.2", "yeah, it was here")
nanotest.nanoconf['pass'] += 1


# end-of-run
nanotest_summary();
