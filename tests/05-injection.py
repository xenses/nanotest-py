import nanotest
import nanotest.injection as ni

n = nanotest.Nanotester()  # the object we're using to report our results
n2 = nanotest.Nanotester() # the object we're exercising code with

# file failure modes
n2.inject("foo")
n.test(n2.results[-1]["msg"], ":re:could not open", "doesn't exist")

n2.inject("./tests/corpus/05-injection-notjson.txt")
n.test(n2.results[-1]["msg"], ":re:could not unmarshal JSON", "not valid json")

n2.inject("./tests/corpus/05-injection-notdict.json")
n.test(n2.results[-1]["msg"], ":re:Injected test data should be dict", "top struct isn't a dict")

# ok, load some tests
n2 = nanotest.Nanotester() 
n2.inject("./tests/corpus/05-injection-base.json")
n.test(len(n2.injt),       3,                     "dict of 3 elements")
n.test("test1" in n2.injt, True,                  "there is a 'test1'")
n.test(n2.injt["test1"],   ["foobar", "generic"], "test1 should look like this")
# try running a test that doesn't exist
n2.itest("test99", 37)
n.test(n2.results[-1]["pass"], False, "top struct isn't a dict")
n.test(n2.results[-1]["msg"], ":re:Injected test \w+? not found", "there is no 'test99'")

# let's go for a spin
n.inject("./tests/corpus/05-injection-base.json")
n.itest("test1", "foobar")
n.itest("test2", 47 - 5)
n.itest("test3", "barfoo")
n.unitest("test1", "quux")
n.unitest("test2", 1009)
n.unitest("test3", "foobar")
