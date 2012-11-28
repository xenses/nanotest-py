import nanotest

n = nanotest.Nanotester()

recv = {}

t1 = ['a', 'b', 4]

n._hash(t1, recv)

n.test(len(recv), 3, "recv hash should be 3 elements")
n.test(recv["l0"], 'a', "key 'l0', value 'a'")
