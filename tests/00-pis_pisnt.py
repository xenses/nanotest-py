import nanotest # we only do this because we're testing the module itself!
from nanotest import *

pis(nanotest.nanoconf["run"], 0, "technically, this one hasn't run yet");
pis(nanotest.nanoconf["pass"], 1, "and this one hasn't passed yet");
pisnt(nanotest.nanoconf["pass"], 37, "we certainly haven't run that many yet, much less passed");

pis(nanotest._is_core(1,1), True, "identity");
pis(nanotest._is_core(1,0), False, "nonidentity");
nanotest.nanoconf["run"] -= 2; # make the two inner tests go away for counting purposes

pis(nanotest.nanoconf["pass"], 5, "5 tests passing before pis fail")
nanotest.nanoconf["silent"] = True
pis(1, 0, "pis() failure: Of course zero doesn't equal one.");
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"], 6, "6 tests passing after pis fail")
nanotest.nanoconf["silent"] = True
pisnt(1, 1, "pisnt() failure: Of course one equals one.");
nanotest.nanoconf["silent"] = False
pis(nanotest.nanoconf["pass"], 7, "7 tests passing after pisnt fail")
nanotest.nanoconf["run"] -= 2; # smooth over failing tests, which we will treat as passing:)

# make sure tests return values
pis( pis(1,1,1), True, 'should return True')
nanotest.nanoconf["silent"] = True
pis( pis(1,0,0), False, 'should return False')
nanotest.nanoconf["silent"] = False
pis( pisnt(1,0,1), True, 'should return True')
nanotest.nanoconf["silent"] = True
pis( pisnt(1,1,0), False, 'should return False')
nanotest.nanoconf["silent"] = False
nanotest.nanoconf["run"] -= 2; # smooth over failing inner tests, which we will treat as passing:)

# check regexes
nanotest.nanoconf["silent"] = True
pis( pis(14,':re:^\d+$',1), True, "14 is all digits")
pis( pis('14987t267',':re:^\d+$',0), False, 't is not a digit')
pis( pisnt('14987t267',':re:^\d+$',1), True, 't is not a digit (pisnt)')
pis( pisnt('14987267',':re:^\d+$',0), False, '2 is a digit')
nanotest.nanoconf["silent"] = False
nanotest.nanoconf["run"] -= 2; # smooth over failing inner tests, which we will treat as passing:)

# end-of-run
nanotest_summary();
