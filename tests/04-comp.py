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

n.untest(t1, t2, "missing element; should be different (pass untest)")
n.untest(t1, t3, "different element value; should be different (pass untest)")
