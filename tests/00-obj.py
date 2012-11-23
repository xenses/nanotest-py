import nanotest

n = nanotest.Nanotester()

n.test(isinstance(n, nanotest.Nanotester), True, "nanotest object type test")
