import nanotest
import nanotest.injection as ni

n = nanotest.Nanotester()  # the object we're using to report our results
n2 = nanotest.Nanotester() # the object we're exercising code with

n2.inject("foo")
n.test(n2.results[-1]["msg"], ":re:could not open", "doesn't exist")

