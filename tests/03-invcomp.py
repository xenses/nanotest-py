import nanotest

n = nanotest.Nanotester()

t1 = [ {'a':[1, 2, 3], 'b':{'c':"d", 'e':"f"}},
       ("foo", "bar"),
       [["x", "y", "z"], 37, 42 ] ]

# t2 is missing an element, compared to t1
t2 = [ {'a':[1, 3], 'b':{'c':"d", 'e':"f"}},
       ("foo", "bar"),
       [["x", "y", "z"], 37, 42 ] ]

# t3 has an element value changed, compared to t1
t3 = [ {'a':[1, 2, 3], 'b':{'c':"d", 'e':"g"}},
       ("foo", "bar"),
       [["x", "y", "z"], 37, 42 ] ]

nanotest.core.hash(n, t1, n.xhash) # hash t1 into n.xhash
n.ghash = n.xhash    # copy xhash to ghash
n.test(nanotest.core.inv_compare(n, n.xhash, n.ghash), False, "inv_compare on identity should be False")

n.ghash = {}
nanotest.core.hash(n, t2, n.ghash)
n.test(nanotest.core.inv_compare(n, n.xhash, n.ghash), True, "different elements; should be True")

n.ghash = {}
nanotest.core.hash(n, t3, n.ghash)
n.test(nanotest.core.inv_compare(n, n.xhash, n.ghash), True, "different values; should be True")
