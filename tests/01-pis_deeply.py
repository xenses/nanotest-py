import nanotest # we only do this because we're testing the module itself!
from nanotest import *

# initial state
pis(len(nanotest.nanotest_deepstack), 1,          "should be one element")
pis(nanotest.nanotest_deepstack,      ["root"],   "that element should be 'root'")
pisnt("root" in nanotest.nanotest_deephash, True, "but root shouldn't exist here yet")
pis(len(nanotest.nanotest_deephash),        0,    "no elements in hash")

# test hash generation
#
# the trivial case
nanotest._deep_build_hash(1, False, "msg")
pis(len(nanotest.nanotest_deepstack), 1,        "should still be one element")
pis(nanotest.nanotest_deepstack,      ["root"], "that element should still be 'root'")
pis("root" in nanotest.nanotest_deephash, True, "root should exist here yet now")
pis(len(nanotest.nanotest_deephash) ,        1, "one element now in hash")
# tuple
nanotest.nanotest_deepstack = ["root"] # manual reset because this
nanotest.nanotest_deephash  = {}       # happens programmaticaly in
                                       # pis_deeply
nanotest._deep_build_hash((1, 'a', 34), False, "msg")
pis(len(nanotest.nanotest_deepstack),        1, "should *still* be one element, due to popping")
pis(nanotest.nanotest_deepstack,      ["root"], "that element should *still* be 'root'")
pis(len(nanotest.nanotest_deephash) ,        3, "three elements now in hash")
pis("root.tuple.0" in nanotest.nanotest_deephash,   True, "tuple elem 0")
pis(nanotest.nanotest_deephash["root.tuple.0"][0],     1, "tuple elem 0[0] is '1'")     # value
pis(nanotest.nanotest_deephash["root.tuple.0"][1], False, "tuple elem 0[1] is 'False'") # 'seen' flag
pis("root.tuple.1" in nanotest.nanotest_deephash,   True, "tuple elem 1")
pis(nanotest.nanotest_deephash["root.tuple.1"][0],   'a', "tuple elem 1[0] is 'a'")
pis(nanotest.nanotest_deephash["root.tuple.1"][1], False, "tuple elem 1[1] is 'False'")
pis("root.tuple.2" in nanotest.nanotest_deephash,   True, "tuple elem 2")
pis(nanotest.nanotest_deephash["root.tuple.2"][0],    34, "tuple elem 2[0] is '34'")
pis(nanotest.nanotest_deephash["root.tuple.2"][1], False, "tuple elem 2[1] is 'False'")
pis("root.tuple.3" in nanotest.nanotest_deephash,  False, "tuple elem 3 doesn't exist")
# list
nanotest.nanotest_deepstack = ["root"]
nanotest.nanotest_deephash  = {}
nanotest._deep_build_hash([1, 'a', 34], False, "msg")
pis(len(nanotest.nanotest_deepstack),        1, "should *still* be one element, due to popping")
pis(nanotest.nanotest_deepstack,      ["root"], "that element should *still* be 'root'")
pis(len(nanotest.nanotest_deephash) ,        3, "three elements now in hash")
pis("root.list.0" in nanotest.nanotest_deephash,   True, "list elem 0")
pis(nanotest.nanotest_deephash["root.list.0"][0],     1, "list elem 0[0] is '1'")     # value
pis(nanotest.nanotest_deephash["root.list.0"][1], False, "list elem 0[1] is 'False'") # 'seen' flag
pis("root.list.1" in nanotest.nanotest_deephash,   True, "list elem 1")
pis(nanotest.nanotest_deephash["root.list.1"][0],   'a', "list elem 1[0] is 'a'")
pis(nanotest.nanotest_deephash["root.list.1"][1], False, "list elem 1[1] is 'False'")
pis("root.list.2" in nanotest.nanotest_deephash,   True, "list elem 2")
pis(nanotest.nanotest_deephash["root.list.2"][0],    34, "list elem 2[0] is '34'")
pis(nanotest.nanotest_deephash["root.list.2"][1], False, "list elem 2[1] is 'False'")
pis("root.list.3" in nanotest.nanotest_deephash,  False, "list elem 3 doesn't exist")
# dict
nanotest.nanotest_deepstack = ["root"]
nanotest.nanotest_deephash  = {}
nanotest._deep_build_hash({'a':22, 'b':"foo"}, False, "msg")
pis(len(nanotest.nanotest_deepstack),        1, "should *still* be one element, due to popping")
pis(nanotest.nanotest_deepstack,      ["root"], "that element should *still* be 'root'")
pis(len(nanotest.nanotest_deephash) ,        2, "two elements now in hash")
pis("root.dict.a" in nanotest.nanotest_deephash,   True, "dict elem a")
pis(nanotest.nanotest_deephash["root.dict.a"][0],    22, "dict elem a[0] is '22'")
pis(nanotest.nanotest_deephash["root.dict.a"][1], False, "dict elem a[1] is 'False'")
pis("root.dict.b" in nanotest.nanotest_deephash,   True, "dict elem b")
pis(nanotest.nanotest_deephash["root.dict.b"][0], "foo", "dict elem b[0] is 'foo'")
pis(nanotest.nanotest_deephash["root.dict.b"][1], False, "dict elem b[1] is 'False'")
pis("root.dict.c" in nanotest.nanotest_deephash,  False, "dict elem c doesn't exist")


# failures
#
# value mismatch
print(">>>>>>> Now testing failing tests:  3 tests will appear to fail <<<<<<<")
print(">>> So long as the end-of-run result is success, everything is okay <<<")


# end-of-run
nanotest_summary();
