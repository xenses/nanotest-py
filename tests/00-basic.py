import nanotest

n = nanotest.Nanotester()

n.test(1, 1, "basic identity test")
n.untest(0, 1, "basic inverted identity test")

n.test(isinstance(n, nanotest.Nanotester), True, "nanotest object type test")
n.test(len(n.results), 3, "three successful tests up to now")

test1 = n.results[0]
n.test(test1["file"], "./tests/00-basic.py", "tests in this file")
n.test(test1["line"], 5, "first test was on line 5")
n.test(test1["pass"], True, "first test passed")
n.test(test1["msg"], "basic identity test", "msg")
n.test(test1["comp"][0]["xpect"], 1, "1")
n.test(test1["comp"][0]["got"], 1, "also 1")
n.test(test1["comp"][0]["reason"], None, "don't store reason for _is_eq tests")

n.test(0, 1, "generating a failure")
test2 = n.results[11]
n.test(test2["file"], "./tests/00-basic.py", "tests in this file")
n.test(test2["line"], 20, "11th test was on line 20")
n.test(test2["pass"], False, "11th test failed")
n.test(test2["msg"], "generating a failure", "msg was 'generating a failure'")
n.test(test2["comp"][0]["xpect"], 1, "expected '1'")
n.test(test2["comp"][0]["got"], 0, "expected '0'")
n.test(test2["comp"][0]["reason"], None, "no reason for _is_eq tests")
# elide failing test before reporting gets to it
a = n.results[:11]
b = n.results[12:]
n.results = a + b
