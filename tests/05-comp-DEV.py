import nanotest

n = nanotest.Nanotester()

t1 = [ {'a':[1, 2, 3], 'b':{'c':"d", 'e':"f"}},
       ("foo", "bar"),
       [["x", "y", "z"], 37, 42 ] ]

# t2 is missing 3 elements, compared to t1
t2 = [ {'a':[1], 'b':{'c':"d", 'e':"f"}},
       ("foo", "bar"),
       [["x", "y", "z"], 42 ] ]

# t3 has 2 element values changed, compared to t1
t3 = [ {'a':[1, 2, 3], 'b':{'c':"d", 'e':"g"}},
       ("foo", "baz"),
       [["x", "y", "z"], 37, 42 ] ]

n.test(t1, t2, "this should fail due to missing elements")
n.test(t1, t3, "this should fail due to differing values")
n.test(t2, t3, "this should fail for both reasons")
n.test(t2, t1, "first test, upside down")
n.test(t3, t1, "second test, upside down")
