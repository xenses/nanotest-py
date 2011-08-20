import nanotest # we only do this because we're testing the module itself!
from nanotest import *

pis(nanotest.nanotest_run, 0, "technically, this one hasn't run yet");
pis(nanotest.nanotest_pass, 1, "and this one hasn't passed yet");
pisnt(nanotest.nanotest_pass, 37, "we certainly haven't run that many yet, much less passed");

pis(nanotest._is_core(1,1), True, "identity");
pis(nanotest._is_core(1,0), False, "nonidentity");
nanotest.nanotest_run -= 2; # make the two inner tests go away for counting purposes

print("The next test will fail, as failure is being tested. Please disregard.");
pis(1, 0, "Of course zero doesn't equal one.");
nanotest.nanotest_pass += 1; # let's smooth that over :)

# end-of-run
nanotest_summary();
