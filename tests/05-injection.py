import nanotest
import nanotest.injection as ni

n = nanotest.Nanotester()  # the object we're using to report our results
n2 = nanotest.Nanotester() # the object we're exercising code with

# failure modes
n2.inject("foo")
n.test(n2.results[-1]["msg"], ":re:could not open", "doesn't exist")

n2.inject("./tests/corpus/05-injection-notjson.txt")
n.test(n2.results[-1]["msg"], ":re:could not unmarshal JSON", "not valid json")

n2.inject("./tests/corpus/05-injection-notdict.json")
n.test(n2.results[-1]["msg"], ":re:Injected test data should be dict", "top struct isn't a dict")
