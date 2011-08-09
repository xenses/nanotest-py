nanotest_run = 0
nanotest_pass = 0

def is_core(test, expect):
    nanotest_run = nanotest_run + 1
    if (test == expect) return True
    return False

def pis(test, expect, msg):
    if (is_core(test, expect)) nanotest_pass = nanotest_pass + 1
    else test_print_fail_msg(test, expect, msg, False)

def pisnt(test, expect, msg):
    if (not is_core(test, expect)) nanotest_pass = nanotest_pass + 1
    else test_print_fail_msg(test, expect, msg, True)
    
def test_print_fail_msg(test, expect, msg, invert):
    print("Test {} FAILED: {}".format(nanotest_run, msg))
    if invert:
        print("Expected anything but {} and got it anyway".format(expect))
    else:
        print("  Expected: {}".format(expect))
        print("  Got     : {}".format(test))

def test_print_summary:
    print("{} {}".format(nanotest_run, nanotest_pass))
