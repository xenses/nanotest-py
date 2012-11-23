import nanotest

n = nanotest.Nanotester()

n.test(1, 0, "assert that 0 is 1")
n.test(True, False, "assert that False is True")
