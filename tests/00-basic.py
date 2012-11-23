import nanotest

n = nanotest.Nanotester()

n.test(1, 1, "basic identity test")
n.untest(0, 1, "basic inverted identity test")

n.test(isinstance(n, nanotest.Nanotester), True, "nanotest object type test")
n.test(len(n.results), 3, "three successful tests up to now")

n.test(n.results[0]["file"], "./tests/00-basic.py", "tests in this file")
n.test(n.results[0]["line"], 5, "first test was on line 5")
n.test(n.results[0]["pass"], True, "first test passed")
n.test(n.results[0]["xpect"], None, "don't store expected values for successful tests")
n.test(n.results[0]["got"], None, "don't store received values for successful tests")
n.test(n.results[0]["msg"], None, "don't store msg for successful tests")
n.test(n.results[0]["reason"], None, "don't store reason for successful tests")
