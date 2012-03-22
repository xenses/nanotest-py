// load test lib
load("../nanotest.js");

is(jsltest_run, 0, "technically, this one hasn't run yet");
is(jsltest_pass, 1, "and this one hasn't passed yet");
isnt(jsltest_pass, 37, "we certainly haven't run that many yet, much less passed");

is(is_core(1,1), true, "identity");
is(is_core(1,0), false, "nonidentity");
jsltest_run -= 2; // make the two inner tests go away for counting purposes

print("The next test will fail, as failure is being tested. Please disregard.");
is(1, 0, "Of course zero doesn't equal one.");
jsltest_pass++; // let's smooth that over :)

// end-of-run
testPrintSummary();
