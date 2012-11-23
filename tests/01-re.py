import nanotest

n = nanotest.Nanotester()

n.test("foobar",   ":re:bar",        "'foobar' contains 'bar'")
n.untest("foobar", ":re:^bar",       "'foobar' does not start with 'bar'")
n.test("foobar",   ":re:^foo",       "'foobar' starts with 'foo'")
n.test("foobar",   ":re:foo[abc]ar", "'foobar' matches 'foo[abc]ar'")
n.test("foobar",   ":re:^\S+$",      "'foobar' contains no spaces'")
n.untest("foobar", ":re:\s",         "'foobar' still contains no spaces'")

n.test("foobar", ":re:\s", "no spaces, will fail")
test1 = n.results[6]
n.test(test1["file"], "./tests/01-re.py", "tests in this file")
n.test(test1["line"], 12, "7th test was on line 12")
n.test(test1["pass"], False, "7th test failed")
n.test(test1["got"], "foobar", "'foobar' was the string to match")
n.test(test1["xpect"], "\s", "'\s' was the regexp to match against")
n.test(test1["msg"], "no spaces, will fail", "msg was 'no spaces, will fail'")
n.test(test1["reason"], "regexp failure ('got' is not a match for 'expected')",
       "regexp failures do have reasons set")
# elide failing test before reporting gets to it
a = n.results[:6]
b = n.results[7:]
n.results = a + b

