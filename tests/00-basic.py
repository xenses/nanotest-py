import nanotest

n = nanotest.Nanotester()

n.test(1, 1, "identity")
n.untest(0, 1, "unidentity")

n.test(isinstance(n, nanotest.Nanotester), True, "nanotest object type test")
n.test(len(n.results), 3, "three successful tests up to now")
