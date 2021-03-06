import nanotest

n = nanotest.Nanotester()

# simple list
r = {}
t = ['a', 'b', 4]
nanotest.core.hash(n, t, r)
n.test(len(r),    3, "recv hash should be 3 elements")
n.test(r["l.0"], 'a', "key 'l0', value 'a'")
n.test(r["l.1"], 'b', "key 'l1', value 'b'")
n.test(r["l.2"],   4, "key 'l2', value '4'")

# simple dict
r = {}
t = {'a': 1, 'b': 2, 4: 3}
nanotest.core.hash(n, t, r)
n.test(len(r),  3, "recv hash should be 3 elements")
n.test(r["d.a"], 1, "key 'da', value '1'")
n.test(r["d.b"], 2, "key 'db', value '2'")
n.test(r["d.4"], 3, "key 'd4', value '3'")

# simple tuple
r = {}
t = (1, 2, 3)
nanotest.core.hash(n, t, r)
n.test(len(r),  3, "recv hash should be 3 elements")
n.test(r["t.0"], 1, "key 't0', value '1'")
n.test(r["t.1"], 2, "key 't1', value '2'")
n.test(r["t.2"], 3, "key 't2', value '3'")
n.test("t3" in r, False, "there is no key 't3'")

# complex example
r = {}
t = [ {'a':[1, 2, 3], 'b':{'c':"d", 'e':"f"}},
      ("foo", "bar"),
      [["x", "y", "z"], 37, 42 ] ]
nanotest.core.hash(n, t, r)
n.test(len(r),  12, "recv hash should be 12 elements")
n.test(r["l.0.d.a.l.0"],     1, "val 1")
n.test(r["l.0.d.a.l.1"],     2, "val 2")
n.test(r["l.0.d.a.l.2"],     3, "val 3")
n.test(r["l.0.d.b.d.c"],   "d", "val 4")
n.test(r["l.0.d.b.d.e"],   "f", "val 5")
n.test(r["l.1.t.0"],     "foo", "val 6")
n.test(r["l.1.t.1"],     "bar", "val 7")
n.test(r["l.2.l.0.l.0"],   "x", "val 8")
n.test(r["l.2.l.0.l.1"],   "y", "val 9")
n.test(r["l.2.l.0.l.2"],   "z", "val 10")
n.test(r["l.2.l.1"],        37, "val 11")
n.test(r["l.2.l.2"],        42, "val 12")

