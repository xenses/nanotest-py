import nanotest # we only do this because we're testing the module itself!
from nanotest import *


# failures
#
# value mismatch
print(">>>>>>> Now testing failing tests:  3 tests will appear to fail <<<<<<<")
print(">>> So long as the end-of-run result is success, everything is okay <<<")

# end-of-run
nanotest_summary();
