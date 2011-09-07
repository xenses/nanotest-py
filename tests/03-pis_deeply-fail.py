import nanotest # we only do this because we're testing the module itself!
from nanotest import *

fail = 0

# failures
#
# value mismatch, trivial
nanotest.nanoconf["silent"] = True
pis_deeply(1, 2, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],             0, "No tests passing after trivial fail")
pis(nanotest.nanoconf["error"],         True, "error has been set")
pis(nanotest.nanoconf['errcode'], "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'],      "root", "error was on root elem")
# value mismatch, tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2), (1, 3), "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                4, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],            True, "error has been set")
pis(nanotest.nanoconf['errcode'],    "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.tuple.1", "error was on 2nd tuple elem")
# value mismatch, list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2, 3, 4], [4, 1, 2, 3], "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               8, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.list.0", "error was on 1st list elem")
# value mismatch, dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1, 'b':2}, {'a':1, 'b':4}, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],              12, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],           True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.b", "error was on dict elem 'b'")
# value mismatch, blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'q'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],            16, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],         True, "error has been set")
pis(nanotest.nanoconf['errcode'], "badvalue", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.1", "yeah, it was here")

# not-found in experimental (1st arg), tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2), (1, 2, 3), "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                20, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],   "root.tuple.2", "3rd tuple elem doesn't exist in expr")
# not-found in experimental (1st arg), list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2], [1, 2, 3], "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 24, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.list.2", "3rd list elem doesn't exist in expr")
# not-found in experimental (1st arg), dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1}, {'a':1, 'b':2}, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 28, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.dict.b", "dict elem 'b' doesn't exist in expr")
# not-found in experimental (1st arg), blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'y', 'z'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                 32, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],              True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchinexpr", "error type was bad value match")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.2", "yeah, it was here")

# not-found in given (2nd arg), tuple
nanotest.nanoconf["silent"] = True
pis_deeply((1, 2, 3), (1, 2), "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                  36, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],               True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],    "root.tuple.2", "3rd tuple elem doesn't exist in expr")
# not-found in given (2nd arg), list
nanotest.nanoconf["silent"] = True
pis_deeply([1, 2, 3], [1, 2], "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                  40, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],               True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],     "root.list.2", "3rd list elem doesn't exist in expr")
# not-found in given (2nd arg), dict
nanotest.nanoconf["silent"] = True
pis_deeply({'a':1, 'b':2}, {'a':1}, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                  44, "No new tests passing after tuple fail")
pis(nanotest.nanoconf["error"],               True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'],     "root.dict.b", "dict elem 'b' doesn't exist in expr")
# not-found in given (2nd arg), blended
struct1 = {'a':1, 'q':[11, 22, ('x', 'y', 'z'), 33], 'c':{'z':44}}
struct2 = {'a':1, 'q':[11, 22, ('x', 'y'), 33], 'c':{'z':44}}
nanotest.nanoconf["silent"] = True
pis_deeply(struct1, struct2, "these don't match")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],                  48, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],               True, "error has been set")
pis(nanotest.nanoconf['errcode'], "nomatchingiven", "error type was key not found in expr struct")
pis(nanotest.nanoconf['errkey'], "root.dict.q.list.2.tuple.2", "yeah, it was here")

# regex failure
struct = {'a':1, 'b':'4893 03q3 2873 8937'}
regex = ':re:4\d{3} \d{4} \d{4} \d{4}'
nanotest.nanoconf["silent"] = True
pis_deeply(struct, {'a':1, 'b':regex}, "regex test")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               52, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],            True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "renomatch", "error type was regex no match")
pis(nanotest.nanoconf['errkey'],  "root.dict.b", "q isn't a digit")
struct = {'a':1, 'b':'7893 0343 2873 8937'}
nanotest.nanoconf["silent"] = True
pis_deeply(struct, {'a':1, 'b':regex}, "regex test")
fail += 1
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"],               56, "No new tests passing after list fail")
pis(nanotest.nanoconf["error"],            True, "error has been set")
pis(nanotest.nanoconf['errcode'],   "renomatch", "error type was regex no match")
pis(nanotest.nanoconf['errkey'],  "root.dict.b", "7 isn't 4")


# remove failing tests from the total count (since we wanted them to
# fail, but we want this script to pass)
nanotest.nanoconf['run'] -= fail

# end-of-run
nanotest_summary();
